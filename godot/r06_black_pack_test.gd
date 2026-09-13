extends SceneTree

var errors: Array[String] = []
var events: Array = []
var pack: Dictionary
var pack_path := ""
var track_filter := ""
var render_observation := ""
var capture_path := ""
var compositor_samples: Array = []
var capture_written := false
var measured_assets: Dictionary = {}
var frame_post_draw_seen := false
var track_render_observed := false

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--pack="): pack_path = arg.trim_prefix("--pack=")
		if arg.begins_with("--track="): track_filter = arg.trim_prefix("--track=")
		if arg.begins_with("--capture="): capture_path = arg.trim_prefix("--capture=")
	if pack_path.is_empty(): _finish("missing --pack"); return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(pack_path))
	if not parsed is Dictionary: _finish("pack JSON invalid"); return
	pack = parsed
	root.size = Vector2i(640, 640)
	root.content_scale_size = Vector2i(640, 640)
	root.transparent_bg = false
	RenderingServer.set_default_clear_color(Color.BLACK)
	var source_pack: bool = pack.get("profile") == "MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1"
	var ingested_pack: bool = pack.get("profile") == "MON_INGESTED_FRAME_PACK_V1" and pack.get("source_profile") == "MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1"
	if not source_pack and not ingested_pack: errors.append("wrong source profile")
	if pack.get("timing", {}).get("fps") != 24: errors.append("timing fps is not 24")
	var tracks: Array = pack.get("tracks", [])
	if not track_filter.is_empty(): tracks = tracks.filter(func(t): return t.get("track_id") == track_filter)
	if tracks.is_empty(): errors.append("requested track missing"); _finish("track missing"); return
	for track in tracks:
		track_render_observed = false
		await _play_track(track)
		if not track_render_observed:
			break
	_finish("complete")

func _play_track(track: Dictionary) -> void:
	var container := Node2D.new(); get_root().add_child(container)
	var sprite := AnimatedSprite2D.new(); sprite.position = Vector2(320, 320); sprite.scale = Vector2(0.5, 0.5); sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST; container.add_child(sprite)
	var frames := SpriteFrames.new(); frames.remove_animation("default"); var name := String(track.get("track_id")); frames.add_animation(name); frames.set_animation_speed(name, 24.0)
	var parent := pack_path.get_base_dir()
	for frame in track.get("frames", []):
		var image_path := parent.path_join(String(frame.get("filename", "")))
		var image := Image.load_from_file(image_path)
		if image == null or image.is_empty(): errors.append("frame load failed: "+image_path); continue
		if image.get_width() != 1254 or image.get_height() != 1254: errors.append("native dimensions changed")
		var tex := ImageTexture.create_from_image(image); frames.add_frame(name, tex, float(frame.get("duration_ticks", 1)))
	sprite.sprite_frames = frames
	if frames.get_frame_count(name) == 0: errors.append("track has no frames"); container.queue_free(); return
	events.append({"event":"intent_received","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	events.append({"event":"track_resolved","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	events.append({"event":"track_validated","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	sprite.animation = name; sprite.frame = 0; sprite.play(name)
	if not await _await_frame_post_draw():
		errors.append("render boundary not observed")
		container.queue_free()
		return
	track_render_observed = true
	var rendered := get_root().get_texture().get_image()
	if rendered == null or rendered.is_empty():
		errors.append("viewport readback unavailable")
		container.queue_free()
		return
	var source_image := Image.load_from_file(image_path_for_frame(track, 0, parent))
	if source_image == null or source_image.is_empty():
		errors.append("source image unavailable for compositor measurement")
		container.queue_free()
		return
	var first_frame: Dictionary = track.get("frames", [])[0]
	var first_asset_id := String(first_frame.get("source_asset_id", name))
	_measure_compositor(source_image, rendered, first_asset_id)
	measured_assets[first_asset_id] = true
	if not capture_path.is_empty() and not capture_written:
		rendered.save_png(capture_path)
		capture_written = true
	events.append({"event":"first_frame_viewport_readback_observed","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	# Render each remaining unique source master once so field blending is
	# measured inside the transformed source rectangle for the complete pack.
	var frame_list: Array = track.get("frames", [])
	for frame_index in range(1, frame_list.size()):
		var asset_id := String(frame_list[frame_index].get("source_asset_id", ""))
		if measured_assets.has(asset_id):
			continue
		sprite.stop(); sprite.frame = frame_index
		if not await _await_frame_post_draw():
			errors.append("render boundary not observed for compositor source")
			continue
		var source_path := image_path_for_frame(track, frame_index, parent)
		var unique_source := Image.load_from_file(source_path)
		var unique_rendered := get_root().get_texture().get_image()
		if unique_source == null or unique_source.is_empty() or unique_rendered == null or unique_rendered.is_empty():
			errors.append("compositor source readback unavailable")
		else:
			_measure_compositor(unique_source, unique_rendered, asset_id)
			measured_assets[asset_id] = true
	events.append({"event":"first_frame_render_committed","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	events.append({"event":"started","track_id":name,"frame":0,"monotonic_usec":Time.get_ticks_usec()})
	var total_ticks := 0
	for frame in track.get("frames", []): total_ticks += int(frame.get("duration_ticks", 1))
	await create_timer(float(total_ticks) / 24.0 + 0.02).timeout
	events.append({"event":"completed","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	container.queue_free(); await process_frame

func _await_frame_post_draw() -> bool:
	# Observe the strict engine signal with a bounded wait.  A callback is
	# connected before queuing the draw so a backend that emits the signal can
	# be observed without allowing a missing signal to hang qualification.
	frame_post_draw_seen = false
	if RenderingServer.frame_post_draw.is_connected(_on_frame_post_draw):
		RenderingServer.frame_post_draw.disconnect(_on_frame_post_draw)
	RenderingServer.frame_post_draw.connect(_on_frame_post_draw, CONNECT_ONE_SHOT)
	await process_frame
	RenderingServer.force_draw()
	for _i in range(30):
		if frame_post_draw_seen:
			render_observation = "RenderingServer.frame_post_draw"
			return true
		await process_frame
	if RenderingServer.frame_post_draw.is_connected(_on_frame_post_draw):
		RenderingServer.frame_post_draw.disconnect(_on_frame_post_draw)
	return frame_post_draw_seen

func _on_frame_post_draw() -> void:
	frame_post_draw_seen = true

func image_path_for_frame(track: Dictionary, index: int, parent: String) -> String:
	var frames: Array = track.get("frames", [])
	if index < 0 or index >= frames.size():
		return ""
	return parent.path_join(String(frames[index].get("filename", "")))

func _measure_compositor(source: Image, rendered: Image, track_name: String) -> void:
	var source_points := [Vector2i(1, 1), Vector2i(1252, 1), Vector2i(1, 1252), Vector2i(1252, 1252), Vector2i(8, 627), Vector2i(1245, 627), Vector2i(627, 8), Vector2i(627, 1245)]
	var center := Vector2(320.0, 320.0)
	for point in source_points:
		var viewport_point := Vector2i(round(center.x + (float(point.x) - 627.0) * 0.5), round(center.y + (float(point.y) - 627.0) * 0.5))
		var outside := viewport_point
		if abs(point.x - 627) >= abs(point.y - 627):
			outside.x += -2 if point.x < 627 else 2
		else:
			outside.y += -2 if point.y < 627 else 2
		var src := source.get_pixelv(point)
		var rendered_pixel := rendered.get_pixelv(viewport_point)
		var outside_pixel := rendered.get_pixelv(outside)
		compositor_samples.append({"track_id":track_name,"source_point":[point.x,point.y],"viewport_point":[viewport_point.x,viewport_point.y],"source_rgb":[round(src.r*255.0),round(src.g*255.0),round(src.b*255.0)],"rendered_rgb":[round(rendered_pixel.r*255.0),round(rendered_pixel.g*255.0),round(rendered_pixel.b*255.0)],"outside_rgb":[round(outside_pixel.r*255.0),round(outside_pixel.g*255.0),round(outside_pixel.b*255.0)],"delta_from_black":max(round(rendered_pixel.r*255.0),max(round(rendered_pixel.g*255.0),round(rendered_pixel.b*255.0)))})

func _finish(reason: String) -> void:
	print(JSON.stringify({"status":"PASS" if errors.is_empty() else "FAIL","reason":reason,"errors":errors,"events":events,"godot_version":Engine.get_version_info().get("string","unknown"),"render_observation":render_observation,"compositor_samples":compositor_samples,"fps":24}, "  "))
	quit(0 if errors.is_empty() else 1)

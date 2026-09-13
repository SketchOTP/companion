extends SceneTree

var errors: Array[String] = []
var events: Array = []
var pack: Dictionary
var pack_path := ""
var track_filter := ""

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--pack="): pack_path = arg.trim_prefix("--pack=")
		if arg.begins_with("--track="): track_filter = arg.trim_prefix("--track=")
	if pack_path.is_empty(): _finish("missing --pack"); return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(pack_path))
	if not parsed is Dictionary: _finish("pack JSON invalid"); return
	pack = parsed
	var source_pack: bool = pack.get("profile") == "MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1"
	var ingested_pack: bool = pack.get("profile") == "MON_INGESTED_FRAME_PACK_V1" and pack.get("source_profile") == "MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1"
	if not source_pack and not ingested_pack: errors.append("wrong source profile")
	if pack.get("timing", {}).get("fps") != 24: errors.append("timing fps is not 24")
	var tracks: Array = pack.get("tracks", [])
	if not track_filter.is_empty(): tracks = tracks.filter(func(t): return t.get("track_id") == track_filter)
	if tracks.is_empty(): errors.append("requested track missing"); _finish("track missing"); return
	for track in tracks:
		await _play_track(track)
	_finish("complete")

func _play_track(track: Dictionary) -> void:
	var container := SubViewportContainer.new(); container.size = Vector2(640, 640); get_root().add_child(container)
	var viewport := SubViewport.new(); viewport.size = Vector2i(640, 640); viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS; viewport.transparent_bg = false; container.add_child(viewport)
	var sprite := AnimatedSprite2D.new(); sprite.position = Vector2(320, 320); sprite.scale = Vector2(0.5, 0.5); sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST; viewport.add_child(sprite)
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
	await RenderingServer.frame_post_draw
	var rendered := viewport.get_texture().get_image()
	if rendered == null or rendered.is_empty():
		errors.append("viewport readback unavailable")
	else:
		for corner in [Vector2i(0, 0), Vector2i(rendered.get_width() - 1, 0), Vector2i(0, rendered.get_height() - 1), Vector2i(rendered.get_width() - 1, rendered.get_height() - 1)]:
			var pixel := rendered.get_pixelv(corner)
			if max(pixel.r, max(pixel.g, pixel.b)) > 4.0 / 255.0:
				errors.append("visible non-black source field")
				break
	events.append({"event":"first_frame_render_committed","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	events.append({"event":"started","track_id":name,"frame":0,"monotonic_usec":Time.get_ticks_usec()})
	var total_ticks := 0
	for frame in track.get("frames", []): total_ticks += int(frame.get("duration_ticks", 1))
	await create_timer(float(total_ticks) / 24.0 + 0.02).timeout
	events.append({"event":"completed","track_id":name,"monotonic_usec":Time.get_ticks_usec()})
	container.queue_free(); await process_frame

func _finish(reason: String) -> void:
	print(JSON.stringify({"status":"PASS" if errors.is_empty() else "FAIL","reason":reason,"errors":errors,"events":events,"godot_version":Engine.get_version_info().get("string","unknown"),"render_observation":"RenderingServer.frame_post_draw","fps":24}, "  "))
	quit(0 if errors.is_empty() else 1)

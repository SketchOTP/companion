extends SceneTree
## Explicit opaque candidate-review player. Never a production intake fallback.

var seen: Array[int] = []
var finished := false
var sprite: AnimatedSprite2D

func _initialize() -> void:
	call_deferred("_run")

func _changed() -> void:
	seen.append(sprite.frame)

func _finished() -> void:
	finished = true

func _run() -> void:
	var manifest := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--requests="): manifest = arg.trim_prefix("--requests=")
	var errors: Array[String] = []
	var observations: Array[Dictionary] = []
	if manifest.is_empty() or not FileAccess.file_exists(manifest):
		print(JSON.stringify({"status":"FAILED", "reason":"review_manifest_missing"}))
		quit(1)
		return
	var request = JSON.parse_string(FileAccess.get_file_as_string(manifest))
	if not request is Dictionary or request.get("profile") != "BLACK_BACKED_MOTION_REVIEW_V1" or request.get("approval_state") != "candidate":
		print(JSON.stringify({"status":"FAILED", "reason":"not_explicit_candidate_review"}))
		quit(1)
		return
	if request.get("tracks", []).is_empty() or request.get("drawings", []).is_empty():
		print(JSON.stringify({"status":"FAILED", "reason":"empty_review_manifest"}))
		quit(1)
		return
	if DisplayServer.get_name() == "headless": errors.append("render_boundary_unavailable")
	root.size = Vector2i(640, 640)
	root.content_scale_size = Vector2i(640, 640)
	root.transparent_bg = false
	root.title = "Companion — black candidate motion study, not approved"
	RenderingServer.set_default_clear_color(Color.BLACK)
	var fixture := Node2D.new()
	root.add_child(fixture)
	sprite = AnimatedSprite2D.new()
	sprite.position = Vector2(320, 320)
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	fixture.add_child(sprite)
	sprite.frame_changed.connect(_changed)
	sprite.animation_finished.connect(_finished)
	var textures: Dictionary = {}
	var paths: Dictionary = {}
	var hashes: Dictionary = {}
	for drawing in request.get("drawings", []):
		var source: String = manifest.get_base_dir().path_join("raw").path_join(drawing["file"])
		var image := Image.new()
		if FileAccess.get_sha256(source) != drawing["sha256"] or image.load(source) != OK:
			errors.append("source_hash_or_decode_failure:" + drawing["id"])
			continue
		textures[drawing["id"]] = ImageTexture.create_from_image(image)
		paths[drawing["id"]] = source
		hashes[drawing["id"]] = drawing["sha256"]
	if errors.is_empty():
		for track in request.get("tracks", []):
			var frames := SpriteFrames.new()
			frames.remove_animation("default")
			frames.add_animation(track["id"])
			frames.set_animation_speed(track["id"], 24.0)
			# Observe one complete traversal even when the source requests a loop.
			frames.set_animation_loop(track["id"], false)
			var ticks := 0
			for frame in track["frames"]:
				var weight = frame["duration_ticks"]
				if not textures.has(frame["drawing_id"]) or weight < 1 or weight != int(weight):
					errors.append("invalid_review_frame:" + track["id"])
					break
				frames.add_frame(track["id"], textures[frame["drawing_id"]], float(weight))
				ticks += int(weight)
			if not errors.is_empty(): break
			sprite.stop()
			sprite.sprite_frames = frames
			sprite.animation = track["id"]
			sprite.set_frame_and_progress(0, 0.0)
			var texture: Texture2D = frames.get_frame_texture(track["id"], 0)
			sprite.scale = Vector2.ONE * (560.0 / max(texture.get_width(), texture.get_height()))
			await process_frame
			await RenderingServer.frame_post_draw
			var presented: bool = sprite.frame == 0 and sprite.animation == track["id"] and sprite.is_visible_in_tree()
			var rendered := root.get_texture().get_image()
			var visible_pixels := 0
			for y in range(0, rendered.get_height(), 8):
				for x in range(0, rendered.get_width(), 8):
					var color := rendered.get_pixel(x, y)
					if max(color.r, max(color.g, color.b)) > 0.1: visible_pixels += 1
			if not presented or visible_pixels < 25 or rendered.get_pixel(0, 0) != Color.BLACK:
				errors.append("first_frame_presentation_failed:" + track["id"])
				break
			# Texture loading/readback may make the first frame unusually long.
			# Begin measured playback only after two subsequent render boundaries.
			for boundary in range(2):
				await process_frame
				await RenderingServer.frame_post_draw
			seen = [0]
			finished = false
			var start := Time.get_ticks_usec()
			sprite.play(track["id"])
			while not finished and Time.get_ticks_usec() - start < int((ticks / 24.0 + 5.0) * 1000000):
				await process_frame
			var elapsed := (Time.get_ticks_usec() - start) / 1000000.0
			var expected: Array[int] = []
			for i in range(track["frames"].size()): expected.append(i)
			if not finished or seen != expected: errors.append("frame_order_or_completion_failure:" + track["id"])
			if abs(elapsed - ticks / 24.0) > 0.075: errors.append("timing_tolerance_exceeded:" + track["id"])
			observations.append({"track":track["id"], "frame_order":seen.duplicate(), "expected_frame_order":expected,
				"first_frame_post_draw":presented, "visible_pixel_samples":visible_pixels,
				"source_ticks":ticks, "fps":24, "elapsed_seconds":elapsed, "timing_tolerance_seconds":0.075, "warmup_render_boundaries":2,
				"completed":finished, "source_completion":track["completion"], "review_traversals":1})
	for id in paths:
		if FileAccess.get_sha256(paths[id]) != hashes[id]: errors.append("source_mutated:" + id)
	fixture.queue_free()
	textures.clear()
	await process_frame
	await process_frame
	print(JSON.stringify({"status":"PASSED" if errors.is_empty() else "FAILED", "mode":"black_candidate_motion_review",
		"tracks":observations, "background_rgb":[0,0,0], "source_bytes_unchanged":not errors.any(func(e): return e.begins_with("source_mutated")),
		"motion_quality":"NOT_APPROVED", "world_contacts":"NOT_RUN", "transparent_intake":"NOT_RUN", "errors":errors}))
	quit(0 if errors.is_empty() else 1)

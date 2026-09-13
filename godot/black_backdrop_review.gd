extends SceneTree
## Explicit still-review operation, never an authored-pack importer or fallback.

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var image_path := ""
	var capture_path := ""
	var self_test := false
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--image="): image_path = arg.trim_prefix("--image=")
		if arg.begins_with("--capture="): capture_path = arg.trim_prefix("--capture=")
		if arg == "--self-test": self_test = true
	var errors: Array[String] = []
	var configured: Color = ProjectSettings.get_setting("rendering/environment/defaults/default_clear_color")
	if configured != Color.BLACK: errors.append("project_background_not_black")
	if image_path.is_empty() or not FileAccess.file_exists(image_path):
		errors.append("review_image_missing")
	var image := Image.new()
	if errors.is_empty() and image.load(image_path) != OK:
		errors.append("review_image_unloadable")
	if not errors.is_empty():
		print(JSON.stringify({"status":"FAILED", "mode":"black_backdrop_still_review", "errors":errors}))
		quit(1)
		return
	var source_hash := FileAccess.get_sha256(image_path)
	root.size = Vector2i(640, 640)
	root.content_scale_size = Vector2i(640, 640)
	root.title = "Companion — black-background candidate still (not animation)"
	root.transparent_bg = false
	var fixture := Node2D.new()
	root.add_child(fixture)
	var sprite := Sprite2D.new()
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	sprite.texture = ImageTexture.create_from_image(image)
	sprite.position = Vector2(320, 320)
	sprite.scale = Vector2.ONE * (560.0 / max(image.get_width(), image.get_height()))
	fixture.add_child(sprite)
	if not self_test:
		return
	if DisplayServer.get_name() == "headless":
		errors.append("render_boundary_unavailable")
	else:
		await process_frame
		await RenderingServer.frame_post_draw
		var rendered := root.get_texture().get_image()
		for point in [Vector2i(0,0), Vector2i(639,0), Vector2i(0,639), Vector2i(639,639)]:
			if rendered.get_pixelv(point) != Color.BLACK: errors.append("rendered_background_not_black")
		var visible_pixels := 0
		for y in range(0, rendered.get_height(), 4):
			for x in range(0, rendered.get_width(), 4):
				var color := rendered.get_pixel(x,y)
				if max(color.r, max(color.g,color.b)) > 0.1: visible_pixels += 1
		if visible_pixels < 100: errors.append("review_subject_not_presented")
		if not capture_path.is_empty() and rendered.save_png(capture_path) != OK:
			errors.append("capture_failed")
	if FileAccess.get_sha256(image_path) != source_hash: errors.append("source_changed")
	fixture.queue_free()
	await process_frame
	print(JSON.stringify({"status":"PASSED" if errors.is_empty() else "FAILED", "mode":"black_backdrop_still_review", "source_sha256":source_hash, "source_unchanged":not errors.has("source_changed"), "render_observation":"RenderingServer.frame_post_draw" if DisplayServer.get_name() != "headless" else "NOT_OBSERVED", "background_rgb":[0,0,0], "animation_tested":false, "transparent_intake_tested":false, "errors":errors}))
	quit(0 if errors.is_empty() else 1)

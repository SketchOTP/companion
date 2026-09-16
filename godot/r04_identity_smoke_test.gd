extends SceneTree

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var path := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--image="): path = arg.trim_prefix("--image=")
	var errors: Array[String] = []
	if path.is_empty() or not FileAccess.file_exists(path): errors.append("identity smoke path missing")
	var image := Image.new()
	if errors.is_empty() and image.load(path) != OK: errors.append("identity smoke image failed to load")
	if errors.is_empty() and image.get_size() != Vector2i(1254, 1254): errors.append("identity smoke dimensions mismatch")
	if errors.is_empty() and image.get_format() != Image.FORMAT_RGBA8: errors.append("identity smoke format mismatch")
	var texture := ImageTexture.create_from_image(image) if errors.is_empty() else null
	if errors.is_empty() and texture == null: errors.append("identity smoke texture failed to load")
	print(JSON.stringify({"status": "PASS" if errors.is_empty() else "FAIL", "fixture_role": "one_frame_import_smoke_only", "candidate_art": false, "source_mutated": false, "dimensions": [1254, 1254], "format": "RGBA8", "errors": errors}, "  "))
	quit(0 if errors.is_empty() else 1)

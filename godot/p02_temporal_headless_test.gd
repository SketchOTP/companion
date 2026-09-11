extends SceneTree

## Headless contract test for the generated temporal-track artifact. It is
## intentionally synthetic: no organism, sensor, speech, or care logic is
## involved.
func _initialize() -> void:
	var errors: Array[String] = []
	var manifest_file := FileAccess.open("res://assets/p02-core/temporal_tracks.json", FileAccess.READ)
	if manifest_file == null:
		print(JSON.stringify({"status":"BLOCKED","reason":"core motion artifact not staged"})); quit(2); return
	var parsed = JSON.parse_string(manifest_file.get_as_text())
	if not parsed is Dictionary: errors.append("manifest parse")
	var tracks: Array = parsed.get("tracks", []) if parsed is Dictionary else []
	var idle_count := 0; var walk_count := 0; var run_count := 0
	for track in tracks:
		if track.get("direction") not in ["N","NE","E","SE","S","SW","W","NW"]: errors.append("direction")
		if track.get("frame_profile") != "MON_FRAME_V1": errors.append("frame profile")
		if track.get("root_motion_policy") != "forbidden": errors.append("root motion")
		if track.get("family", "").begins_with("idle_breathe"):
			idle_count += 1
			if track.get("frames", []).size() < 6: errors.append("idle count")
		if track.get("family") == "walk":
			walk_count += 1
			if track.get("frames", []).size() < 8: errors.append("walk count")
		if track.get("family") == "run":
			run_count += 1
			if track.get("frames", []).size() < 6: errors.append("run count")
	if idle_count != 24: errors.append("idle direction coverage")
	if walk_count != 8: errors.append("walk direction coverage")
	if run_count != 8: errors.append("run direction coverage")
	var scene: Node = load("res://main.tscn").instantiate(); root.add_child(scene); await process_frame
	var avatar = scene.get_node("MonAvatar")
	var first := avatar.director.request_intent("idle", 0, true, "N", "neutral", "neutral", "low", 1)
	if first.get("status") not in ["started", "degraded"]: errors.append("idle intent")
	var second := avatar.director.request_intent("walk", 0, true, "E", "neutral", "neutral", "medium", 1)
	if second.get("status") not in ["started", "degraded"]: errors.append("walk intent")
	await process_frame
	var state: Dictionary = avatar.visible_state()
	if state.get("schema_major") != 1: errors.append("visible state schema")
	print(JSON.stringify({"status":"PASSED" if errors.is_empty() else "FAILED", "errors":errors, "tracks":tracks.size(), "idle_tracks":idle_count, "walk_tracks":walk_count, "run_tracks":run_count, "visible":state}))
	quit(0 if errors.is_empty() else 1)

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
	var idle_count := 0; var walk_count := 0; var orient_count := 0; var reaction_count := 0
	for track in tracks:
		if track.get("direction") != "front_left": errors.append("direction selection")
		if track.get("frame_profile") != "MON_FRAME_V1": errors.append("frame profile")
		if track.get("root_motion_policy") != "forbidden": errors.append("root motion")
		if track.get("family", "").begins_with("idle_breathe"):
			idle_count += 1
			if track.get("frames", []).size() < 6: errors.append("idle count")
		if track.get("family") == "walk":
			walk_count += 1
			if track.get("frames", []).size() < 8: errors.append("walk count")
		if track.get("family", "").begins_with("orient_"):
			orient_count += 1
			if track.get("frames", []).size() != 3: errors.append("orient count")
		if track.get("family") in ["listen", "acknowledge"]:
			reaction_count += 1
			if track.get("frames", []).size() != 3: errors.append("reaction count")
	if tracks.size() != 6: errors.append("proof track count")
	if idle_count != 1: errors.append("idle facing coverage")
	if walk_count != 1: errors.append("walk facing coverage")
	if orient_count != 2: errors.append("orient connector pair")
	if reaction_count != 2: errors.append("listen acknowledge proof")
	var scene: Node = load("res://main.tscn").instantiate(); root.add_child(scene); await process_frame
	var avatar = scene.get_node("MonAvatar")
	var markers: Array = []
	var completions: Array = []
	avatar.frame_marker.connect(func(event): markers.append(event))
	avatar.clip_completed.connect(func(event): completions.append(event))
	var first: Dictionary = avatar.director.request_intent("idle", 0, true, "front_left", "neutral", "neutral", "low", 1)
	if first.get("status") != "started": errors.append("idle intent")
	for _i in range(8): await process_frame
	var second: Dictionary = avatar.director.request_intent("walk", 0, true, "front_left", "neutral", "neutral", "medium", 1)
	if second.get("status") != "started": errors.append("walk intent")
	for _i in range(8): await process_frame
	if markers.is_empty(): errors.append("observed frame markers")
	if markers.size() > 0 and markers[0].get("track_id", "").find("front_left") < 0: errors.append("marker facing")
	avatar.play_track("orient_front_to_front_left", "front_left", "neutral", 1, "proof")
	await create_timer(1.0).timeout
	await process_frame
	if completions.is_empty(): errors.append("observed completion")
	var state: Dictionary = avatar.visible_state()
	if state.get("schema_major") != 1: errors.append("visible state schema")
	print(JSON.stringify({"status":"PASSED" if errors.is_empty() else "FAILED", "errors":errors, "tracks":tracks.size(), "idle_tracks":idle_count, "walk_tracks":walk_count, "orient_tracks":orient_count, "reaction_tracks":reaction_count, "observed_frame_markers":markers.size(), "observed_completions":completions.size(), "visible":state}))
	quit(0 if errors.is_empty() else 1)

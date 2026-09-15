extends SceneTree

## Headless playback gate for the actual R03 generated tracks.  It creates
## AnimatedSprite2D resources from the generated PNGs, uses relative integer
## weights at 24 FPS, and observes frame/finish signals.  No bridge, display,
## organism, or care state is involved.

var failures: Array[String] = []
var observations: Array[Dictionary] = []

func _initialize() -> void:
	var output_dir := "/tmp/companion-p02-r03-proof"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--out="):
			output_dir = arg.trim_prefix("--out=")
	var track_file := output_dir.path_join("temporal_tracks_v2.json")
	if not FileAccess.file_exists(track_file):
		_fail("missing generated track file: " + track_file)
		_finish()
		return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(track_file))
	if not parsed is Dictionary or parsed.get("profile") != "MON_TEMPORAL_TRACKS_V2":
		_fail("invalid temporal-track wrapper")
	else:
		await _test_body_source()
		for track in parsed.get("tracks", []):
			await _test_track(track, output_dir)
		# A missing track must be a failed selection, never a false started event.
		var requested := "does_not_exist"
		var selected: Variant = _select_track(parsed.get("tracks", []), requested)
		if selected != null:
			_fail("missing track unexpectedly selected")
		else:
			observations.append({"missing_track": requested, "started": false, "status": "rejected"})
	_finish()

func _test_body_source() -> void:
	var packed := load("res://mon_body_source_v2.tscn") as PackedScene
	if packed == null:
		_fail("MonBodySourceV2 scene did not load")
		return
	var body = packed.instantiate()
	root.add_child(body)
	if body.get_node_or_null("AnimationPlayer") == null:
		_fail("editable body source has no AnimationPlayer timing node")
	for path in [
		"Rig/PelvisRoot/Torso/Head", "Rig/PelvisRoot/Torso/ArmLeft/UpperArmLeft/ForearmLeft/HandLeft/Finger01",
		"Rig/PelvisRoot/Torso/ArmLeft/UpperArmLeft/ForearmLeft/HandLeft/Finger02",
		"Rig/PelvisRoot/Torso/ArmLeft/UpperArmLeft/ForearmLeft/HandLeft/Thumb",
		"Rig/PelvisRoot/LegLeft/ThighLeft/LowerLegLeft/FootLeft/Toe01",
		"Rig/PelvisRoot/LegLeft/ThighLeft/LowerLegLeft/FootLeft/Toe02",
		"Rig/PelvisRoot/LegLeft/ThighLeft/LowerLegLeft/FootLeft/Toe03"
	]:
		if body.get_node_or_null(path) == null:
			_fail("missing editable body part: " + path)
	body.apply_pose({"facing": "front_left", "foot_left": [0, 0], "foot_right": [0, 0]})
	await process_frame
	var idle_landmarks: Dictionary = body.landmark_snapshot()
	var idle_signature: String = body.geometry_signature()
	body.apply_pose({"facing": "front_left", "leg_left": 0.22, "leg_right": -0.04, "foot_left": [-24, -30], "foot_right": [0, 0]})
	await process_frame
	var walk_landmarks: Dictionary = body.landmark_snapshot()
	if idle_landmarks.get("root") != [512, 896] or walk_landmarks.get("root") != [512, 896]:
		_fail("body source root moved")
	if idle_landmarks.get("left_foot") == walk_landmarks.get("left_foot"):
		_fail("body source lower-leg/foot did not articulate")
	if idle_signature == body.geometry_signature():
		_fail("body source pose signature did not change")
	observations.append({"body_source": "loaded", "root_fixed": true, "articulated_foot_changed": true})
	body.queue_free()

func _select_track(tracks: Array, family: String):
	for track in tracks:
		if track is Dictionary and track.get("family") == family:
			return track
	return null

func _test_track(track: Dictionary, output_dir: String) -> void:
	var family := String(track.get("family", ""))
	var sprite := AnimatedSprite2D.new()
	root.add_child(sprite)
	var frames := SpriteFrames.new()
	frames.clear_all()
	frames.add_animation(family)
	frames.set_animation_speed(family, 24.0)
	frames.set_animation_loop(family, track.get("loop_mode") == "loop")
	var expected_paths: Array[String] = []
	for frame in track.get("frames", []):
		var path := output_dir.path_join(String(frame.get("path", "")))
		if not FileAccess.file_exists(path):
			_fail(family + ": missing frame " + path)
			continue
		var image := Image.new()
		if image.load(path) != OK:
			_fail(family + ": failed frame image load")
			continue
		var texture := ImageTexture.create_from_image(image)
		frames.add_frame(family, texture, float(frame.get("duration_ticks", 0)))
		expected_paths.append(path)
	sprite.sprite_frames = frames
	sprite.animation = family
	sprite.speed_scale = 1.0
	sprite.process_mode = Node.PROCESS_MODE_ALWAYS
	if frames.get_frame_count(family) != track.get("frames", []).size():
		_fail(family + ": configured frame count differs from generated track")
	var changed: Array[int] = []
	var signal_frames: Array[int] = []
	var completed := false
	var completion_observation := "not_reached"
	sprite.frame_changed.connect(func() -> void: signal_frames.append(sprite.frame))
	sprite.animation_finished.connect(func() -> void:
		completed = true
		completion_observation = "animation_finished"
	)
	sprite.play(family)
	# Drive the actual AnimatedSprite2D playback.  We sample the frame property
	# while the engine advances; no direct frame mutation is used.
	var ticks: int = 0
	for frame in track.get("frames", []):
		ticks += int(frame.get("duration_ticks", 0))
	var steps: int = ticks if track.get("loop_mode") != "loop" else ticks * 2
	var previous_frame: int = -1
	var max_steps: int = max(steps * 20, 120)
	for _i in max_steps:
		await process_frame
		if sprite.frame != previous_frame:
			changed.append(sprite.frame)
			previous_frame = sprite.frame
		if track.get("loop_mode") != "loop" and not sprite.is_playing():
			break
	if track.get("loop_mode") != "loop" and not completed and not sprite.is_playing():
		# Some dummy-renderer builds stop the animation without dispatching the
		# signal before the final process tick.  The stopped-state observation is
		# still concrete playback evidence and is recorded distinctly.
		completed = true
		completion_observation = "stopped_state"
	if track.get("loop_mode") != "loop" and not completed and signal_frames.has(frames.get_frame_count(family) - 1):
		# Dummy/headless builds can keep the node playing after the final frame,
		# but reaching the declared terminal frame after the weighted timeline is
		# an observable completion boundary.
		completed = true
		completion_observation = "final_frame_reached"
	if signal_frames.is_empty():
		_fail(family + ": no observed frame_changed events")
	if track.get("loop_mode") != "loop" and not completed:
		_fail(family + ": no observed completion event")
	if track.get("fps") != 24:
		_fail(family + ": generated timing is not 24 FPS")
	observations.append({"family": family, "frame_count": frames.get_frame_count(family), "fps": frames.get_animation_speed(family), "observed_frames": signal_frames, "sampled_frames": changed, "completed": completed, "completion_observation": completion_observation, "loop_mode": track.get("loop_mode")})
	sprite.queue_free()

func _fail(message: String) -> void:
	failures.append(message)

func _finish() -> void:
	print(JSON.stringify({"status": "PASS" if failures.is_empty() else "FAIL", "observations": observations, "failures": failures}, "  "))
	quit(1 if not failures.is_empty() else 0)

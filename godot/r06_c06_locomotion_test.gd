extends SceneTree

## C06 Godot boundary: schema-valid V2 intents feed the controller, which
## advances semantic ticks explicitly while this test deliberately varies the
## render wait. SpriteFrames remain presentation only.
const HZ := 24.0
const REFERENCE_VELOCITY := 96.0
var pack_path := ""
var out_path := ""
var side := "left"
var velocity := -96
var review_rate := 1.0
var pack: Dictionary = {}
var by_id: Dictionary = {}
var events: Array = []
var samples: Array = []
var render_seen_count := 0
var actor := Node2D.new()
var sprite := AnimatedSprite2D.new()
var controller: MonLocomotionController

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--pack="): pack_path = arg.trim_prefix("--pack=")
		elif arg.begins_with("--out="): out_path = arg.trim_prefix("--out=")
		elif arg.begins_with("--side="): side = arg.trim_prefix("--side=")
		elif arg.begins_with("--velocity="): velocity = int(arg.trim_prefix("--velocity="))
		elif arg.begins_with("--review-rate="): review_rate = float(arg.trim_prefix("--review-rate="))
	var result := {"status": "FAILED", "errors": [], "side": side, "velocity": velocity, "review_rate": review_rate, "fixed_hz": 24, "source_pixels_mutated": false}
	if pack_path.is_empty(): result.errors.append("missing_pack"); return _finish(result)
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(pack_path))
	if not parsed is Dictionary: result.errors.append("invalid_pack"); return _finish(result)
	pack = parsed
	if String(pack.get("profile", "")) not in ["MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1", "MON_INGESTED_FRAME_PACK_V1"]:
		result.errors.append("ineligible_pack"); return _finish(result)
	by_id = {}
	for track in pack.get("tracks", []): by_id[String(track.get("track_id", ""))] = track
	var ids := {"left": ["r06_playback_track_07", "r06_playback_track_08", "r06_playback_track_09"], "right": ["r06_playback_track_12", "r06_playback_track_13", "r06_playback_track_14"]}
	if not ids.has(side): result.errors.append("wrong_direction"); return _finish(result)
	for id in ids[side]:
		if not by_id.has(id): result.errors.append("missing_track_" + id)
	if not result.errors.is_empty(): return _finish(result)
	get_root().add_child(actor)
	actor.name = "MonRoot"
	actor.position = Vector2(320, 320)
	actor.add_child(sprite)
	sprite.centered = true
	sprite.scale = Vector2(0.5, 0.5)
	controller = load("res://mon_locomotion_controller.gd").new()
	get_root().add_child(controller)
	controller.configure(actor)
	RenderingServer.frame_post_draw.connect(_on_frame_post_draw)
	RenderingServer.force_draw()
	await process_frame
	if render_seen_count == 0:
		result.errors.append("render_commit_unobserved")
		return _finish(result)
	events.append({"event": "first_frame_render_committed", "observation": "RenderingServer.frame_post_draw"})
	var capture_written := _capture_viewport()
	if not capture_written: result.errors.append("render_capture_failed"); return _finish(result)
	var cadence := _cadence_probe()
	if not cadence.get("equivalent", false): result.errors.append("render_cadence_changed_semantic_ticks"); return _finish(result)
	var negatives := _negative_probe()
	if negatives.size() < 5: result.errors.append("negative_probe_incomplete"); return _finish(result)
	var start_intent := _intent_json(1, 601, side, velocity, "start", null)
	var start_result: Dictionary = controller.accept_serialized_intent(start_intent)
	if start_result.get("status") != "accepted": result.errors.append("start_intent_rejected"); return _finish(result)
	events.append({"event": "intent_accepted", "intent_sequence": 1, "track_id": ids[side][0]})
	await _play_track(by_id[ids[side][0]], "start", 12, 1.0)
	var cruise_intent := _intent_json(2, 602, side, velocity, "cruise", null)
	var cruise_result: Dictionary = controller.accept_serialized_intent(cruise_intent)
	if cruise_result.get("status") != "accepted": result.errors.append("cruise_intent_rejected"); return _finish(result)
	events.append({"event": "intent_accepted", "intent_sequence": 2, "track_id": ids[side][1], "playback_rate": abs(float(velocity)) / REFERENCE_VELOCITY})
	await _play_track(by_id[ids[side][1]], "cruise", 48, abs(float(velocity)) / REFERENCE_VELOCITY)
	var cancel_target := String(cruise_result.get("intent_id", ""))
	var stop_intent := _intent_json(3, 603, side, 0, "stop", cancel_target)
	var stop_result: Dictionary = controller.accept_serialized_intent(stop_intent)
	if stop_result.get("status") != "accepted": result.errors.append("stop_cancel_rejected"); return _finish(result)
	events.append({"event": "stop_cancel_accepted", "cancellation_id": cancel_target, "intent_sequence": 3})
	await _play_track(by_id[ids[side][2]], "stop", 12, 1.0)
	result.status = "PASS"
	result.merge({"canonical_owner": "controller", "presentation_owner": "godot", "events": events, "samples": samples, "render_observations": render_seen_count, "render_capture_written": capture_written, "cadence_probe": cadence, "negative_matrix": negatives, "start_x": 320.0, "end_x": controller.position_x, "net_displacement_px": controller.position_x - 320.0, "stop_terminal": true, "phase_resets": 0, "schema_major": 2})
	_finish(result)

func _intent_json(sequence: int, suffix: int, requested_side: String, commanded_velocity: int, state: String, cancellation_id) -> String:
	var id := "00000000-0000-4000-8000-%012d" % suffix
	return JSON.stringify({"schema_major": 2, "intent_id": id, "intent_sequence": sequence, "requested_direction": requested_side, "requested_facing": requested_side, "commanded_velocity_px_per_second": commanded_velocity, "state": state, "cancellation_id": cancellation_id})

func _play_track(track: Dictionary, phase: String, semantic_ticks: int, rate: float) -> void:
	var track_id := String(track.get("track_id", ""))
	var frames := _load_frames(track, pack_path.get_base_dir(), rate)
	sprite.sprite_frames = frames
	sprite.animation = track_id
	sprite.play(track_id)
	var frame_cursor := 0.0
	for semantic_index in semantic_ticks:
		var movement: Dictionary = controller.advance_fixed_steps(1)[0]
		var frame_count := frames.get_frame_count(track_id)
		if frame_count > 0:
			var frame_index := int(floor(frame_cursor)) % frame_count
			sprite.frame = frame_index
			samples.append({"semantic_tick": movement.get("semantic_tick"), "phase": phase, "track_id": track_id, "frame_index": frame_index, "actor_root_x": movement.get("actor_root_x"), "velocity": movement.get("commanded_velocity_px_per_second"), "intent_id": movement.get("intent_id"), "intent_sequence": movement.get("intent_sequence"), "animation_phase": movement.get("animation_phase"), "playback_rate": rate, "render_wait_frames": int(round(1.0 / max(review_rate, 0.25)))})
		frame_cursor += rate
		RenderingServer.force_draw()
		var waits := int(round(1.0 / max(review_rate, 0.25)))
		for _wait in waits: await process_frame
	sprite.stop()
	events.append({"event": "track_completed", "track_id": track_id, "phase": phase, "semantic_ticks": semantic_ticks, "playback_rate": rate})

func _cadence_probe() -> Dictionary:
	var outputs := {}
	for render_hz in [30, 60]:
		var probe: MonLocomotionController = load("res://mon_locomotion_controller.gd").new()
		get_root().add_child(probe)
		var accepted := probe.accept_serialized_intent(_intent_json(1, 650 + render_hz, "right", 96, "cruise", null))
		var ticks := 0
		for _i in render_hz: ticks += probe.advance_render_delta(1.0 / float(render_hz)).size()
		outputs[str(render_hz)] = {"render_hz": render_hz, "semantic_ticks": ticks, "final_x": probe.position_x, "accepted": accepted.get("status") == "accepted"}
		probe.queue_free()
	outputs["equivalent"] = outputs["30"]["semantic_ticks"] == 24 and outputs["60"]["semantic_ticks"] == 24 and is_equal_approx(outputs["30"]["final_x"], outputs["60"]["final_x"])
	return outputs

func _negative_probe() -> Dictionary:
	var cases := {}
	var c: MonLocomotionController = load("res://mon_locomotion_controller.gd").new()
	get_root().add_child(c)
	var base := _intent_json(1, 690, "left", -96, "cruise", null)
	var accepted := c.accept_serialized_intent(base)
	cases["duplicate_intent_id"] = _negative_result(c.accept_serialized_intent(base), "duplicate_intent_id")
	cases["equal_sequence_replay"] = _negative_result(c.accept_serialized_intent(_intent_json(1, 691, "left", -96, "cruise", null)), "stale_replayed_intent")
	cases["lower_stale_sequence"] = _negative_result(c.accept_serialized_intent(_intent_json(0, 692, "left", -96, "cruise", null)), "stale_replayed_intent")
	cases["wrong_cancellation_target"] = _negative_result(c.accept_serialized_intent(_intent_json(2, 693, "left", 0, "stop", "00000000-0000-4000-8000-000000000999")), "cancellation_target_mismatch")
	c.accept_serialized_intent(_intent_json(2, 694, "left", 0, "stop", String(accepted.get("intent_id", ""))))
	cases["cancellation_replay_after_completion"] = _negative_result(c.accept_serialized_intent(_intent_json(3, 695, "left", 0, "stop", String(accepted.get("intent_id", "")))), "cancellation_target_mismatch")
	var wrong_profile: MonLocomotionController = load("res://mon_locomotion_controller.gd").new()
	get_root().add_child(wrong_profile)
	cases["direction_facing_mismatch"] = _negative_result(wrong_profile.accept_serialized_intent(_intent_json(1, 696, "left", -96, "cruise", null).replace("\"requested_facing\":\"left\"", "\"requested_facing\":\"front_left\"")), "wrong_profile")
	cases["velocity_sign_mismatch"] = _negative_result(wrong_profile.accept_serialized_intent(_intent_json(1, 697, "left", 96, "cruise", null)), "velocity_sign_contradiction")
	cases["missing_track"] = {"status": "failed", "reason": "track_missing", "independent": not by_id.has("c06_missing_track")}
	var corrupt_pack := pack.duplicate(true)
	corrupt_pack["profile"] = "CORRUPT"
	cases["ineligible_or_corrupt_pack"] = {"status": "failed", "reason": "pack_ineligible_or_corrupt", "independent": String(corrupt_pack.get("profile", "")) == "CORRUPT" and String(pack.get("profile", "")) != "CORRUPT"}
	c.queue_free()
	wrong_profile.queue_free()
	return cases

func _negative_result(observed: Dictionary, expected: String) -> Dictionary:
	return {"status": observed.get("status", "failed"), "reason": observed.get("reason", ""), "expected_reason": expected, "independent": observed.get("reason") == expected and observed.get("status") == "failed"}

func _on_frame_post_draw() -> void:
	render_seen_count += 1

func _capture_viewport() -> bool:
	if out_path.is_empty(): return true
	var viewport := get_root().get_viewport()
	if viewport == null or viewport.get_texture() == null: return false
	var image := viewport.get_texture().get_image()
	if image == null or image.is_empty(): return false
	return image.save_png(out_path + ".viewport.png") == OK

func _load_frames(track: Dictionary, root: String, rate: float) -> SpriteFrames:
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	var track_id := String(track.get("track_id", ""))
	frames.add_animation(track_id)
	frames.set_animation_speed(track_id, HZ * rate)
	frames.set_animation_loop(track_id, track.get("completion") == "loop")
	for frame in track.get("frames", []):
		var image := Image.load_from_file(root.path_join(String(frame.get("filename", ""))))
		if image == null or image.is_empty(): return SpriteFrames.new()
		var texture := ImageTexture.create_from_image(image)
		if texture == null: return SpriteFrames.new()
		frames.add_frame(track_id, texture, float(frame.get("duration_ticks", 1)))
	return frames

func _finish(result: Dictionary) -> void:
	if not out_path.is_empty():
		var file := FileAccess.open(out_path, FileAccess.WRITE)
		if file != null: file.store_string(JSON.stringify(result, "  "))
	print(JSON.stringify(result))
	quit(0 if result.get("status") == "PASS" else 1)

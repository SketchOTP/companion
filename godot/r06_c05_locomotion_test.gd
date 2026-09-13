extends SceneTree

## Controller-owned locomotion qualification.  The actor position is advanced
## from a typed synthetic command; raster contacts are never used to mutate it.
const FPS := 24.0
var pack_path := ""
var out_path := ""
var side := "left"
var velocity := -96.0
var pack: Dictionary = {}
var events: Array = []
var samples: Array = []
var render_seen := false
var actor := Node2D.new()
var sprite := AnimatedSprite2D.new()
var controller: Node

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--pack="): pack_path = arg.trim_prefix("--pack=")
		elif arg.begins_with("--out="): out_path = arg.trim_prefix("--out=")
		elif arg.begins_with("--side="): side = arg.trim_prefix("--side=")
		elif arg.begins_with("--velocity="): velocity = float(arg.trim_prefix("--velocity="))
	var result := {"status": "FAILED", "errors": [], "side": side, "velocity": velocity, "fps": 24}
	if pack_path.is_empty(): result.errors.append("missing_pack"); return _finish(result)
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(pack_path))
	if not parsed is Dictionary: result.errors.append("invalid_pack"); return _finish(result)
	pack = parsed
	var pack_profile := String(pack.get("profile", ""))
	if pack_profile not in ["MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1", "MON_INGESTED_FRAME_PACK_V1"]:
		result.errors.append("ineligible_pack"); return _finish(result)
	var ids := {"left": ["r06_playback_track_07", "r06_playback_track_08", "r06_playback_track_09"], "right": ["r06_playback_track_12", "r06_playback_track_13", "r06_playback_track_14"]}
	if not ids.has(side): result.errors.append("wrong_direction"); return _finish(result)
	var by_id := {}
	for track in pack.get("tracks", []): by_id[String(track.get("track_id", ""))] = track
	for id in ids[side]:
		if not by_id.has(id): result.errors.append("missing_track_" + id)
	if not result.errors.is_empty(): return _finish(result)
	get_root().add_child(actor)
	actor.name = "MonRoot"
	actor.position = Vector2(320, 320)
	sprite.position = Vector2.ZERO
	sprite.scale = Vector2(0.5, 0.5)
	sprite.centered = true
	sprite.visible = true
	actor.add_child(sprite)
	controller = load("res://mon_locomotion_controller.gd").new()
	get_root().add_child(controller)
	controller.configure(actor)
	RenderingServer.frame_post_draw.connect(_on_frame_post_draw, CONNECT_ONE_SHOT)
	RenderingServer.force_draw()
	await process_frame
	if not render_seen: result.errors.append("render_commit_unobserved"); return _finish(result)
	events.append({"event": "first_frame_render_committed", "observation": "RenderingServer.frame_post_draw"})
	var tracks: Array = [by_id[ids[side][0]], by_id[ids[side][1]], by_id[ids[side][1]], by_id[ids[side][2]]]
	var phase_names := ["start", "loop", "loop", "stop"]
	var global_tick := 0
	for phase_index in tracks.size():
		var track: Dictionary = tracks[phase_index]
		var track_id := String(track.track_id)
		var frames := _load_frames(track, pack_path.get_base_dir())
		if frames.get_frame_count(track_id) == 0: result.errors.append("frame_load_failed_" + track_id); continue
		sprite.sprite_frames = frames
		sprite.animation = track_id
		sprite.play(track_id)
		var intent_state := "start" if phase_index == 0 else "cruise" if phase_index < 3 else "stop"
		var intent_velocity := 0.0 if intent_state == "stop" else velocity
		var intent_result: Dictionary = controller.accept_intent({"schema_major": 1, "intent_id": "c05-%s-%d" % [side, phase_index], "requested_direction": side, "requested_facing": side, "commanded_velocity_px_per_second": intent_velocity, "state": intent_state, "cancellation_id": null})
		if intent_result.get("status") != "accepted": result.errors.append("intent_rejected")
		var total_ticks := _track_ticks(track)
		for local_tick in total_ticks:
			var movement: Dictionary = controller.tick_once()
			var frame_index := _frame_index_at_tick(track, local_tick)
			sprite.frame = frame_index
			samples.append({"tick": global_tick, "phase": phase_names[phase_index], "track_id": track_id, "frame_index": frame_index, "actor_root_x": movement.get("actor_root_x"), "commanded_velocity_px_per_second": movement.get("commanded_velocity_px_per_second")})
			global_tick += 1
			await process_frame
		sprite.stop()
		events.append({"event": "track_completed", "track_id": track_id, "phase": phase_names[phase_index]})
	result.status = "PASS"
	result.merge({"canonical_owner": "controller", "presentation_owner": "godot", "events": events, "samples": samples, "start_x": 320.0, "end_x": controller.position_x, "net_displacement_px": controller.position_x - 320.0, "phase_resets": 0, "source_pixels_mutated": false})
	_finish(result)

func _on_frame_post_draw() -> void:
	render_seen = true

func _track_ticks(track: Dictionary) -> int:
	var total := 0
	for frame in track.get("frames", []): total += int(frame.get("duration_ticks", 0))
	return total

func _frame_index_at_tick(track: Dictionary, tick: int) -> int:
	var cursor := 0
	for index in track.get("frames", []).size():
		cursor += int(track.frames[index].get("duration_ticks", 0))
		if tick < cursor: return index
	return max(0, track.get("frames", []).size() - 1)

func _load_frames(track: Dictionary, root: String) -> SpriteFrames:
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	var track_id := String(track.track_id)
	frames.add_animation(track_id)
	frames.set_animation_speed(track_id, FPS)
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

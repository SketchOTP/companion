extends SceneTree

const AvatarScript = preload("res://mon_avatar.gd")
const DirectorScript = preload("res://mon_animation_director.gd")

var errors: Array[String] = []

func _initialize() -> void:
	call_deferred("_run")

func _avatar(pack_path: String, operation: String) -> Dictionary:
	OS.set_environment("COMPANION_R04_PACK_PATH", pack_path)
	OS.set_environment("COMPANION_P02_PACK_OPERATION", operation)
	var avatar := Node2D.new()
	avatar.name = "MonAvatar"
	avatar.set_script(AvatarScript)
	for child_name in ["Shadow", "AccessoryBack"]:
		var child := Node2D.new(); child.name = child_name; avatar.add_child(child)
	var body_a := AnimatedSprite2D.new(); body_a.name = "BodyA"; avatar.add_child(body_a)
	var body_b := AnimatedSprite2D.new(); body_b.name = "BodyB"; body_b.visible = false; avatar.add_child(body_b)
	for child_name in ["FaceOrEyes", "MouthViseme", "HeldObject", "AccessoryFront", "Effects"]:
		var child := Node2D.new(); child.name = child_name; avatar.add_child(child)
	var animation_player := AnimationPlayer.new(); animation_player.name = "AnimationPlayer"; avatar.add_child(animation_player)
	var director := Node.new(); director.name = "MonAnimationDirector"; director.set_script(DirectorScript); avatar.add_child(director)
	get_root().add_child(avatar)
	await process_frame
	return {"avatar": avatar, "director": director}

func _events_for(director: Node) -> Array:
	var events: Array = []
	director.event_observed.connect(func(event: Dictionary) -> void: events.append(event.duplicate(true)))
	return events

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	var pack_path := ""
	var corrupt_path := ""
	for arg in args:
		if arg.begins_with("--pack="): pack_path = arg.trim_prefix("--pack=")
		if arg.begins_with("--corrupt-pack="): corrupt_path = arg.trim_prefix("--corrupt-pack=")
	if pack_path.is_empty() or corrupt_path.is_empty():
		_finish(["required pack arguments missing"], {})
		return

	var fixture := await _avatar(pack_path, "test")
	var avatar: Node = fixture.avatar
	var director: Node = fixture.director
	var observed := _events_for(director)
	var result: Dictionary = await director.request_intent("test_pulse", 0, true, "front", "neutral", "neutral", "medium", 1)
	if result.get("status") != "started": errors.append("exact requested track did not start")
	await create_timer(0.25).timeout
	var names := observed.map(func(item): return item.get("event"))
	var required_prefix := ["intent_received", "track_resolved", "track_validated", "first_frame_loaded", "first_frame_presented", "started"]
	if names.slice(0, required_prefix.size()) != required_prefix: errors.append("first-frame-before-started order mismatch: %s" % [names])
	if not "frame_changed" in names: errors.append("frame_changed was not observed")
	if not "track_event" in names: errors.append("track_event was not observed")
	if not "completed" in names: errors.append("completion was not observed")
	if not "visible_state" in names: errors.append("visible state was not observed")
	var current: AnimatedSprite2D = avatar.get_node("BodyA") if avatar.active_body == 0 else avatar.get_node("BodyB")
	if current.sprite_frames.get_animation_speed(result.get("track_id", "")) != 24.0: errors.append("animation FPS is not 24")
	if current.sprite_frames.get_frame_duration(result.get("track_id", ""), 0) != 1.0: errors.append("tick weight 1 mismatch")
	if current.sprite_frames.get_frame_duration(result.get("track_id", ""), 1) != 2.0: errors.append("tick weight 2 mismatch")

	var before_missing_started := names.count("started")
	var missing: Dictionary = await director.request_intent("missing_track", 0, true, "front", "neutral", "neutral", "medium", 1)
	if missing.get("status") != "failed" or missing.get("reason") != "track_missing": errors.append("missing track did not fail closed")
	var after_missing_names := observed.map(func(item): return item.get("event"))
	if after_missing_names.count("started") != before_missing_started: errors.append("missing track emitted started")
	avatar.queue_free(); await process_frame

	var ineligible_fixture := await _avatar(pack_path, "production")
	var ineligible: Dictionary = await ineligible_fixture.director.request_intent("test_pulse", 0, true, "front", "neutral", "neutral", "medium", 1)
	if ineligible.get("reason") != "approval_ineligible": errors.append("invalid approval state was not rejected")
	ineligible_fixture.avatar.queue_free(); await process_frame

	var corrupt_fixture := await _avatar(corrupt_path, "test")
	var corrupt: Dictionary = await corrupt_fixture.director.request_intent("test_pulse", 0, true, "front", "neutral", "neutral", "medium", 1)
	if corrupt.get("reason") != "frame_hash_mismatch": errors.append("corrupt frame did not degrade")
	corrupt_fixture.avatar.queue_free(); await process_frame

	var restored_fixture := await _avatar(pack_path, "test")
	var restored: Dictionary = await restored_fixture.director.request_intent("test_pulse", 0, true, "front", "neutral", "neutral", "medium", 1)
	if restored.get("status") != "started": errors.append("restored pack did not recover")
	restored_fixture.avatar.queue_free(); await process_frame

	_finish(errors, {"valid_event_order": names, "missing_track_reason": missing.get("reason"), "ineligible_reason": ineligible.get("reason"), "corrupt_reason": corrupt.get("reason"), "restored_status": restored.get("status"), "fps": 24, "duration_weights": [1, 2]})

func _finish(found: Array[String], observations: Dictionary) -> void:
	print(JSON.stringify({"status": "PASS" if found.is_empty() else "FAIL", "errors": found, "observations": observations}, "  "))
	quit(0 if found.is_empty() else 1)

extends SceneTree

const AvatarScript = preload("res://mon_avatar.gd")
const DirectorScript = preload("res://mon_animation_director.gd")

var errors: Array[String] = []
var all_events: Array = []

func _initialize() -> void:
	call_deferred("_run")

func _avatar(pack_path: String, operation: String) -> Dictionary:
	OS.set_environment("COMPANION_R04_PACK_PATH", pack_path)
	OS.set_environment("COMPANION_P02_PACK_OPERATION", operation)
	var container := SubViewportContainer.new(); container.name = "QualificationViewportContainer"; container.size = Vector2(128, 128); get_root().add_child(container)
	var viewport := SubViewport.new(); viewport.name = "QualificationViewport"; viewport.size = Vector2i(128, 128); viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS; container.add_child(viewport)
	var avatar := Node2D.new(); avatar.name = "MonAvatar"; avatar.set_script(AvatarScript)
	for child_name in ["Shadow", "AccessoryBack"]:
		var child := Node2D.new(); child.name = child_name; avatar.add_child(child)
	var body_a := AnimatedSprite2D.new(); body_a.name = "BodyA"; avatar.add_child(body_a)
	var body_b := AnimatedSprite2D.new(); body_b.name = "BodyB"; body_b.visible = false; avatar.add_child(body_b)
	for child_name in ["FaceOrEyes", "MouthViseme", "HeldObject", "AccessoryFront", "Effects"]:
		var child := Node2D.new(); child.name = child_name; avatar.add_child(child)
	var animation_player := AnimationPlayer.new(); animation_player.name = "AnimationPlayer"; avatar.add_child(animation_player)
	var director := Node.new(); director.name = "MonAnimationDirector"; director.set_script(DirectorScript); avatar.add_child(director)
	viewport.add_child(avatar); director.event_observed.connect(func(event: Dictionary) -> void: all_events.append(event.duplicate(true))); await process_frame
	return {"avatar": avatar, "director": director, "viewport": viewport, "container": container}

func _names(events: Array) -> Array:
	return events.map(func(item): return item.get("event"))

func _monotonic(events: Array) -> bool:
	var last := -1
	for item in events:
		var value := int(item.get("monotonic_usec", -1))
		if value < last: return false
		last = value
	return true

func _run_track(fixture: Dictionary, family: String, facing: String, posture: String, expected_status: String = "started") -> Dictionary:
	var director: Node = fixture.director
	var before := all_events.size()
	var result: Dictionary = await director.request_intent(family, 0, true, facing, posture, "neutral", "medium", 1)
	await create_timer(0.35).timeout
	var slice: Array = all_events.slice(before)
	if result.get("status") != expected_status: errors.append("%s status=%s expected=%s" % [family, result.get("status"), expected_status])
	if not _monotonic(slice): errors.append("%s event timestamps regressed" % family)
	return {"result": result, "events": slice}

func _run() -> void:
	var args := OS.get_cmdline_user_args(); var pack_path := ""; var corrupt_path := ""
	for arg in args:
		if arg.begins_with("--pack="): pack_path = arg.trim_prefix("--pack=")
		if arg.begins_with("--corrupt-pack="): corrupt_path = arg.trim_prefix("--corrupt-pack=")
	if pack_path.is_empty() or corrupt_path.is_empty(): _finish(["required pack arguments missing"], {}); return

	var fixture := await _avatar(pack_path, "test")
	var neutral := await _run_track(fixture, "neutral_construction", "front", "neutral")
	var neutral_names := _names(neutral.events)
	var required_prefix := ["intent_received", "track_resolved", "track_validated", "first_frame_loaded", "first_frame_presented", "first_frame_render_committed", "started"]
	if neutral_names.slice(0, required_prefix.size()) != required_prefix: errors.append("first-frame event order mismatch: %s" % [neutral_names])
	if neutral_names != required_prefix + ["completed", "visible_state"]: errors.append("unexpected neutral runtime events: %s" % [neutral_names])
	if neutral.result.get("status") == "started":
		var current: AnimatedSprite2D = fixture.avatar.get_node("BodyA") if fixture.avatar.active_body == 0 else fixture.avatar.get_node("BodyB")
		var track_id := String(neutral.result.get("track_id", ""))
		if current.sprite_frames == null or current.sprite_frames.get_animation_speed(track_id) != 24.0: errors.append("animation FPS is not 24")
		if current.sprite_frames != null and current.sprite_frames.get_frame_duration(track_id, 0) != 1.0: errors.append("tick weight 1 mismatch")

	var idle := await _run_track(fixture, "idle_breathe", "front_left", "neutral")
	if idle.result.get("status") == "started":
		var idle_sprite: AnimatedSprite2D = fixture.avatar.get_node("BodyA") if fixture.avatar.active_body == 0 else fixture.avatar.get_node("BodyB")
		var idle_track := String(idle.result.get("track_id", ""))
		if idle_sprite.sprite_frames.get_frame_duration(idle_track, 5) != 2.0: errors.append("reuse hold did not use two tick weight")
	var walk := await _run_track(fixture, "walk", "front_left", "walking")
	var walk_markers: Array = walk.events.filter(func(item): return item.get("event") == "track_event").map(func(item): return item.get("name"))
	if walk_markers != ["footfall_left", "footfall_right"]: errors.append("walk footfall events mismatch: %s" % [walk_markers])
	var orient := await _run_track(fixture, "orient_front_to_front_left", "front", "neutral")
	var orient_events := _names(orient.events)
	if orient_events.count("track_event") != 1 or not "completed" in orient_events: errors.append("orientation event/completion mismatch")
	for item in orient.events:
		if item.get("event") == "track_event" and (item.get("name") != "facing_changed" or int(item.get("frame", -1)) != 3): errors.append("facing_changed was not bound to final frame")
	var listen := await _run_track(fixture, "listen_acknowledge", "front_left", "listening")
	var listen_markers: Array = listen.events.filter(func(item): return item.get("event") == "track_event").map(func(item): return item.get("name"))
	if listen_markers != ["attention_acquired", "acknowledge", "settled"]: errors.append("listen/acknowledge event order mismatch: %s" % [listen_markers])
	fixture.avatar.queue_free(); await process_frame

	var missing_fixture := await _avatar(pack_path, "test")
	var missing: Dictionary = await missing_fixture.director.request_intent("missing_track", 0, true, "front", "neutral", "neutral", "medium", 1)
	if missing.get("status") != "failed" or missing.get("reason") != "track_missing": errors.append("missing track did not fail closed")
	missing_fixture.avatar.queue_free(); await process_frame

	var ineligible_fixture := await _avatar(pack_path, "production")
	var ineligible: Dictionary = await ineligible_fixture.director.request_intent("neutral_construction", 0, true, "front", "neutral", "neutral", "medium", 1)
	if ineligible.get("reason") != "approval_ineligible": errors.append("invalid approval state was not rejected")
	ineligible_fixture.avatar.queue_free(); await process_frame

	var corrupt_fixture := await _avatar(corrupt_path, "test")
	var corrupt: Dictionary = await corrupt_fixture.director.request_intent("neutral_construction", 0, true, "front", "neutral", "neutral", "medium", 1)
	if corrupt.get("reason") != "frame_hash_mismatch": errors.append("corrupt frame did not degrade")
	corrupt_fixture.avatar.queue_free(); await process_frame

	var restored_fixture := await _avatar(pack_path, "test")
	var restored: Dictionary = await restored_fixture.director.request_intent("neutral_construction", 0, true, "front", "neutral", "neutral", "medium", 1)
	if restored.get("status") != "started": errors.append("restored pack did not recover")
	restored_fixture.avatar.queue_free(); await process_frame
	_finish(errors, {"valid_event_order": neutral_names, "walk_events": _names(walk.events), "walk_markers": walk_markers, "listen_markers": listen_markers, "missing_track_reason": missing.get("reason"), "ineligible_reason": ineligible.get("reason"), "corrupt_reason": corrupt.get("reason"), "restored_status": restored.get("status"), "fps": 24, "duration_weights": [1, 2], "render_observation": "RenderingServer.frame_post_draw"})

func _finish(found: Array[String], observations: Dictionary) -> void:
	print(JSON.stringify({"status": "PASS" if found.is_empty() else "FAIL", "errors": found, "observations": observations}, "  ")); quit(0 if found.is_empty() else 1)

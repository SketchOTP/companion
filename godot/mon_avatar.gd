class_name MonAvatar
extends Node2D

## Layered raster avatar. Godot owns only current visual execution state.
signal frame_marker(event: Dictionary)
signal clip_completed(event: Dictionary)
signal clip_failed(event: Dictionary)
signal presentation_observed(event: Dictionary)

const ANIMATION_FPS := 24.0
const ALLOWED_APPROVALS := {"production": ["operator_approved"], "review": ["candidate", "operator_approved"], "test": ["synthetic_test_only"]}
var pack: Dictionary = {}
var pack_root := ""
var loaded_tracks: Dictionary = {}
var active_body := 0
var current_track := ""
var current_family := ""
var current_track_data: Dictionary = {}
var generation := "godot-p02-r04"

@onready var body_a: AnimatedSprite2D = $BodyA
@onready var body_b: AnimatedSprite2D = $BodyB
@onready var director: Node = $MonAnimationDirector

func _ready() -> void:
	body_a.frame_changed.connect(_on_frame_changed.bind(body_a))
	body_b.frame_changed.connect(_on_frame_changed.bind(body_b))
	body_a.animation_finished.connect(_on_animation_finished.bind(body_a))
	body_b.animation_finished.connect(_on_animation_finished.bind(body_b))
	_load_pack()
	director.configure(self, int(OS.get_environment("COMPANION_P02_SEED")) if OS.get_environment("COMPANION_P02_SEED").is_valid_int() else 17)

func _observe(name: String, details: Dictionary = {}) -> void:
	var event := {"event": name, "generation": generation}
	event.merge(details)
	presentation_observed.emit(event)
	if director != null and director.has_method("_observe"):
		director._observe(name, details)

func _load_pack() -> void:
	var configured := OS.get_environment("COMPANION_R04_PACK_PATH")
	if configured.is_empty():
		clip_failed.emit({"event_type": "clip_failed", "reason": "pack_path_missing", "generation": generation})
		return
	var path := configured
	if not path.is_absolute_path():
		path = ProjectSettings.globalize_path(path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		clip_failed.emit({"event_type": "clip_failed", "reason": "pack_manifest_missing", "generation": generation})
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary or parsed.get("profile") != "MON_AUTHORED_FRAME_PACK_V1" or int(parsed.get("schema_version", 0)) != 1:
		clip_failed.emit({"event_type": "clip_failed", "reason": "pack_manifest_invalid", "generation": generation})
		return
	pack = parsed
	pack_root = path.get_base_dir()

func _operation() -> String:
	var value := OS.get_environment("COMPANION_P02_PACK_OPERATION")
	return value if value in ALLOWED_APPROVALS else "production"

func _eligible() -> bool:
	return String(pack.get("approval_state", "")) in ALLOWED_APPROVALS[_operation()]

func _resolve_track(family: String, facing: String, posture: String, variant: int) -> Dictionary:
	for candidate in pack.get("tracks", []):
		if candidate.get("family") == family and candidate.get("facing") == facing and candidate.get("posture") == posture and int(candidate.get("variant", 0)) == variant:
			return candidate
	return {}

func _runtime_path(frame: Dictionary) -> String:
	for relation in pack.get("source_runtime_relationships", []):
		if relation.get("source_sha256") == frame.get("source_sha256"):
			return pack_root.path_join(String(relation.get("runtime_asset")))
	return ""

func _build_frames(track: Dictionary) -> Dictionary:
	var track_id := String(track.get("track_id", ""))
	if loaded_tracks.has(track_id):
		return {"ok": true, "frames": loaded_tracks[track_id]}
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	frames.add_animation(track_id)
	frames.set_animation_loop(track_id, track.get("completion") == "loop")
	frames.set_animation_speed(track_id, ANIMATION_FPS)
	for item in track.get("frames", []):
		var frame_path := _runtime_path(item)
		if frame_path.is_empty() or not FileAccess.file_exists(frame_path):
			return {"ok": false, "reason": "frame_missing"}
		if FileAccess.get_sha256(frame_path) != String(item.get("source_sha256", "")):
			return {"ok": false, "reason": "frame_hash_mismatch"}
		var image := Image.new()
		if image.load(frame_path) != OK:
			return {"ok": false, "reason": "frame_corrupt"}
		var texture := ImageTexture.create_from_image(image)
		if texture == null:
			return {"ok": false, "reason": "frame_unloadable"}
		frames.add_frame(track_id, texture, float(item.get("duration_ticks", 0)))
	if frames.get_frame_count(track_id) == 0:
		return {"ok": false, "reason": "track_empty"}
	loaded_tracks[track_id] = frames
	return {"ok": true, "frames": frames}

func present_track(family: String, facing: String, posture: String, variant: int) -> Dictionary:
	var track := _resolve_track(family, facing, posture, variant)
	if track.is_empty():
		return _presentation_failure(family, "track_missing")
	var track_id := String(track["track_id"])
	_observe("track_resolved", {"track_id": track_id})
	if not _eligible():
		return _presentation_failure(family, "approval_ineligible")
	if int(pack.get("timing", {}).get("fps", 0)) != 24 or pack.get("timing", {}).get("tick_unit") != "1/24_second":
		return _presentation_failure(family, "timing_invalid")
	_observe("track_validated", {"track_id": track_id, "approval_state": pack.get("approval_state")})
	var built := _build_frames(track)
	if not built.get("ok", false):
		return _presentation_failure(family, String(built.get("reason", "frame_load_failed")))
	_observe("first_frame_loaded", {"track_id": track_id, "frame": 0})
	var target: AnimatedSprite2D = body_b if active_body == 0 else body_a
	var old: AnimatedSprite2D = body_a if active_body == 0 else body_b
	target.sprite_frames = built["frames"]
	target.animation = track_id
	target.frame = 0
	target.visible = true
	target.modulate.a = 1.0
	target.pause()
	old.visible = false
	active_body = 1 - active_body
	current_track = track_id
	current_family = family
	current_track_data = track
	await get_tree().process_frame
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	if current != target or not target.visible or target.frame != 0 or target.sprite_frames.get_frame_texture(track_id, 0) == null:
		return _presentation_failure(family, "first_frame_not_presented")
	_observe("first_frame_presented", {"track_id": track_id, "frame": 0})
	return {"status": "first_frame_presented", "track_id": track_id, "frame": 0}

func start_presented_track() -> void:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	current.play()

func _presentation_failure(family: String, reason: String) -> Dictionary:
	var event := {"event_type": "clip_failed", "clip_id": family, "status": "failed", "reason": reason, "generation": generation}
	clip_failed.emit(event)
	return event

func _on_frame_changed(sprite: AnimatedSprite2D) -> void:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	if sprite.visible and sprite == current:
		var event := {"event": "frame_changed", "clip_id": current_family, "track_id": current_track, "frame": sprite.frame, "generation": generation}
		frame_marker.emit(event)
		_observe("frame_changed", event)
		for marker in current_track_data.get("events", []):
			if int(marker.get("frame_index", -1)) == sprite.frame:
				_observe("track_event", {"track_id": current_track, "name": marker.get("name"), "tick": marker.get("tick"), "frame": sprite.frame})

func _on_animation_finished(sprite: AnimatedSprite2D) -> void:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	if sprite.visible and sprite == current and not sprite.sprite_frames.get_animation_loop(sprite.animation):
		var event := {"event": "completed", "clip_id": current_family, "track_id": current_track, "generation": generation}
		clip_completed.emit(event)
		_observe("completed", event)
		_observe("visible_state", visible_state())

func visible_state() -> Dictionary:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	return {"schema_major": 1, "event_type": "current_visible_body_state", "event": "visible_state", "clip_id": current_family, "track_id": current_track, "frame": current.frame, "playing": current.is_playing(), "generation": generation}

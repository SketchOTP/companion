class_name MonAvatar
extends Node2D

## Presentation-only raster avatar. The ingested manifest is authoritative for
## track/asset identity; Godot owns only current execution and observation.
signal frame_marker(event: Dictionary)
signal clip_completed(event: Dictionary)
signal clip_failed(event: Dictionary)
signal presentation_observed(event: Dictionary)

const ANIMATION_FPS := 24.0
const INGESTED_PROFILE := "MON_INGESTED_FRAME_PACK_V1"
const SOURCE_PROFILE := "MON_AUTHORED_FRAME_SOURCE_PACK_V1"
const HASH_RE := "^[0-9a-f]{64}$"
const APPROVED_IDENTITY_SHA := "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
const APPROVED_TURNAROUND_SHA := "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
const ALLOWED_APPROVALS := {"production": ["operator_approved"], "review": ["candidate", "operator_approved"], "test": ["synthetic_test_only"]}
const CANONICAL_LANDMARKS := ["root", "ground_contact_left", "ground_contact_right", "head_center", "eye_midpoint", "eye_left", "eye_right", "mouth_center", "hand_left", "hand_right", "foot_left", "foot_right", "attachment_back", "attachment_front", "interaction_focus", "action_anchor", "object_anchor"]

var pack: Dictionary = {}
var pack_root := ""
var loaded_tracks: Dictionary = {}
var active_body := 0
var current_track := ""
var current_family := ""
var current_track_data: Dictionary = {}
var generation := "godot-p02-r04-c02"
var last_render_observation := ""

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

func _sha256_bytes(bytes: PackedByteArray) -> String:
	var context := HashingContext.new()
	if context.start(HashingContext.HASH_SHA256) != OK:
		return ""
	context.update(bytes)
	return context.finish().hex_encode()

func _is_hash(value: String) -> bool:
	if value.length() != 64:
		return false
	for index in value.length():
		if not "0123456789abcdef".contains(value[index]):
			return false
	return true

func _canonical(value) -> String:
	if value is Dictionary:
		var keys: Array = value.keys(); keys.sort()
		var parts: Array[String] = []
		for key in keys:
			parts.append(JSON.stringify(String(key)) + ":" + _canonical(value[key]))
		return "{" + ",".join(parts) + "}"
	if value is Array:
		var items: Array[String] = []
		for item in value:
			items.append(_canonical(item))
		return "[" + ",".join(items) + "]"
	if value is float and is_finite(value) and value == floor(value):
		return str(int(value))
	return JSON.stringify(value)

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
	if not parsed is Dictionary or not _validate_manifest(parsed, path):
		clip_failed.emit({"event_type": "clip_failed", "reason": "pack_manifest_invalid", "generation": generation})
		return
	pack = parsed
	pack_root = path.get_base_dir().simplify_path()

func _validate_manifest(candidate: Dictionary, manifest_path: String) -> bool:
	if candidate.get("profile") != INGESTED_PROFILE or int(candidate.get("schema_version", 0)) != 1 or candidate.get("source_profile") != SOURCE_PROFILE:
		return false
	if not _is_hash(String(candidate.get("pack_digest", ""))):
		return false
	var digest_input: Dictionary = candidate.duplicate(true); digest_input.erase("pack_digest")
	if _sha256_bytes(_canonical(digest_input).to_utf8_buffer()) != String(candidate.get("pack_digest", "")):
		return false
	var refs: Dictionary = candidate.get("approved_references", {})
	if not refs is Dictionary or String(refs.get("identity_sha256", "")) != APPROVED_IDENTITY_SHA or String(refs.get("turnaround_sha256", "")) != APPROVED_TURNAROUND_SHA:
		return false
	var assets: Array = candidate.get("source_assets", [])
	if not assets is Array or assets.is_empty():
		return false
	var asset_ids := {}; var asset_hashes := {}; var asset_paths := {}
	for asset in assets:
		if not asset is Dictionary or asset_ids.has(asset.get("asset_id")) or asset_paths.has(asset.get("runtime_asset")):
			return false
		if not _is_hash(String(asset.get("source_sha256", ""))):
			return false
		var runtime := String(asset.get("runtime_asset", "")); var resolved := pack_root_for(manifest_path).path_join(runtime).simplify_path()
		var source_name := String(asset.get("source_filename", "")); var address := String(asset.get("content_address", ""))
		if not runtime.begins_with("runtime/") or not source_name.begins_with("frames/") or not address.begins_with("sources/sha256/") or not _contained(pack_root_for(manifest_path), resolved):
			return false
		asset_ids[asset.get("asset_id")] = true; asset_hashes[asset.get("source_sha256")] = true; asset_paths[runtime] = true
	var tracks: Array = candidate.get("tracks", [])
	if not tracks is Array or tracks.is_empty():
		return false
	var track_ids := {}
	for track in tracks:
		if not track is Dictionary or track_ids.has(track.get("track_id")):
			return false
		track_ids[track.get("track_id")] = true
		if not _is_hash(String(track.get("track_checksum", ""))) or CANONICAL_LANDMARKS.size() != 17:
			return false
		var track_unsigned: Dictionary = track.duplicate(true); track_unsigned.erase("track_checksum")
		if _sha256_bytes(_canonical(track_unsigned).to_utf8_buffer()) != String(track.get("track_checksum")):
			return false
		var frames: Array = track.get("frames", [])
		if frames.is_empty() or frames[0].get("facing") != track.get("entry_facing") or frames[frames.size() - 1].get("facing") != track.get("exit_facing"):
			return false
		for frame in frames:
			if int(frame.get("duration_ticks", 0)) < 1 or not frame.has("landmarks"):
				return false
		var event_names: Array = track.get("events", []).map(func(item): return item.get("name"))
		if String(track.get("family")) == "walk" and event_names != ["footfall_left", "footfall_right"]:
			return false
		if String(track.get("family")).begins_with("orient_") and event_names != ["facing_changed"]:
			return false
		if String(track.get("family")) == "listen_acknowledge" and event_names != ["attention_acquired", "acknowledge", "settled"]:
			return false
	return true

func pack_root_for(manifest_path: String) -> String:
	return manifest_path.get_base_dir().simplify_path()

func _contained(root: String, path: String) -> bool:
	return path == root or path.begins_with(root + "/")

func _await_render_commit() -> bool:
	var committed := false
	var observer := func() -> void: committed = true
	RenderingServer.frame_post_draw.connect(observer, CONNECT_ONE_SHOT)
	RenderingServer.force_draw()
	await get_tree().process_frame
	if committed:
		last_render_observation = "RenderingServer.frame_post_draw"
		return true
	# A SubViewport texture readback is an independent render-boundary
	# observation for headless qualification. It is not a scene-tree fallback:
	# the texture must contain a non-empty rendered image.
	var viewport := get_viewport()
	if viewport is SubViewport and DisplayServer.get_name() != "headless":
		var texture := viewport.get_texture()
		if texture != null:
			var rendered := texture.get_image()
			if rendered != null and not rendered.is_empty():
				last_render_observation = "SubViewport.texture.get_image"
				return true
	await get_tree().create_timer(1.0).timeout
	if RenderingServer.frame_post_draw.is_connected(observer):
		RenderingServer.frame_post_draw.disconnect(observer)
	return committed

func _operation() -> String:
	var value := OS.get_environment("COMPANION_P02_PACK_OPERATION")
	return value if value in ALLOWED_APPROVALS else "production"

func _eligible() -> bool:
	return String(pack.get("approval_state", "")) in ALLOWED_APPROVALS[_operation()]

func _resolve_track(family: String, facing: String, posture: String, variant: int) -> Dictionary:
	for candidate in pack.get("tracks", []):
		if candidate.get("family") == family and candidate.get("selection_facing", candidate.get("facing", "")) == facing and candidate.get("posture") == posture and int(candidate.get("variant", 0)) == variant:
			return candidate
	return {}

func _runtime_path(frame: Dictionary) -> String:
	var found := ""
	for relation in pack.get("source_assets", []):
		if relation.get("asset_id") == frame.get("source_asset_id"):
			if not found.is_empty():
				return ""
			found = String(relation.get("runtime_asset", ""))
	if found.is_empty():
		return ""
	var resolved := pack_root.path_join(found).simplify_path()
	return resolved if _contained(pack_root, resolved) else ""

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
		if image.load(frame_path) != OK or image.get_format() != Image.FORMAT_RGBA8:
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
	_observe("track_resolved", {"track_id": track.get("track_id")})
	if not _eligible():
		return _presentation_failure(family, "approval_ineligible")
	if int(pack.get("timing", {}).get("fps", 0)) != 24 or pack.get("timing", {}).get("tick_unit") != "1/24_second":
		return _presentation_failure(family, "timing_invalid")
	_observe("track_validated", {"track_id": track.get("track_id"), "approval_state": pack.get("approval_state")})
	var built := _build_frames(track)
	if not built.get("ok", false):
		return _presentation_failure(family, String(built.get("reason", "frame_load_failed")))
	_observe("first_frame_loaded", {"track_id": track.get("track_id"), "frame": 0})
	var target: AnimatedSprite2D = body_b if active_body == 0 else body_a
	var old: AnimatedSprite2D = body_a if active_body == 0 else body_b
	target.sprite_frames = built["frames"]; target.animation = String(track["track_id"]); target.frame = 0; target.visible = true; target.modulate.a = 1.0; target.pause()
	old.visible = false
	active_body = 1 - active_body; current_track = String(track["track_id"]); current_family = family; current_track_data = track
	if not await _await_render_commit():
		return _presentation_failure(family, "render_commit_unobserved")
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	if current != target or not target.visible or target.frame != 0 or target.sprite_frames.get_frame_texture(current_track, 0) == null:
		return _presentation_failure(family, "first_frame_not_render_committed")
	_observe("first_frame_presented", {"track_id": current_track, "frame": 0})
	_observe("first_frame_render_committed", {"track_id": current_track, "frame": 0, "render_observation": last_render_observation})
	return {"status": "first_frame_render_committed", "track_id": current_track, "frame": 0}

func start_presented_track() -> void:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	_emit_events_for_frame(current.frame)
	current.play()

func _emit_events_for_frame(frame_index: int) -> void:
	for marker in current_track_data.get("events", []):
		if int(marker.get("frame_index", -1)) == frame_index:
			_observe("track_event", {"track_id": current_track, "event_id": marker.get("event_id"), "name": marker.get("name"), "tick": marker.get("tick"), "frame": frame_index})

func _presentation_failure(family: String, reason: String) -> Dictionary:
	var event := {"event_type": "clip_failed", "clip_id": family, "status": "failed", "reason": reason, "generation": generation}
	clip_failed.emit(event); _observe("failed", event)
	return event

func _on_frame_changed(sprite: AnimatedSprite2D) -> void:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	if sprite.visible and sprite == current:
		var event := {"event": "frame_changed", "clip_id": current_family, "track_id": current_track, "frame": sprite.frame, "generation": generation}
		frame_marker.emit(event); _observe("frame_changed", event)
		_emit_events_for_frame(sprite.frame)

func _on_animation_finished(sprite: AnimatedSprite2D) -> void:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	if sprite.visible and sprite == current and not sprite.sprite_frames.get_animation_loop(sprite.animation):
		var event := {"event": "completed", "clip_id": current_family, "track_id": current_track, "generation": generation}
		clip_completed.emit(event); _observe("completed", event); _observe("visible_state", visible_state())

func visible_state() -> Dictionary:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	return {"schema_major": 1, "event_type": "current_visible_body_state", "event": "visible_state", "clip_id": current_family, "track_id": current_track, "frame": current.frame, "playing": current.is_playing(), "generation": generation}

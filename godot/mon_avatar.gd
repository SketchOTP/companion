class_name MonAvatar
extends Node2D

## Layered raster avatar. Godot owns only current visual execution state.
signal frame_marker(event: Dictionary)
signal clip_completed(event: Dictionary)
signal clip_failed(event: Dictionary)

const FRAME_ROOT := "res://assets/p02/"
const Director = preload("res://mon_animation_director.gd")
var clip_manifest: Dictionary = {}
var loaded_clips: Dictionary = {}
var active_body := 0
var current_clip := ""
var generation := "godot-p02-v1"

@onready var body_a: AnimatedSprite2D = $BodyA
@onready var body_b: AnimatedSprite2D = $BodyB
@onready var director: Node = $MonAnimationDirector

func _ready() -> void:
	_load_manifest()
	director.configure(self, int(OS.get_environment("COMPANION_P02_SEED")) if OS.get_environment("COMPANION_P02_SEED").is_valid_int() else 17)
	request_initial_intent()

func request_initial_intent() -> void:
	director.request_intent("idle")

func _load_manifest() -> void:
	var file := FileAccess.open(FRAME_ROOT + "clip_manifest.json", FileAccess.READ)
	if file == null:
		clip_failed.emit({"schema_major":1,"event_type":"clip_failed","status":"degraded","reason":"pack_manifest_missing","generation":generation})
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary: clip_manifest = parsed

func _frames_for(clip_id: String) -> SpriteFrames:
	if loaded_clips.has(clip_id): return loaded_clips[clip_id]
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	frames.add_animation(clip_id)
	frames.set_animation_loop(clip_id, clip_id.begins_with("idle") or clip_id in ["walk", "run", "sleep", "dream_neutral"])
	var families: Array = clip_manifest.get("families", [])
	for family in families:
		if family.get("clip_id") != clip_id: continue
		for item in family.get("frames", []):
			var texture := load(FRAME_ROOT + String(item.get("path", "")).get_file())
			if texture is Texture2D: frames.add_frame(clip_id, texture, float(item.get("duration_ticks", 2)) / 24.0)
	if frames.get_frame_count(clip_id) == 0:
		clip_failed.emit({"schema_major":1,"event_type":"clip_failed","clip_id":clip_id,"status":"degraded","reason":"clip_frames_missing","generation":generation})
	loaded_clips[clip_id] = frames
	return frames

func play_clip(clip_id: String) -> void:
	var frames := _frames_for(clip_id)
	if frames.get_animation_names().has(clip_id) and frames.get_frame_count(clip_id) > 0:
		var target: AnimatedSprite2D = body_b if active_body == 0 else body_a
		target.sprite_frames = frames
		target.animation = clip_id
		target.frame = 0
		target.play()
		target.visible = true
		var old: AnimatedSprite2D = body_a if active_body == 0 else body_b
		old.visible = false
		active_body = 1 - active_body
		current_clip = clip_id
		frame_marker.emit({"schema_major":1,"event_type":"frame_marker","clip_id":clip_id,"frame":0,"generation":generation})
	else:
		clip_failed.emit({"schema_major":1,"event_type":"clip_failed","clip_id":clip_id,"status":"degraded","reason":"corrupt_or_empty_pack","generation":generation})

func visible_state() -> Dictionary:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	return {"schema_major":1,"event_type":"current_visible_body_state","clip_id":current_clip,"frame":current.frame,"playing":current.is_playing(),"generation":generation}

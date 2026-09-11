class_name MonAvatar
extends Node2D

## Layered raster avatar. Godot owns only current visual execution state.
signal frame_marker(event: Dictionary)
signal clip_completed(event: Dictionary)
signal clip_failed(event: Dictionary)

const FRAME_ROOT := "res://assets/p02-core/"
const ANIMATION_FPS := 12.0
const Director = preload("res://mon_animation_director.gd")
var clip_manifest: Dictionary = {}
var temporal_tracks: Array = []
var loaded_clips: Dictionary = {}
var active_body := 0
var current_clip := ""
var generation := "godot-p02-v1"

@onready var body_a: AnimatedSprite2D = $BodyA
@onready var body_b: AnimatedSprite2D = $BodyB
@onready var director: Node = $MonAnimationDirector

func _ready() -> void:
	body_a.frame_changed.connect(_on_frame_changed.bind(body_a))
	body_b.frame_changed.connect(_on_frame_changed.bind(body_b))
	body_a.animation_finished.connect(_on_animation_finished.bind(body_a))
	body_b.animation_finished.connect(_on_animation_finished.bind(body_b))
	_load_manifest()
	director.configure(self, int(OS.get_environment("COMPANION_P02_SEED")) if OS.get_environment("COMPANION_P02_SEED").is_valid_int() else 17)
	request_initial_intent()

func request_initial_intent() -> void:
	director.request_intent("idle")

func _load_manifest() -> void:
	var file := FileAccess.open(FRAME_ROOT + "temporal_tracks.json", FileAccess.READ)
	if file == null:
		clip_failed.emit({"schema_major":1,"event_type":"clip_failed","status":"degraded","reason":"pack_manifest_missing","generation":generation})
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		clip_manifest = parsed
		temporal_tracks = parsed.get("tracks", [])

func _frames_for(track_id: String) -> SpriteFrames:
	if loaded_clips.has(track_id): return loaded_clips[track_id]
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	frames.add_animation(track_id)
	var track: Dictionary = {}
	for candidate in temporal_tracks:
		if candidate.get("track_id", "") == track_id: track = candidate; break
	if track.is_empty():
		clip_failed.emit({"schema_major":1,"event_type":"clip_failed","track_id":track_id,"status":"degraded","reason":"track_missing","generation":generation})
		return frames
	frames.set_animation_loop(track_id, track.get("loop_mode", "once") == "loop")
	frames.set_animation_speed(track_id, ANIMATION_FPS)
	for item in track.get("frames", []):
		var texture := load(FRAME_ROOT + String(item.get("path", "")))
		# SpriteFrames duration is a relative weight. Integer 24 Hz ticks are
		# retained as weights at the declared 12 drawings/s animation FPS.
		if texture is Texture2D: frames.add_frame(track_id, texture, float(item.get("duration_ticks", 1)))
	if frames.get_frame_count(track_id) == 0:
		clip_failed.emit({"schema_major":1,"event_type":"clip_failed","track_id":track_id,"status":"degraded","reason":"track_frames_missing","generation":generation})
	loaded_clips[track_id] = frames
	return frames

func play_clip(clip_id: String) -> void:
	play_track(clip_id, "N", "neutral", 1)

func play_track(family: String, direction: String = "N", posture: String = "neutral", variant: int = 1, stage: String = "candidate") -> void:
	var track_id := "mon-body-v1:%s:%s:%s:%s:%d" % [stage, family, direction, posture, variant]
	var frames := _frames_for(track_id)
	if frames.get_animation_names().has(track_id) and frames.get_frame_count(track_id) > 0:
		var target: AnimatedSprite2D = body_b if active_body == 0 else body_a
		target.sprite_frames = frames
		target.animation = track_id
		target.frame = 0
		target.play()
		target.visible = true
		target.modulate.a = 0.0
		var old: AnimatedSprite2D = body_a if active_body == 0 else body_b
		var tween := create_tween().set_parallel(true)
		tween.tween_property(target, "modulate:a", 1.0, 0.08)
		if old.visible: tween.tween_property(old, "modulate:a", 0.0, 0.08)
		tween.chain().tween_callback(func(): old.visible = false)
		active_body = 1 - active_body
		current_clip = family
		frame_marker.emit({"schema_major":1,"event_type":"frame_marker","clip_id":family,"track_id":track_id,"frame":0,"generation":generation})
	else:
		clip_failed.emit({"schema_major":1,"event_type":"clip_failed","clip_id":family,"track_id":track_id,"status":"degraded","reason":"corrupt_or_empty_pack","generation":generation})

func _on_frame_changed(sprite: AnimatedSprite2D) -> void:
	if sprite.visible and sprite == (body_a if active_body == 0 else body_b):
		frame_marker.emit({"schema_major":1,"event_type":"frame_marker","clip_id":current_clip,"track_id":sprite.animation,"frame":sprite.frame,"generation":generation})

func _on_animation_finished(sprite: AnimatedSprite2D) -> void:
	if sprite.visible and not sprite.sprite_frames.get_animation_loop(sprite.animation):
		clip_completed.emit({"schema_major":1,"event_type":"clip_completed","clip_id":current_clip,"track_id":sprite.animation,"generation":generation})

func visible_state() -> Dictionary:
	var current: AnimatedSprite2D = body_a if active_body == 0 else body_b
	return {"schema_major":1,"event_type":"current_visible_body_state","clip_id":current_clip,"track_id":current.animation,"frame":current.frame,"playing":current.is_playing(),"generation":generation}

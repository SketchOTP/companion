class_name MonAnimationDirector
extends Node

## Presentation-only semantic director. It never owns organism or care truth.
signal intent_started(result: Dictionary)
signal intent_completed(result: Dictionary)
signal intent_degraded(result: Dictionary)
signal event_observed(event: Dictionary)

const VERSION := "MonAnimationDirector-r04-c02"
var deterministic_seed: int = 17
var sequence: int = 0
var avatar: Node

func configure(target: Node, seed: int = 17) -> void:
	avatar = target
	deterministic_seed = seed

func _observe(name: String, details: Dictionary = {}) -> void:
	var event := {"event": name, "sequence": sequence, "monotonic_usec": Time.get_ticks_usec()}
	event.merge(details)
	event_observed.emit(event)

func request_intent(family: String, _priority: int = 0, _interruptible: bool = true, facing: String = "front", posture: String = "neutral", _affect: String = "neutral", _energy: String = "medium", variant: int = 1) -> Dictionary:
	sequence += 1
	_observe("intent_received", {"family": family, "facing": facing, "posture": posture, "variant": variant})
	if avatar == null or not avatar.has_method("present_track"):
		return _fail(family, "avatar_unavailable")
	var result: Dictionary = await avatar.present_track(family, facing, posture, variant)
	if result.get("status") != "first_frame_render_committed":
		return _fail(family, String(result.get("reason", "presentation_failed")))
	var started := _result("started", family, "first_frame_render_committed")
	started["track_id"] = result["track_id"]
	started["frame"] = 0
	intent_started.emit(started)
	_observe("started", {"track_id": result["track_id"], "frame": 0})
	avatar.start_presented_track()
	return started

func _fail(family: String, reason: String) -> Dictionary:
	var result := _result("failed", family, reason)
	intent_degraded.emit(result)
	_observe("failed", {"family": family, "reason": reason})
	return result

func _result(status: String, family: String, reason: String) -> Dictionary:
	return {"schema_major": 1, "event_type": "clip_started" if status == "started" else "clip_failed", "sequence": sequence, "intent_id": "%032x" % (deterministic_seed * 100000 + sequence), "clip_id": family, "status": status, "reason": reason, "generation": "godot-p02-r04-c02", "version": VERSION}

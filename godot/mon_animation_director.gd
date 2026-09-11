class_name MonAnimationDirector
extends Node

## Presentation-only semantic director. It never owns organism or care truth.
signal intent_started(result: Dictionary)
signal intent_completed(result: Dictionary)
signal intent_degraded(result: Dictionary)

const VERSION := "MonAnimationDirector-v1"
const CLIPS := ["idle_breathe_a", "idle_breathe_b", "idle_breathe_c", "gaze", "listen", "think", "acknowledge", "speak_neutral", "interrupt", "greeting", "unknown_observer", "sit_stand", "stand_sit", "lie_down", "sleep", "dream_neutral", "wake", "stretch", "walk", "run", "hop", "approach", "retreat", "stop", "curiosity", "inspection", "hesitation", "refusal", "surprise", "calm_joy", "disappointment", "tiredness", "boredom", "sensor_degraded"]
const CONNECTORS := {"idle_breathe_a": ["gaze", "listen", "think", "greeting", "walk", "run"], "walk": ["stop", "run", "approach", "retreat"], "run": ["stop", "walk", "approach", "retreat"], "stop": ["idle_breathe_a", "gaze", "listen"], "sleep": ["wake", "dream_neutral"], "wake": ["stretch", "idle_breathe_a"]}
var deterministic_seed: int = 17
var recent: Array[String] = []
var current_clip := "idle_breathe_a"
var sequence: int = 0
var avatar: Node
var current_direction := "N"
var current_posture := "neutral"
var current_variant := 1

func configure(target: Node, seed: int = 17) -> void:
	avatar = target
	deterministic_seed = seed

func request_intent(kind: String, priority: int = 0, interruptible: bool = true, direction: String = "N", posture: String = "neutral", affect: String = "neutral", energy: String = "medium", variant: int = 1) -> Dictionary:
	sequence += 1
	var normalized := kind if kind in CLIPS else "idle_breathe_a"
	var candidates: Array[String] = [normalized]
	if normalized == "idle": candidates = ["idle_breathe_a", "idle_breathe_b", "idle_breathe_c"]
	var selected := _choose(candidates)
	var legal := _legal_transition(current_clip, selected)
	if not legal:
		var connector := _connector_for(selected)
		if connector.is_empty():
			var result := _result("degraded", selected, "illegal_transition_no_connector", priority)
			intent_degraded.emit(result)
			return result
		selected = connector
	var result := _result("started", selected, "deterministic_selection", priority)
	result["interruptible"] = interruptible
	result["version"] = VERSION
	result["direction"] = direction
	result["posture"] = posture
	result["affect"] = affect
	result["energy"] = energy
	result["variant"] = variant
	current_clip = selected
	current_direction = direction
	current_posture = posture
	var selected_variant := variant
	if kind == "idle": selected_variant = ["idle_breathe_a", "idle_breathe_b", "idle_breathe_c"].find(selected) + 1
	current_variant = selected_variant
	recent.push_front(selected)
	if recent.size() > 4: recent.pop_back()
	if avatar != null and avatar.has_method("play_track"):
		avatar.play_track(selected, direction, posture, selected_variant)
	intent_started.emit(result)
	return result

func _choose(candidates: Array[String]) -> String:
	var available := candidates.filter(func(c): return c not in recent or candidates.size() == 1)
	if available.is_empty(): available = candidates
	return available[abs(deterministic_seed + sequence * 31) % available.size()]

func _legal_transition(from: String, to: String) -> bool:
	if from == to: return true
	if CONNECTORS.has(from) and to in CONNECTORS[from]: return true
	return to in ["interrupt", "acknowledge", "speak_neutral", "surprise", "refusal"]

func _connector_for(target: String) -> String:
	for key in CONNECTORS:
		if target in CONNECTORS[key] and key == current_clip: return target
	return "stop" if current_clip in ["walk", "run"] else "idle_breathe_a"

func _result(status: String, clip: String, reason: String, priority: int) -> Dictionary:
	return {"schema_major": 1, "event_type": "clip_started", "sequence": sequence, "intent_id": "%032x" % (deterministic_seed * 100000 + sequence), "clip_id": clip, "status": status, "reason": reason, "priority": priority, "generation": "godot-p02-v1"}

class_name MonLocomotionController
extends Node

## Canonical movement owner for the bounded R06-C05 synthetic qualification.
## Sprite pixels, landmarks, and contacts are presentation diagnostics only.
signal movement_sample(sample: Dictionary)

const FPS := 24.0
var actor_root: Node2D
var intent: Dictionary = {}
var position_x := 0.0
var tick := 0

func configure(root: Node2D) -> void:
	actor_root = root
	position_x = root.position.x if root != null else 0.0

func accept_intent(candidate: Dictionary) -> Dictionary:
	var direction := String(candidate.get("requested_direction", ""))
	var facing := String(candidate.get("requested_facing", ""))
	var state := String(candidate.get("state", ""))
	var velocity := float(candidate.get("commanded_velocity_px_per_second", 0))
	if int(candidate.get("schema_major", 0)) != 1: return {"status": "failed", "reason": "schema_major"}
	if direction not in ["left", "right"] or facing != direction: return {"status": "failed", "reason": "wrong_profile"}
	if state not in ["start", "cruise", "stop"]: return {"status": "failed", "reason": "state"}
	if state == "stop" and velocity != 0: return {"status": "failed", "reason": "velocity_sign_contradiction"}
	if state != "stop" and ((direction == "left" and velocity >= 0) or (direction == "right" and velocity <= 0)): return {"status": "failed", "reason": "velocity_sign_contradiction"}
	intent = candidate.duplicate(true)
	return {"status": "accepted", "intent_id": intent.get("intent_id"), "direction": direction, "facing": facing}

func tick_once() -> Dictionary:
	if intent.is_empty(): return {"status": "failed", "reason": "intent_missing"}
	var velocity := float(intent.get("commanded_velocity_px_per_second", 0))
	if String(intent.get("state")) == "stop": velocity = 0.0
	position_x += velocity / FPS
	tick += 1
	if actor_root != null: actor_root.position.x = position_x
	var sample := {"tick": tick - 1, "actor_root_x": position_x, "commanded_velocity_px_per_second": velocity, "direction": intent.get("requested_direction"), "facing": intent.get("requested_facing"), "state": intent.get("state")}
	movement_sample.emit(sample)
	return sample

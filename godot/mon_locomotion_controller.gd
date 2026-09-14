class_name MonLocomotionController
extends Node

## Controller-owned movement primitive for R06-C06. Canonical position is
## advanced by an explicit 24 Hz semantic clock; render cadence is unrelated.
## Sprite pixels and contacts are presentation diagnostics only.
signal movement_sample(sample: Dictionary)
signal intent_decision(result: Dictionary)

const SEMANTIC_HZ := 24.0
const REFERENCE_VELOCITY := 96.0
const INTENT_SCHEMA_MAJOR := 2
const INTENT_SEQUENCE_MAX := 9223372036854775807
const AUTHORED_PROFILE_LOOP_TICKS := 32.0

var actor_root: Node2D
var intent: Dictionary = {}
var position_x := 0.0
var semantic_tick := 0
var _accumulator := 0.0
var _last_sequence := -1
var _accepted_ids: Dictionary = {}
var _active_movement_id := ""
var _active_movement_sequence := -1
var _stop_latched := false
var _animation_phase := 0.0

func configure(root: Node2D) -> void:
	actor_root = root
	position_x = root.position.x if root != null else 0.0

func accept_serialized_intent(serialized: String) -> Dictionary:
	var sequence_digits := _wire_sequence_digits(serialized)
	if sequence_digits.is_empty() or not _wire_sequence_is_representable(sequence_digits):
		return _reject("intent_sequence")
	var decoded = JSON.parse_string(serialized)
	if not decoded is Dictionary:

		return _reject("invalid_json")
	decoded["intent_sequence"] = int(sequence_digits)
	return accept_intent(decoded)

func accept_intent(candidate: Dictionary) -> Dictionary:
	var schema_major := int(candidate.get("schema_major", 0))
	var intent_id := String(candidate.get("intent_id", ""))
	var sequence_value = candidate.get("intent_sequence", null)
	var direction := String(candidate.get("requested_direction", ""))
	var facing := String(candidate.get("requested_facing", ""))
	var state := String(candidate.get("state", ""))
	var velocity := int(candidate.get("commanded_velocity_px_per_second", 0))
	var cancellation_id = candidate.get("cancellation_id", null)
	if schema_major != INTENT_SCHEMA_MAJOR:
		return _reject("schema_major")
	if not _is_uuid(intent_id):
		return _reject("intent_id_uuid")
	if sequence_value == null or (typeof(sequence_value) != TYPE_INT and typeof(sequence_value) != TYPE_FLOAT) or int(sequence_value) != sequence_value or float(sequence_value) < 0.0 or float(sequence_value) > float(INTENT_SEQUENCE_MAX):
		return _reject("intent_sequence")
	var sequence := int(sequence_value)
	if _accepted_ids.has(intent_id):
		return _reject("duplicate_intent_id")
	if sequence <= _last_sequence:
		return _reject("stale_replayed_intent")
	if direction not in ["left", "right"] or facing != direction:
		return _reject("wrong_profile")
	if state not in ["start", "cruise", "stop"]:
		return _reject("state")
	if state == "stop":
		if velocity != 0:
			return _reject("stop_velocity_nonzero")
		if typeof(cancellation_id) != TYPE_STRING or not _is_uuid(String(cancellation_id)):
			return _reject("cancellation_required")
		if _active_movement_id.is_empty() or String(cancellation_id) != _active_movement_id:
			return _reject("cancellation_target_mismatch")
		if _stop_latched:
			return _reject("cancellation_after_completion")
	else:
		if cancellation_id != null:
			return _reject("unexpected_cancellation")
		if (direction == "left" and velocity >= 0) or (direction == "right" and velocity <= 0):
			return _reject("velocity_sign_contradiction")
		if _stop_latched and state != "start":
			return _reject("movement_after_stop")
	_accepted_ids[intent_id] = sequence
	_last_sequence = sequence
	intent = candidate.duplicate(true)
	if state == "stop":
		_stop_latched = true
		_active_movement_id = ""
		_active_movement_sequence = -1
	else:
		_stop_latched = false
		_active_movement_id = intent_id
		_active_movement_sequence = sequence
	var result := {"status": "accepted", "intent_id": intent_id, "intent_sequence": sequence, "direction": direction, "facing": facing, "state": state, "presentation_rate": _presentation_rate(velocity)}
	intent_decision.emit(result)
	return result

func advance_render_delta(delta_seconds: float) -> Array:
	_accumulator += max(0.0, delta_seconds)
	var samples: Array = []
	while _accumulator + 0.0000001 >= (1.0 / SEMANTIC_HZ):
		_accumulator -= 1.0 / SEMANTIC_HZ
		samples.append(tick_once())
	return samples

func advance_fixed_steps(count: int) -> Array:
	var samples: Array = []
	for _i in count:
		samples.append(tick_once())
	return samples

func tick_once() -> Dictionary:
	if intent.is_empty():
		return {"status": "failed", "reason": "intent_missing"}
	var velocity := int(intent.get("commanded_velocity_px_per_second", 0))
	if String(intent.get("state", "")) == "stop":
		velocity = 0
	var before := position_x
	position_x += float(velocity) / SEMANTIC_HZ
	semantic_tick += 1
	if velocity != 0:
		_animation_phase = fmod(_animation_phase + _presentation_rate(velocity) / AUTHORED_PROFILE_LOOP_TICKS, 1.0)
	if actor_root != null:
		actor_root.position.x = position_x
	var sample := {"status": "tick", "semantic_tick": semantic_tick - 1, "actor_root_x": position_x, "delta_x": position_x - before, "commanded_velocity_px_per_second": velocity, "direction": intent.get("requested_direction"), "facing": intent.get("requested_facing"), "state": intent.get("state"), "intent_id": intent.get("intent_id"), "intent_sequence": intent.get("intent_sequence"), "animation_phase": _animation_phase, "playback_rate": _presentation_rate(velocity)}
	movement_sample.emit(sample)
	return sample

func presentation_rate_for_velocity(velocity: int) -> float:
	return _presentation_rate(velocity)

func animation_phase() -> float:
	return _animation_phase

func _presentation_rate(velocity: int) -> float:
	if velocity == 0:
		return 1.0
	return abs(float(velocity)) / REFERENCE_VELOCITY

func _reject(reason: String) -> Dictionary:
	var result := {"status": "failed", "reason": reason}
	intent_decision.emit(result)
	return result

func _is_uuid(value: String) -> bool:
	var regex := RegEx.new()
	regex.compile("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
	return regex.search(value) != null

func _wire_sequence_digits(serialized: String) -> String:
	var regex := RegEx.new()
	regex.compile("\\\"intent_sequence\\\"\\s*:\\s*(\\d+)")
	var match := regex.search(serialized)
	if match == null: return ""
	var digits := String(match.get_string(1)).lstrip("0")
	if digits.is_empty(): digits = "0"
	return digits

func _wire_sequence_is_representable(digits: String) -> bool:
	var maximum := str(INTENT_SEQUENCE_MAX)
	return digits.length() < maximum.length() or (digits.length() == maximum.length() and digits.naturalnocasecmp_to(maximum) <= 0)

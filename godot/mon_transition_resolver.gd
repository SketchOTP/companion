class_name MonTransitionResolver
extends RefCounted

## Single production transition authority shared by live presentation and the
## Godot qualification campaign.  The graph is data (project-role metadata),
## not a qualification-only switch statement.
const AUTHORITY_REVISION := "r06-production-transition-authority-v1"
static var _authority_cache: Dictionary = {}

static func _authority() -> Dictionary:
	if _authority_cache.is_empty():
		var parsed = JSON.parse_string(FileAccess.get_file_as_string("res://transition_authority.json"))
		if parsed is Dictionary and parsed.get("revision") == AUTHORITY_REVISION and parsed.get("edges") is Dictionary:
			_authority_cache = parsed
	return _authority_cache

static func resolve(start_state: String, request: String) -> Array:
	var by_request: Dictionary = _authority().get("edges", {}).get(start_state, {})
	var route = by_request.get(request, [])
	return route.duplicate() if route is Array else []

static func is_legal(start_state: String, request: String) -> bool:
	return not resolve(start_state, request).is_empty()

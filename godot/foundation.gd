extends Control
const DisplayTopology = preload("res://display_topology.gd")
var topology := DisplayTopology.new()

## Neutral, non-production Phase 01 habitat placeholder.
## It reports foundation connectivity only; no organism, media, or care logic.
enum BridgeState { CONNECTING, CONNECTED, DEGRADED, DISCONNECTED, INCOMPATIBLE }
var bridge_state: BridgeState = BridgeState.CONNECTING
var status := "FOUNDATION / BRIDGE: CONNECTING"
var target_screen := 0
var min_size := Vector2i(320, 180)
var max_size := Vector2i(1366, 768)
var reconnect_attempts := 0

func _ready() -> void:
	set_process(true)
	_restore_geometry()
	_apply_screen_policy()
	_poll_bridge()
	queue_redraw()

func _process(_delta: float) -> void:
	_poll_bridge()
	queue_redraw()

func _poll_bridge() -> void:
	# The bridge handshake is local and versioned. A missing bridge is an
	# explicit degraded state; it never fabricates a connected product state.
	var marker := "user://foundation_bridge_v1.json"
	if not FileAccess.file_exists(marker):
		bridge_state = BridgeState.DISCONNECTED
		status = "FOUNDATION / BRIDGE: DISCONNECTED"
		return
	var file := FileAccess.open(marker, FileAccess.READ)
	var parsed = JSON.parse_string(file.get_as_text()) if file else null
	if parsed is Dictionary and parsed.get("protocol") == "companion-foundation-v1":
		bridge_state = BridgeState.CONNECTED
		status = "FOUNDATION / BRIDGE: CONNECTED"
		reconnect_attempts = 0
	else:
		bridge_state = BridgeState.INCOMPATIBLE
		status = "FOUNDATION / BRIDGE: INCOMPATIBLE"

func _apply_screen_policy() -> void:
	var screens := DisplayServer.get_screen_count()
	if screens <= target_screen:
		bridge_state = BridgeState.DEGRADED
		status = "FOUNDATION / BRIDGE: DEGRADED (TARGET DISPLAY ABSENT)"
		return
	var area := DisplayServer.screen_get_usable_rect(target_screen)
	var position := DisplayServer.window_get_position()
	var size := DisplayServer.window_get_size()
	var bounded := topology.clamp_window(position, size, area, min_size, max_size)
	DisplayServer.window_set_size(bounded["size"])
	DisplayServer.window_set_position(bounded["position"])

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		_persist_geometry()
		get_tree().quit()

func _persist_geometry() -> void:
	var payload := {"position": DisplayServer.window_get_position(), "size": DisplayServer.window_get_size()}
	var file := FileAccess.open("user://foundation_geometry.json", FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(payload))

func _restore_geometry() -> void:
	if not FileAccess.file_exists("user://foundation_geometry.json"):
		return
	var file := FileAccess.open("user://foundation_geometry.json", FileAccess.READ)
	if not file:
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary and parsed.has("size"):
		var size: Vector2i = parsed["size"]
		if size.x >= 320 and size.y >= 180:
			DisplayServer.window_set_size(size)

func _draw() -> void:
	var font := ThemeDB.fallback_font
	var size := get_viewport_rect().size
	draw_rect(Rect2(Vector2.ZERO, size), Color("211447"))
	draw_rect(Rect2(24, 24, max(size.x - 48, 10), max(size.y - 48, 10)), Color("3d2670"), false, 2.0)
	draw_string(font, Vector2(48, 86), "COMPANION FOUNDATION", HORIZONTAL_ALIGNMENT_LEFT, -1, 26, Color("efe7ff"))
	draw_string(font, Vector2(48, 126), status, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color("efc26b"))
	draw_string(font, Vector2(48, 168), "Phase 01 engineering shell — no product capability", HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color("c4b5e8"))

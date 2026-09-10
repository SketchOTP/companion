extends Control
const DisplayTopology = preload("res://display_topology.gd")
var topology := DisplayTopology.new()

## Neutral, non-production Phase 01 habitat placeholder.
## It reports foundation connectivity only; no organism, media, or care logic.
enum BridgeState { CONNECTING, CONNECTED, DEGRADED, DISCONNECTED, INCOMPATIBLE }
var bridge_state: BridgeState = BridgeState.CONNECTING
var status := "FOUNDATION / BRIDGE: CONNECTING"
var target_screen := DisplayServer.get_primary_screen()
var min_size := Vector2i(320, 180)
var max_size := Vector2i(1366, 768)
var reconnect_attempts := 0
var bridge_peer: StreamPeerUDS
var bridge_socket_path := ""

func _ready() -> void:
	set_process(true)
	_restore_geometry()
	var configured_screen := OS.get_environment("COMPANION_TARGET_SCREEN")
	if configured_screen.is_valid_int():
		target_screen = configured_screen.to_int()
	bridge_socket_path = _bridge_socket_path()
	_apply_screen_policy()
	_poll_bridge()
	queue_redraw()

func _process(_delta: float) -> void:
	_poll_bridge()
	_apply_screen_policy()
	queue_redraw()

func _poll_bridge() -> void:
	# The bridge handshake is a real local versioned Unix-domain connection.
	# Missing or incompatible bridge state is explicit degradation.
	if bridge_peer != null:
		bridge_peer.poll()
	if bridge_peer == null or bridge_peer.get_status() != StreamPeerSocket.STATUS_CONNECTED:
		bridge_peer = StreamPeerUDS.new()
		var connect_error := bridge_peer.connect_to_host(bridge_socket_path)
		if connect_error != OK:
			bridge_state = BridgeState.DISCONNECTED
			status = "FOUNDATION / BRIDGE: DISCONNECTED"
			reconnect_attempts += 1
			return
		var request := JSON.stringify({"protocol": "companion-foundation-v1", "schema_major": 1}).to_utf8_buffer()
		bridge_peer.put_data(request)
	if bridge_peer.get_available_bytes() <= 0:
		bridge_state = BridgeState.DISCONNECTED
		status = "FOUNDATION / BRIDGE: DISCONNECTED"
		return
	var response := bridge_peer.get_data(bridge_peer.get_available_bytes())
	var parsed = JSON.parse_string(response[1].get_string_from_utf8()) if response[0] == OK else null
	if parsed is Dictionary and parsed.get("protocol") == "companion-foundation-v1" and parsed.get("state") == "connected":
		bridge_state = BridgeState.CONNECTED
		status = "FOUNDATION / BRIDGE: CONNECTED"
		reconnect_attempts = 0
	else:
		bridge_state = BridgeState.INCOMPATIBLE
		status = "FOUNDATION / BRIDGE: INCOMPATIBLE"

func _bridge_socket_path() -> String:
	var root := OS.get_environment("COMPANION_XDG_ROOT")
	if root.is_empty():
		root = OS.get_environment("XDG_RUNTIME_DIR")
	return root.path_join("companion").path_join("godot-bridge.sock")

func _apply_screen_policy() -> void:
	var screens := DisplayServer.get_screen_count()
	if screens <= target_screen:
		bridge_state = BridgeState.DEGRADED
		status = "FOUNDATION / BRIDGE: DEGRADED (TARGET DISPLAY ABSENT)"
		return
	# Explicitly select the configured habitat output before clamping geometry.
	get_window().current_screen = target_screen
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
	var payload := {"output": target_screen, "position": DisplayServer.window_get_position(), "size": DisplayServer.window_get_size()}
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
		if parsed.has("output"):
			target_screen = int(parsed["output"])
		if parsed.has("position") and parsed["position"] is Array and parsed["position"].size() == 2:
			DisplayServer.window_set_position(Vector2i(int(parsed["position"][0]), int(parsed["position"][1])))
		if not parsed["size"] is Array or parsed["size"].size() != 2:
			return
		var size := Vector2i(int(parsed["size"][0]), int(parsed["size"][1]))
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

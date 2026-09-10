extends Control

## Neutral, non-production Phase 01 habitat placeholder.
## It reports foundation connectivity only; no organism, media, or care logic.
var status := "FOUNDATION / BRIDGE: DEGRADED (HEADLESS OR DISCONNECTED)"

func _ready() -> void:
	set_process(true)
	_restore_geometry()
	queue_redraw()

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

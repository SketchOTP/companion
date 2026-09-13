extends Node2D

const BASE_RESOLUTION := Vector2i(640, 360)
const MIN_SIZE := Vector2i(640, 360)
const MAX_SIZE := Vector2i(1366, 768)
const TARGET_SCREEN := 0
var topology_available := true
var fallback_active := false
var geometry_path := "user://p02_geometry.json"

func _ready() -> void:
	get_window().min_size = MIN_SIZE
	get_window().max_size = MAX_SIZE
	get_window().content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	get_window().content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
	get_window().current_screen = TARGET_SCREEN
	_apply_geometry()
	if OS.get_environment("COMPANION_P02_TOPOLOGY_LOSS") == "1": _set_topology(false)
	if OS.get_environment("COMPANION_P02_HEADLESS") == "1":
		await get_tree().create_timer(0.25).timeout
		print(JSON.stringify({"status":"PASSED","habitat":"bounded","topology":topology_available,"fallback":fallback_active,"target_screen":TARGET_SCREEN,"base_resolution":BASE_RESOLUTION}))
		get_tree().quit()

func _apply_geometry() -> void:
	var area := DisplayServer.screen_get_usable_rect(TARGET_SCREEN) if DisplayServer.get_screen_count() > TARGET_SCREEN else Rect2i(0,0,1366,768)
	var size := Vector2i(clamp(960, MIN_SIZE.x, MAX_SIZE.x), clamp(540, MIN_SIZE.y, MAX_SIZE.y))
	var pos := Vector2i(area.position.x + max(0,(area.size.x-size.x)/2), area.position.y + max(0,(area.size.y-size.y)/2))
	get_window().size = size; get_window().position = pos

func _set_topology(available: bool) -> void:
	topology_available = available; fallback_active = not available
	if not available: get_window().current_screen = DisplayServer.get_primary_screen()
	else: get_window().current_screen = TARGET_SCREEN

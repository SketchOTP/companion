class_name FoundationDisplayTopology
extends RefCounted

## Injectable display topology for headless tests. It only carries geometry;
## no desktop screenshots or media are captured.
var screens: Array[Rect2i] = []

func _init(rects: Array[Rect2i] = []) -> void:
	screens = rects

func target(index: int, fallback: Rect2i) -> Rect2i:
	if index >= 0 and index < screens.size():
		return screens[index]
	return fallback

func clamp_window(position: Vector2i, size: Vector2i, area: Rect2i, minimum: Vector2i, maximum: Vector2i) -> Dictionary:
	var bounded_size := Vector2i(clamp(size.x, minimum.x, min(maximum.x, area.size.x)), clamp(size.y, minimum.y, min(maximum.y, area.size.y)))
	var bounded_position := Vector2i(clamp(position.x, area.position.x, area.end.x - bounded_size.x), clamp(position.y, area.position.y, area.end.y - bounded_size.y))
	return {"position": bounded_position, "size": bounded_size}

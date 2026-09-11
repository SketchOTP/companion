class_name MonBodySourceV2
extends Node2D

## Editable, Godot-native R03 authoring source.  The rendered body is made of
## explicit named parts and bounded transforms; the runtime still consumes
## baked raster frames.  No organism or care state is represented here.

const ROOT := Vector2(512, 896)
const BASE := Color("7541D4")
const LIGHT := Color("8E5BE8")
const SHADOW := Color("452296")
const SHADOW_2 := Color("5B32B3")
const OUTLINE := Color("1A0D39")
const EYE := Color("090711")
const PUPIL := Color("FFFDF7")
const MOUTH := Color("2B1238")

var pose: Dictionary = {
	"facing": "front_left",
	"torso_scale": Vector2.ONE,
	"head_turn": 0.35,
	"head_tilt": 0.0,
	"arm_left": 0.0,
	"arm_right": 0.0,
	"leg_left": 0.0,
	"leg_right": 0.0,
	"foot_left": Vector2.ZERO,
	"foot_right": Vector2.ZERO,
	"gaze": 0.0,
	"mouth_open": 0.0,
	"attention": 0.0
}

var rendered_landmarks: Dictionary = {}
var last_geometry_signature := ""

func apply_pose(next_pose: Dictionary) -> void:
	for key in next_pose:
		var value = next_pose[key]
		if key in ["torso_scale", "foot_left", "foot_right"] and value is Array and value.size() == 2:
			value = Vector2(float(value[0]), float(value[1]))
		pose[key] = value
	queue_redraw()

func reset_pose() -> void:
	pose = {
		"facing": "front_left", "torso_scale": Vector2.ONE, "head_turn": 0.35,
		"head_tilt": 0.0, "arm_left": 0.0, "arm_right": 0.0, "leg_left": 0.0,
		"leg_right": 0.0, "foot_left": Vector2.ZERO, "foot_right": Vector2.ZERO,
		"gaze": 0.0, "mouth_open": 0.0, "attention": 0.0
	}
	queue_redraw()

func landmark_snapshot() -> Dictionary:
	return rendered_landmarks.duplicate(true)

func geometry_signature() -> String:
	return last_geometry_signature

func _draw() -> void:
	var torso_scale: Vector2 = pose.get("torso_scale", Vector2.ONE)
	var head_turn := float(pose.get("head_turn", 0.35))
	var head_tilt := float(pose.get("head_tilt", 0.0))
	var facing := String(pose.get("facing", "front_left"))
	var arm_l := float(pose.get("arm_left", 0.0))
	var arm_r := float(pose.get("arm_right", 0.0))
	var leg_l := float(pose.get("leg_left", 0.0))
	var leg_r := float(pose.get("leg_right", 0.0))
	var foot_l: Vector2 = pose.get("foot_left", Vector2.ZERO)
	var foot_r: Vector2 = pose.get("foot_right", Vector2.ZERO)
	var gaze := float(pose.get("gaze", 0.0))
	var mouth_open := float(pose.get("mouth_open", 0.0))
	var attention := float(pose.get("attention", 0.0))

	# Shadow stays under the fixed root and is not part of locomotion.
	draw_oval(Vector2(512, 900), Vector2(160, 24), SHADOW)

	# Legs are independent chains.  A foot's contact point is calculated from
	# the pose, not copied from a manifest constant.
	var hip_l := Vector2(465, 745)
	var hip_r := Vector2(559, 745)
	var knee_l := hip_l + Vector2(-10, 82).rotated(leg_l)
	var knee_r := hip_r + Vector2(10, 82).rotated(leg_r)
	var ankle_l := knee_l + Vector2(-6, 93).rotated(leg_l * 0.55)
	var ankle_r := knee_r + Vector2(6, 93).rotated(leg_r * 0.55)
	var contact_l := Vector2(410, 896) + foot_l
	var contact_r := Vector2(614, 896) + foot_r
	draw_chain(hip_l, knee_l, ankle_l, contact_l, 54, BASE)
	draw_chain(hip_r, knee_r, ankle_r, contact_r, 54, BASE)
	draw_foot(contact_l, -1.0)
	draw_foot(contact_r, 1.0)

	# Torso and pelvis are separate source parts; breathing scales around ROOT.
	var torso_center := Vector2(512, 635)
	var torso_poly := PackedVector2Array([
		Vector2(-112, -120), Vector2(112, -120), Vector2(132, 45), Vector2(78, 142),
		Vector2(-78, 142), Vector2(-132, 45)
	])
	draw_transformed_polygon(torso_poly, torso_center, torso_scale, 0.0, BASE)
	draw_transformed_polygon(PackedVector2Array([Vector2(-100, 24), Vector2(0, 118), Vector2(100, 24), Vector2(72, 124), Vector2(-72, 124)]), torso_center, torso_scale, 0.0, SHADOW_2)

	# Arms are independently rotated chains with complete hands.
	var shoulder_l := Vector2(399, 545)
	var shoulder_r := Vector2(625, 545)
	var elbow_l := shoulder_l + Vector2(-52, 106).rotated(arm_l)
	var elbow_r := shoulder_r + Vector2(52, 106).rotated(arm_r)
	var wrist_l := elbow_l + Vector2(-32, 92).rotated(arm_l * 0.6)
	var wrist_r := elbow_r + Vector2(32, 92).rotated(arm_r * 0.6)
	draw_chain(shoulder_l, elbow_l, wrist_l, wrist_l, 42, BASE)
	draw_chain(shoulder_r, elbow_r, wrist_r, wrist_r, 42, BASE)
	draw_hand(wrist_l, -1.0)
	draw_hand(wrist_r, 1.0)

	# Head and stable spike topology.  front_left has a narrowed silhouette and
	# asymmetric eye spacing; the transition therefore changes facing, not scale.
	var turn_shift := 42.0 * head_turn
	var head_scale := Vector2(1.0 - 0.10 * head_turn, 1.0)
	var head_center := Vector2(512 + turn_shift, 365)
	draw_oval(head_center + Vector2(0, 32), Vector2(205 * head_scale.x, 178), BASE)
	# Each spike is an independent convex replacement shape, so a bad polygon
	# cannot silently invalidate the whole head silhouette.
	var spike_triangles := [
		[Vector2(-196, 35), Vector2(-150, -96), Vector2(-108, 12)],
		[Vector2(-135, -22), Vector2(-42, -305), Vector2(-28, -20)],
		[Vector2(-12, -12), Vector2(125, -286), Vector2(94, 35)],
		[Vector2(82, 20), Vector2(205, -206), Vector2(182, 66)],
		[Vector2(160, 50), Vector2(258, -6), Vector2(208, 110)]
	]
	for triangle in spike_triangles:
		var points := PackedVector2Array()
		for point in triangle:
			points.append(head_center + Vector2(point.x * head_scale.x, point.y).rotated(head_tilt))
		draw_colored_polygon(points, BASE)
		draw_polyline(points, OUTLINE, 8.0, true)
	draw_transformed_polygon(PackedVector2Array([Vector2(-195, 72), Vector2(-118, 126), Vector2(0, 164), Vector2(130, 126), Vector2(208, 66)]), head_center, head_scale, head_tilt, SHADOW_2)

	var eye_l := head_center + Vector2(-86 + 18 * head_turn, 62)
	var eye_r := head_center + Vector2(78 + 18 * head_turn, 62)
	draw_eye(eye_l, -0.20 - 0.12 * attention, gaze)
	if head_turn < 0.92:
		draw_eye(eye_r, 0.20 - 0.12 * attention, gaze)
	var mouth := head_center + Vector2(0, 148)
	draw_arc(mouth, 50.0, 0.3, 2.8, 32, MOUTH, 8.0)
	if mouth_open > 0.1:
		draw_line(mouth + Vector2(-32, 5), mouth + Vector2(32, 5), MOUTH, 8.0)

	rendered_landmarks = {
		"root": [int(ROOT.x), int(ROOT.y)],
		"left_foot": [int(contact_l.x), int(contact_l.y)],
		"right_foot": [int(contact_r.x), int(contact_r.y)],
		"head": [int(head_center.x), int(head_center.y - 270)],
		"eye_left": [int(eye_l.x), int(eye_l.y)],
		"eye_right": [int(eye_r.x), int(eye_r.y)]
	}
	last_geometry_signature = "%s|%.3f|%.3f|%.3f|%.3f|%.3f|%s" % [facing, arm_l, arm_r, leg_l, leg_r, head_turn, str(torso_scale)]

func draw_transformed_polygon(points: PackedVector2Array, center: Vector2, scale: Vector2, rotation: float, color: Color) -> void:
	var result := PackedVector2Array()
	for p in points:
		result.append(center + Vector2(p.x * scale.x, p.y * scale.y).rotated(rotation))
	draw_colored_polygon(result, color)
	draw_polyline(result, OUTLINE, 8.0, true)

func draw_chain(a: Vector2, b: Vector2, c: Vector2, d: Vector2, width: float, color: Color) -> void:
	draw_line(a, b, color, width, true); draw_circle(a, width * 0.5, color)
	draw_line(b, c, color, width * 0.9, true); draw_circle(b, width * 0.45, color)
	draw_line(c, d, color, width * 0.85, true); draw_circle(c, width * 0.42, color)
	draw_line(a, b, OUTLINE, 8.0, true); draw_line(b, c, OUTLINE, 7.0, true)

func draw_hand(center: Vector2, side: float) -> void:
	draw_circle(center, 37, BASE); draw_arc(center, 37, 0, TAU, 24, OUTLINE, 8.0)
	# Exactly two fingers plus one thumb, each independently visible.
	for i in 2:
		var p := center + Vector2(side * (22 + i * 19), 18 + i * 5)
		draw_line(center + Vector2(side * (8 + i * 12), 8), p, BASE, 23.0, true)
		draw_circle(p, 11, BASE); draw_circle(p, 11, OUTLINE, false, 5.0)
	var thumb := center + Vector2(side * 30, -18)
	draw_line(center, thumb, BASE, 24.0, true); draw_circle(thumb, 12, BASE); draw_circle(thumb, 12, OUTLINE, false, 5.0)

func draw_foot(contact: Vector2, side: float) -> void:
	var heel := contact + Vector2(0, -26)
	draw_oval(heel, Vector2(82, 37), BASE)
	draw_arc(heel, 82, 0, TAU, 32, OUTLINE, 8.0)
	# Exactly three toes, separated by dark seams.
	for i in 3:
		var toe := contact + Vector2(side * (38 + i * 24), -10 - i * 2)
		draw_oval(toe, Vector2(28, 22), BASE)
		draw_arc(toe, 28, 0, TAU, 16, OUTLINE, 5.0)

func draw_eye(center: Vector2, rotation: float, gaze: float) -> void:
	var eye_poly := PackedVector2Array([Vector2(-48, -4), Vector2(-28, -48), Vector2(28, -48), Vector2(48, -4), Vector2(25, 52), Vector2(-25, 52)])
	draw_transformed_polygon(eye_poly, center, Vector2(1, 1), rotation, EYE)
	var pupil := center + Vector2(gaze * 14, 7)
	draw_oval(pupil, Vector2(14, 26), PUPIL)

func draw_oval(center: Vector2, radii: Vector2, color: Color) -> void:
	var points := PackedVector2Array()
	for i in 32:
		var angle := TAU * float(i) / 32.0
		points.append(center + Vector2(cos(angle) * radii.x, sin(angle) * radii.y))
	draw_colored_polygon(points, color)

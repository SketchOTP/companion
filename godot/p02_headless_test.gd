extends SceneTree

func _initialize() -> void:
	var scene: Node = load("res://main.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	var avatar = scene.get_node("MonAvatar")
	var result: Dictionary = await avatar.director.request_intent("gaze")
	var state = avatar.visible_state()
	var errors: Array[String] = []
	if result.get("schema_major") != 1: errors.append("intent schema")
	if result.get("status") not in ["started", "failed"]: errors.append("intent status")
	if state.get("schema_major") != 1: errors.append("visible state schema")
	if avatar.get_node("BodyA") == null or avatar.get_node("BodyB") == null: errors.append("body layers")
	print(JSON.stringify({"status":"PASSED" if errors.is_empty() else "FAILED","errors":errors,"intent":result,"visible":state,"layer_names":["Shadow","AccessoryBack","BodyA","BodyB","FaceOrEyes","MouthViseme","HeldObject","AccessoryFront","Effects","AnimationPlayer","MonAnimationDirector"]}))
	quit(0 if errors.is_empty() else 1)

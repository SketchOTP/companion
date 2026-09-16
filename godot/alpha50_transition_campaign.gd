extends SceneTree
const TransitionResolver = preload("res://mon_transition_resolver.gd")

const PACK_SHA := "1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40"
const STATES := ["front_rest", "left_profile_rest", "right_profile_rest", "left_start", "left_loop", "left_stop", "right_start", "right_loop", "right_stop", "listen"]
const REQUESTS := ["left", "right", "listen", "stop", "cancel"]

var output_path := ""
var case_count := 10000

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output_path = arg.trim_prefix("--output=")
		if arg.begins_with("--cases="): case_count = int(arg.trim_prefix("--cases="))
	if output_path.is_empty():
		printerr("missing --output")
		quit(2)
		return
	var cases: Array = []
	var illegal := 0
	for i in range(case_count):
		var start: String = STATES[(i * 17 + 3) % STATES.size()]
		var request: String = REQUESTS[(i * 31 + 5) % REQUESTS.size()]
		var route := TransitionResolver.resolve(start, request)
		var accepted: bool = not route.is_empty()
		if not accepted: illegal += 1
		cases.append({"case_id": "godot-alpha50-%06d" % i, "start_state": start, "request": request, "accepted": accepted, "route": route, "terminal_state": route[-1] if accepted else start, "pack_sha256": PACK_SHA})
	var result := {"status": "PASS" if cases.size() == case_count and illegal > 0 else "FAIL", "process": "Godot", "cases": cases, "case_count": cases.size(), "illegal_count": illegal, "pack_sha256": PACK_SHA, "authority": "godot_production_legal_graph", "authority_revision": TransitionResolver.AUTHORITY_REVISION}
	var file := FileAccess.open(output_path, FileAccess.WRITE)
	file.store_string(JSON.stringify(result))
	file.close()
	print(JSON.stringify({"status": result.status, "case_count": cases.size(), "illegal_count": illegal, "pack_sha256": PACK_SHA}))
	quit(0 if result.status == "PASS" else 1)

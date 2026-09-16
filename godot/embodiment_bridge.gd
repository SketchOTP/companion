class_name EmbodimentBridge
extends Node

signal bridge_event(event: Dictionary)
const PROTOCOL := "companion-embodiment-v1"
var sequence := 0
var connected := false
var bridge_generation := "p02-bridge-v1"

func acknowledge_intent(intent_id: String, clip_id: String) -> Dictionary:
	sequence += 1
	var event := {"schema_major":1,"event_type":"intent_ack","sequence":sequence,"intent_id":intent_id,"clip_id":clip_id,"status":"accepted","protocol":PROTOCOL,"generation":bridge_generation}
	bridge_event.emit(event); return event

func report(event_type: String, clip_id: String, status: String = "observed") -> Dictionary:
	sequence += 1
	var event := {"schema_major":1,"event_type":event_type,"sequence":sequence,"clip_id":clip_id,"status":status,"protocol":PROTOCOL,"generation":bridge_generation}
	bridge_event.emit(event); return event

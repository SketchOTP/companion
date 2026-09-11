class_name MonAnimationTrackResource
extends Resource

## Godot-side representation of one MON_TEMPORAL_TRACKS_V1 track. The resource
## is a presentation adapter; it cannot own organism, memory, identity, or care
## authority.
@export var track_id: String
@export var clip_id: String
@export var body_revision: String
@export var stage: String
@export var family: String
@export var direction: String
@export var facing: String
@export var travel_direction: String
@export var posture: String
@export var variant: int = 1
@export var frame_profile: String = "MON_FRAME_V1"
@export var loop_mode: String = "once"
@export var fps: int = 24
@export var duration_ticks: PackedInt32Array
@export var frame_paths: PackedStringArray
@export var frame_hashes: PackedStringArray
@export var root_motion_policy: String = "forbidden"

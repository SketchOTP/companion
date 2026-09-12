use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EventEnvelope {
    pub schema_major: u16,
    pub event_type: String,
    pub message_id: Uuid,
    pub boot_id: String,
    pub monotonic_ns: u64,
    pub utc_observed: String,
    pub utc_uncertainty_us: u64,
    pub event_sequence: u64,
    pub causation_id: Option<Uuid>,
    pub payload: serde_json::Value,
}

/// R04-C01 source/ingested boundary types. These are deliberately separate:
/// source manifests contain only Architect-supplied facts while ingested packs
/// add content-addressed runtime relationships.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum LandmarkState {
    Visible,
    Occluded,
    NotApplicable,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LandmarkObservation {
    pub state: LandmarkState,
    pub point: Option<LandmarkPoint>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct CanonicalLandmarks {
    pub root: LandmarkObservation,
    pub ground_contact_left: LandmarkObservation,
    pub ground_contact_right: LandmarkObservation,
    pub head_center: LandmarkObservation,
    pub eye_midpoint: LandmarkObservation,
    pub eye_left: LandmarkObservation,
    pub eye_right: LandmarkObservation,
    pub mouth_center: LandmarkObservation,
    pub hand_left: LandmarkObservation,
    pub hand_right: LandmarkObservation,
    pub foot_left: LandmarkObservation,
    pub foot_right: LandmarkObservation,
    pub attachment_back: LandmarkObservation,
    pub attachment_front: LandmarkObservation,
    pub interaction_focus: LandmarkObservation,
    pub action_anchor: LandmarkObservation,
    pub object_anchor: LandmarkObservation,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct SourceAsset {
    pub asset_id: String,
    pub filename: String,
    pub sha256: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct SourceFrame {
    pub frame_id: String,
    pub frame_index: u16,
    pub filename: String,
    pub sidecar_filename: String,
    pub duration_ticks: u16,
    pub source_asset_id: String,
    pub source_sha256: String,
    pub facing: Facing,
    pub posture: Posture,
    pub action_phase: Option<String>,
    pub landmarks: CanonicalLandmarks,
    pub provenance: FrameProvenance,
    pub reuse_of: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct SourceTrack {
    pub track_id: String,
    pub family: String,
    pub selection_facing: Facing,
    pub entry_facing: Facing,
    pub exit_facing: Facing,
    pub posture: Posture,
    pub variant: u16,
    pub entry_posture: Posture,
    pub exit_posture: Posture,
    pub completion: TrackCompletion,
    pub frames: Vec<SourceFrame>,
    pub contacts: Vec<ContactSpan>,
    pub events: Vec<AnimationEvent>,
    pub interruption_ranges: Vec<InterruptionRange>,
    pub track_checksum: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct MonAuthoredFrameSourcePackV1 {
    pub profile: String,
    pub schema_version: u16,
    pub pack_id: Uuid,
    pub pack_revision: String,
    pub body_revision: String,
    pub developmental_stage: String,
    pub approval_state: ApprovalState,
    pub approved_references: ApprovedReferenceHashes,
    pub provenance: PackProvenance,
    pub timing: TimingProfile,
    pub request_profile: String,
    pub source_assets: Vec<SourceAsset>,
    pub tracks: Vec<SourceTrack>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct IngestedAsset {
    pub asset_id: String,
    pub source_sha256: String,
    pub source_filename: String,
    pub content_address: String,
    pub runtime_asset: String,
    pub validation: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct MonIngestedFramePackV1 {
    pub profile: String,
    pub schema_version: u16,
    pub source_profile: String,
    pub source_pack_id: Uuid,
    pub pack_revision: String,
    pub body_revision: String,
    pub developmental_stage: String,
    pub approval_state: ApprovalState,
    pub approved_references: ApprovedReferenceHashes,
    pub provenance: PackProvenance,
    pub timing: TimingProfile,
    pub request_profile: String,
    pub source_assets: Vec<IngestedAsset>,
    pub tracks: Vec<SourceTrack>,
    pub pack_digest: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct FrameIntakeObservation {
    pub frame_id: String,
    pub source_asset_id: String,
    pub input_sha256: String,
    pub stored_sha256: String,
    pub runtime_sha256: String,
    pub byte_identical: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct IntakeValidation {
    pub status: String,
    pub errors: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct MonFrameIntakeReceiptV1 {
    pub profile: String,
    pub schema_version: u16,
    pub operation: String,
    pub validation_profile: String,
    pub source_pack_sha256: String,
    pub source_tree_sha256: String,
    pub ingested_pack_sha256: String,
    pub output_tree_sha256: String,
    pub publication_state: String,
    pub source_bytes_mutated: bool,
    pub frames: Vec<FrameIntakeObservation>,
    pub validation: IntakeValidation,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Readiness {
    pub role: String,
    pub version: String,
    pub ready: bool,
    pub degraded: bool,
    pub reason: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SafetyCandidate {
    pub schema_major: u16,
    pub message_id: Uuid,
    pub producer_generation: String,
    pub auth_scheme: String,
    pub mac: String,
    pub observed_at: String,
    pub confidence_milli: u16,
    pub quality_milli: u16,
    pub replay: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CareReceipt {
    pub receipt_id: Uuid,
    pub candidate_id: Uuid,
    pub accepted: bool,
    pub duplicate: bool,
    pub reason: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct HealthSnapshot {
    pub role: String,
    pub status: String,
    pub boot_id: String,
    pub sequence: u64,
    pub correlation_id: Option<Uuid>,
    pub causation_id: Option<Uuid>,
    pub reason: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct OrdinaryObservation {
    pub schema_major: u16,
    pub message_id: Uuid,
    pub producer: String,
    pub observed_at: String,
    pub kind: String,
    pub payload: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EmbodimentIntent {
    pub schema_major: u16,
    pub intent_id: Uuid,
    pub kind: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EmbodimentResult {
    pub schema_major: u16,
    pub intent_id: Uuid,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MonAnimationClip {
    pub clip_id: String,
    pub version: u16,
    pub body_revision: String,
    pub stage: String,
    pub direction_coverage: Vec<String>,
    pub start_posture: String,
    pub end_posture: String,
    pub behavior_tags: Vec<String>,
    pub affect_compatibility: Vec<String>,
    pub energy_compatibility: Vec<String>,
    pub loop_mode: String,
    pub root_motion_policy: String,
    pub pack_revision: String,
    pub checksum: String,
}

/// A temporal body track. Direction selects a track; it is never a frame in
/// the temporal sequence. Runtime consumers may deserialize this type without
/// taking ownership of organism or care state.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MonAnimationTrack {
    pub track_id: String,
    pub clip_id: String,
    pub version: u16,
    pub body_revision: String,
    pub stage: String,
    pub family: String,
    pub direction: String,
    pub posture: String,
    pub variant: u16,
    pub source_revision: String,
    pub source_reference_sha256: String,
    pub frame_profile: String,
    pub frames: Vec<MonAnimationTrackFrame>,
    pub loop_mode: String,
    pub root_motion_policy: String,
    pub track_checksum: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MonAnimationTrackFrame {
    pub frame_id: String,
    pub duration_ticks: u16,
    pub path: String,
    pub sha256: String,
}

/// R03 temporal track contract. Facing is a selection key; frame order is
/// temporal and carries source-space landmarks and contact/event evidence.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MonTemporalTrackV2 {
    pub track_id: String,
    pub clip_id: String,
    pub version: u16,
    pub body_revision: String,
    pub stage: String,
    pub family: String,
    pub facing: String,
    pub travel_direction: Option<String>,
    pub posture: String,
    pub variant: u16,
    pub source_revision: String,
    pub source_reference_sha256: String,
    pub frame_profile: String,
    pub fps: u16,
    pub frames: Vec<MonTemporalTrackFrameV2>,
    pub loop_mode: String,
    pub root_motion_policy: String,
    pub entry_posture: String,
    pub exit_posture: String,
    pub events: Vec<serde_json::Value>,
    pub interruptible_ranges: Vec<Vec<u32>>,
    pub source_checksum: String,
    pub pack_revision: String,
    pub track_checksum: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MonTemporalTrackFrameV2 {
    pub frame_id: String,
    pub frame_index: u32,
    pub duration_ticks: u16,
    pub path: String,
    pub sha256: String,
    pub source_pose_id: String,
    pub landmarks: serde_json::Value,
    pub contacts: Vec<serde_json::Value>,
    pub events: Vec<serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MonTemporalTracksV2 {
    pub profile: String,
    pub body_revision: String,
    pub timing: serde_json::Value,
    pub tracks: Vec<MonTemporalTrackV2>,
}

/// Immutable externally authored frame-pack boundary. Production eligibility
/// is a manifest property, never something inferred from a filename.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Facing {
    Front,
    FrontRight,
    Right,
    BackRight,
    Back,
    BackLeft,
    Left,
    FrontLeft,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Posture {
    Neutral,
    Listening,
    Acknowledging,
    Walking,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ApprovalState {
    Candidate,
    OperatorApproved,
    Rejected,
    SyntheticTestOnly,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ContactState {
    Planted,
    Swing,
    Clear,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum TrackCompletion {
    Once,
    Loop,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LandmarkPoint {
    pub x: u16,
    pub y: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct FrameLandmarks {
    pub root: LandmarkPoint,
    pub head: LandmarkPoint,
    pub eye_left: LandmarkPoint,
    pub eye_right: LandmarkPoint,
    pub hand_left: LandmarkPoint,
    pub hand_right: LandmarkPoint,
    pub foot_left: LandmarkPoint,
    pub foot_right: LandmarkPoint,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ContactSpan {
    pub landmark: String,
    pub state: ContactState,
    pub start_tick: u32,
    pub end_tick: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct AnimationEvent {
    #[serde(default)]
    pub event_id: Option<String>,
    pub name: String,
    pub tick: u32,
    pub frame_index: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct TimingProfile {
    pub fps: u16,
    pub tick_unit: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct FrameProvenance {
    pub authored_by: String,
    pub method: String,
    pub source_revision: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct PackProvenance {
    pub art_authority: String,
    pub generation_or_edit_method: String,
    pub source_authority: String,
    pub rights_record: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct InterruptionRange {
    pub start_tick: u32,
    pub end_tick: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ApprovedReferenceHashes {
    pub identity_sha256: String,
    pub turnaround_sha256: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct SourceRuntimeRelationship {
    pub source_sha256: String,
    pub content_address: String,
    pub runtime_asset: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct AuthoredFrame {
    pub frame_id: String,
    pub frame_index: u16,
    pub filename: String,
    pub sidecar_filename: String,
    pub duration_ticks: u16,
    pub source_sha256: String,
    pub root: LandmarkPoint,
    pub landmarks: FrameLandmarks,
    pub provenance: FrameProvenance,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct AuthoredTrack {
    pub track_id: String,
    pub family: String,
    pub facing: Facing,
    pub posture: Posture,
    pub variant: u16,
    pub entry_posture: Posture,
    pub exit_posture: Posture,
    pub completion: TrackCompletion,
    pub frames: Vec<AuthoredFrame>,
    pub contacts: Vec<ContactSpan>,
    pub events: Vec<AnimationEvent>,
    pub interruption_ranges: Vec<InterruptionRange>,
    pub track_checksum: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct MonAuthoredFramePackV1 {
    pub profile: String,
    pub schema_version: u16,
    pub pack_id: Uuid,
    pub pack_revision: String,
    pub body_revision: String,
    pub developmental_stage: String,
    pub approval_state: ApprovalState,
    pub approved_references: ApprovedReferenceHashes,
    pub provenance: PackProvenance,
    pub timing: TimingProfile,
    pub tracks: Vec<AuthoredTrack>,
    pub source_runtime_relationships: Vec<SourceRuntimeRelationship>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EmbodimentEvent {
    pub schema_major: u16,
    pub event_type: String,
    pub intent_id: uuid::Uuid,
    pub clip_id: Option<String>,
    pub frame: Option<u32>,
    pub status: String,
    pub generation: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct VaultDecision {
    pub schema_major: u16,
    pub decision_id: Uuid,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct BackupManifest {
    pub schema_major: u16,
    pub authority: String,
    pub schema_version: u32,
    pub integrity: String,
    pub created_utc: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DegradedState {
    pub role: String,
    pub status: String,
    pub reason: String,
}

#[cfg(test)]
mod tests {
    use super::{
        ApprovalState, MonAnimationClip, MonAnimationTrack, MonAnimationTrackFrame,
        MonAuthoredFramePackV1, MonTemporalTrackV2, MonTemporalTracksV2,
    };

    #[test]
    fn mon_animation_clip_round_trips_project_profile_fields() {
        let clip = MonAnimationClip {
            clip_id: "idle_breathe_a".into(),
            version: 1,
            body_revision: "mon-body-v1".into(),
            stage: "candidate".into(),
            direction_coverage: vec!["N".into(), "NE".into()],
            start_posture: "neutral".into(),
            end_posture: "neutral".into(),
            behavior_tags: vec!["idle".into()],
            affect_compatibility: vec!["neutral".into()],
            energy_compatibility: vec!["low".into()],
            loop_mode: "loop".into(),
            root_motion_policy: "forbidden".into(),
            pack_revision: "p02-pack-v1".into(),
            checksum: "0".repeat(64),
        };
        let bytes = serde_json::to_vec(&clip).expect("serialize");
        let decoded: MonAnimationClip = serde_json::from_slice(&bytes).expect("deserialize");
        assert_eq!(clip, decoded);
    }

    #[test]
    fn temporal_track_round_trips_with_direction_as_selection_key() {
        let track = MonAnimationTrack {
            track_id: "mon-body-v1:candidate:idle_breathe_a:N:neutral:1".into(),
            clip_id: "idle_breathe_a".into(),
            version: 1,
            body_revision: "mon-body-v1".into(),
            stage: "candidate".into(),
            family: "idle_breathe_a".into(),
            direction: "N".into(),
            posture: "neutral".into(),
            variant: 1,
            source_revision: "p02-native-reference-v1".into(),
            source_reference_sha256: "0".repeat(64),
            frame_profile: "MON_FRAME_V1".into(),
            frames: vec![MonAnimationTrackFrame {
                frame_id: "idle_breathe_a_N_1_00".into(),
                duration_ticks: 1,
                path: "frames/x.png".into(),
                sha256: "0".repeat(64),
            }],
            loop_mode: "loop".into(),
            root_motion_policy: "forbidden".into(),
            track_checksum: "0".repeat(64),
        };
        let decoded: MonAnimationTrack =
            serde_json::from_slice(&serde_json::to_vec(&track).unwrap()).unwrap();
        assert_eq!(track, decoded);
        assert_eq!(decoded.direction, "N");
        assert_eq!(decoded.frames.len(), 1);
    }

    #[test]
    fn r03_temporal_fixture_round_trips_with_facing_and_landmarks() {
        let fixture = include_str!("../../../contracts/fixtures/mon-temporal-track-v2.json");
        let track: MonTemporalTrackV2 =
            serde_json::from_str(fixture).expect("R03 fixture deserializes");
        assert_eq!(track.version, 2);
        assert_eq!(track.facing, "front_left");
        assert_eq!(
            track.frames[0].landmarks["root"],
            serde_json::json!([512, 896])
        );
        let encoded = serde_json::to_vec(&track).expect("R03 fixture reserializes");
        let decoded: MonTemporalTrackV2 =
            serde_json::from_slice(&encoded).expect("R03 fixture round trips");
        assert_eq!(track, decoded);
    }

    #[test]
    fn r03_tracks_wrapper_round_trips() {
        let wrapper = MonTemporalTracksV2 {
            profile: "MON_TEMPORAL_TRACKS_V2".into(),
            body_revision: "mon-body-v2-r03".into(),
            timing: serde_json::json!({"fps": 24, "unit": "1/24s"}),
            tracks: Vec::new(),
        };
        let decoded: MonTemporalTracksV2 =
            serde_json::from_slice(&serde_json::to_vec(&wrapper).unwrap()).unwrap();
        assert_eq!(wrapper, decoded);
    }

    #[test]
    fn r03_generated_tracks_round_trip_when_bundle_is_provided() {
        let Ok(path) = std::env::var("R03_TRACKS_PATH") else {
            return;
        };
        let bytes = std::fs::read(path).expect("R03 generated tracks readable");
        let decoded: MonTemporalTracksV2 =
            serde_json::from_slice(&bytes).expect("R03 generated tracks deserialize");
        assert_eq!(decoded.profile, "MON_TEMPORAL_TRACKS_V2");
        assert!(!decoded.tracks.is_empty());
        for track in decoded.tracks {
            let encoded = serde_json::to_vec(&track).expect("R03 track reserialize");
            let round_trip: MonTemporalTrackV2 =
                serde_json::from_slice(&encoded).expect("R03 track re-deserialize");
            assert_eq!(round_trip.version, 2);
            assert_eq!(round_trip.fps, 24);
        }
    }

    #[test]
    fn authored_frame_pack_fixture_round_trips_with_explicit_types() {
        let fixture = include_str!("../../../contracts/fixtures/mon-authored-frame-pack-v1.json");
        let pack: MonAuthoredFramePackV1 =
            serde_json::from_str(fixture).expect("R04 authored pack fixture deserializes");
        assert_eq!(pack.profile, "MON_AUTHORED_FRAME_PACK_V1");
        assert_eq!(pack.approval_state, ApprovalState::SyntheticTestOnly);
        assert_eq!(pack.timing.fps, 24);
        assert_eq!(pack.tracks[0].frames[0].root.x, 512);
        let encoded = serde_json::to_vec(&pack).expect("R04 pack reserializes");
        let decoded: MonAuthoredFramePackV1 =
            serde_json::from_slice(&encoded).expect("R04 pack round trips");
        assert_eq!(pack, decoded);
    }
}

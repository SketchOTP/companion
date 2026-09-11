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
    use super::{MonAnimationClip, MonAnimationTrack, MonAnimationTrackFrame};

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
}

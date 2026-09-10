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

//! Persistent, deterministic organism state for the Alpha50 integration slice.
//!
//! This module is deliberately model-free: canonical identity, physiology,
//! drive arbitration, memory provenance, and body-neutral intents are all
//! represented as typed Rust data.  Godot and optional model workers are
//! downstream adapters and never own this state.
use crate::persistence::{Store, StoreError};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use uuid::Uuid;

pub const ORGANISM_SCHEMA: u16 = 1;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct InternalState {
    pub energy: f32,
    pub rest_pressure: f32,
    pub engagement: f32,
    pub social_need: f32,
    pub curiosity: f32,
    pub confidence: f32,
    pub stress: f32,
}

impl Default for InternalState {
    fn default() -> Self {
        Self {
            energy: 0.78,
            rest_pressure: 0.12,
            engagement: 0.35,
            social_need: 0.25,
            curiosity: 0.30,
            confidence: 0.70,
            stress: 0.10,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Drive {
    pub name: String,
    pub urgency: f32,
    pub inhibition: f32,
    pub cause: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Goal {
    pub goal_id: Uuid,
    pub kind: String,
    pub priority: u32,
    pub status: String,
    pub reason_memory: Option<Uuid>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Commitment {
    pub commitment_id: Uuid,
    pub description: String,
    pub state: String,
    pub due_organism_tick: u64,
    pub provenance: Option<Uuid>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct RetrievalResult {
    pub records: Vec<MemoryRecord>,
    pub abstained: bool,
    pub reason: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Skill {
    pub skill_id: String,
    pub stage: String,
    pub evidence_count: u32,
    pub stability: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EvidenceRef {
    pub event_id: Uuid,
    pub source: String,
    pub observed_at_tick: u64,
    pub confidence_milli: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum MemoryKind {
    Event,
    Episodic,
    Semantic,
    Procedural,
    Relationship,
    Preference,
    Prospective,
    DreamSynthetic,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MemoryRecord {
    pub memory_id: Uuid,
    pub kind: MemoryKind,
    pub subject: String,
    pub content: String,
    pub evidence: Vec<EvidenceRef>,
    pub supporting: Vec<Uuid>,
    pub contradicting: Vec<Uuid>,
    pub supersedes: Option<Uuid>,
    pub valid_from_tick: u64,
    pub valid_until_tick: Option<u64>,
    pub confidence_milli: u16,
    pub scope: String,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct BodyNeutralIntent {
    pub intent_id: Uuid,
    pub intent_sequence: u64,
    pub action: String,
    pub facing: String,
    pub reason: String,
    pub source_goal: Option<Uuid>,
}

impl BodyNeutralIntent {
    /// The common wire ceiling is the signed int64 range consumed by Godot.
    pub const WIRE_SEQUENCE_MAX: u64 = i64::MAX as u64;

    pub fn validate_wire(&self) -> Result<(), &'static str> {
        (self.intent_sequence <= Self::WIRE_SEQUENCE_MAX)
            .then_some(())
            .ok_or("intent_sequence_exceeds_common_signed_64_range")
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct OrganismState {
    pub schema_version: u16,
    pub identity: Uuid,
    pub origin: String,
    pub organism_epoch: u64,
    pub organism_tick: u64,
    pub lifecycle: String,
    pub developmental_stage: String,
    pub capability_gates: BTreeMap<String, bool>,
    pub internal: InternalState,
    pub drives: Vec<Drive>,
    pub goals: Vec<Goal>,
    pub commitments: Vec<Commitment>,
    pub unfinished_actions: Vec<String>,
    pub attention: String,
    pub memory_refs: Vec<Uuid>,
    pub memories: Vec<MemoryRecord>,
    pub skills: Vec<Skill>,
    pub learned_preferences: BTreeMap<String, String>,
    pub learned_outcomes: BTreeMap<String, i32>,
    pub degradation: Vec<String>,
    pub next_intent_sequence: u64,
    pub last_intent: Option<BodyNeutralIntent>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct LifeStep {
    pub tick: u64,
    pub drives: Vec<Drive>,
    pub selected: BodyNeutralIntent,
    pub state_digest: String,
}

impl OrganismState {
    pub fn new(identity: Uuid) -> Self {
        Self {
            schema_version: ORGANISM_SCHEMA,
            identity,
            origin: "alpha50-local".into(),
            organism_epoch: 1,
            organism_tick: 0,
            lifecycle: "alive".into(),
            developmental_stage: "seed".into(),
            capability_gates: BTreeMap::new(),
            internal: InternalState::default(),
            drives: Vec::new(),
            goals: Vec::new(),
            commitments: Vec::new(),
            unfinished_actions: Vec::new(),
            attention: "none".into(),
            memory_refs: Vec::new(),
            memories: Vec::new(),
            skills: Vec::new(),
            degradation: Vec::new(),
            next_intent_sequence: 1,
            last_intent: None,
            learned_preferences: BTreeMap::new(),
            learned_outcomes: BTreeMap::new(),
        }
    }

    pub fn deterministic(seed: u64) -> Self {
        let identity =
            Uuid::from_u128(0xA1FA_5000_0000_0000_0000_0000_0000_0000u128 | seed as u128);
        Self::new(identity)
    }

    pub fn recompute_drives(&mut self) {
        self.drives = vec![
            Drive {
                name: "rest".into(),
                urgency: self.internal.rest_pressure,
                inhibition: self.internal.energy * 0.15,
                cause: "rest_pressure".into(),
            },
            Drive {
                name: "social".into(),
                urgency: self.internal.social_need,
                inhibition: self.internal.stress * 0.10,
                cause: "social_need".into(),
            },
            Drive {
                name: "curiosity".into(),
                urgency: self.internal.curiosity,
                inhibition: (1.0 - self.internal.confidence) * 0.20,
                cause: "curiosity".into(),
            },
            Drive {
                name: "engagement".into(),
                urgency: self.internal.engagement,
                inhibition: self.internal.rest_pressure * 0.25,
                cause: "engagement".into(),
            },
        ];
        for d in &mut self.drives {
            d.urgency = (d.urgency - d.inhibition).clamp(0.0, 1.0);
        }
    }

    pub fn select_action(&mut self, user_present: bool) -> BodyNeutralIntent {
        self.recompute_drives();
        let commitment = self.commitments.iter().find(|c| c.state == "pending");
        let preferred = self.learned_preferences.get("default").cloned();
        let (action, reason, goal) = if let Some(c) = commitment {
            (
                "acknowledge",
                format!("unfinished_commitment:{}", c.commitment_id),
                None,
            )
        } else if let Some(pref) = preferred.as_deref().filter(|_| user_present) {
            (
                pref,
                "remembered_preference".into(),
                self.goals.first().map(|g| g.goal_id),
            )
        } else if self
            .drives
            .iter()
            .find(|d| d.name == "rest")
            .is_some_and(|d| d.urgency > 0.68)
        {
            ("idle", "rest_pressure".into(), None)
        } else if user_present && self.internal.social_need > 0.30 {
            (
                "acknowledge",
                "social_need_with_user_present".into(),
                self.goals.first().map(|g| g.goal_id),
            )
        } else if self.internal.curiosity >= self.internal.engagement {
            (
                "listen",
                "curiosity_exceeds_engagement".into(),
                self.goals.first().map(|g| g.goal_id),
            )
        } else {
            (
                "idle",
                "low_urgency_resting_presence".into(),
                self.goals.first().map(|g| g.goal_id),
            )
        };
        let intent = BodyNeutralIntent {
            intent_id: Uuid::from_u128(
                0xB0D0_0000_0000_0000_0000_0000_0000_0000u128 | self.next_intent_sequence as u128,
            ),
            intent_sequence: self.next_intent_sequence,
            action: action.into(),
            facing: "front".into(),
            reason,
            source_goal: goal,
        };
        self.next_intent_sequence += 1;
        self.last_intent = Some(intent.clone());
        intent
    }

    pub fn step(&mut self, user_present: bool) -> LifeStep {
        self.organism_tick += 1;
        self.internal.energy = (self.internal.energy - 0.002).max(0.0);
        self.internal.rest_pressure = (self.internal.rest_pressure + 0.004).min(1.0);
        self.internal.social_need =
            (self.internal.social_need + if user_present { -0.03 } else { 0.006 }).clamp(0.0, 1.0);
        self.internal.curiosity =
            (self.internal.curiosity + if user_present { 0.002 } else { 0.004 }).clamp(0.0, 1.0);
        let selected = self.select_action(user_present);
        let bytes = serde_json::to_vec(self).expect("organism state serializes");
        let digest = format!("{:x}", sha2::Sha256::digest(bytes));
        LifeStep {
            tick: self.organism_tick,
            drives: self.drives.clone(),
            selected,
            state_digest: digest,
        }
    }

    pub fn add_memory(&mut self, memory: MemoryRecord) {
        self.memory_refs.push(memory.memory_id);
        self.memories.push(memory);
    }

    /// Retrieve only current, in-scope evidence. Conflicting current records
    /// deliberately abstain instead of selecting a convenient belief.
    pub fn retrieve(
        &self,
        subject: &str,
        scope: &str,
        min_confidence_milli: u16,
    ) -> RetrievalResult {
        let records: Vec<_> = self
            .memories
            .iter()
            .filter(|m| {
                m.subject == subject
                    && m.scope == scope
                    && m.status == "current"
                    && m.confidence_milli >= min_confidence_milli
            })
            .cloned()
            .collect();
        let conflicting = records.iter().any(|m| {
            records
                .iter()
                .any(|other| other.memory_id != m.memory_id && other.content != m.content)
        });
        if records.is_empty() {
            RetrievalResult {
                records,
                abstained: true,
                reason: "no_current_evidence".into(),
            }
        } else if conflicting {
            RetrievalResult {
                records: Vec::new(),
                abstained: true,
                reason: "unresolved_conflict".into(),
            }
        } else {
            RetrievalResult {
                records,
                abstained: false,
                reason: "current_evidence".into(),
            }
        }
    }

    pub fn transition_commitment(
        &mut self,
        commitment_id: Uuid,
        next: &str,
    ) -> Result<(), &'static str> {
        if !matches!(next, "pending" | "completed" | "expired" | "revoked") {
            return Err("invalid_commitment_state");
        }
        let commitment = self
            .commitments
            .iter_mut()
            .find(|c| c.commitment_id == commitment_id)
            .ok_or("commitment_not_found")?;
        if commitment.state != "pending" && commitment.state != next {
            return Err("terminal_commitment");
        }
        commitment.state = next.into();
        Ok(())
    }

    pub fn record_interaction(&mut self, subject: &str, preference: &str) -> Uuid {
        let event_id = Uuid::from_u128(
            0xE000_0000_0000_0000_0000_0000_0000_0000u128 | self.organism_tick as u128,
        );
        let memory_id = Uuid::from_u128(
            0xE100_0000_0000_0000_0000_0000_0000_0000u128 | self.organism_tick as u128,
        );
        self.internal.social_need = (self.internal.social_need - 0.20).max(0.0);
        self.internal.engagement = (self.internal.engagement + 0.20).min(1.0);
        self.learned_preferences
            .insert("default".into(), "acknowledge".into());
        self.add_memory(MemoryRecord {
            memory_id,
            kind: MemoryKind::Preference,
            subject: subject.into(),
            content: preference.into(),
            evidence: vec![EvidenceRef {
                event_id,
                source: "ordinary_observation".into(),
                observed_at_tick: self.organism_tick,
                confidence_milli: 900,
            }],
            supporting: vec![event_id],
            contradicting: Vec::new(),
            supersedes: None,
            valid_from_tick: self.organism_tick,
            valid_until_tick: None,
            confidence_milli: 900,
            scope: "user-local".into(),
            status: "current".into(),
        });
        memory_id
    }

    pub fn record_action_outcome(&mut self, action: &str, success: bool) {
        let entry = self.learned_outcomes.entry(action.into()).or_insert(0);
        *entry += if success { 1 } else { -1 };
        let skill = self.skills.iter_mut().find(|s| s.skill_id == action);
        if let Some(skill) = skill {
            skill.evidence_count += 1;
            skill.stability = (skill.stability + if success { 0.1 } else { -0.02 }).clamp(0.0, 1.0);
            if skill.evidence_count >= 4 && skill.stability >= 0.7 {
                skill.stage = "competent".into();
            }
        } else {
            self.skills.push(Skill {
                skill_id: action.into(),
                stage: "attempted".into(),
                evidence_count: 1,
                stability: if success { 0.6 } else { 0.2 },
            });
        }
    }

    pub fn correct_memory(&mut self, old: Uuid, corrected: &str) -> Result<Uuid, &'static str> {
        let idx = self
            .memories
            .iter()
            .position(|m| m.memory_id == old)
            .ok_or("memory_not_found")?;
        let event_id = Uuid::from_u128(
            0xE200_0000_0000_0000_0000_0000_0000_0000u128 | self.organism_tick as u128,
        );
        self.memories[idx].status = "superseded".into();
        self.memories[idx].valid_until_tick = Some(self.organism_tick);
        let id = Uuid::from_u128(
            0xE300_0000_0000_0000_0000_0000_0000_0000u128 | self.organism_tick as u128,
        );
        self.add_memory(MemoryRecord {
            memory_id: id,
            kind: MemoryKind::Semantic,
            subject: self.memories[idx].subject.clone(),
            content: corrected.into(),
            evidence: vec![EvidenceRef {
                event_id,
                source: "correction".into(),
                observed_at_tick: self.organism_tick,
                confidence_milli: 1000,
            }],
            supporting: vec![event_id],
            contradicting: vec![old],
            supersedes: Some(old),
            valid_from_tick: self.organism_tick,
            valid_until_tick: None,
            confidence_milli: 1000,
            scope: "user-local".into(),
            status: "current".into(),
        });
        Ok(id)
    }

    pub fn consolidate(&mut self) -> usize {
        let mut proposals = 0;
        let repeated = self
            .memories
            .iter()
            .filter(|m| m.kind == MemoryKind::Episodic)
            .count();
        if repeated >= 2 {
            proposals += 1;
        }
        // Synthetic dream material remains explicitly non-evidence.
        if self
            .memories
            .iter()
            .any(|m| m.kind == MemoryKind::DreamSynthetic && !m.evidence.is_empty())
        {
            self.degradation.push("invalid_dream_evidence_link".into());
        }
        proposals
    }

    pub fn snapshot_to(&self, store: &Store) -> Result<bool, StoreError> {
        let payload =
            serde_json::to_string(self).map_err(|e| StoreError::Authority(e.to_string()))?;
        store.append_organism_snapshot(
            &self.identity.to_string(),
            self.organism_epoch,
            &payload,
            &format!("tick:{}", self.organism_tick),
        )
    }
}

use sha2::Digest;

pub fn restore_latest(store: &Store) -> Result<Option<OrganismState>, StoreError> {
    let Some(payload) = store.latest_organism_snapshot()? else {
        return Ok(None);
    };
    serde_json::from_str(&payload)
        .map(Some)
        .map_err(|e| StoreError::Authority(e.to_string()))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn competing_drives_change_action() {
        let mut state = OrganismState::deterministic(1);
        state.internal.rest_pressure = 0.9;
        assert_eq!(state.step(false).selected.action, "idle");
        state.internal.rest_pressure = 0.05;
        state.internal.curiosity = 0.9;
        assert_eq!(state.step(false).selected.action, "listen");
    }
    #[test]
    fn correction_preserves_history_and_supersedes() {
        let mut s = OrganismState::deterministic(2);
        let old = s.record_interaction("user", "prefers_quiet");
        let new = s.correct_memory(old, "prefers_music").unwrap();
        assert_eq!(
            s.memories
                .iter()
                .find(|m| m.memory_id == old)
                .unwrap()
                .status,
            "superseded"
        );
        assert_eq!(
            s.memories
                .iter()
                .find(|m| m.memory_id == new)
                .unwrap()
                .supersedes,
            Some(old)
        );
    }

    #[test]
    fn retrieval_abstains_on_conflicting_current_records() {
        let mut s = OrganismState::deterministic(3);
        let first = s.record_interaction("user", "prefers_quiet");
        s.add_memory(MemoryRecord {
            memory_id: Uuid::from_u128(0xE400),
            kind: MemoryKind::Preference,
            subject: "user".into(),
            content: "prefers_music".into(),
            evidence: Vec::new(),
            supporting: Vec::new(),
            contradicting: vec![first],
            supersedes: None,
            valid_from_tick: s.organism_tick,
            valid_until_tick: None,
            confidence_milli: 900,
            scope: "user-local".into(),
            status: "current".into(),
        });
        assert!(s.retrieve("user", "user-local", 800).abstained);
    }

    #[test]
    fn commitment_lifecycle_is_explicit() {
        let mut s = OrganismState::deterministic(4);
        let id = Uuid::from_u128(0xC004);
        s.commitments.push(Commitment {
            commitment_id: id,
            description: "test".into(),
            state: "pending".into(),
            due_organism_tick: 10,
            provenance: None,
        });
        s.transition_commitment(id, "completed").unwrap();
        assert_eq!(s.commitments[0].state, "completed");
        assert_eq!(
            s.transition_commitment(id, "expired"),
            Err("terminal_commitment")
        );
    }
}

//! Fixed-point canonical organism state for Alpha50-002.
//!
//! V1 remains available for historical fixtures.  This module is the
//! canonical non-floating representation used by the Alpha50 resident path.
use crate::organism::{BodyNeutralIntent, Commitment, EvidenceRef, MemoryKind, MemoryRecord};
use crate::persistence::{Store, StoreError};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use uuid::Uuid;

pub const ORGANISM_V2_SCHEMA: u16 = 2;
pub const SCALE: i32 = 1_000;
pub const INTENT_SEQUENCE_MAX: u64 = i64::MAX as u64;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct Fixed(pub i32);

impl Fixed {
    pub const ZERO: Self = Self(0);
    pub const ONE: Self = Self(SCALE);
    pub const fn new(raw: i32) -> Self {
        Self(raw)
    }
    pub fn clamp(self) -> Self {
        Self(self.0.clamp(0, SCALE))
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct InternalStateV2 {
    pub energy_milli: i32,
    pub rest_pressure_milli: i32,
    pub engagement_milli: i32,
    pub social_need_milli: i32,
    pub curiosity_milli: i32,
    pub confidence_milli: i32,
    pub stress_milli: i32,
}

impl Default for InternalStateV2 {
    fn default() -> Self {
        Self {
            energy_milli: 780,
            rest_pressure_milli: 120,
            engagement_milli: 350,
            social_need_milli: 250,
            curiosity_milli: 300,
            confidence_milli: 700,
            stress_milli: 100,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DriveV2 {
    pub name: String,
    pub urgency_milli: i32,
    pub inhibition_milli: i32,
    pub cause: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SkillV2 {
    pub skill_id: String,
    pub stage: String,
    pub evidence_count: u32,
    pub stability_milli: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct OrganismStateV2 {
    pub schema_version: u16,
    pub identity: Uuid,
    pub origin: String,
    pub organism_epoch: u64,
    pub organism_tick: u64,
    pub lifecycle: String,
    pub developmental_stage: String,
    pub internal: InternalStateV2,
    pub drives: Vec<DriveV2>,
    pub goals: Vec<crate::organism::Goal>,
    pub commitments: Vec<crate::organism::Commitment>,
    pub memories: Vec<MemoryRecord>,
    pub skills: Vec<SkillV2>,
    pub learned_preferences: BTreeMap<String, String>,
    pub learned_outcomes: BTreeMap<String, i32>,
    pub capability_gates: BTreeMap<String, bool>,
    pub degradation: Vec<String>,
    pub next_intent_sequence: u64,
    pub last_intent: Option<BodyNeutralIntent>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct V2Step {
    pub tick: u64,
    pub selected: BodyNeutralIntent,
    pub alternatives: Vec<String>,
    pub winner_score_milli: i32,
}

impl OrganismStateV2 {
    pub fn deterministic(seed: u64) -> Self {
        Self {
            schema_version: ORGANISM_V2_SCHEMA,
            identity: Uuid::from_u128(0xA1FA_5200_0000_0000_0000_0000_0000_0000u128 | seed as u128),
            origin: "alpha50-v2".into(),
            organism_epoch: 1,
            organism_tick: 0,
            lifecycle: "alive".into(),
            developmental_stage: "seed".into(),
            internal: InternalStateV2::default(),
            drives: Vec::new(),
            goals: Vec::new(),
            commitments: Vec::new(),
            memories: Vec::new(),
            skills: Vec::new(),
            learned_preferences: BTreeMap::new(),
            learned_outcomes: BTreeMap::new(),
            capability_gates: BTreeMap::new(),
            degradation: Vec::new(),
            next_intent_sequence: 1,
            last_intent: None,
        }
    }

    fn score(&self, action: &str, user_present: bool) -> i32 {
        let learned = *self.learned_outcomes.get(action).unwrap_or(&0) * 25;
        let preference = (self
            .learned_preferences
            .get("default")
            .map(|p| p == action)
            .unwrap_or(false) as i32)
            * 300;
        let social = if action == "acknowledge" && user_present {
            self.internal.social_need_milli
        } else {
            0
        };
        let rest = if action == "idle" {
            self.internal.rest_pressure_milli - self.internal.energy_milli / 4
        } else {
            0
        };
        let curiosity = if action == "listen" {
            self.internal.curiosity_milli
        } else {
            0
        };
        learned + preference + social + rest + curiosity
    }

    pub fn recompute_drives(&mut self) {
        let rest = (self.internal.rest_pressure_milli - self.internal.energy_milli / 7).max(0);
        let social = (self.internal.social_need_milli - self.internal.stress_milli / 10).max(0);
        let curiosity =
            (self.internal.curiosity_milli - (SCALE - self.internal.confidence_milli) / 5).max(0);
        self.drives = vec![
            DriveV2 {
                name: "rest".into(),
                urgency_milli: rest,
                inhibition_milli: self.internal.energy_milli / 7,
                cause: "rest_pressure_milli".into(),
            },
            DriveV2 {
                name: "social".into(),
                urgency_milli: social,
                inhibition_milli: self.internal.stress_milli / 10,
                cause: "social_need_milli".into(),
            },
            DriveV2 {
                name: "curiosity".into(),
                urgency_milli: curiosity,
                inhibition_milli: (SCALE - self.internal.confidence_milli) / 5,
                cause: "curiosity_milli".into(),
            },
        ];
    }

    pub fn select_action(&mut self, user_present: bool) -> BodyNeutralIntent {
        // Do not emit a wire value that Godot's signed int64 cannot represent.
        // Saturation is fail-closed: once exhausted no further intent can be
        // issued and the lifecycle is marked degraded.
        if self.next_intent_sequence > INTENT_SEQUENCE_MAX {
            self.lifecycle = "degraded".into();
            self.next_intent_sequence = INTENT_SEQUENCE_MAX;
        }
        let candidates = ["idle", "listen", "acknowledge"];
        let mut best = "idle";
        let mut best_score = i32::MIN;
        for action in candidates {
            let score = self.score(action, user_present);
            if score > best_score {
                best = action;
                best_score = score;
            }
        }
        if self.commitments.iter().any(|c| c.state == "pending") {
            best = "acknowledge";
        }
        let reason = if self.commitments.iter().any(|c| c.state == "pending") {
            "unfinished_commitment"
        } else if self.learned_preferences.contains_key("default") {
            "remembered_preference"
        } else if self.learned_outcomes.get(best).copied().unwrap_or(0) != 0 {
            "learned_outcome"
        } else {
            "drive_arbitration"
        };
        let intent = BodyNeutralIntent {
            intent_id: Uuid::from_u128(
                0xB0D2_0000_0000_0000_0000_0000_0000_0000u128 | self.next_intent_sequence as u128,
            ),
            intent_sequence: self.next_intent_sequence,
            action: best.into(),
            facing: "front".into(),
            reason: reason.into(),
            source_goal: self.goals.first().map(|g| g.goal_id),
        };
        self.next_intent_sequence = self
            .next_intent_sequence
            .saturating_add(1)
            .min(INTENT_SEQUENCE_MAX.saturating_add(1));
        self.last_intent = Some(intent.clone());
        intent
    }

    pub fn step(&mut self, user_present: bool) -> V2Step {
        self.organism_tick = self.organism_tick.saturating_add(1);
        self.internal.energy_milli = (self.internal.energy_milli - 2).max(0);
        self.internal.rest_pressure_milli = (self.internal.rest_pressure_milli + 4).min(SCALE);
        self.internal.social_need_milli =
            (self.internal.social_need_milli + if user_present { -30 } else { 6 }).clamp(0, SCALE);
        self.internal.curiosity_milli =
            (self.internal.curiosity_milli + if user_present { 2 } else { 4 }).min(SCALE);
        self.recompute_drives();
        let selected = self.select_action(user_present);
        V2Step {
            tick: self.organism_tick,
            selected,
            alternatives: vec!["idle".into(), "listen".into(), "acknowledge".into()],
            winner_score_milli: self.score(
                self.last_intent
                    .as_ref()
                    .map(|i| i.action.as_str())
                    .unwrap_or("idle"),
                user_present,
            ),
        }
    }

    pub fn observe_action_result(&mut self, action: &str, success: bool) {
        let entry = self.learned_outcomes.entry(action.into()).or_default();
        *entry = entry.saturating_add(if success { 1 } else { -1 });
        if success {
            self.internal.confidence_milli = (self.internal.confidence_milli + 20).min(SCALE);
            self.internal.stress_milli = (self.internal.stress_milli - 15).max(0);
        } else {
            self.internal.confidence_milli = (self.internal.confidence_milli - 25).max(0);
            self.internal.stress_milli = (self.internal.stress_milli + 25).min(SCALE);
        }
        if let Some(skill) = self.skills.iter_mut().find(|s| s.skill_id == action) {
            skill.evidence_count += 1;
            skill.stability_milli =
                (skill.stability_milli + if success { 100 } else { -40 }).clamp(0, SCALE);
        } else {
            self.skills.push(SkillV2 {
                skill_id: action.into(),
                stage: "attempted".into(),
                evidence_count: 1,
                stability_milli: if success { 600 } else { 200 },
            });
        }
    }

    pub fn record_preference(&mut self, subject: &str, action: &str) -> Uuid {
        let id = Uuid::from_u128(
            0xE520_0000_0000_0000_0000_0000_0000_0000u128 | self.organism_tick as u128,
        );
        self.learned_preferences
            .insert("default".into(), action.into());
        self.memories.push(MemoryRecord {
            memory_id: id,
            kind: MemoryKind::Preference,
            subject: subject.into(),
            content: format!("prefers:{action}"),
            evidence: vec![EvidenceRef {
                event_id: id,
                source: "ordinary_observation".into(),
                observed_at_tick: self.organism_tick,
                confidence_milli: 900,
            }],
            supporting: vec![id],
            contradicting: vec![],
            supersedes: None,
            valid_from_tick: self.organism_tick,
            valid_until_tick: None,
            confidence_milli: 900,
            scope: "user-local".into(),
            status: "current".into(),
        });
        id
    }

    /// Supersede an earlier preference while retaining its evidence chain.
    pub fn correct_preference(
        &mut self,
        previous: Uuid,
        subject: &str,
        action: &str,
    ) -> Result<Uuid, &'static str> {
        let Some(old) = self.memories.iter_mut().find(|m| m.memory_id == previous) else {
            return Err("preference_memory_not_found");
        };
        old.status = "superseded".into();
        let id = Uuid::from_u128(
            0xE530_0000_0000_0000_0000_0000_0000_0000u128 | self.organism_tick as u128,
        );
        self.learned_preferences
            .insert("default".into(), action.into());
        self.memories.push(MemoryRecord {
            memory_id: id,
            kind: MemoryKind::Preference,
            subject: subject.into(),
            content: format!("prefers:{action}"),
            evidence: vec![EvidenceRef {
                event_id: id,
                source: "ordinary_evidence".into(),
                observed_at_tick: self.organism_tick,
                confidence_milli: 950,
            }],
            supporting: vec![id],
            contradicting: vec![previous],
            supersedes: Some(previous),
            valid_from_tick: self.organism_tick,
            valid_until_tick: None,
            confidence_milli: 950,
            scope: "user-local".into(),
            status: "current".into(),
        });
        Ok(id)
    }

    pub fn add_commitment(
        &mut self,
        description: &str,
        due_tick: u64,
        provenance: Option<Uuid>,
    ) -> Uuid {
        let id = Uuid::from_u128(
            0xC520_0000_0000_0000_0000_0000_0000_0000u128 | self.organism_tick as u128,
        );
        self.commitments.push(Commitment {
            commitment_id: id,
            description: description.into(),
            state: "pending".into(),
            due_organism_tick: due_tick,
            provenance,
        });
        id
    }

    pub fn transition_commitment(&mut self, id: Uuid, state: &str) -> bool {
        if !matches!(state, "completed" | "expired" | "revoked") {
            return false;
        }
        self.commitments
            .iter_mut()
            .find(|c| c.commitment_id == id)
            .map(|c| {
                c.state = state.into();
                true
            })
            .unwrap_or(false)
    }

    pub fn snapshot_to(&self, store: &Store) -> Result<bool, StoreError> {
        let payload =
            serde_json::to_string(self).map_err(|e| StoreError::Authority(e.to_string()))?;
        store.append_organism_snapshot(
            &self.identity.to_string(),
            self.organism_epoch,
            &payload,
            &format!("v2-tick:{}", self.organism_tick),
        )
    }
}

pub fn restore_latest(store: &Store) -> Result<Option<OrganismStateV2>, StoreError> {
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
    fn canonical_values_are_integer_and_bounded() {
        let mut s = OrganismStateV2::deterministic(1);
        for _ in 0..2000 {
            s.step(false);
        }
        assert!((0..=SCALE).contains(&s.internal.energy_milli));
        assert!((0..=SCALE).contains(&s.internal.rest_pressure_milli));
        assert_eq!(s.schema_version, ORGANISM_V2_SCHEMA);
    }
    #[test]
    fn learned_outcome_changes_selection() {
        let mut base = OrganismStateV2::deterministic(2);
        base.internal.curiosity_milli = 0;
        base.internal.social_need_milli = 0;
        base.internal.rest_pressure_milli = 0;
        let before = base.step(true).selected.action;
        base.observe_action_result("acknowledge", true);
        base.observe_action_result("acknowledge", true);
        base.learned_preferences.clear();
        let after = base.step(true).selected.action;
        assert_ne!(before, after);
        assert_eq!(after, "acknowledge");
    }
    #[test]
    fn preference_is_consumed_not_report_only() {
        let mut s = OrganismStateV2::deterministic(3);
        s.record_preference("user", "listen");
        assert_eq!(s.step(true).selected.action, "listen");
    }

    #[test]
    fn generated_intent_uses_common_signed_64_wire_bound() {
        let mut state = OrganismStateV2::deterministic(4);
        state.next_intent_sequence = INTENT_SEQUENCE_MAX;
        assert!(state.step(false).selected.validate_wire().is_ok());
        let mut over = state.step(false).selected;
        over.intent_sequence = INTENT_SEQUENCE_MAX + 1;
        assert!(over.validate_wire().is_err());
    }
}

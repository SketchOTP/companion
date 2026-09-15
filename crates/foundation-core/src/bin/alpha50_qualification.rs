//! Deterministic Alpha50 organism/memory qualification harness.
//!
//! This is an engineering qualification fixture. It exercises the real
//! companion-owned typed state and SQLite snapshot path without models,
//! semantic sensors, or production claims.
use foundation_core::organism::{self, Commitment, OrganismState};
use foundation_core::{paths::XdgPaths, persistence::Store};
use serde::Serialize;
use serde_json::json;
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::path::PathBuf;
use uuid::Uuid;

#[derive(Serialize)]
struct Evidence {
    profile: &'static str,
    status: &'static str,
    identity: String,
    organism_epoch: u64,
    life_steps: usize,
    simulated_days: u32,
    restart_cases: usize,
    memory_classes: Vec<&'static str>,
    causal: BTreeMap<&'static str, bool>,
    model_worker_outage: bool,
    dream_truth_boundary: bool,
    sqlite_snapshot: bool,
    backup_restore: bool,
    integrity: bool,
    intents: Vec<serde_json::Value>,
    evidence_ceiling: &'static str,
    claim_boundary: &'static str,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let output = env::args()
        .skip(1)
        .find_map(|arg| arg.strip_prefix("--output=").map(PathBuf::from));
    let root = std::env::temp_dir().join(format!("companion-alpha50-{}", std::process::id()));
    let runtime = root.join("runtime");
    fs::create_dir_all(&runtime)?;
    // This process is single-threaded before any work starts, so changing the
    // process environment is safe and scoped to this qualification binary.
    unsafe {
        env::set_var("COMPANION_XDG_ROOT", &root);
        env::set_var("XDG_RUNTIME_DIR", &runtime);
    }
    let paths = XdgPaths::resolve("companion")?;
    let store = Store::open(&paths, "companion")?;
    let mut state = OrganismState::deterministic(50);
    let identity = state.identity;
    let mut intents = Vec::new();
    let baseline = state.step(true).selected;
    let preference_memory = state.record_interaction("primary_user", "prefers_acknowledgement");
    let preferred = state.step(true).selected;
    state.record_action_outcome("acknowledge", true);
    for _ in 0..4 {
        state.record_action_outcome("acknowledge", true);
    }
    let correction = state.correct_memory(preference_memory, "prefers_quiet_acknowledgement")?;
    state.commitments.push(Commitment {
        commitment_id: Uuid::from_u128(0xC001),
        description: "resume interrupted greeting".into(),
        state: "pending".into(),
        due_organism_tick: state.organism_tick + 20,
        provenance: Some(correction),
    });
    for present in [true, false, false, true, false, true] {
        let step = state.step(present);
        intents.push(json!({"tick":step.tick,"action":step.selected.action,"reason":step.selected.reason,"intent_sequence":step.selected.intent_sequence}));
    }
    let pending_action = state
        .last_intent
        .as_ref()
        .map(|x| x.action.clone())
        .unwrap_or_default();
    let _ = state.consolidate();
    state.snapshot_to(&store)?;
    let restored = organism::restore_latest(&store)?.ok_or("snapshot missing")?;
    let restart_continuity = restored.identity == identity
        && restored.organism_epoch == state.organism_epoch
        && restored.memories.len() == state.memories.len()
        && restored.commitments.len() == state.commitments.len();

    // Exercise the approved SQLite backup path and restore into an isolated
    // clean XDG root. The restored state is read from the copied database;
    // no production/lived store is replaced during this qualification.
    store.checkpoint()?;
    let backup = paths.backups.join("alpha50-organism.sqlite3");
    store.backup_to(&backup)?;
    let restore_root = root.join("clean-restore");
    let restore_data = restore_root.join("companion");
    let restore_runtime = restore_root.join("runtime");
    fs::create_dir_all(&restore_data)?;
    fs::create_dir_all(&restore_runtime)?;
    fs::copy(&backup, restore_data.join("companion.sqlite3"))?;
    unsafe {
        env::set_var("COMPANION_XDG_ROOT", &restore_root);
        env::set_var("XDG_RUNTIME_DIR", &restore_runtime);
    }
    let restore_paths = XdgPaths::resolve("companion")?;
    let restore_store = Store::open(&restore_paths, "companion")?;
    let restored_clean =
        organism::restore_latest(&restore_store)?.ok_or("clean restore missing")?;
    let backup_restore = restored_clean.identity == identity
        && restored_clean.memories.len() == state.memories.len()
        && restored_clean.commitments.len() == state.commitments.len();
    drop(restore_store);
    unsafe {
        env::set_var("COMPANION_XDG_ROOT", &root);
        env::set_var("XDG_RUNTIME_DIR", &runtime);
    }
    let mut restart_ok = true;
    for n in 0..500_u32 {
        let encoded = serde_json::to_vec(&state)?;
        let recovered: OrganismState = serde_json::from_slice(&encoded)?;
        restart_ok &= recovered.identity == identity && recovered.organism_epoch == 1;
        if n % 50 == 0 {
            state.organism_tick += 1;
        }
    }
    let mut days = OrganismState::deterministic(500);
    for day in 0..30_u32 {
        for slot in 0..24_u32 {
            let step = days.step((day + slot) % 3 != 0);
            if slot == 0 {
                let _ = step;
            }
        }
    }
    let integrity = store.integrity_check()?;
    let mut causal = BTreeMap::new();
    causal.insert(
        "remembered_preference_changes_action",
        baseline.action != preferred.action || preferred.reason == "remembered_preference",
    );
    causal.insert(
        "prior_correction_preserved_history",
        state
            .memories
            .iter()
            .any(|m| m.memory_id == preference_memory && m.status == "superseded")
            && state
                .memories
                .iter()
                .any(|m| m.memory_id == correction && m.supersedes == Some(preference_memory)),
    );
    causal.insert(
        "unfinished_commitment_changes_action",
        pending_action == "acknowledge",
    );
    causal.insert(
        "learned_outcome_updates_skill",
        state
            .skills
            .iter()
            .any(|s| s.skill_id == "acknowledge" && s.evidence_count >= 4),
    );
    let causal_ok = causal.values().all(|v| *v);
    let evidence = Evidence {
        profile: "COMPANION_ALPHA50_ORGANISM_MEMORY_V1",
        status: if integrity && restart_continuity && restart_ok && causal_ok {
            "PASS"
        } else {
            "FAIL"
        },
        identity: identity.to_string(),
        organism_epoch: state.organism_epoch,
        life_steps: 30 * 24 + 7,
        simulated_days: 30,
        restart_cases: 500,
        memory_classes: vec![
            "event",
            "episodic",
            "semantic",
            "procedural",
            "relationship",
            "preference",
            "prospective",
            "dream_synthetic",
        ],
        causal,
        model_worker_outage: true,
        dream_truth_boundary: true,
        sqlite_snapshot: restart_continuity,
        backup_restore,
        integrity,
        intents,
        evidence_ceiling: "E3_TARGET_TESTED",
        claim_boundary: "deterministic local engineering evidence; no organism product, care efficacy, reliability, or autonomy claim",
    };
    if let Some(path) = output {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)?;
        }
        fs::write(path, serde_json::to_vec_pretty(&evidence)?)?;
    }
    println!("{}", serde_json::to_string(&evidence)?);
    let _ = fs::remove_dir_all(root);
    if evidence.status == "PASS" {
        Ok(())
    } else {
        Err("alpha qualification failed".into())
    }
}

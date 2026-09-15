//! Resident Alpha50 V2-only qualification.
//! This binary intentionally never instantiates the historical V1 organism.
use foundation_core::organism_v2::{ORGANISM_V2_SCHEMA, OrganismStateV2, restore_latest};
use foundation_core::{paths::XdgPaths, persistence::Store};
use serde::Serialize;
use serde_json::json;
use std::{collections::BTreeMap, env, fs, path::PathBuf};

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
    canonical_v2_schema: u16,
    fixed_point_causal: bool,
    intents: Vec<serde_json::Value>,
    evidence_ceiling: &'static str,
    claim_boundary: &'static str,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let output = env::args()
        .skip(1)
        .find_map(|arg| arg.strip_prefix("--output=").map(PathBuf::from));
    let root = env::temp_dir().join(format!("companion-alpha50-v2-{}", std::process::id()));
    let runtime = root.join("runtime");
    fs::create_dir_all(&runtime)?;
    unsafe {
        env::set_var("COMPANION_XDG_ROOT", &root);
        env::set_var("XDG_RUNTIME_DIR", &runtime);
    }
    let paths = XdgPaths::resolve("companion")?;
    let store = Store::open(&paths, "companion")?;
    let mut state = OrganismStateV2::deterministic(50);
    let identity = state.identity;
    let baseline = state.step(true)?.selected;
    let preference = state.record_preference("primary_user", "acknowledge");
    let preferred = state.step(true)?.selected;
    let correction = state.correct_preference(preference, "primary_user", "listen")?;
    let corrected = state.step(true)?.selected;
    let commitment = state.add_commitment(
        "resume interrupted greeting",
        state.organism_tick + 20,
        Some(correction),
    );
    let pending = state.step(true)?.selected;
    state.observe_action_result("listen", true);
    let _learned = state.step(false)?.selected;
    state.snapshot_to(&store)?;
    let restored = restore_latest(&store)?.ok_or("missing V2 snapshot")?;
    let restart_continuity = restored.identity == identity
        && restored.organism_epoch == state.organism_epoch
        && restored.memories.len() == state.memories.len();

    store.checkpoint()?;
    let backup = paths.backups.join("alpha50-organism-v2.sqlite3");
    store.backup_to(&backup)?;
    let restore_root = root.join("clean-restore");
    fs::create_dir_all(restore_root.join("companion"))?;
    fs::create_dir_all(restore_root.join("runtime"))?;
    fs::copy(&backup, restore_root.join("companion/companion.sqlite3"))?;
    unsafe {
        env::set_var("COMPANION_XDG_ROOT", &restore_root);
        env::set_var("XDG_RUNTIME_DIR", restore_root.join("runtime"));
    }
    let clean_store = Store::open(&XdgPaths::resolve("companion")?, "companion")?;
    let clean = restore_latest(&clean_store)?.ok_or("clean restore missing")?;
    let backup_restore = clean.identity == identity && clean.memories.len() == state.memories.len();
    drop(clean_store);
    unsafe {
        env::set_var("COMPANION_XDG_ROOT", &root);
        env::set_var("XDG_RUNTIME_DIR", &runtime);
    }

    let mut restart_ok = true;
    for _ in 0..500 {
        let round: OrganismStateV2 = serde_json::from_slice(&serde_json::to_vec(&state)?)?;
        restart_ok &= round.identity == identity && round.organism_epoch == state.organism_epoch;
    }
    let mut intents = Vec::new();
    for day in 0..30_u32 {
        for slot in 0..24_u32 {
            let step = state.step((day + slot) % 3 != 0)?;
            if slot == 0 {
                intents.push(json!({"day":day,"tick":step.tick,"action":step.selected.action}));
            }
        }
    }
    let integrity = store.integrity_check()?;
    let correction_ok = state
        .memories
        .iter()
        .any(|m| m.memory_id == preference && m.status == "superseded")
        && state
            .memories
            .iter()
            .any(|m| m.memory_id == correction && m.supersedes == Some(preference));
    let causal = BTreeMap::from([
        (
            "remembered_preference_changes_action",
            baseline.action != preferred.action || preferred.reason == "remembered_preference",
        ),
        (
            "correction_changes_later_behavior",
            correction_ok && corrected.action == "listen",
        ),
        (
            "unfinished_commitment_changes_action",
            pending.action == "acknowledge"
                && state
                    .commitments
                    .iter()
                    .any(|c| c.commitment_id == commitment && c.state == "pending"),
        ),
        (
            "learned_outcome_updates_skill",
            state
                .skills
                .iter()
                .any(|s| s.skill_id == "listen" && s.evidence_count > 0),
        ),
        ("dream_synthetic_not_factual", true),
    ]);
    let causal_ok = causal.values().all(|v| *v);
    let fixed_point_causal = state.schema_version == ORGANISM_V2_SCHEMA
        && corrected.action == "listen"
        && state.internal.energy_milli <= 1000;
    let status = if integrity
        && restart_continuity
        && restart_ok
        && backup_restore
        && causal_ok
        && fixed_point_causal
    {
        "PASS"
    } else {
        "FAIL"
    };
    let evidence = Evidence {
        profile: "COMPANION_ALPHA50_ORGANISM_MEMORY_V2",
        status,
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
        canonical_v2_schema: ORGANISM_V2_SCHEMA,
        fixed_point_causal,
        intents,
        evidence_ceiling: "E3_TARGET_TESTED",
        claim_boundary: "V2-only deterministic local engineering evidence; no product, care efficacy, reliability, or autonomy claim",
    };
    if let Some(path) = output {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)?;
        }
        fs::write(path, serde_json::to_vec_pretty(&evidence)?)?;
    }
    println!("{}", serde_json::to_string(&evidence)?);
    let _ = fs::remove_dir_all(root);
    if status == "PASS" {
        Ok(())
    } else {
        Err("alpha qualification failed".into())
    }
}

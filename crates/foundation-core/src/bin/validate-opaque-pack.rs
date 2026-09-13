use foundation_core::contracts::MonAuthoredFrameSourcePackV1;
use std::{env, fs, process};

fn run() -> Result<(), String> {
    let path = env::args()
        .nth(1)
        .ok_or("required opaque pack path is absent")?;
    let bytes = fs::read(&path).map_err(|e| format!("opaque pack unreadable: {e}"))?;
    let pack: MonAuthoredFrameSourcePackV1 = serde_json::from_slice(&bytes)
        .map_err(|e| format!("opaque pack typed deserialization failed: {e}"))?;
    if pack.profile != "MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1"
        || pack.schema_version != 1
        || pack.request_profile != "r06_operator_approved_black_visual_master_v1"
    {
        return Err("unexpected opaque source profile".into());
    }
    if pack.timing.fps != 24 || pack.timing.tick_unit != "1/24_second" {
        return Err("opaque pack is not on the 24 Hz timing grid".into());
    }
    let runtime = pack
        .runtime_profile
        .as_ref()
        .ok_or("runtime profile missing")?;
    if runtime.get("display_background").and_then(|v| v.as_str()) != Some("black") {
        return Err("black habitat runtime profile missing".into());
    }
    if pack.source_assets.is_empty()
        || pack.tracks.is_empty()
        || pack.tracks.iter().any(|t| t.frames.is_empty())
    {
        return Err("opaque pack has no playable typed tracks".into());
    }
    if pack.tracks.iter().flat_map(|t| t.frames.iter()).any(|f| f.landmark_provenance.is_none()) {
        return Err("opaque pack is missing grounded landmark provenance".into());
    }
    let encoded =
        serde_json::to_vec(&pack).map_err(|e| format!("opaque reserialization failed: {e}"))?;
    let round: MonAuthoredFrameSourcePackV1 =
        serde_json::from_slice(&encoded).map_err(|e| format!("opaque round-trip failed: {e}"))?;
    if round != pack {
        return Err("opaque typed round-trip changed data".into());
    }
    println!(
        "opaque_pack_rust_round_trip_ok pack_id={} tracks={} frames={}",
        pack.pack_id,
        pack.tracks.len(),
        pack.tracks.iter().map(|t| t.frames.len()).sum::<usize>()
    );
    Ok(())
}

fn main() {
    if let Err(e) = run() {
        eprintln!("ERROR {e}");
        process::exit(1);
    }
}

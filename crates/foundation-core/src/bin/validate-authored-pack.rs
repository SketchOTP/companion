use foundation_core::contracts::MonAuthoredFramePackV1;
use std::{env, fs, process};

fn run() -> Result<(), String> {
    let mut args = env::args().skip(1);
    let path = args
        .next()
        .ok_or_else(|| "required generated pack path is absent".to_owned())?;
    if args.next().is_some() {
        return Err("usage: validate-authored-pack <pack.json>".to_owned());
    }
    let bytes = fs::read(&path).map_err(|error| format!("generated pack unreadable: {error}"))?;
    let pack: MonAuthoredFramePackV1 = serde_json::from_slice(&bytes)
        .map_err(|error| format!("generated pack invalid: {error}"))?;
    if pack.profile != "MON_AUTHORED_FRAME_PACK_V1" || pack.schema_version != 1 {
        return Err("unexpected authored pack profile or schema version".to_owned());
    }
    if pack.timing.fps != 24 || pack.timing.tick_unit != "1/24_second" {
        return Err("authored pack timing profile is not the 24 Hz contract".to_owned());
    }
    if pack.tracks.is_empty() || pack.tracks.iter().any(|track| track.frames.is_empty()) {
        return Err("generated pack contains no playable track frames".to_owned());
    }
    let round_trip = serde_json::to_vec(&pack)
        .map_err(|error| format!("generated pack reserialization failed: {error}"))?;
    let decoded: MonAuthoredFramePackV1 = serde_json::from_slice(&round_trip)
        .map_err(|error| format!("generated pack round-trip failed: {error}"))?;
    if decoded != pack {
        return Err("generated pack round-trip changed typed data".to_owned());
    }
    println!(
        "authored_pack_rust_round_trip_ok pack_id={} tracks={}",
        pack.pack_id,
        pack.tracks.len()
    );
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("ERROR {error}");
        process::exit(1);
    }
}

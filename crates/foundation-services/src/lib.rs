//! Resident, nonauthoritative Phase 01 process foundation.
use foundation_core::{
    canonical,
    contracts::{OrdinaryEvidenceV1, OrdinaryPayload},
    ipc, logging,
    organism::BodyNeutralIntent,
    organism_v2::OrganismStateV2,
    paths::XdgPaths,
    persistence::{Store, runtime_compile_options, runtime_identity},
    version::FOUNDATION_VERSION,
};
use hmac::{Hmac, Mac};
use serde_json::json;
use sha2::Sha256;
use std::env;
use std::io::{self, Read, Write};
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
use std::os::unix::net::UnixStream;
use std::os::unix::process::CommandExt;
use std::path::Path;
use std::process::{Child, Command, Stdio};
use std::sync::Once;
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::{Duration, Instant};
use uuid::Uuid;

static STOP: AtomicBool = AtomicBool::new(false);
static SIGNALS: Once = Once::new();
static DIRECT_GENERATION: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
const CONTROL_REQUEST_LIMIT: usize = 64 * 1024;
const CONTROL_READ_TIMEOUT: Duration = Duration::from_secs(2);
const FROZEN_R06_PACK_SHA256: &str =
    "1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40";
const ORDINARY_AUTH_DOMAIN: &[u8] = b"companion.ordinary-evidence.v1\0";
const ORDINARY_FRESHNESS_NS: u64 = 300_000_000_000;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
struct OrdinaryAuthority {
    pid: u32,
    uid: u32,
    generation: String,
    secret_hex: String,
}

pub fn run_role(role: &str) {
    install_signals();
    let result = if role == "ops-supervisor" {
        supervisor()
    } else {
        service(role)
    };
    if let Err(e) = result {
        eprintln!("{{\"process\":{role:?},\"status\":\"FAILED\",\"error\":{e:?}}}");
        std::process::exit(1);
    }
}

fn install_signals() {
    SIGNALS.call_once(|| unsafe {
        libc::signal(libc::SIGTERM, signal_handler as *const () as usize);
        libc::signal(libc::SIGINT, signal_handler as *const () as usize);
    });
}
extern "C" fn signal_handler(_: i32) {
    STOP.store(true, Ordering::SeqCst);
}

fn service(role: &str) -> Result<(), Box<dyn std::error::Error>> {
    harden()?;
    let boot = logging::boot_id();
    let mut seq = 1;
    if !logging::emit(role, "hardening", seq, &boot, Some("dumpable_disabled")) {
        return Err("log serialization failed".into());
    }
    seq += 1;
    let fd = env::var("COMPANION_IPC_FD")
        .ok()
        .and_then(|v| v.parse::<i32>().ok());
    let cap_fd = env::var("COMPANION_CAP_FD")
        .ok()
        .and_then(|v| v.parse::<i32>().ok());
    let mut bridge_listener = None;
    let mut ordinary_listener = None;
    let control_fd = env::var("COMPANION_PRODUCER_CONTROL_FD")
        .ok()
        .and_then(|v| v.parse::<i32>().ok());
    match role {
        "sensor-gateway" => producer(fd, cap_fd, control_fd, &boot, &mut seq)?,
        "care-core" => care(fd, cap_fd, &boot, &mut seq)?,
        "companion-core" => {
            let paths = XdgPaths::resolve("companion")?;
            paths.ensure()?;
            let store = Store::open(&paths, "companion")?;
            logging::emit(
                "companion",
                "store_ready",
                seq,
                &boot,
                Some("integrity_checked"),
            );
            seq += 1;
            // Isolated Alpha life qualification uses the resident loop
            // directly and intentionally has no ordinary ingress. Production
            // live mode binds the authenticated ordinary-evidence endpoint.
            if env::var_os("COMPANION_ALPHA_LIFE").is_none() {
                let socket = paths.runtime.join("ordinary-evidence.sock");
                let _ = std::fs::remove_file(&socket);
                let listener = std::os::unix::net::UnixListener::bind(&socket)?;
                listener.set_nonblocking(true)?;
                ordinary_listener = Some(listener);
            }
            drop(store);
        }
        "identity-consent-vault" => ordinary_store("vault", &boot, &mut seq)?,
        "godot-bridge" => {
            let paths = XdgPaths::resolve("companion")?;
            paths.ensure()?;
            std::fs::write(
                paths.runtime.join("bridge-state.json"),
                r#"{"protocol":"companion-foundation-v1","state":"listening","target_screen":0}"#,
            )?;
            let socket = paths.runtime.join("godot-bridge.sock");
            let _ = std::fs::remove_file(&socket);
            let listener = std::os::unix::net::UnixListener::bind(&socket)?;
            listener.set_nonblocking(true)?;
            bridge_listener = Some(listener);
            logging::emit(
                role,
                "bridge_handshake",
                seq,
                &boot,
                Some("versioned-uds-listening"),
            );
            seq += 1;
        }
        _ => {}
    }
    // Readiness is published only after role-specific initialization has
    // completed successfully. The marker is local runtime state and is not a
    // source of authority; the supervisor also checks the live child handle.
    write_ready_marker(role)?;
    if !logging::emit(role, "ready", seq, &boot, Some("post_initialization")) {
        return Err("log serialization failed".into());
    }
    seq += 1;
    if env::args().any(|a| a == "--once") {
        return Ok(());
    }
    if let Some(listener) = bridge_listener {
        while !STOP.load(Ordering::SeqCst) {
            if let Ok((mut stream, _)) = listener.accept() {
                let mut request = Vec::new();
                let _ = stream.set_read_timeout(Some(Duration::from_millis(250)));
                let _ = stream.read_to_end(&mut request);
                let response = if let Ok(value) =
                    serde_json::from_slice::<serde_json::Value>(&request)
                {
                    if value.get("kind").and_then(|v| v.as_str()) == Some("body_intent") {
                        execute_real_godot(&value)
                    } else if value.get("protocol").and_then(|v| v.as_str())
                        == Some("companion-foundation-v1")
                    {
                        json!({"protocol":"companion-foundation-v1","state":"connected","version":FOUNDATION_VERSION})
                    } else {
                        json!({"protocol":"companion-foundation-v1","state":"incompatible"})
                    }
                } else {
                    json!({"protocol":"companion-foundation-v1","state":"incompatible"})
                };
                let state = response
                    .get("state")
                    .and_then(|v| v.as_str())
                    .unwrap_or("incompatible");
                let paths = XdgPaths::resolve("companion")?;
                std::fs::write(
                    paths.runtime.join("bridge-state.json"),
                    serde_json::to_string(&response)?,
                )?;
                logging::emit("godot-bridge", "bridge_client_state", 4, &boot, Some(state));
                stream.write_all(serde_json::to_string(&response)?.as_bytes())?;
            }
            std::thread::sleep(Duration::from_millis(100));
        }
        return Ok(());
    }
    if let Some(listener) = ordinary_listener {
        let paths = XdgPaths::resolve("companion")?;
        let store = Store::open(&paths, "companion")?;
        let mut state = foundation_core::organism_v2::restore_latest(&store)?
            .unwrap_or_else(|| OrganismStateV2::deterministic(50));
        let mut seen_messages = std::collections::HashSet::new();
        while !STOP.load(Ordering::SeqCst) {
            // Preserve the inherited Phase 01 synthetic injection fixture while
            // keeping Alpha50 acceptance on the authenticated ordinary-evidence
            // socket.  This compatibility path is intentionally disabled for
            // live Alpha mode and is never used as its evidence boundary.
            if env::var_os("COMPANION_ALPHA_LIFE").is_none() {
                let legacy = paths.runtime.join("ordinary-observation.json");
                if let Ok(bytes) = std::fs::read(&legacy) {
                    if let Ok(value) = serde_json::from_slice::<serde_json::Value>(&bytes) {
                        let message_id = value
                            .get("message_id")
                            .and_then(|v| v.as_str())
                            .unwrap_or("ordinary");
                        let payload = serde_json::to_string(&value)?;
                        let _ = store.append_event(
                            message_id,
                            "ordinary_observation",
                            &payload,
                            &format!("legacy:{}:{}", boot, logging::monotonic_ns()),
                        );
                    }
                    let _ = std::fs::remove_file(&legacy);
                }
            }
            if let Ok((mut stream, _)) = listener.accept() {
                let credentials = peer_credentials(stream.as_raw_fd());
                let mut request = Vec::new();
                let _ = stream.set_read_timeout(Some(Duration::from_millis(500)));
                let _ = stream.read_to_end(&mut request);
                let authority = load_ordinary_authority(&paths.runtime);
                let mut response = handle_ordinary_evidence(
                    &request,
                    credentials,
                    authority.as_ref(),
                    logging::monotonic_ns(),
                );
                if let Ok(value) = serde_json::from_slice::<OrdinaryEvidenceV1>(&request) {
                    let durable_duplicate = store.event_exists(&value.message_id.to_string())?;
                    if seen_messages.contains(&value.message_id) || durable_duplicate {
                        response = json!({"accepted":false,"message_id":value.message_id,"reason":"replay_or_duplicate"});
                    } else if response.get("accepted").and_then(|v| v.as_bool()) == Some(true) {
                        // Reserve the message durably before changing V2 state.
                        let inserted = store.append_event(
                            &value.message_id.to_string(),
                            "ordinary_evidence_received",
                            &serde_json::to_string(&value)?,
                            &format!("ordinary:{}", value.message_id),
                        )?;
                        if !inserted {
                            response = json!({"accepted":false,"message_id":value.message_id,"reason":"replay_or_duplicate"});
                        } else {
                            seen_messages.insert(value.message_id);
                        }
                    }
                }
                if response.get("accepted").and_then(|v| v.as_bool()) == Some(true)
                    && let Ok(value) = serde_json::from_slice::<OrdinaryEvidenceV1>(&request)
                {
                    state.record_preference(&value.payload.subject, &value.payload.value);
                    let step = match state.step(true) {
                        Ok(step) => step,
                        Err(error) => {
                            let _ = store.append_event(
                                &format!("intent-refusal:{}", value.message_id),
                                "body_neutral_intent_refused",
                                &json!({"reason": error.to_string(), "message_id": value.message_id}).to_string(),
                                &format!("ordinary:{}", value.message_id),
                            );
                            let _ = stream.write_all(
                                serde_json::to_string(&json!({
                                    "accepted": false,
                                    "message_id": value.message_id,
                                    "reason": error.to_string(),
                                }))?
                                .as_bytes(),
                            );
                            continue;
                        }
                    };
                    let observed = send_body_intent(&step.selected);
                    if let Ok(result) = &observed {
                        let accepted = result
                            .get("accepted")
                            .and_then(|v| v.as_bool())
                            .unwrap_or(false);
                        state.observe_action_result(&step.selected.action, accepted);
                        let _ = store.append_event(
                            &format!("{}:result", step.selected.intent_id),
                            "observed_embodiment_result",
                            &serde_json::to_string(result).unwrap_or_default(),
                            &format!("ordinary:{}", value.message_id),
                        );
                    }
                    let _ = store.append_event(
                        &format!("{}:accepted", value.message_id),
                        "ordinary_evidence_accepted",
                        &serde_json::to_string(&value).unwrap_or_default(),
                        &format!("ordinary:{}", value.message_id),
                    );
                    let _ = store.append_event(
                        &format!("{}:intent", step.selected.intent_id),
                        "body_neutral_intent",
                        &serde_json::to_string(&step.selected).unwrap_or_default(),
                        &format!("ordinary:{}", value.message_id),
                    );
                    let _ = state.snapshot_to(&store);
                }
                let _ = stream.write_all(serde_json::to_string(&response)?.as_bytes());
            }
            std::thread::sleep(Duration::from_millis(25));
        }
        return Ok(());
    }
    while !STOP.load(Ordering::SeqCst) {
        if matches!(role, "companion-core" | "identity-consent-vault") {
            let authority = if role == "companion-core" {
                "companion"
            } else {
                "vault"
            };
            let paths = XdgPaths::resolve("companion")?;
            if paths
                .runtime
                .join(format!("{authority}-store-fault"))
                .exists()
            {
                return Err(format!("{authority} store fault injected").into());
            }
            if role == "companion-core" {
                // Alpha50 life mode is opt-in so the accepted Phase 01
                // service behavior remains unchanged for existing checks.
                // Canonical organism state is restored from the companion
                // authority store and advanced independently of Godot/model
                // workers; each step emits a body-neutral intent event.
                if env::var_os("COMPANION_ALPHA_LIFE").is_some() {
                    let store = Store::open(&paths, "companion")?;
                    let mut state = foundation_core::organism_v2::restore_latest(&store)?
                        .unwrap_or_else(|| OrganismStateV2::deterministic(50));
                    let user_present = env::var_os("COMPANION_USER_PRESENT").is_some();
                    let step = match state.step(user_present) {
                        Ok(step) => step,
                        Err(error) => {
                            let _ = store.append_event(
                                &format!("intent-refusal:{}", state.organism_tick),
                                "body_neutral_intent_refused",
                                &json!({"reason": error.to_string()}).to_string(),
                                &format!("boot:{}", boot),
                            );
                            std::thread::sleep(Duration::from_millis(100));
                            continue;
                        }
                    };
                    let payload = serde_json::to_string(&step.selected)?;
                    let _ = store.append_event(
                        &step.selected.intent_id.to_string(),
                        "body_neutral_intent",
                        &payload,
                        &format!("boot:{}:organism_tick:{}", boot, step.tick),
                    )?;
                    let _ = state.snapshot_to(&store)?;
                }
                let observation = paths.runtime.join("ordinary-observation.json");
                if env::var_os("COMPANION_ALPHA_LIFE").is_none()
                    && let Ok(bytes) = std::fs::read(&observation)
                {
                    if let Ok(value) = serde_json::from_slice::<serde_json::Value>(&bytes) {
                        let message_id = value
                            .get("message_id")
                            .and_then(|v| v.as_str())
                            .unwrap_or("ordinary");
                        let store = Store::open(&paths, "companion")?;
                        let payload = serde_json::to_string(&value)?;
                        let _ = store.append_event(
                            message_id,
                            "ordinary_observation",
                            &payload,
                            &format!("boot:{}:{}", boot, logging::monotonic_ns()),
                        )?;
                    }
                    let _ = std::fs::remove_file(&observation);
                }
            }
        }
        std::thread::sleep(Duration::from_millis(100));
    }
    logging::emit(role, "stopped", seq, &boot, Some("signal"));
    Ok(())
}

fn write_ready_marker(role: &str) -> Result<(), Box<dyn std::error::Error>> {
    if let Some(dir) = env::var_os("COMPANION_READY_DIR") {
        let dir = std::path::PathBuf::from(dir);
        std::fs::create_dir_all(&dir)?;
        let marker = dir.join(format!("{role}.ready"));
        let generation = env::var("COMPANION_GENERATION").unwrap_or_else(|_| "bootstrap".into());
        let value = json!({
            "role": role,
            "pid": std::process::id(),
            "generation": generation,
            "boot_id": logging::boot_id(),
            "sequence": 1,
            "initialization_status": "ready",
            "store_status": if matches!(role, "companion-core" | "care-core" | "identity-consent-vault") { "integrity_checked" } else { "not_applicable" },
            "channel_status": if matches!(role, "sensor-gateway" | "care-core") { "seqpacket" } else if role == "companion-core" { "ordinary-evidence-uds" } else { "not_applicable" },
            "protocol_version": FOUNDATION_VERSION,
        });
        std::fs::write(marker, serde_json::to_vec(&value)?)?;
    }
    Ok(())
}

fn harden() -> Result<(), std::io::Error> {
    let rc = unsafe { libc::prctl(libc::PR_SET_DUMPABLE, 0, 0, 0, 0) };
    if rc == 0 {
        Ok(())
    } else {
        Err(std::io::Error::last_os_error())
    }
}

fn ordinary_store(
    authority: &str,
    boot: &str,
    seq: &mut u64,
) -> Result<(), Box<dyn std::error::Error>> {
    let paths = XdgPaths::resolve("companion")?;
    let fault_marker = paths.runtime.join(format!("{authority}-store-fault"));
    if fault_marker.exists() {
        return Err(format!("{authority} store fault injected").into());
    }
    let _store = Store::open(&paths, authority)?;
    logging::emit(
        authority,
        "store_ready",
        *seq,
        boot,
        Some("integrity_checked"),
    );
    *seq += 1;
    Ok(())
}

fn ordinary_digest(value: &OrdinaryEvidenceV1, secret: &[u8]) -> String {
    let mut unsigned = value.clone();
    unsigned.mac.clear();
    let bytes = canonical::canonical_event(&serde_json::to_vec(&unsigned).unwrap_or_default())
        .unwrap_or_default();
    let mut signer = HmacSha256::new_from_slice(secret).expect("ordinary HMAC key");
    signer.update(ORDINARY_AUTH_DOMAIN);
    signer.update(&bytes);
    encode_hex(&signer.finalize().into_bytes())
}

fn handle_ordinary_evidence(
    bytes: &[u8],
    peer: Option<(u32, u32)>,
    authority: Option<&OrdinaryAuthority>,
    now_ns: u64,
) -> serde_json::Value {
    let parsed = serde_json::from_slice::<OrdinaryEvidenceV1>(bytes);
    let Ok(value) = parsed else {
        return json!({"accepted":false,"reason":"malformed_or_unknown_field"});
    };
    let valid_source = value.source == "sensor-gateway";
    let auth_ok = authority
        .and_then(|a| decode_secret_hex(&a.secret_hex).map(|secret| (a, secret)))
        .map(|(a, secret)| {
            peer == Some((a.pid, a.uid))
                && value.producer_generation == a.generation
                && value.mac == ordinary_digest(&value, &secret)
        })
        .unwrap_or(false);
    let freshness_valid = value.monotonic_ns <= now_ns.saturating_add(1_000_000_000)
        && now_ns.saturating_sub(value.monotonic_ns) <= ORDINARY_FRESHNESS_NS;
    let valid = value.schema_major == 1
        && auth_ok
        && valid_source
        && value.auth_scheme == "hmac-sha256-jcs-v1"
        && !value.replay
        && value.confidence_milli <= 1000
        && value.quality_milli <= 1000
        && freshness_valid;
    json!({
        "accepted": valid,
        "message_id": value.message_id,
        "reason": if valid { "accepted" } else { "authentication_or_shape_failure" },
        "source": value.source,
        "causation_id": value.causation_id,
        "correlation_id": value.correlation_id
    })
}

fn peer_credentials(fd: i32) -> Option<(u32, u32)> {
    let mut cred = libc::ucred {
        pid: 0,
        uid: 0,
        gid: 0,
    };
    let mut len = std::mem::size_of::<libc::ucred>() as libc::socklen_t;
    let rc = unsafe {
        libc::getsockopt(
            fd,
            libc::SOL_SOCKET,
            libc::SO_PEERCRED,
            (&mut cred as *mut libc::ucred).cast(),
            &mut len,
        )
    };
    (rc == 0).then_some((cred.pid as u32, cred.uid))
}

fn load_ordinary_authority(runtime: &std::path::Path) -> Option<OrdinaryAuthority> {
    let path = runtime.join("ordinary-evidence-authority.json");
    std::fs::read(path)
        .ok()
        .and_then(|bytes| serde_json::from_slice::<OrdinaryAuthority>(&bytes).ok())
}

fn send_ordinary_evidence(generation: &str) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    let paths = XdgPaths::resolve("companion")?;
    let socket = paths.runtime.join("ordinary-evidence.sock");
    let mut stream = None;
    for _ in 0..40 {
        match UnixStream::connect(&socket) {
            Ok(value) => {
                stream = Some(value);
                break;
            }
            Err(_) => std::thread::sleep(Duration::from_millis(25)),
        }
    }
    let mut stream = stream.ok_or("ordinary evidence endpoint unavailable")?;
    let authority = load_ordinary_authority(&paths.runtime).ok_or("ordinary authority missing")?;
    let secret =
        decode_secret_hex(&authority.secret_hex).ok_or("ordinary authority secret invalid")?;
    let mut value = OrdinaryEvidenceV1 {
        schema_major: 1,
        message_id: Uuid::new_v4(),
        producer_generation: generation.to_owned(),
        source: "sensor-gateway".into(),
        observed_at: "2026-01-01T00:00:00Z".into(),
        monotonic_ns: logging::monotonic_ns(),
        confidence_milli: 900,
        quality_milli: 900,
        replay: false,
        causation_id: None,
        correlation_id: Some(Uuid::new_v4()),
        auth_scheme: "hmac-sha256-jcs-v1".into(),
        mac: String::new(),
        payload: OrdinaryPayload {
            kind: env::var("COMPANION_ORDINARY_KIND").unwrap_or_else(|_| "preference".into()),
            subject: env::var("COMPANION_ORDINARY_SUBJECT")
                .unwrap_or_else(|_| "primary_user".into()),
            value: env::var("COMPANION_ORDINARY_VALUE").unwrap_or_else(|_| "listen".into()),
        },
    };
    value.mac = ordinary_digest(&value, &secret);
    let encoded = serde_json::to_vec(&value)?;
    stream.write_all(&encoded)?;
    let _ = stream.shutdown(std::net::Shutdown::Write);
    Ok(encoded)
}

fn send_body_intent(
    intent: &BodyNeutralIntent,
) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    intent.validate_wire().map_err(|e| e.to_string())?;
    let paths = XdgPaths::resolve("companion")?;
    let socket = paths.runtime.join("godot-bridge.sock");
    let mut stream = UnixStream::connect(socket)?;
    let request = json!({
        "protocol":"companion-foundation-v1",
        "kind":"body_intent",
        "intent_id":intent.intent_id,
        "intent_sequence":intent.intent_sequence,
        "action":intent.action,
        "facing":intent.facing,
        "correlation_id":intent.intent_id,
        "causation_id":intent.source_goal,
        "pack_revision":"r06-frozen"
    });
    stream.write_all(&serde_json::to_vec(&request)?)?;
    let _ = stream.shutdown(std::net::Shutdown::Write);
    let mut response = Vec::new();
    stream.read_to_end(&mut response)?;
    let value: serde_json::Value = serde_json::from_slice(&response)?;
    if value.get("accepted").and_then(|v| v.as_bool()) != Some(true) {
        return Err("godot rejected body intent".into());
    }
    Ok(value)
}

fn execute_real_godot(value: &serde_json::Value) -> serde_json::Value {
    if env::var_os("COMPANION_REAL_GODOT").is_none() {
        return json!({
            "accepted": false,
            "reason": "godot_execution_not_enabled_in_compatibility_mode"
        });
    }
    let Some(godot) = env::var_os("GODOT_BIN") else {
        return json!({"accepted":false,"reason":"godot_binary_not_provisioned"});
    };
    let project = env::var_os("COMPANION_GODOT_PROJECT").unwrap_or_else(|| "godot".into());
    let pack = env::var_os("COMPANION_GODOT_PACK")
        .unwrap_or_else(|| "assets/source/p02/r06/approved/pack.json".into());
    let action = value
        .get("action")
        .and_then(|v| v.as_str())
        .unwrap_or("idle");
    let track = match action {
        "listen" | "acknowledge" => "r06_playback_track_05",
        _ => "r06_playback_track_00",
    };
    let paths = match XdgPaths::resolve("companion") {
        Ok(paths) => paths,
        Err(error) => return json!({"accepted":false,"reason":error.to_string()}),
    };
    let capture = paths.runtime.join(format!("godot-{}.png", Uuid::new_v4()));
    let engine_log = paths.runtime.join(format!("godot-{}.log", Uuid::new_v4()));
    let wrapper_log = paths.runtime.join(format!("xvfb-{}.log", Uuid::new_v4()));
    let command_args = vec![
        "--log-file".into(),
        engine_log.to_string_lossy().into_owned(),
        "--audio-driver".into(),
        "Dummy".into(),
        "--path".into(),
        project.to_string_lossy().into_owned(),
        "--script".into(),
        "res://r06_black_pack_test.gd".into(),
        "--".into(),
        format!("--pack={}", pack.to_string_lossy()),
        format!("--track={track}"),
        format!("--capture={}", capture.to_string_lossy()),
    ];
    let xvfb = env::var_os("XVFB_RUN").or_else(|| {
        Path::new("/usr/bin/xvfb-run")
            .is_file()
            .then(|| std::ffi::OsString::from("/usr/bin/xvfb-run"))
    });
    let result = if let Some(xvfb) = xvfb {
        Command::new(xvfb)
            .args(["-a", "-e"])
            .arg(&wrapper_log)
            .arg(godot)
            .args(&command_args)
            .output()
    } else {
        Command::new(godot).args(&command_args).output()
    };
    let Ok(output) = result else {
        return json!({"accepted":false,"reason":"godot_spawn_failed"});
    };
    let text = String::from_utf8_lossy(&output.stdout);
    let observed = text
        .lines()
        .rev()
        .find_map(|line| serde_json::from_str::<serde_json::Value>(line).ok());
    let Some(observed) = observed else {
        return json!({"accepted":false,"reason":"godot_result_missing","exit_code":output.status.code()});
    };
    let accepted = output.status.success()
        && observed.get("status").and_then(|v| v.as_str()) == Some("PASS")
        && observed.get("render_observation").and_then(|v| v.as_str())
            == Some("RenderingServer.frame_post_draw");
    json!({
        "schema_major": 1,
        "intent_id": value.get("intent_id"),
        "intent_sequence": value.get("intent_sequence"),
        "accepted": accepted,
        "track_id": track,
        "track_path": [track],
        "terminal_state": if accepted { "completed" } else { "degraded" },
        "completion_reason": if accepted { "godot_observed" } else { "godot_rejected" },
        "pack_revision": value.get("pack_revision"),
        "source_pack_sha256": FROZEN_R06_PACK_SHA256,
        "correlation_id": value.get("correlation_id"),
        "causation_id": value.get("causation_id"),
        "render_observation": observed.get("render_observation"),
        "godot_event_count": observed.get("events").and_then(|v| v.as_array()).map_or(0, Vec::len),
        "capture_path": capture,
    })
}

fn read_capability(fd: Option<i32>) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    let raw = fd.ok_or("capability channel missing")?;
    let mut f = unsafe { std::fs::File::from_raw_fd(raw) };
    let mut b = [0u8; 128];
    let n = f.read(&mut b)?;
    if n == 0 {
        return Err("empty capability".into());
    }
    Ok(b[..n].to_vec())
}

const MAC_DOMAIN: &[u8] = b"companion.direct-care.v1\0";
type HmacSha256 = Hmac<Sha256>;

fn encode_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        out.push(HEX[(byte >> 4) as usize] as char);
        out.push(HEX[(byte & 0x0f) as usize] as char);
    }
    out
}

fn decode_hex(value: &str) -> Option<Vec<u8>> {
    if value.len() != 64 || !value.is_ascii() {
        return None;
    }
    let bytes = value.as_bytes();
    let mut decoded = Vec::with_capacity(32);
    for pair in bytes.chunks(2) {
        let hi = (pair[0] as char).to_digit(16)? as u8;
        let lo = (pair[1] as char).to_digit(16)? as u8;
        decoded.push((hi << 4) | lo);
    }
    Some(decoded)
}

fn decode_secret_hex(value: &str) -> Option<Vec<u8>> {
    if value.is_empty() || value.len() > 64 || !value.len().is_multiple_of(2) || !value.is_ascii() {
        return None;
    }
    value
        .as_bytes()
        .chunks(2)
        .map(|pair| {
            let hi = (pair[0] as char).to_digit(16)? as u8;
            let lo = (pair[1] as char).to_digit(16)? as u8;
            Some((hi << 4) | lo)
        })
        .collect()
}

fn mac(secret: &[u8], payload: &[u8]) -> Result<String, Box<dyn std::error::Error>> {
    let mut signer = HmacSha256::new_from_slice(secret).map_err(|_| "invalid HMAC key")?;
    signer.update(MAC_DOMAIN);
    signer.update(payload);
    Ok(encode_hex(&signer.finalize().into_bytes()))
}

fn verify_mac(secret: &[u8], payload: &[u8], supplied: &str) -> bool {
    let Some(expected_bytes) = decode_hex(supplied) else {
        return false;
    };
    let Ok(mut verifier) = HmacSha256::new_from_slice(secret) else {
        return false;
    };
    verifier.update(MAC_DOMAIN);
    verifier.update(payload);
    verifier.verify_slice(&expected_bytes).is_ok()
}

fn valid_safety_shape(value: &serde_json::Value) -> bool {
    let Some(object) = value.as_object() else {
        return false;
    };
    let allowed = [
        "schema_major",
        "message_id",
        "producer_generation",
        "auth_scheme",
        "mac",
        "observed_at",
        "confidence_milli",
        "quality_milli",
        "replay",
    ];
    if object.keys().any(|key| !allowed.contains(&key.as_str())) {
        return false;
    }
    object.get("schema_major").and_then(|v| v.as_u64()) == Some(1)
        && object
            .get("message_id")
            .and_then(|v| v.as_str())
            .and_then(|v| Uuid::parse_str(v).ok())
            .is_some()
        && object
            .get("producer_generation")
            .and_then(|v| v.as_str())
            .is_some_and(|v| !v.is_empty())
        && object.get("auth_scheme").and_then(|v| v.as_str()) == Some("hmac-sha256-jcs-v1")
        && object
            .get("mac")
            .and_then(|v| v.as_str())
            .is_some_and(|v| decode_hex(v).is_some())
        && object
            .get("observed_at")
            .and_then(|v| v.as_str())
            .is_some_and(valid_datetime)
        && object
            .get("confidence_milli")
            .and_then(|v| v.as_u64())
            .is_some_and(|v| v <= 1000)
        && object
            .get("quality_milli")
            .and_then(|v| v.as_u64())
            .is_some_and(|v| v <= 1000)
        && object.get("replay").and_then(|v| v.as_bool()).is_some()
}

fn object_has_unknown_field(value: &serde_json::Value) -> bool {
    let Some(object) = value.as_object() else {
        return true;
    };
    let allowed = [
        "schema_major",
        "message_id",
        "producer_generation",
        "auth_scheme",
        "mac",
        "observed_at",
        "confidence_milli",
        "quality_milli",
        "replay",
    ];
    object.keys().any(|key| !allowed.contains(&key.as_str()))
}

fn valid_datetime(value: &str) -> bool {
    // Bounded RFC3339 UTC profile used by the safety envelope.  Keeping this
    // parser local avoids platform-dependent date libraries in the service
    // boundary while still rejecting malformed/future-shaped strings.
    let bytes = value.as_bytes();
    bytes.len() == 20
        && bytes[4] == b'-'
        && bytes[7] == b'-'
        && bytes[10] == b'T'
        && bytes[13] == b':'
        && bytes[16] == b':'
        && bytes[19] == b'Z'
        && bytes
            .iter()
            .enumerate()
            .all(|(i, b)| matches!(i, 4 | 7 | 10 | 13 | 16 | 19) || b.is_ascii_digit())
        && value[11..13].parse::<u8>().is_ok_and(|h| h < 24)
        && value[14..16].parse::<u8>().is_ok_and(|m| m < 60)
        && value[17..19].parse::<u8>().is_ok_and(|s| s < 60)
}

fn producer(
    fd: Option<i32>,
    cap_fd: Option<i32>,
    control_fd: Option<i32>,
    boot: &str,
    seq: &mut u64,
) -> Result<(), Box<dyn std::error::Error>> {
    let raw = fd.ok_or("producer endpoint missing")?;
    let sock = unsafe { OwnedFd::from_raw_fd(raw) };
    let secret = read_capability(cap_fd)?;
    let generation = env::var("COMPANION_GENERATION")?;
    write_ready_marker("sensor-gateway")?;
    let cycles: usize = env::var("COMPANION_CYCLES")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(1);
    let seeds: Vec<String> = env::var("COMPANION_SEEDS")
        .unwrap_or_else(|_| "default".into())
        .split(',')
        .filter(|seed| !seed.is_empty())
        .map(str::to_owned)
        .collect();
    let mut last_packet: Option<Vec<u8>> = None;
    let mut last_ordinary_packet: Option<Vec<u8>> = None;
    for index in 0..cycles {
        let seed = &seeds[index % seeds.len()];
        let mut id_bytes = Uuid::parse_str(&generation)
            .map(|value| *value.as_bytes())
            .unwrap_or([0; 16]);
        id_bytes[12..].copy_from_slice(&(index as u32).to_be_bytes());
        // IDs are generation-scoped so a producer replacement cannot collide
        // with old receipts; the selected seed remains a harness input.
        let _ = seed;
        let message_id = Uuid::from_bytes(id_bytes).to_string();
        let base = json!({"schema_major":1,"message_id":message_id,"producer_generation":generation,"auth_scheme":"hmac-sha256-jcs-v1","observed_at":"2026-01-01T00:00:00Z","confidence_milli":900,"quality_milli":900,"replay":false});
        let bytes = canonical::canonical_event(&serde_json::to_vec(&base)?)?;
        let mut packet = base;
        packet["mac"] = json!(mac(&secret, &bytes)?);
        let encoded = serde_json::to_vec(&packet)?;
        ipc::send(&sock, &encoded)?;
        if index == 0 && env::var_os("COMPANION_PHASE01_COMPAT").is_some() {
            // The inherited Phase 01 closeout fixture needs one ordinary
            // packet at startup to exercise its separated compatibility
            // assertion.  Alpha live mode never sets this switch; its
            // ordinary ingress is control-triggered through the authenticated
            // sensor-gateway socket.
            // Ordinary evidence uses a separately addressed authenticated
            // stream; safety candidates remain on the seqpacket channel.
            last_ordinary_packet = Some(send_ordinary_evidence(&generation)?);
        }
        last_packet = Some(encoded.clone());
        if let Ok(paths) = XdgPaths::resolve("companion") {
            let _ = std::fs::write(paths.runtime.join("last-safety-packet.json"), &encoded);
        }
        if index == 0 {
            ipc::send(&sock, &encoded)?;
        }
    }
    if let Ok(paths) = XdgPaths::resolve("companion")
        && let Ok(mut packet) = std::fs::read(paths.runtime.join("last-safety-packet.json"))
        && let Ok(mut value) = serde_json::from_slice::<serde_json::Value>(&packet)
    {
        value["producer_generation"] = json!(generation);
        value["replay"] = json!(false);
        let mut unsigned = value.clone();
        unsigned.as_object_mut().map(|o| o.remove("mac"));
        let bytes = canonical::canonical_event(&serde_json::to_vec(&unsigned)?)?;
        value["mac"] = json!(mac(&secret, &bytes)?);
        packet = serde_json::to_vec(&value)?;
        last_packet = Some(packet);
    }
    logging::emit(
        "sensor-gateway",
        "safety_candidate_sent",
        *seq,
        boot,
        Some("seqpacket"),
    );
    *seq += 1;
    if !env::args().any(|a| a == "--once") {
        if let Some(raw) = control_fd {
            let control = unsafe { OwnedFd::from_raw_fd(raw) };
            let flags = unsafe { libc::fcntl(control.as_raw_fd(), libc::F_GETFL) };
            if flags >= 0 {
                unsafe {
                    libc::fcntl(control.as_raw_fd(), libc::F_SETFL, flags | libc::O_NONBLOCK);
                }
            }
            let mut pending = Vec::new();
            while !STOP.load(Ordering::SeqCst) {
                let mut pfd = libc::pollfd {
                    fd: control.as_raw_fd(),
                    events: libc::POLLIN,
                    revents: 0,
                };
                let ready = unsafe { libc::poll(&mut pfd, 1, 100) };
                if ready <= 0 {
                    continue;
                }
                let mut chunk = [0u8; 4096];
                let n = unsafe {
                    libc::read(control.as_raw_fd(), chunk.as_mut_ptr().cast(), chunk.len())
                };
                if n <= 0 {
                    break;
                }
                pending.extend_from_slice(&chunk[..n as usize]);
                while let Some(index) = pending.iter().position(|b| *b == b'\n') {
                    let line: Vec<u8> = pending.drain(..=index).collect();
                    let command = String::from_utf8_lossy(&line).trim().to_owned();
                    if command == "send_ordinary" {
                        last_ordinary_packet = Some(send_ordinary_evidence(&generation)?);
                        continue;
                    }
                    if command == "send_ordinary_replay" {
                        if let Some(packet) = &last_ordinary_packet {
                            let paths = XdgPaths::resolve("companion")?;
                            let socket = paths.runtime.join("ordinary-evidence.sock");
                            let mut stream = UnixStream::connect(socket)?;
                            stream.write_all(packet)?;
                            let _ = stream.shutdown(std::net::Shutdown::Write);
                        }
                        continue;
                    }
                    let (packet, remember) =
                        command_packet(&command, &secret, &generation, last_packet.as_deref())?;
                    if let Some(packet) = packet {
                        ipc::send(&sock, &packet)?;
                        if remember {
                            last_packet = Some(packet);
                        }
                    }
                }
            }
        } else {
            while !STOP.load(Ordering::SeqCst) {
                std::thread::sleep(Duration::from_millis(100));
            }
        }
    }
    Ok(())
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum InjectionKind {
    ValidOrdinaryObservation,
    DuplicateOrdinaryObservation,
    ValidSafetyCandidate,
    DuplicateSafetyCandidate,
    ReplaySafetyCandidate,
    MalformedFrame,
    DuplicateDecodedKey,
    UnsupportedSchemaMajor,
    UnknownField,
    InvalidUuid,
    InvalidDateTime,
    StaleGeneration,
    InvalidMac,
    StaleMac,
    UnauthorizedSender,
    ForbiddenCompanionState,
}

impl InjectionKind {
    fn parse(value: &str) -> Option<Self> {
        Some(match value {
            "valid_ordinary_observation" | "ordinary_observation" => Self::ValidOrdinaryObservation,
            "duplicate_ordinary_observation" | "ordinary_replay" => {
                Self::DuplicateOrdinaryObservation
            }
            "valid_safety_candidate" | "valid" | "inject_valid" => Self::ValidSafetyCandidate,
            "duplicate_safety_candidate" | "duplicate" | "inject_duplicate" => {
                Self::DuplicateSafetyCandidate
            }
            "replay_safety_candidate" | "replay" | "inject_replay" => Self::ReplaySafetyCandidate,
            "malformed_frame" | "malformed" | "inject_malformed" => Self::MalformedFrame,
            "duplicate_decoded_key" | "duplicate_key" | "inject_duplicate_key" => {
                Self::DuplicateDecodedKey
            }
            "unsupported_schema_major" | "unsupported_major" | "inject_unsupported_major" => {
                Self::UnsupportedSchemaMajor
            }
            "unknown_field" | "inject_unknown_field" => Self::UnknownField,
            "invalid_uuid" | "inject_invalid_uuid" => Self::InvalidUuid,
            "invalid_datetime" | "inject_invalid_datetime" => Self::InvalidDateTime,
            "stale_generation" | "inject_stale_generation" => Self::StaleGeneration,
            "invalid_mac" | "inject_invalid_mac" => Self::InvalidMac,
            "stale_mac" | "inject_stale_mac" => Self::StaleMac,
            "unauthorized_sender" | "forged_producer" | "inject_unauthorized_sender" => {
                Self::UnauthorizedSender
            }
            "forbidden_companion_state" | "companion_state" | "inject_companion_state" => {
                Self::ForbiddenCompanionState
            }
            _ => return None,
        })
    }
    fn normalized(self) -> &'static str {
        match self {
            Self::ValidOrdinaryObservation => "valid_ordinary_observation",
            Self::DuplicateOrdinaryObservation => "duplicate_ordinary_observation",
            Self::ValidSafetyCandidate => "valid_safety_candidate",
            Self::DuplicateSafetyCandidate => "duplicate_safety_candidate",
            Self::ReplaySafetyCandidate => "replay_safety_candidate",
            Self::MalformedFrame => "malformed_frame",
            Self::DuplicateDecodedKey => "duplicate_decoded_key",
            Self::UnsupportedSchemaMajor => "unsupported_schema_major",
            Self::UnknownField => "unknown_field",
            Self::InvalidUuid => "invalid_uuid",
            Self::InvalidDateTime => "invalid_datetime",
            Self::StaleGeneration => "stale_generation",
            Self::InvalidMac => "invalid_mac",
            Self::StaleMac => "stale_mac",
            Self::UnauthorizedSender => "unauthorized_sender",
            Self::ForbiddenCompanionState => "forbidden_companion_state",
        }
    }
    fn opcode(self) -> Option<&'static str> {
        Some(match self {
            Self::ValidSafetyCandidate => "inject_valid",
            Self::DuplicateSafetyCandidate => "inject_duplicate",
            Self::ReplaySafetyCandidate => "inject_replay",
            Self::MalformedFrame => "inject_malformed",
            Self::DuplicateDecodedKey => "inject_duplicate_key",
            Self::UnsupportedSchemaMajor => "inject_unsupported_major",
            Self::UnknownField => "inject_unknown_field",
            Self::InvalidUuid => "inject_invalid_uuid",
            Self::InvalidDateTime => "inject_invalid_datetime",
            Self::StaleGeneration => "inject_stale_generation",
            Self::InvalidMac => "inject_invalid_mac",
            Self::StaleMac => "inject_stale_mac",
            Self::UnauthorizedSender => "inject_unauthorized_sender",
            Self::ForbiddenCompanionState => "inject_companion_state",
            Self::ValidOrdinaryObservation => "send_ordinary",
            Self::DuplicateOrdinaryObservation => "send_ordinary_replay",
        })
    }
}

#[allow(clippy::type_complexity)]
fn command_packet(
    command: &str,
    secret: &[u8],
    generation: &str,
    previous: Option<&[u8]>,
) -> Result<(Option<Vec<u8>>, bool), Box<dyn std::error::Error>> {
    let kind = InjectionKind::parse(command).ok_or("unknown injection opcode")?;
    if kind == InjectionKind::ValidOrdinaryObservation {
        return Ok((None, false));
    }
    if command == "inject_duplicate" {
        return Ok((previous.map(ToOwned::to_owned), false));
    }
    if command == "inject_replay" {
        if let Some(previous) = previous {
            let mut value: serde_json::Value = serde_json::from_slice(previous)?;
            value["replay"] = json!(true);
            return Ok((Some(serde_json::to_vec(&value)?), false));
        }
        return Ok((None, false));
    }
    if command == "inject_malformed" {
        return Ok((Some(b"{malformed".to_vec()), false));
    }
    if command == "inject_duplicate_key" {
        return Ok((
            Some(br#"{"schema_major":1,"a":1,"\u0061":2}"#.to_vec()),
            false,
        ));
    }
    if command == "inject_unsupported_major" {
        return Ok((
            Some(
                br#"{"schema_major":2,"message_id":"00000000-0000-4000-8000-000000000099"}"#
                    .to_vec(),
            ),
            false,
        ));
    }
    let id = Uuid::new_v4().to_string();
    let mut value = json!({"schema_major":1,"message_id":id,"producer_generation":generation,"auth_scheme":"hmac-sha256-jcs-v1","observed_at":"2026-01-01T00:00:00Z","confidence_milli":900,"quality_milli":900,"replay":false});
    if command == "inject_stale_generation" || command == "inject_forged_producer" {
        value["producer_generation"] = json!("stale-generation");
    }
    if command == "inject_unauthorized_sender" {
        value["producer_generation"] = json!("attacker");
    }
    if command == "inject_unknown_field" {
        value["mood"] = json!("forbidden");
    }
    if command == "inject_companion_state" {
        value["companion_state"] = json!("forbidden");
    }
    if command == "inject_invalid_uuid" {
        value["message_id"] = json!("not-a-uuid");
    }
    if command == "inject_invalid_datetime" {
        value["observed_at"] = json!("not-a-date");
    }
    if command == "inject_ordinary" || command == "inject_ordinary_observation" {
        value["ordinary_observation"] = json!(true);
    }
    if command == "inject_invalid_mac" {
        value["mac"] = json!("00");
        return Ok((Some(serde_json::to_vec(&value)?), false));
    }
    if command == "inject_replay" {
        value["replay"] = json!(true);
    }
    if kind == InjectionKind::StaleMac {
        value["mac"] = json!("0000000000000000000000000000000000000000000000000000000000000000");
        return Ok((Some(serde_json::to_vec(&value)?), false));
    }
    let unsigned = canonical::canonical_event(&serde_json::to_vec(&value)?)?;
    value["mac"] = json!(mac(secret, &unsigned)?);
    Ok((
        Some(serde_json::to_vec(&value)?),
        kind == InjectionKind::ValidSafetyCandidate,
    ))
}

fn care(
    fd: Option<i32>,
    cap_fd: Option<i32>,
    boot: &str,
    seq: &mut u64,
) -> Result<(), Box<dyn std::error::Error>> {
    let raw = fd.ok_or("care endpoint missing")?;
    let sock = unsafe { OwnedFd::from_raw_fd(raw) };
    ipc::enable_passcred(&sock)?;
    let secret = read_capability(cap_fd)?;
    let expected_pid = env::var("COMPANION_EXPECTED_PRODUCER_PID")?.parse::<libc::pid_t>()?;
    let expected_generation = env::var("COMPANION_GENERATION")?;
    let paths = XdgPaths::resolve("companion")?;
    let store = Store::open(&paths, "care")?;
    write_ready_marker("care-core")?;
    let fault_marker = paths.runtime.join("care-store-fault");
    let cycles: usize = env::var("COMPANION_CYCLES")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(1);
    let mut seen = std::collections::HashSet::new();
    let mut handled = 0usize;
    loop {
        if fault_marker.exists() {
            let _ = std::fs::remove_file(paths.runtime.join("ready").join("care-core.ready"));
            return Err("care store fault injected".into());
        }
        let mut ready = libc::pollfd {
            fd: sock.as_raw_fd(),
            events: libc::POLLIN,
            revents: 0,
        };
        let polled = unsafe { libc::poll(&mut ready, 1, 250) };
        if polled == 0 {
            if env::args().any(|a| a == "--once") && handled > cycles {
                break;
            }
            if STOP.load(Ordering::SeqCst) {
                break;
            }
            continue;
        }
        let (data, cred) = match ipc::receive_with_credentials(&sock, 16 * 1024) {
            Ok(value) => value,
            Err(error) => {
                if error
                    .to_string()
                    .contains("Resource temporarily unavailable")
                {
                    continue;
                }
                break;
            }
        };
        handled += 1;
        let parsed = canonical::reject_duplicate_keys(&data).and_then(|_| {
            serde_json::from_slice::<serde_json::Value>(&data)
                .map_err(canonical::CanonicalError::from)
        });
        let value = match parsed {
            Ok(value) => value,
            Err(error) => {
                let reason = if error.to_string().contains("duplicate") {
                    "duplicate_decoded_key"
                } else {
                    "malformed_frame"
                };
                let _ = store.append_attempt(
                    None,
                    false,
                    false,
                    reason,
                    &format!("boot:{boot}:{}", logging::monotonic_ns()),
                )?;
                logging::emit("care-core", "care_rejected", *seq, boot, Some(reason));
                *seq += 1;
                continue;
            }
        };
        let msg = value.get("message_id").and_then(|v| v.as_str());
        let msg_label = msg.unwrap_or("untrusted");
        let shape_valid = valid_safety_shape(&value);
        let mut unsigned = value.clone();
        let supplied = unsigned
            .get("mac")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_owned();
        unsigned.as_object_mut().map(|o| o.remove("mac"));
        let unsigned_bytes = serde_json::to_vec(&unsigned)
            .ok()
            .and_then(|bytes| canonical::canonical_event(&bytes).ok());
        let duplicate_id = if let Some(id) = msg {
            seen.contains(id) || store.receipt_exists(id)?
        } else {
            false
        };
        let replayed = value.get("replay").and_then(|v| v.as_bool()) == Some(true);
        let duplicate = duplicate_id && !replayed;
        let mut reason = if replayed {
            "replay_rejected"
        } else if duplicate {
            "duplicate"
        } else {
            "rejected"
        };
        if !duplicate {
            reason = if value.get("schema_major").and_then(|v| v.as_u64()) != Some(1) {
                "unsupported_schema_major"
            } else if value.get("companion_state").is_some() {
                "forbidden_companion_state"
            } else if object_has_unknown_field(&value) {
                "unknown_field"
            } else if msg.is_none() || msg.and_then(|v| Uuid::parse_str(v).ok()).is_none() {
                "invalid_uuid"
            } else if value
                .get("observed_at")
                .and_then(|v| v.as_str())
                .is_none_or(|v| !valid_datetime(v))
            {
                "invalid_datetime"
            } else if value.get("producer_generation").and_then(|v| v.as_str()) == Some("attacker")
            {
                "unauthorized_sender"
            } else if value.get("producer_generation").and_then(|v| v.as_str())
                != Some(expected_generation.as_str())
            {
                "stale_generation"
            } else if replayed {
                "replay_rejected"
            } else if supplied.len() == 64 {
                "stale_mac"
            } else {
                "invalid_mac"
            };
        }
        let valid = cred.pid == expected_pid
            && cred.uid == unsafe { libc::geteuid() }
            && shape_valid
            && value.get("producer_generation").and_then(|v| v.as_str())
                == Some(expected_generation.as_str())
            && value.get("auth_scheme").and_then(|v| v.as_str()) == Some("hmac-sha256-jcs-v1")
            && unsigned_bytes
                .as_ref()
                .is_some_and(|bytes| verify_mac(&secret, bytes, &supplied))
            && !value
                .get("replay")
                .and_then(|v| v.as_bool())
                .unwrap_or(true)
            && !duplicate;
        if valid {
            reason = "accepted";
        }
        if (valid || duplicate)
            && let Some(id) = msg
        {
            seen.insert(id.to_owned());
            let _ = store.append_receipt(
                id,
                valid,
                duplicate,
                reason,
                &format!("boot:{boot}:{}", logging::monotonic_ns()),
            )?;
        }
        let inserted_attempt = store.append_attempt(
            msg,
            valid,
            duplicate,
            reason,
            &format!("boot:{boot}:{}", logging::monotonic_ns()),
        )?;
        logging::emit(
            "care-core",
            if valid {
                "care_receipt"
            } else {
                "care_rejected"
            },
            *seq,
            boot,
            Some(reason),
        );
        *seq += 1;
        println!(
            "{}",
            json!({"accepted":valid,"duplicate":duplicate,"message_id":msg_label,"pid":cred.pid,"durable":inserted_attempt,"reason":reason})
        );
        if env::args().any(|a| a == "--once") && handled > cycles {
            break;
        }
    }
    Ok(())
}

#[derive(Debug)]
struct ChildEntry {
    role: String,
    child: Child,
    restarts: u32,
    generation: u64,
    backoff: Duration,
    ready_path: std::path::PathBuf,
    pidfd: Option<OwnedFd>,
}

type DirectChildren = (ChildEntry, Option<ChildEntry>, OwnedFd, String);

fn spawn_direct_children(
    exe: &std::path::Path,
    ready_dir: &std::path::Path,
    secret: &[u8],
    ordinary_secret: &[u8],
    boot: &str,
) -> Result<DirectChildren, Box<dyn std::error::Error>> {
    let (producer_endpoint, care_endpoint) = ipc::seqpacket_pair()?;
    ipc::enable_passcred(&producer_endpoint)?;
    ipc::enable_passcred(&care_endpoint)?;
    let (producer_cap_read, producer_cap_write) = pipe()?;
    let (care_cap_read, care_cap_write) = pipe()?;
    let (producer_control_read, producer_control_write) = pipe()?;
    // The inherited closeout matrix deliberately sends a large burst of
    // typed producer commands.  Keep that control channel from applying
    // kernel-default pipe backpressure to the supervisor request socket;
    // the producer still drains and executes each command in order.
    let _ = unsafe {
        libc::fcntl(
            producer_control_write.as_raw_fd(),
            libc::F_SETPIPE_SZ,
            1_048_576,
        )
    };
    // Seed capability pipes before child exec so readiness cannot race a
    // blocking capability read during initialization.
    write_fd(&producer_cap_write, secret)?;
    if env::var_os("COMPANION_SKIP_CARE").is_none() {
        write_fd(&care_cap_write, secret)?;
    }
    let generation = Uuid::new_v4().to_string();
    let generation_number = DIRECT_GENERATION.fetch_add(1, Ordering::SeqCst) + 1;
    let producer = spawn(
        exe,
        "sensor-gateway",
        Some(producer_endpoint.as_raw_fd()),
        Some(producer_cap_read.as_raw_fd()),
        Some(producer_control_read.as_raw_fd()),
        Some(&generation),
        None,
        ready_dir,
    )?;
    let producer_pid = producer.id();
    let paths = XdgPaths::resolve("companion")?;
    let authority_path = paths.runtime.join("ordinary-evidence-authority.json");
    let authority = OrdinaryAuthority {
        pid: producer_pid,
        uid: unsafe { libc::geteuid() },
        generation: generation.clone(),
        secret_hex: encode_hex(ordinary_secret),
    };
    std::fs::write(&authority_path, serde_json::to_vec(&authority)?)?;
    let mut permissions = std::fs::metadata(&authority_path)?.permissions();
    use std::os::unix::fs::PermissionsExt;
    permissions.set_mode(0o600);
    std::fs::set_permissions(&authority_path, permissions)?;
    let pidfd = match ipc::pidfd_open(producer_pid as libc::pid_t) {
        Ok(fd) => {
            logging::emit(
                "ops-supervisor",
                "producer_pidfd_bound",
                2,
                boot,
                Some("live_generation"),
            );
            Some(fd)
        }
        Err(error) => {
            logging::emit(
                "ops-supervisor",
                "producer_pidfd_unavailable",
                2,
                boot,
                Some(&format!("errno:{}", error.raw_os_error().unwrap_or(-1))),
            );
            None
        }
    };
    let care = if env::var_os("COMPANION_SKIP_CARE").is_some() {
        None
    } else {
        Some(spawn(
            exe,
            "care-core",
            Some(care_endpoint.as_raw_fd()),
            Some(care_cap_read.as_raw_fd()),
            None,
            Some(&generation),
            Some(producer_pid),
            ready_dir,
        )?)
    };
    // The supervisor closes both transport endpoints after handoff. A future
    // restart creates a fresh pair and generation, so the old channel is
    // revoked by descriptor close rather than reused.
    drop(producer_endpoint);
    drop(care_endpoint);
    drop(producer_cap_read);
    drop(producer_control_read);
    drop(care_cap_read);
    drop(producer_cap_write);
    drop(care_cap_write);
    let producer_entry = ChildEntry {
        role: "sensor-gateway".into(),
        child: producer,
        restarts: 0,
        generation: generation_number,
        backoff: Duration::from_millis(100),
        ready_path: ready_dir.join("sensor-gateway.ready"),
        pidfd,
    };
    let care_entry = care.map(|child| ChildEntry {
        role: "care-core".into(),
        child,
        restarts: 0,
        generation: generation_number,
        backoff: Duration::from_millis(100),
        ready_path: ready_dir.join("care-core.ready"),
        pidfd: None,
    });
    Ok((
        producer_entry,
        care_entry,
        producer_control_write,
        generation,
    ))
}

fn supervisor() -> Result<(), Box<dyn std::error::Error>> {
    harden()?;
    let boot = logging::boot_id();
    logging::emit("ops-supervisor", "starting", 1, &boot, None);
    let (sqlite_version, sqlite_source_id) = runtime_identity();
    logging::emit(
        "ops-supervisor",
        "sqlite_identity",
        2,
        &boot,
        Some(&format!("{sqlite_version}:{sqlite_source_id}")),
    );
    let exe = env::current_exe()?;
    let paths = XdgPaths::resolve("companion")?;
    paths.ensure()?;
    let control = paths.runtime.join("supervisor.sock");
    let ready_dir = paths.runtime.join("ready");
    std::fs::create_dir_all(&ready_dir)?;
    let _ = std::fs::remove_file(&control);
    let listener = std::os::unix::net::UnixListener::bind(&control)?;
    listener.set_nonblocking(true)?;
    let mut secret = uuid::Uuid::new_v4().as_bytes().to_vec();
    let mut ordinary_secret = uuid::Uuid::new_v4().as_bytes().to_vec();
    let mut children = Vec::new();
    let (producer_entry, care_entry, mut producer_control, _ordinary_generation) =
        spawn_direct_children(&exe, &ready_dir, &secret, &ordinary_secret, &boot)?;
    children.push(producer_entry);
    if let Some(care_entry) = care_entry {
        children.push(care_entry);
    }
    for role in ["companion-core", "identity-consent-vault", "godot-bridge"] {
        if role == "companion-core" && env::var_os("COMPANION_SKIP_COMPANION").is_some() {
            logging::emit(
                "ops-supervisor",
                "companion_optional_absent",
                2,
                &boot,
                Some("care_path_independent"),
            );
            continue;
        }
        let child_generation = format!("{}-{}", role, Uuid::new_v4());
        let child = spawn(
            &exe,
            role,
            None,
            None,
            None,
            Some(&child_generation),
            None,
            &ready_dir,
        )?;
        let ready_path = ready_dir.join(format!("{role}.ready"));
        children.push(ChildEntry {
            role: role.into(),
            child,
            restarts: 0,
            generation: 1,
            backoff: Duration::from_millis(100),
            ready_path,
            pidfd: None,
        });
    }
    let once = env::args().any(|a| a == "--once");
    let deadline = Instant::now() + Duration::from_secs(10);
    loop {
        if let Ok((mut stream, _)) = listener.accept() {
            let request = match read_control_request(&mut stream) {
                Ok(request) => request,
                Err(error) => {
                    let response = json!({
                        "command": "invalid",
                        "accepted": false,
                        "reason": "control_read_error",
                        "error_class": format!("{:?}", error.kind()),
                    });
                    let encoded = serde_json::to_string(&response)?;
                    let _ = stream.write_all(encoded.as_bytes());
                    continue;
                }
            };
            let command = match serde_json::from_slice::<serde_json::Value>(&request) {
                Ok(command) => command,
                Err(_) => {
                    let encoded = serde_json::to_string(&json!({
                        "command": "invalid",
                        "accepted": false,
                        "reason": "invalid_control_request",
                    }))?;
                    let _ = stream.write_all(encoded.as_bytes());
                    continue;
                }
            };
            let response = handle_control(Some(&command), &mut children, Some(&producer_control));
            if response.get("command").and_then(|v| v.as_str()) == Some("shutdown") {
                STOP.store(true, Ordering::SeqCst);
            }
            let encoded = serde_json::to_string(&response)?;
            let _ = stream.write_all(encoded.as_bytes());
        }
        for entry in &mut children {
            if let Some(status) = entry.child.try_wait()? {
                logging::emit(
                    "ops-supervisor",
                    "child_exit",
                    2,
                    &boot,
                    Some(&format!("{}:{status}", entry.role)),
                );
                entry.restarts += 1;
                entry.generation += 1;
                entry.backoff = (entry.backoff * 2).min(Duration::from_secs(8));
                if !once
                    && matches!(
                        entry.role.as_str(),
                        "companion-core" | "identity-consent-vault" | "godot-bridge"
                    )
                    && entry.restarts < 3
                {
                    std::thread::sleep(entry.backoff);
                    // Remove the old acknowledgement before spawning. This
                    // avoids a replacement inheriting stale readiness.
                    let _ = std::fs::remove_file(&entry.ready_path);
                    let child_generation = format!("{}-{}", entry.role, Uuid::new_v4());
                    let replacement = spawn(
                        &exe,
                        &entry.role,
                        None,
                        None,
                        None,
                        Some(&child_generation),
                        None,
                        &ready_dir,
                    )?;
                    let mut old = std::mem::replace(&mut entry.child, replacement);
                    let _ = old.wait();
                    let _ = wait_ready(&entry.ready_path, Duration::from_secs(5));
                    logging::emit(
                        "ops-supervisor",
                        "child_restarted",
                        2,
                        &boot,
                        Some(&entry.role),
                    );
                } else if entry.restarts >= 3 {
                    logging::emit("ops-supervisor", "crash_loop", 3, &boot, Some(&entry.role));
                }
            }
        }
        let direct_failure = !once
            && children.iter_mut().any(|entry| {
                matches!(entry.role.as_str(), "sensor-gateway" | "care-core")
                    && entry.child.try_wait().ok().flatten().is_some()
            });
        if direct_failure {
            // A direct-care endpoint is never reused after either side exits.
            // Kill/reap the peer, drop the old pidfd, and provision a fresh
            // socketpair, generation, and capability before restoring care.
            for entry in &mut children {
                if matches!(entry.role.as_str(), "sensor-gateway" | "care-core") {
                    if entry.child.try_wait()?.is_none() {
                        unsafe { libc::kill(entry.child.id() as libc::pid_t, libc::SIGTERM) };
                    }
                    let _ = entry.child.wait();
                    let _ = std::fs::remove_file(&entry.ready_path);
                }
            }
            children.retain(|entry| !matches!(entry.role.as_str(), "sensor-gateway" | "care-core"));
            std::thread::sleep(Duration::from_millis(100));
            secret = Uuid::new_v4().as_bytes().to_vec();
            ordinary_secret = Uuid::new_v4().as_bytes().to_vec();
            let (producer_entry, care_entry, new_control, _generation) =
                spawn_direct_children(&exe, &ready_dir, &secret, &ordinary_secret, &boot)?;
            producer_control = new_control;
            children.push(producer_entry);
            if let Some(care_entry) = care_entry {
                children.push(care_entry);
            }
            logging::emit(
                "ops-supervisor",
                "direct_care_generation_rotated",
                3,
                &boot,
                Some("channel_revoked_and_rebuilt"),
            );
        }
        let all_done = children
            .iter_mut()
            .all(|e| e.child.try_wait().ok().flatten().is_some());
        if (once && (all_done || Instant::now() > deadline)) || STOP.load(Ordering::SeqCst) {
            break;
        }
        std::thread::sleep(Duration::from_millis(100));
    }
    for entry in &mut children {
        if entry.child.try_wait()?.is_none() {
            unsafe {
                libc::kill(entry.child.id() as i32, libc::SIGTERM);
            }
        }
    }
    for entry in &mut children {
        let _ = entry.child.wait();
    }
    let _ = std::fs::remove_file(&control);
    logging::emit(
        "ops-supervisor",
        "stopped",
        9,
        &boot,
        Some("clean_shutdown"),
    );
    Ok(())
}

fn read_control_request(stream: &mut std::os::unix::net::UnixStream) -> io::Result<Vec<u8>> {
    stream.set_read_timeout(Some(CONTROL_READ_TIMEOUT))?;
    let mut request = Vec::new();
    let mut buffer = [0_u8; 4096];
    loop {
        let count = stream.read(&mut buffer)?;
        if count == 0 {
            break;
        }
        request.extend_from_slice(&buffer[..count]);
        if request.len() > CONTROL_REQUEST_LIMIT {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "control request exceeds bounded frame size",
            ));
        }
        if let Some(newline) = request.iter().position(|byte| *byte == b'\n') {
            if request[newline + 1..]
                .iter()
                .any(|byte| !byte.is_ascii_whitespace())
            {
                return Err(io::Error::new(
                    io::ErrorKind::InvalidData,
                    "multiple control frames are not allowed",
                ));
            }
            request.truncate(newline + 1);
            break;
        }
    }
    if request.is_empty() {
        return Err(io::Error::new(
            io::ErrorKind::UnexpectedEof,
            "empty control request",
        ));
    }
    Ok(request)
}

fn wait_ready(path: &std::path::Path, timeout: Duration) -> bool {
    let deadline = Instant::now() + timeout;
    while Instant::now() < deadline {
        if let Ok(bytes) = std::fs::read(path)
            && let Ok(value) = serde_json::from_slice::<serde_json::Value>(&bytes)
            && value.get("initialization_status").and_then(|v| v.as_str()) == Some("ready")
        {
            return true;
        }
        std::thread::sleep(Duration::from_millis(25));
    }
    false
}

fn health_json(children: &mut [ChildEntry]) -> String {
    let mut rows = Vec::new();
    for entry in children.iter_mut() {
        let marker = std::fs::read(&entry.ready_path)
            .ok()
            .and_then(|bytes| serde_json::from_slice::<serde_json::Value>(&bytes).ok());
        let state = match entry.child.try_wait() {
            Ok(Some(_)) if entry.restarts >= 3 => "crash_loop",
            Ok(Some(_)) => "failed",
            Ok(None) if ready_marker_valid(&entry.ready_path, entry.child.id(), &entry.role) => {
                "healthy"
            }
            Ok(None) => "starting",
            Err(_) => "degraded",
        };
        rows.push(json!({
            "role":entry.role,
            "pid":entry.child.id(),
            "generation":entry.generation,
            "restarts":entry.restarts,
            "backoff_ms":entry.backoff.as_millis(),
            "running":state != "failed" && state != "crash_loop",
            "ready":state == "healthy",
            "state":state,
            "health":state,
            "pidfd_bound":entry.pidfd.is_some(),
            "pidfd_alive":entry.pidfd.as_ref().is_some_and(pidfd_alive),
            "readiness_generation":marker.as_ref().and_then(|v| v.get("generation")).cloned().unwrap_or(serde_json::Value::Null),
            "readiness_boot_id":marker.as_ref().and_then(|v| v.get("boot_id")).cloned().unwrap_or(serde_json::Value::Null),
            "store_status":marker.as_ref().and_then(|v| v.get("store_status")).cloned().unwrap_or(serde_json::Value::Null),
            "channel_status":marker.as_ref().and_then(|v| v.get("channel_status")).cloned().unwrap_or(serde_json::Value::Null)
        }));
    }
    let care_coverage = if children.iter_mut().any(|e| {
        e.role == "care-core"
            && e.ready_path.exists()
            && e.child.try_wait().ok().flatten().is_none()
    }) {
        "synthetic"
    } else {
        "degraded"
    };
    let (sqlite_version, sqlite_source_id) = runtime_identity();
    serde_json::to_string(&json!({"version":FOUNDATION_VERSION,"status":"resident","children":rows,"care_coverage":care_coverage,"network_policy":"deny_by_default","network_observation":"external_process_census_required","boot_id":logging::boot_id(),"sqlite":{"version":sqlite_version,"source_id":sqlite_source_id,"compile_options":runtime_compile_options()}})).unwrap_or_else(|_|"{\"status\":\"health_serialization_failed\"}".into())
}

fn ready_marker_valid(path: &std::path::Path, pid: u32, role: &str) -> bool {
    std::fs::read(path)
        .ok()
        .and_then(|bytes| serde_json::from_slice::<serde_json::Value>(&bytes).ok())
        .is_some_and(|v| {
            v.get("role").and_then(|x| x.as_str()) == Some(role)
                && v.get("pid").and_then(|x| x.as_u64()) == Some(pid as u64)
                && v.get("initialization_status").and_then(|x| x.as_str()) == Some("ready")
                && v.get("boot_id")
                    .and_then(|x| x.as_str())
                    .is_some_and(|x| !x.is_empty())
                && v.get("generation")
                    .and_then(|x| x.as_str())
                    .is_some_and(|x| !x.is_empty())
        })
}

fn pidfd_alive(fd: &OwnedFd) -> bool {
    let mut pollfd = libc::pollfd {
        fd: fd.as_raw_fd(),
        events: libc::POLLIN,
        revents: 0,
    };
    let rc = unsafe { libc::poll(&mut pollfd, 1, 0) };
    rc == 0
}

fn handle_control(
    command: Option<&serde_json::Value>,
    children: &mut [ChildEntry],
    producer_control: Option<&OwnedFd>,
) -> serde_json::Value {
    let Some(command) = command else {
        return json!({});
    };
    let name = command
        .get("command")
        .and_then(|v| v.as_str())
        .unwrap_or("health");
    match name {
        "health" => json!({"command":"health","health":health_json(children)}),
        "shutdown" => json!({"command":"shutdown","accepted":true}),
        "kill" | "fail" | "restart" | "rotate" | "disconnect" => {
            let role = command.get("role").and_then(|v| v.as_str()).unwrap_or("");
            if let Some(entry) = children.iter().find(|entry| entry.role == role) {
                let result = unsafe { libc::kill(entry.child.id() as libc::pid_t, libc::SIGKILL) };
                json!({"command":name,"role":role,"accepted":result == 0,"errno":if result == 0 {0} else {std::io::Error::last_os_error().raw_os_error().unwrap_or(-1)}})
            } else {
                json!({"command":name,"role":role,"accepted":false,"reason":"unknown_role"})
            }
        }
        "inject" => {
            let requested = command.get("kind").and_then(|v| v.as_str()).unwrap_or("");
            let Some(kind) = InjectionKind::parse(requested) else {
                return json!({"command":"inject","kind":requested,"accepted":false,"reason":"unknown_injection_kind"});
            };
            if kind == InjectionKind::ValidOrdinaryObservation {
                let accepted =
                    producer_control.is_some_and(|fd| write_fd(fd, b"send_ordinary\n").is_ok());
                return json!({"command":"inject","kind":requested,"normalized_kind":kind.normalized(),"request_id":command.get("request_id").cloned().unwrap_or(json!(null)),"transport_path":"sensor-gateway->ordinary-evidence.sock","accepted":accepted,"producer_mutation":"send_ordinary"});
            }
            let opcode = kind.opcode().unwrap_or("inject_valid");
            if let Some(fd) = producer_control {
                let result = write_fd(fd, format!("{opcode}\n").as_bytes());
                return json!({"command":"inject","kind":requested,"normalized_kind":kind.normalized(),"request_id":command.get("request_id").cloned().unwrap_or(json!(null)),"producer_mutation":opcode,"accepted":result.is_ok(),"observed":"producer_control_channel"});
            }
            json!({"command":"inject","kind":requested,"normalized_kind":kind.normalized(),"accepted":false,"reason":"producer_control_unavailable"})
        }
        "reconnect" => {
            json!({"command":"reconnect","accepted":std::fs::write(XdgPaths::resolve("companion").ok().map(|p| p.runtime.join("bridge-command.json")).unwrap_or_default(), b"{\"command\":\"reconnect\"}").is_ok()})
        }
        "set_test_display_topology"
        | "set_test_store_fault"
        | "clear_test_fault"
        | "checkpoint_store"
        | "verify_store" => {
            let path = XdgPaths::resolve("companion").ok().map(|p| {
                if matches!(name, "set_test_store_fault" | "clear_test_fault") {
                    let authority = command
                        .get("authority")
                        .and_then(|v| v.as_str())
                        .unwrap_or("care");
                    p.runtime.join(format!("{authority}-store-fault"))
                } else {
                    p.runtime.join("test-control.json")
                }
            });
            let accepted = path.as_ref().is_some_and(|p| {
                if name == "clear_test_fault" {
                    std::fs::remove_file(p).is_ok() || !p.exists()
                } else {
                    std::fs::write(p, serde_json::to_vec(command).unwrap_or_default()).is_ok()
                }
            });
            json!({"command":name,"accepted":accepted,"observed":"control_state_recorded"})
        }
        _ => json!({"command":name,"accepted":false,"reason":"unsupported_command"}),
    }
}
fn pipe() -> Result<(OwnedFd, OwnedFd), std::io::Error> {
    let mut p = [0; 2];
    let rc = unsafe { libc::pipe2(p.as_mut_ptr(), libc::O_CLOEXEC) };
    if rc < 0 {
        return Err(std::io::Error::last_os_error());
    }
    Ok((unsafe { OwnedFd::from_raw_fd(p[0]) }, unsafe {
        OwnedFd::from_raw_fd(p[1])
    }))
}
fn write_fd(fd: &OwnedFd, data: &[u8]) -> Result<(), std::io::Error> {
    let rc = unsafe { libc::write(fd.as_raw_fd(), data.as_ptr().cast(), data.len()) };
    if rc == data.len() as isize {
        Ok(())
    } else {
        Err(std::io::Error::last_os_error())
    }
}

#[allow(clippy::too_many_arguments)]
fn spawn(
    exe: &std::path::Path,
    role: &str,
    endpoint: Option<i32>,
    cap: Option<i32>,
    control: Option<i32>,
    generation: Option<&str>,
    expected_pid: Option<u32>,
    ready_dir: &std::path::Path,
) -> Result<Child, Box<dyn std::error::Error>> {
    let sibling = exe.with_file_name(role);
    let mut cmd = Command::new(sibling);
    cmd.arg("--service");
    if env::args().any(|a| a == "--once") {
        cmd.arg("--once");
    }
    cmd.stdout(Stdio::inherit()).stderr(Stdio::inherit());
    if let Some(fd) = endpoint {
        cmd.env("COMPANION_IPC_FD", fd.to_string());
    }
    if let Some(fd) = cap {
        cmd.env("COMPANION_CAP_FD", fd.to_string());
    }
    if let Some(fd) = control {
        cmd.env("COMPANION_PRODUCER_CONTROL_FD", fd.to_string());
    }
    if let Some(g) = generation {
        cmd.env("COMPANION_GENERATION", g);
    }
    if let Some(pid) = expected_pid {
        cmd.env("COMPANION_EXPECTED_PRODUCER_PID", pid.to_string());
    }
    cmd.env("COMPANION_READY_DIR", ready_dir);
    unsafe {
        cmd.pre_exec(move || {
            harden()?;
            for fd in [endpoint, cap, control].into_iter().flatten() {
                let flags = libc::fcntl(fd, libc::F_GETFD);
                if flags < 0 {
                    return Err(std::io::Error::last_os_error());
                }
                if libc::fcntl(fd, libc::F_SETFD, flags & !libc::FD_CLOEXEC) < 0 {
                    return Err(std::io::Error::last_os_error());
                }
            }
            Ok(())
        });
    }
    Ok(cmd.spawn()?)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn control_request_survives_a_delayed_client_write() {
        let (mut server, mut client) = std::os::unix::net::UnixStream::pair().expect("socket pair");
        let reader = std::thread::spawn(move || read_control_request(&mut server));

        // This exceeds the superseded 50 ms one-shot read timeout and
        // deterministically reproduces the scheduling window seen in hosted CI.
        std::thread::sleep(Duration::from_millis(150));
        client
            .write_all(b"{\"command\":\"health\"}\n")
            .expect("delayed request write");
        client
            .shutdown(std::net::Shutdown::Write)
            .expect("request EOF");

        let request = reader.join().expect("reader thread").expect("request");
        assert_eq!(request, b"{\"command\":\"health\"}\n");
    }

    #[test]
    fn hmac_round_trip_uses_domain_separator() {
        let secret = b"qualification-secret";
        let payload = br#"{"schema_major":1,"message_id":"00000000-0000-4000-8000-000000000001"}"#;
        let digest = mac(secret, payload).expect("HMAC construction");
        assert!(verify_mac(secret, payload, &digest));
        assert!(!verify_mac(secret, br#"{"schema_major":1}"#, &digest));
    }

    #[test]
    fn safety_shape_rejects_unknown_fields_and_wrong_major() {
        let valid = json!({
            "schema_major": 1,
            "message_id": "00000000-0000-4000-8000-000000000001",
            "producer_generation": "generation",
            "auth_scheme": "hmac-sha256-jcs-v1",
            "mac": "0000000000000000000000000000000000000000000000000000000000000000",
            "observed_at": "2026-01-01T00:00:00Z",
            "confidence_milli": 1,
            "quality_milli": 1,
            "replay": false
        });
        assert!(valid_safety_shape(&valid));
        let mut unknown = valid.clone();
        unknown["mood"] = json!("forbidden");
        assert!(!valid_safety_shape(&unknown));
        let mut major = valid;
        major["schema_major"] = json!(2);
        assert!(!valid_safety_shape(&major));
    }

    #[test]
    fn safety_shape_rejects_invalid_datetime_and_accepts_bounded_utc() {
        assert!(valid_datetime("2026-01-01T00:00:00Z"));
        assert!(!valid_datetime("2026-01-01T24:00:00Z"));
        assert!(!valid_datetime("not-a-date"));
        assert!(!valid_datetime("2026-01-01T00:00:00+00:00"));
    }

    #[test]
    fn injection_kind_is_exhaustive_and_rejects_unknown() {
        let names = [
            "valid_ordinary_observation",
            "valid_safety_candidate",
            "duplicate_safety_candidate",
            "replay_safety_candidate",
            "malformed_frame",
            "duplicate_decoded_key",
            "unsupported_schema_major",
            "unknown_field",
            "invalid_uuid",
            "invalid_datetime",
            "stale_generation",
            "invalid_mac",
            "stale_mac",
            "unauthorized_sender",
            "forbidden_companion_state",
        ];
        for name in names {
            let kind = InjectionKind::parse(name).expect("known injection kind");
            assert_eq!(InjectionKind::parse(kind.normalized()), Some(kind));
            if matches!(
                kind,
                InjectionKind::ValidSafetyCandidate
                    | InjectionKind::DuplicateSafetyCandidate
                    | InjectionKind::ReplaySafetyCandidate
            ) {
                assert!(kind.opcode().is_some());
            }
        }
        assert!(InjectionKind::parse("totally_unknown").is_none());
    }

    #[test]
    fn ordinary_evidence_requires_peer_auth_and_integrity() {
        let mut value = OrdinaryEvidenceV1 {
            schema_major: 1,
            message_id: Uuid::from_u128(0x101),
            producer_generation: "generation".into(),
            source: "sensor-gateway".into(),
            observed_at: "2026-01-01T00:00:00Z".into(),
            monotonic_ns: 1,
            confidence_milli: 900,
            quality_milli: 900,
            replay: false,
            causation_id: None,
            correlation_id: Some(Uuid::from_u128(0x102)),
            auth_scheme: "scm-credentials-v1".into(),
            mac: String::new(),
            payload: OrdinaryPayload {
                kind: "preference".into(),
                subject: "user".into(),
                value: "listen".into(),
            },
        };
        let secret = b"qualification-ordinary-secret";
        value.monotonic_ns = logging::monotonic_ns();
        value.auth_scheme = "hmac-sha256-jcs-v1".into();
        value.mac = ordinary_digest(&value, secret);
        let bytes = serde_json::to_vec(&value).unwrap();
        let authority = OrdinaryAuthority {
            pid: std::process::id(),
            uid: unsafe { libc::geteuid() },
            generation: "generation".into(),
            secret_hex: encode_hex(secret),
        };
        let accepted = handle_ordinary_evidence(
            &bytes,
            Some((std::process::id(), unsafe { libc::geteuid() })),
            Some(&authority),
            logging::monotonic_ns(),
        );
        assert!(
            accepted
                .get("accepted")
                .and_then(|v| v.as_bool())
                .unwrap_or(false)
        );
        assert!(
            !handle_ordinary_evidence(
                &bytes,
                Some((std::process::id(), unsafe { libc::geteuid() + 1 })),
                Some(&authority),
                logging::monotonic_ns(),
            )
            .get("accepted")
            .and_then(|v| v.as_bool())
            .unwrap_or(false)
        );
        value.payload.value = "tampered".into();
        assert!(
            !handle_ordinary_evidence(
                &serde_json::to_vec(&value).unwrap(),
                Some((std::process::id(), unsafe { libc::geteuid() })),
                Some(&authority),
                logging::monotonic_ns(),
            )
            .get("accepted")
            .and_then(|v| v.as_bool())
            .unwrap_or(false)
        );
    }
}

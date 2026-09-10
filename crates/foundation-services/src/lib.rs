//! Resident, nonauthoritative Phase 01 process foundation.
use foundation_core::{
    canonical, ipc, logging,
    paths::XdgPaths,
    persistence::{Store, runtime_compile_options, runtime_identity},
    version::FOUNDATION_VERSION,
};
use hmac::{Hmac, Mac};
use serde_json::json;
use sha2::Sha256;
use std::env;
use std::io::{Read, Write};
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
use std::os::unix::process::CommandExt;
use std::process::{Child, Command, Stdio};
use std::sync::Once;
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::{Duration, Instant};
use uuid::Uuid;

static STOP: AtomicBool = AtomicBool::new(false);
static SIGNALS: Once = Once::new();
static DIRECT_GENERATION: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);

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
    let control_fd = env::var("COMPANION_PRODUCER_CONTROL_FD")
        .ok()
        .and_then(|v| v.parse::<i32>().ok());
    match role {
        "sensor-gateway" => producer(fd, cap_fd, control_fd, &boot, &mut seq)?,
        "care-core" => care(fd, cap_fd, &boot, &mut seq)?,
        "companion-core" => ordinary_store("companion", &boot, &mut seq)?,
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
                    if value.get("protocol").and_then(|v| v.as_str())
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
            "channel_status": if matches!(role, "sensor-gateway" | "care-core") { "seqpacket" } else { "not_applicable" },
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
        last_packet = Some(encoded.clone());
        if index == 0 {
            ipc::send(&sock, &encoded)?;
        }
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

#[allow(clippy::type_complexity)]
fn command_packet(
    command: &str,
    secret: &[u8],
    generation: &str,
    previous: Option<&[u8]>,
) -> Result<(Option<Vec<u8>>, bool), Box<dyn std::error::Error>> {
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
    if command == "inject_unknown_field" || command == "inject_companion_state" {
        value["mood"] = json!("forbidden");
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
    let unsigned = canonical::canonical_event(&serde_json::to_vec(&value)?)?;
    value["mac"] = json!(mac(secret, &unsigned)?);
    Ok((Some(serde_json::to_vec(&value)?), true))
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
        let duplicate = if let Some(id) = msg {
            seen.contains(id) || store.receipt_exists(id)?
        } else {
            false
        };
        let mut reason = if duplicate { "duplicate" } else { "rejected" };
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
        if let Some(id) = msg {
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

fn spawn_direct_children(
    exe: &std::path::Path,
    ready_dir: &std::path::Path,
    secret: &[u8],
    boot: &str,
) -> Result<(ChildEntry, Option<ChildEntry>, OwnedFd), Box<dyn std::error::Error>> {
    let (producer_endpoint, care_endpoint) = ipc::seqpacket_pair()?;
    ipc::enable_passcred(&producer_endpoint)?;
    ipc::enable_passcred(&care_endpoint)?;
    let (producer_cap_read, producer_cap_write) = pipe()?;
    let (care_cap_read, care_cap_write) = pipe()?;
    let (producer_control_read, producer_control_write) = pipe()?;
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
    Ok((producer_entry, care_entry, producer_control_write))
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
    let mut children = Vec::new();
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
    let (producer_entry, care_entry, mut producer_control) =
        spawn_direct_children(&exe, &ready_dir, &secret, &boot)?;
    children.push(producer_entry);
    if let Some(care_entry) = care_entry {
        children.push(care_entry);
    }
    let once = env::args().any(|a| a == "--once");
    let deadline = Instant::now() + Duration::from_secs(10);
    loop {
        if let Ok((mut stream, _)) = listener.accept() {
            let mut request = Vec::new();
            let _ = stream.set_read_timeout(Some(Duration::from_millis(50)));
            let _ = stream.read_to_end(&mut request);
            let command = serde_json::from_slice::<serde_json::Value>(&request).ok();
            let response = handle_control(command.as_ref(), &mut children, Some(&producer_control));
            if response.get("command").and_then(|v| v.as_str()) == Some("shutdown") {
                STOP.store(true, Ordering::SeqCst);
            }
            let encoded = if command.is_some() {
                serde_json::to_string(&response)?
            } else {
                health_json(&mut children)
            };
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
            let (producer_entry, care_entry, new_control) =
                spawn_direct_children(&exe, &ready_dir, &secret, &boot)?;
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
            let kind = command
                .get("kind")
                .and_then(|v| v.as_str())
                .unwrap_or("valid");
            let opcode = match kind {
                "valid" | "valid_safety_candidate" => "inject_valid",
                "ordinary_observation" => "inject_ordinary",
                other => other,
            };
            if let Some(fd) = producer_control {
                let result = write_fd(fd, format!("{opcode}\n").as_bytes());
                return json!({"command":"inject","kind":kind,"accepted":result.is_ok(),"observed":"producer_control_channel"});
            }
            json!({"command":"inject","kind":kind,"accepted":false,"reason":"producer_control_unavailable"})
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
}

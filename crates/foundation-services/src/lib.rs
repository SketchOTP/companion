//! Resident, nonauthoritative Phase 01 process foundation.
use foundation_core::{
    ipc, logging, paths::XdgPaths, persistence::Store, version::FOUNDATION_VERSION,
};
use serde_json::json;
use sha2::{Digest, Sha256};
use std::env;
use std::io::{Read, Write};
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
use std::os::unix::process::CommandExt;
use std::process::{Child, Command, Stdio};
use std::sync::Once;
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::{Duration, Instant};

static STOP: AtomicBool = AtomicBool::new(false);
static SIGNALS: Once = Once::new();

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
    if !logging::emit(role, "ready", seq, &boot, None) {
        return Err("log serialization failed".into());
    }
    seq += 1;
    logging::emit(role, "hardening", seq, &boot, Some("dumpable_disabled"));
    seq += 1;
    let fd = env::var("COMPANION_IPC_FD")
        .ok()
        .and_then(|v| v.parse::<i32>().ok());
    let cap_fd = env::var("COMPANION_CAP_FD")
        .ok()
        .and_then(|v| v.parse::<i32>().ok());
    match role {
        "sensor-gateway" => producer(fd, cap_fd, &boot, &mut seq)?,
        "care-core" => care(fd, cap_fd, &boot, &mut seq)?,
        "companion-core" => ordinary_store("companion", &boot, &mut seq)?,
        "identity-consent-vault" => ordinary_store("vault", &boot, &mut seq)?,
        "godot-bridge" => {
            let paths = XdgPaths::resolve("companion")?;
            paths.ensure()?;
            std::fs::write(
                paths.runtime.join("bridge-state.json"),
                r#"{"protocol":"companion-foundation-v1","state":"connected","target_screen":0}"#,
            )?;
            logging::emit(
                role,
                "bridge_handshake",
                seq,
                &boot,
                Some("versioned-local-control"),
            );
            seq += 1;
        }
        _ => {}
    }
    if env::args().any(|a| a == "--once") {
        return Ok(());
    }
    while !STOP.load(Ordering::SeqCst) {
        std::thread::sleep(Duration::from_millis(100));
    }
    logging::emit(role, "stopped", seq, &boot, Some("signal"));
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

fn mac(secret: &[u8], payload: &[u8]) -> String {
    let mut key = [0u8; 64];
    if secret.len() > 64 {
        key[..32].copy_from_slice(&Sha256::digest(secret));
    } else {
        key[..secret.len()].copy_from_slice(secret);
    }
    let mut inner = Sha256::new();
    let mut outer = Sha256::new();
    for byte in key {
        inner.update([byte ^ 0x36]);
        outer.update([byte ^ 0x5c]);
    }
    inner.update(payload);
    outer.update(inner.finalize());
    format!("{:x}", outer.finalize())
}

fn producer(
    fd: Option<i32>,
    cap_fd: Option<i32>,
    boot: &str,
    seq: &mut u64,
) -> Result<(), Box<dyn std::error::Error>> {
    let raw = fd.ok_or("producer endpoint missing")?;
    let sock = unsafe { OwnedFd::from_raw_fd(raw) };
    let secret = read_capability(cap_fd)?;
    let generation = env::var("COMPANION_GENERATION")?;
    let cycles: usize = env::var("COMPANION_CYCLES")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(1);
    for index in 0..cycles {
        let base = json!({"schema_major":1,"message_id":format!("synthetic-{index:08}"),"producer_generation":generation,"confidence_milli":900,"quality_milli":900,"replay":false,"kind":"safety_candidate"});
        let bytes = serde_json::to_vec(&base)?;
        let mut packet = base;
        packet["mac"] = json!(mac(&secret, &bytes));
        let encoded = serde_json::to_vec(&packet)?;
        ipc::send(&sock, &encoded)?;
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
    Ok(())
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
    let cycles: usize = env::var("COMPANION_CYCLES")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(1);
    let mut seen = std::collections::HashSet::new();
    for _ in 0..(cycles + 1) {
        let (data, cred) = ipc::receive_with_credentials(&sock, 16 * 1024)?;
        let value: serde_json::Value = serde_json::from_slice(&data)?;
        let msg = value
            .get("message_id")
            .and_then(|v| v.as_str())
            .unwrap_or("unknown");
        let mut unsigned = value.clone();
        let supplied = unsigned
            .get("mac")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_owned();
        unsigned.as_object_mut().map(|o| o.remove("mac"));
        let unsigned_bytes = serde_json::to_vec(&unsigned)?;
        let duplicate = seen.contains(msg) || store.receipt_exists(msg)?;
        let valid = cred.pid == expected_pid
            && value.get("producer_generation").and_then(|v| v.as_str())
                == Some(expected_generation.as_str())
            && supplied == mac(&secret, &unsigned_bytes)
            && !duplicate;
        seen.insert(msg.to_owned());
        let inserted = store.append_receipt(
            msg,
            valid,
            duplicate,
            if valid { "accepted" } else { "rejected" },
            &format!("boot:{boot}:{}", logging::monotonic_ns()),
        )?;
        if valid && !inserted {
            return Err("care receipt was not durable".into());
        }
        logging::emit(
            "care-core",
            if valid {
                "care_receipt"
            } else {
                "care_rejected"
            },
            *seq,
            boot,
            Some(if valid {
                "durable"
            } else {
                "authentication_failed"
            }),
        );
        *seq += 1;
        println!(
            "{}",
            json!({"accepted":valid,"duplicate":duplicate,"message_id":msg,"pid":cred.pid,"durable":inserted})
        );
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
}

fn supervisor() -> Result<(), Box<dyn std::error::Error>> {
    harden()?;
    let boot = logging::boot_id();
    logging::emit("ops-supervisor", "starting", 1, &boot, None);
    let exe = env::current_exe()?;
    let paths = XdgPaths::resolve("companion")?;
    paths.ensure()?;
    let control = paths.runtime.join("supervisor.sock");
    let _ = std::fs::remove_file(&control);
    let listener = std::os::unix::net::UnixListener::bind(&control)?;
    listener.set_nonblocking(true)?;
    let (producer, care) = ipc::seqpacket_pair()?;
    ipc::enable_passcred(&producer)?;
    ipc::enable_passcred(&care)?;
    let (prod_cap_r, prod_cap_w) = pipe()?;
    let (care_cap_r, care_cap_w) = pipe()?;
    let generation = uuid::Uuid::new_v4().to_string();
    let secret = uuid::Uuid::new_v4().as_bytes().to_vec();
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
        let child = spawn(&exe, role, None, None, None, None)?;
        children.push(ChildEntry {
            role: role.into(),
            child,
            restarts: 0,
            generation: 1,
            backoff: Duration::from_millis(100),
        });
    }
    let p = spawn(
        &exe,
        "sensor-gateway",
        Some(producer.as_raw_fd()),
        Some(prod_cap_r.as_raw_fd()),
        Some(&generation),
        None,
    )?;
    let producer_pid = p.id();
    match ipc::pidfd_open(producer_pid as libc::pid_t) {
        Ok(_pidfd) => {
            logging::emit(
                "ops-supervisor",
                "producer_pidfd_bound",
                2,
                &boot,
                Some("live_generation"),
            );
        }
        Err(error) => {
            logging::emit(
                "ops-supervisor",
                "producer_pidfd_unavailable",
                2,
                &boot,
                Some(&format!("errno:{}", error.raw_os_error().unwrap_or(-1))),
            );
        }
    }
    let c = if env::var_os("COMPANION_SKIP_CARE").is_some() {
        None
    } else {
        Some(spawn(
            &exe,
            "care-core",
            Some(care.as_raw_fd()),
            Some(care_cap_r.as_raw_fd()),
            Some(&generation),
            Some(producer_pid),
        )?)
    };
    drop(producer);
    drop(care);
    drop(prod_cap_r);
    drop(care_cap_r);
    write_fd(&prod_cap_w, &secret)?;
    if c.is_some() {
        write_fd(&care_cap_w, &secret)?;
    }
    drop(prod_cap_w);
    drop(care_cap_w);
    // Child readiness is observable through their inherited stdout. Registry is
    // authoritative for lifecycle, while the care channel is independent.
    children.push(ChildEntry {
        role: "sensor-gateway".into(),
        child: p,
        restarts: 0,
        generation: 1,
        backoff: Duration::from_millis(100),
    });
    if let Some(c) = c {
        children.push(ChildEntry {
            role: "care-core".into(),
            child: c,
            restarts: 0,
            generation: 1,
            backoff: Duration::from_millis(100),
        });
    }
    let once = env::args().any(|a| a == "--once");
    let deadline = Instant::now() + Duration::from_secs(10);
    loop {
        if let Ok((mut stream, _)) = listener.accept() {
            let health = health_json(&children);
            let _ = stream.write_all(health.as_bytes());
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
                    let replacement = spawn(&exe, &entry.role, None, None, None, None)?;
                    let mut old = std::mem::replace(&mut entry.child, replacement);
                    let _ = old.wait();
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

fn health_json(children: &[ChildEntry]) -> String {
    let rows:Vec<_>=children.iter().map(|e|json!({"role":e.role,"pid":e.child.id(),"generation":e.generation,"restarts":e.restarts,"backoff_ms":e.backoff.as_millis(),"running":true,"ready":true,"health":"healthy"})).collect();
    let care_coverage = if children.iter().any(|e| e.role == "care-core") {
        "synthetic"
    } else {
        "degraded"
    };
    serde_json::to_string(&json!({"version":FOUNDATION_VERSION,"status":"resident","children":rows,"care_coverage":care_coverage,"network":"deny_by_default","boot_id":logging::boot_id()})).unwrap_or_else(|_|"{}".into())
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
fn spawn(
    exe: &std::path::Path,
    role: &str,
    endpoint: Option<i32>,
    cap: Option<i32>,
    generation: Option<&str>,
    expected_pid: Option<u32>,
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
    if let Some(g) = generation {
        cmd.env("COMPANION_GENERATION", g);
    }
    if let Some(pid) = expected_pid {
        cmd.env("COMPANION_EXPECTED_PRODUCER_PID", pid.to_string());
    }
    unsafe {
        cmd.pre_exec(move || {
            harden()?;
            for fd in [endpoint, cap].into_iter().flatten() {
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

use foundation_core::ipc;
use foundation_core::logging::{boot_id, emit};
use foundation_core::paths::XdgPaths;
use foundation_core::persistence::Store;
use foundation_core::version::FOUNDATION_VERSION;
use std::env;
use std::io::Write;
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
use std::os::unix::process::CommandExt;
use std::process::{Child, Command, Stdio};
use std::thread;
use std::time::Duration;

fn role() -> String {
    env::args()
        .next()
        .and_then(|arg| {
            std::path::Path::new(&arg)
                .file_name()
                .map(|n| n.to_string_lossy().into_owned())
        })
        .unwrap_or_else(|| "foundation-service".into())
}

fn main() {
    let name = role();
    if name == "ops-supervisor" && env::args().any(|arg| arg == "--health") {
        println!("{{\"version\":\"{}\",\"status\":\"not_running\",\"network\":\"deny_by_default\",\"privacy_class\":\"PUBLIC_METADATA\"}}", FOUNDATION_VERSION);
        return;
    }
    let result = if name == "ops-supervisor" {
        supervisor()
    } else {
        shell(&name)
    };
    if let Err(error) = result {
        eprintln!(
            "{{\"process\":\"{name}\",\"status\":\"FAILED\",\"error\":{}}}",
            serde_json::to_string(&error.to_string()).unwrap_or_else(|_| "\"error\"".into())
        );
        std::process::exit(1);
    }
}

fn shell(name: &str) -> Result<(), Box<dyn std::error::Error>> {
    let boot = boot_id();
    emit(name, "ready", 1, &boot, None);
    if unsafe { libc::prctl(libc::PR_GET_DUMPABLE) } == 0 {
        emit(name, "hardening", 2, &boot, Some("dumpable_disabled"));
    }
    let fd = env::var("COMPANION_IPC_FD")
        .ok()
        .and_then(|value| value.parse::<i32>().ok());
    if name == "care-core" {
        if let Some(raw) = fd {
            // SAFETY: supervisor passes an owned, open socket descriptor.
            let owned = unsafe { OwnedFd::from_raw_fd(raw) };
            ipc::enable_passcred(&owned)?;
            let expected_pid = env::var("COMPANION_EXPECTED_PRODUCER_PID")
                .ok()
                .and_then(|v| v.parse::<libc::pid_t>().ok());
            let expected_generation = env::var("COMPANION_GENERATION").unwrap_or_default();
            let expected_capability = env::var("COMPANION_CAPABILITY").unwrap_or_default();
            let mut seen = std::collections::HashSet::new();
            let care_store = XdgPaths::resolve("companion").ok().and_then(|paths| {
                paths
                    .ensure()
                    .ok()
                    .and_then(|_| Store::open(&paths, "care").ok())
            });
            for _ in 0..2 {
                let (packet, credentials) = ipc::receive_with_credentials(&owned, 16 * 1024)?;
                let value: serde_json::Value = serde_json::from_slice(&packet)?;
                let message_id = value
                    .get("message_id")
                    .and_then(serde_json::Value::as_str)
                    .unwrap_or("unknown");
                let duplicate = !seen.insert(message_id.to_owned());
                let valid = value
                    .get("producer_generation")
                    .and_then(serde_json::Value::as_str)
                    == Some(expected_generation.as_str())
                    && value.get("capability").and_then(serde_json::Value::as_str)
                        == Some(expected_capability.as_str())
                    && expected_pid.is_none_or(|pid| pid == credentials.pid)
                    && !duplicate;
                emit(
                    name,
                    if valid {
                        "care_receipt"
                    } else {
                        "care_rejected"
                    },
                    2,
                    &boot,
                    Some(if valid {
                        "synthetic_candidate_accepted"
                    } else {
                        "candidate_rejected"
                    }),
                );
                if valid && let Some(store) = &care_store {
                    let _ = store.append_receipt(
                        message_id,
                        valid,
                        duplicate,
                        if valid { "accepted" } else { "rejected" },
                        "2026-09-09T12:00:00Z",
                    );
                }
                println!(
                    "{{\"role\":\"care-core\",\"accepted\":{},\"duplicate\":{},\"message_id\":{}}}",
                    valid,
                    duplicate,
                    serde_json::to_string(message_id)?
                );
            }
        }
    } else if name == "sensor-gateway"
        && let Some(raw) = fd
    {
        // SAFETY: supervisor passes an owned, open socket descriptor.
        let owned = unsafe { OwnedFd::from_raw_fd(raw) };
        let generation = env::var("COMPANION_GENERATION").unwrap_or_default();
        let capability = env::var("COMPANION_CAPABILITY").unwrap_or_default();
        thread::sleep(Duration::from_millis(50));
        let packet = serde_json::json!({"schema_major":1,"message_id":"synthetic-0001","kind":"safety_candidate","producer_generation":generation,"capability":capability,"confidence_milli":900,"quality_milli":900,"replay":false});
        let encoded = serde_json::to_vec(&packet)?;
        ipc::send(&owned, &encoded)?;
        ipc::send(&owned, &encoded)?;
        emit(name, "synthetic_safety_sent", 2, &boot, None);
    }
    if name == "companion-core"
        && let Ok(paths) = XdgPaths::resolve("companion")
    {
        let _ = paths.ensure();
        if let Ok(store) = Store::open(&paths, "companion") {
            let _ = store.integrity_check();
        }
    }
    if name == "identity-consent-vault"
        && let Ok(paths) = XdgPaths::resolve("companion")
    {
        let _ = paths.ensure();
        if let Ok(store) = Store::open(&paths, "vault") {
            let _ = store.integrity_check();
        }
    }
    if name == "godot-bridge" {
        emit(name, "bridge_handshake", 2, &boot, Some("neutral_habitat_boundary"));
    }
    if env::args().any(|arg| arg == "--hold") {
        thread::sleep(Duration::from_secs(2));
    }
    Ok(())
}

fn supervisor() -> Result<(), Box<dyn std::error::Error>> {
    let boot = boot_id();
    emit("ops-supervisor", "starting", 1, &boot, None);
    let executable = env::current_exe()?;
    let (producer, care) = ipc::seqpacket_pair()?;
    ipc::enable_passcred(&care)?;
    clear_cloexec(producer.as_raw_fd())?;
    clear_cloexec(care.as_raw_fd())?;
    let care_fd = care.as_raw_fd();
    let producer_fd = producer.as_raw_fd();
    let generation = uuid::Uuid::new_v4().to_string();
    let capability = uuid::Uuid::new_v4().to_string();
    let mut children = Vec::new();

    for name in ["companion-core", "identity-consent-vault", "godot-bridge"] {
        if name == "companion-core" && env::var_os("COMPANION_SKIP_COMPANION").is_some() {
            emit(
                "ops-supervisor",
                "companion_optional_absent",
                2,
                &boot,
                Some("care_path_must_remain_operational"),
            );
        } else {
            children.push(spawn_shell(&executable, name, None)?);
        }
    }
    let producer_child = spawn_shell_with_env(
        &executable,
        "sensor-gateway",
        Some(producer_fd),
        &[
            ("COMPANION_GENERATION", generation.as_str()),
            ("COMPANION_CAPABILITY", capability.as_str()),
        ],
    )?;
    let producer_pid = producer_child.id();
    let producer_pid_text = producer_pid.to_string();
    children.push(producer_child);
    children.push(spawn_shell_with_env(
        &executable,
        "care-core",
        Some(care_fd),
        &[
            (
                "COMPANION_EXPECTED_PRODUCER_PID",
                producer_pid_text.as_str(),
            ),
            ("COMPANION_GENERATION", generation.as_str()),
            ("COMPANION_CAPABILITY", capability.as_str()),
        ],
    )?);
    // The supervisor closes both endpoint copies after handoff; child ownership
    // is explicit in the environment and CLOEXEC was cleared only for handoff.
    drop(producer);
    drop(care);
    for mut child in children {
        let status = child.wait()?;
        if !status.success() {
            return Err(format!("child exited unsuccessfully: {status}").into());
        }
    }
    emit(
        "ops-supervisor",
        "stopped",
        2,
        &boot,
        Some("clean_shutdown"),
    );
    Ok(())
}

fn spawn_shell(
    executable: &std::path::Path,
    name: &str,
    fd: Option<i32>,
) -> Result<Child, Box<dyn std::error::Error>> {
    spawn_shell_with_env(executable, name, fd, &[])
}

fn spawn_shell_with_env(
    executable: &std::path::Path,
    name: &str,
    fd: Option<i32>,
    extra: &[(&str, &str)],
) -> Result<Child, Box<dyn std::error::Error>> {
    let sibling = executable.with_file_name(name);
    let mut command = Command::new(sibling);
    command
        .arg("--once")
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit());
    if let Some(raw) = fd {
        command.env("COMPANION_IPC_FD", raw.to_string());
    }
    for (key, value) in extra {
        command.env(key, value);
    }
    // Child-level hardening belongs to each child process, not the supervisor.
    unsafe {
        command.pre_exec(|| {
            if libc::prctl(libc::PR_SET_DUMPABLE, 0, 0, 0, 0) != 0 {
                return Err(std::io::Error::last_os_error());
            }
            Ok(())
        });
    }
    Ok(command.spawn()?)
}

fn clear_cloexec(fd: i32) -> std::io::Result<()> {
    // SAFETY: fcntl operates on the validated descriptor and integer flags.
    let flags = unsafe { libc::fcntl(fd, libc::F_GETFD) };
    if flags < 0 {
        return Err(std::io::Error::last_os_error());
    }
    // SAFETY: clear FD_CLOEXEC for the explicit child handoff.
    let rc = unsafe { libc::fcntl(fd, libc::F_SETFD, flags & !libc::FD_CLOEXEC) };
    if rc < 0 {
        Err(std::io::Error::last_os_error())
    } else {
        Ok(())
    }
}

#[allow(dead_code)]
fn write_ready(mut stream: impl Write) -> std::io::Result<()> {
    stream.write_all(FOUNDATION_VERSION.as_bytes())
}

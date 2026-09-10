use crate::version::FOUNDATION_VERSION;
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct LogRecord<'a> {
    pub process: &'a str,
    pub version: &'static str,
    pub event: &'a str,
    pub severity: &'a str,
    pub privacy_class: &'a str,
    pub boot_id: &'a str,
    pub sequence: u64,
    pub correlation_id: Option<&'a str>,
    pub causation_id: Option<&'a str>,
    pub reason: Option<&'a str>,
}

pub fn boot_id() -> String {
    std::fs::read_to_string("/proc/sys/kernel/random/boot_id")
        .map(|v| v.trim().to_owned())
        .ok()
        .filter(|v| !v.is_empty())
        .unwrap_or_else(|| "boot-unknown".to_owned())
}

pub fn monotonic_ns() -> u64 {
    unsafe {
        let mut ts = libc::timespec {
            tv_sec: 0,
            tv_nsec: 0,
        };
        if libc::clock_gettime(libc::CLOCK_MONOTONIC, &mut ts) == 0 {
            return (ts.tv_sec.max(0) as u64)
                .saturating_mul(1_000_000_000)
                .saturating_add(ts.tv_nsec.max(0) as u64);
        }
    }
    0
}

pub fn emit(process: &str, event: &str, sequence: u64, boot: &str, reason: Option<&str>) -> bool {
    let record = LogRecord {
        process,
        version: FOUNDATION_VERSION,
        event,
        severity: "INFO",
        privacy_class: "PUBLIC_METADATA",
        boot_id: boot,
        sequence,
        correlation_id: None,
        causation_id: None,
        reason,
    };
    match serde_json::to_string(&record) {
        Ok(json) => {
            println!("{json}");
            true
        }
        Err(_) => false,
    }
}

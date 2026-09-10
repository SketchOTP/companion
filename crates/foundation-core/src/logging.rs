use crate::version::FOUNDATION_VERSION;
use serde::Serialize;
use std::time::{SystemTime, UNIX_EPOCH};

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
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    format!("boot-{nanos:x}")
}

pub fn emit(process: &str, event: &str, sequence: u64, boot: &str, reason: Option<&str>) {
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
    if let Ok(json) = serde_json::to_string(&record) {
        println!("{json}");
    }
}

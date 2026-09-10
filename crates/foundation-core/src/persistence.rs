use crate::paths::{PathError, XdgPaths};
use std::path::PathBuf;
use std::process::Command;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum StoreError {
    #[error("path: {0}")]
    Path(#[from] PathError),
    #[error("sqlite command failed: {0}")]
    Sqlite(String),
    #[error("io: {0}")]
    Io(#[from] std::io::Error),
}

#[derive(Debug, Clone)]
pub struct Store {
    pub authority: String,
    pub path: PathBuf,
    sqlite: PathBuf,
}

impl Store {
    pub fn open(paths: &XdgPaths, authority: &str) -> Result<Self, StoreError> {
        let sqlite = std::env::var_os("COMPANION_SQLITE_BIN")
            .map(PathBuf::from)
            .unwrap_or_else(|| PathBuf::from("sqlite3"));
        let path = paths.store(authority)?;
        let store = Self {
            authority: authority.to_owned(),
            path,
            sqlite,
        };
        store.migrate()?;
        Ok(store)
    }

    pub fn migrate(&self) -> Result<(), StoreError> {
        let authority_table = match self.authority.as_str() {
            "care" => {
                "CREATE TABLE IF NOT EXISTS safety_receipts (id INTEGER PRIMARY KEY, candidate_id TEXT UNIQUE NOT NULL, accepted INTEGER NOT NULL, duplicate INTEGER NOT NULL, reason TEXT NOT NULL, created_utc TEXT NOT NULL);"
            }
            "vault" => {
                "CREATE TABLE IF NOT EXISTS privileged_audit (id INTEGER PRIMARY KEY, event_type TEXT NOT NULL, outcome TEXT NOT NULL, created_utc TEXT NOT NULL);"
            }
            _ => {
                "CREATE TABLE IF NOT EXISTS event_log (id INTEGER PRIMARY KEY, message_id TEXT UNIQUE NOT NULL, event_type TEXT NOT NULL, payload TEXT NOT NULL, created_utc TEXT NOT NULL);"
            }
        };
        let sql = format!(
            "PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; CREATE TABLE IF NOT EXISTS authority_meta (k TEXT PRIMARY KEY, v TEXT NOT NULL); {authority_table} INSERT OR IGNORE INTO authority_meta(k,v) VALUES ('authority','{}'),('schema_version','1');",
            self.authority,
        );
        self.exec(&sql)
    }

    pub fn append_event(
        &self,
        message_id: &str,
        event_type: &str,
        payload: &str,
        utc: &str,
    ) -> Result<bool, StoreError> {
        let escaped = |s: &str| s.replace('\'', "''");
        let sql = format!(
            "BEGIN IMMEDIATE; INSERT OR IGNORE INTO event_log(message_id,event_type,payload,created_utc) VALUES ('{}','{}','{}','{}'); SELECT changes(); COMMIT;",
            escaped(message_id),
            escaped(event_type),
            escaped(payload),
            escaped(utc)
        );
        let output = self.output(&sql)?;
        Ok(output.trim().ends_with('1'))
    }

    pub fn append_receipt(
        &self,
        candidate_id: &str,
        accepted: bool,
        duplicate: bool,
        reason: &str,
        utc: &str,
    ) -> Result<bool, StoreError> {
        let escaped = |s: &str| s.replace('\'', "''");
        let sql = format!(
            "BEGIN IMMEDIATE; INSERT OR IGNORE INTO safety_receipts(candidate_id,accepted,duplicate,reason,created_utc) VALUES ('{}',{},{},'{}','{}'); SELECT changes(); COMMIT;",
            escaped(candidate_id),
            i32::from(accepted),
            i32::from(duplicate),
            escaped(reason),
            escaped(utc)
        );
        Ok(self.output(&sql)?.trim().ends_with('1'))
    }

    pub fn integrity_check(&self) -> Result<bool, StoreError> {
        Ok(self.output("PRAGMA integrity_check;")?.trim() == "ok")
    }

    pub fn backup_to(&self, destination: &std::path::Path) -> Result<(), StoreError> {
        if destination.exists() {
            std::fs::remove_file(destination)?;
        }
        let sql = format!(".backup {}", destination.display());
        self.exec(&sql)
    }

    fn exec(&self, sql: &str) -> Result<(), StoreError> {
        self.output(sql).map(|_| ())
    }

    fn output(&self, sql: &str) -> Result<String, StoreError> {
        let output = Command::new(&self.sqlite)
            .arg("-batch")
            .arg("-noheader")
            .arg(&self.path)
            .arg(sql)
            .output()?;
        if output.status.success() {
            Ok(String::from_utf8_lossy(&output.stdout).to_string())
        } else {
            Err(StoreError::Sqlite(
                String::from_utf8_lossy(&output.stderr).trim().to_owned(),
            ))
        }
    }
}

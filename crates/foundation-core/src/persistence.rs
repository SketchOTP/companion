//! Fail-closed SQLite authority stores.
//!
//! Values use prepared statements and bound parameters.  The authoritative
//! services link the SQLite ABI directly; they never invoke a PATH-selected
//! `sqlite3` subprocess.
use crate::paths::{PathError, XdgPaths};
use sha2::{Digest, Sha256};
use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int, c_void};
use std::path::{Path, PathBuf};
use thiserror::Error;

#[allow(non_camel_case_types)]
enum sqlite3 {}
#[allow(non_camel_case_types)]
enum sqlite3_stmt {}
#[allow(non_camel_case_types)]
enum sqlite3_backup {}
const SQLITE_OK: c_int = 0;
const SQLITE_ROW: c_int = 100;
const SQLITE_DONE: c_int = 101;
const SQLITE_OPEN_READWRITE: c_int = 2;
const SQLITE_OPEN_CREATE: c_int = 4;
const SQLITE_OPEN_FULLMUTEX: c_int = 0x00010000;
const SQLITE_TRANSIENT: usize = usize::MAX;

#[link(name = "sqlite3")]
unsafe extern "C" {
    fn sqlite3_libversion() -> *const c_char;
    fn sqlite3_sourceid() -> *const c_char;
    fn sqlite3_compileoption_get(index: c_int) -> *const c_char;
    fn sqlite3_open_v2(
        filename: *const c_char,
        db: *mut *mut sqlite3,
        flags: c_int,
        zvfs: *const c_char,
    ) -> c_int;
    fn sqlite3_close(db: *mut sqlite3) -> c_int;
    fn sqlite3_errmsg(db: *mut sqlite3) -> *const c_char;
    fn sqlite3_exec(
        db: *mut sqlite3,
        sql: *const c_char,
        callback: Option<
            unsafe extern "C" fn(*mut c_void, c_int, *mut *mut c_char, *mut *mut c_char) -> c_int,
        >,
        arg: *mut c_void,
        errmsg: *mut *mut c_char,
    ) -> c_int;
    fn sqlite3_free(ptr: *mut c_void);
    fn sqlite3_prepare_v2(
        db: *mut sqlite3,
        sql: *const c_char,
        nbyte: c_int,
        stmt: *mut *mut sqlite3_stmt,
        tail: *mut *const c_char,
    ) -> c_int;
    fn sqlite3_bind_text(
        stmt: *mut sqlite3_stmt,
        index: c_int,
        value: *const c_char,
        length: c_int,
        destructor: usize,
    ) -> c_int;
    fn sqlite3_bind_int(stmt: *mut sqlite3_stmt, index: c_int, value: c_int) -> c_int;
    fn sqlite3_step(stmt: *mut sqlite3_stmt) -> c_int;
    fn sqlite3_changes(db: *mut sqlite3) -> c_int;
    fn sqlite3_finalize(stmt: *mut sqlite3_stmt) -> c_int;
    fn sqlite3_column_int(stmt: *mut sqlite3_stmt, index: c_int) -> c_int;
    fn sqlite3_column_text(stmt: *mut sqlite3_stmt, index: c_int) -> *const c_char;
    fn sqlite3_backup_init(
        dst: *mut sqlite3,
        dst_name: *const c_char,
        src: *mut sqlite3,
        src_name: *const c_char,
    ) -> *mut sqlite3_backup;
    fn sqlite3_backup_step(backup: *mut sqlite3_backup, pages: c_int) -> c_int;
    fn sqlite3_backup_finish(backup: *mut sqlite3_backup) -> c_int;
}

#[derive(Debug, Error)]
pub enum StoreError {
    #[error("path: {0}")]
    Path(#[from] PathError),
    #[error("sqlite {code}: {message}")]
    Sqlite { code: i32, message: String },
    #[error("io: {0}")]
    Io(#[from] std::io::Error),
    #[error("invalid authority: {0}")]
    Authority(String),
}

pub fn runtime_identity() -> (String, String) {
    unsafe {
        (
            CStr::from_ptr(sqlite3_libversion())
                .to_string_lossy()
                .into_owned(),
            CStr::from_ptr(sqlite3_sourceid())
                .to_string_lossy()
                .into_owned(),
        )
    }
}

/// Return the compile-time options exposed by the linked SQLite build. This
/// is evidence metadata only; acceptance still requires the exact source
/// digest and runtime version/source-id checks in the verification harness.
pub fn runtime_compile_options() -> Vec<String> {
    let mut options = Vec::new();
    for index in 0..256 {
        let value = unsafe { sqlite3_compileoption_get(index) };
        if value.is_null() {
            break;
        }
        options.push(
            unsafe { CStr::from_ptr(value) }
                .to_string_lossy()
                .into_owned(),
        );
    }
    options
}

pub struct Store {
    pub authority: String,
    pub path: PathBuf,
    db: *mut sqlite3,
    pub schema_digest: String,
}
impl std::fmt::Debug for Store {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Store")
            .field("authority", &self.authority)
            .field("path", &self.path)
            .field("schema_digest", &self.schema_digest)
            .finish()
    }
}
impl Drop for Store {
    fn drop(&mut self) {
        if !self.db.is_null() {
            unsafe {
                let _ = sqlite3_close(self.db);
            }
        }
    }
}

impl Store {
    pub fn open(paths: &XdgPaths, authority: &str) -> Result<Self, StoreError> {
        if !matches!(authority, "companion" | "care" | "vault") {
            return Err(StoreError::Authority(authority.into()));
        }
        paths.ensure()?;
        let path = paths.store(authority)?;
        let cpath = CString::new(path.to_string_lossy().as_bytes())
            .map_err(|_| StoreError::Authority("path contains NUL".into()))?;
        let mut db = std::ptr::null_mut();
        let rc = unsafe {
            sqlite3_open_v2(
                cpath.as_ptr(),
                &mut db,
                SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE | SQLITE_OPEN_FULLMUTEX,
                std::ptr::null(),
            )
        };
        if rc != SQLITE_OK {
            return Err(sqlite_error(db, rc));
        }
        let migration = migration(authority);
        let store = Self {
            authority: authority.into(),
            path,
            db,
            schema_digest: format!("{:x}", Sha256::digest(migration.as_bytes())),
        };
        store.configure_and_migrate(migration)?;
        Ok(store)
    }
    fn configure_and_migrate(&self, migration: &str) -> Result<(), StoreError> {
        self.exec("PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; PRAGMA foreign_keys=ON;")?;
        let version = self.scalar_int("PRAGMA user_version;")?;
        if version > 1 {
            return Err(StoreError::Sqlite {
                code: 1,
                message: format!("unsupported schema version {version}"),
            });
        }
        if version == 0 {
            self.exec("BEGIN IMMEDIATE;")?;
            match self.exec(migration).and_then(|_| self.exec("COMMIT;")) {
                Ok(()) => {}
                Err(e) => {
                    let _ = self.exec("ROLLBACK;");
                    return Err(e);
                }
            }
        }
        let sql = format!(
            "INSERT OR REPLACE INTO authority_meta(k,v) VALUES ('authority', '{}');",
            self.authority.replace('\'', "''")
        );
        self.exec(&sql)
    }
    pub fn migrate(&self) -> Result<(), StoreError> {
        self.configure_and_migrate(migration(&self.authority))
    }
    pub fn append_event(
        &self,
        message_id: &str,
        event_type: &str,
        payload: &str,
        utc: &str,
    ) -> Result<bool, StoreError> {
        if self.authority != "companion" {
            return Err(StoreError::Authority(
                "event_log belongs to companion".into(),
            ));
        }
        self.insert("INSERT OR IGNORE INTO event_log(message_id,event_type,payload,created_utc) VALUES (?1,?2,?3,?4);", &[(1,message_id),(2,event_type),(3,payload),(4,utc)], &[])
    }
    pub fn append_receipt(
        &self,
        candidate_id: &str,
        accepted: bool,
        duplicate: bool,
        reason: &str,
        utc: &str,
    ) -> Result<bool, StoreError> {
        if self.authority != "care" {
            return Err(StoreError::Authority(
                "safety_receipts belongs to care".into(),
            ));
        }
        self.insert("INSERT OR IGNORE INTO safety_receipts(candidate_id,accepted,duplicate,reason,created_utc) VALUES (?1,?2,?3,?4,?5);", &[(1,candidate_id),(4,reason),(5,utc)], &[(2, accepted), (3, duplicate)])
    }
    fn insert(
        &self,
        sql: &str,
        texts: &[(c_int, &str)],
        ints: &[(c_int, bool)],
    ) -> Result<bool, StoreError> {
        self.exec("BEGIN IMMEDIATE;")?;
        let result = (|| {
            let csql = CString::new(sql).unwrap();
            let mut stmt = std::ptr::null_mut();
            let rc = unsafe {
                sqlite3_prepare_v2(self.db, csql.as_ptr(), -1, &mut stmt, std::ptr::null_mut())
            };
            if rc != SQLITE_OK {
                return Err(sqlite_error(self.db, rc));
            }
            for &(idx, value) in texts {
                let c = CString::new(value)
                    .map_err(|_| StoreError::Authority("value contains NUL".into()))?;
                let rc = unsafe { sqlite3_bind_text(stmt, idx, c.as_ptr(), -1, SQLITE_TRANSIENT) };
                if rc != SQLITE_OK {
                    unsafe {
                        sqlite3_finalize(stmt);
                    }
                    return Err(sqlite_error(self.db, rc));
                }
            }
            for &(idx, value) in ints {
                let rc = unsafe { sqlite3_bind_int(stmt, idx, i32::from(value)) };
                if rc != SQLITE_OK {
                    unsafe {
                        sqlite3_finalize(stmt);
                    }
                    return Err(sqlite_error(self.db, rc));
                }
            }
            let rc = unsafe { sqlite3_step(stmt) };
            unsafe {
                sqlite3_finalize(stmt);
            }
            if rc != SQLITE_DONE {
                return Err(sqlite_error(self.db, rc));
            }
            Ok(unsafe { sqlite3_changes(self.db) == 1 })
        })();
        match result {
            Ok(v) => {
                self.exec("COMMIT;")?;
                Ok(v)
            }
            Err(e) => {
                let _ = self.exec("ROLLBACK;");
                Err(e)
            }
        }
    }
    pub fn integrity_check(&self) -> Result<bool, StoreError> {
        Ok(self.scalar_text("PRAGMA integrity_check;")? == "ok")
    }
    pub fn receipt_exists(&self, candidate_id: &str) -> Result<bool, StoreError> {
        if self.authority != "care" {
            return Err(StoreError::Authority(
                "receipt lookup belongs to care".into(),
            ));
        }
        let sql =
            CString::new("SELECT 1 FROM safety_receipts WHERE candidate_id=?1 LIMIT 1;").unwrap();
        let mut stmt = std::ptr::null_mut();
        let rc = unsafe {
            sqlite3_prepare_v2(self.db, sql.as_ptr(), -1, &mut stmt, std::ptr::null_mut())
        };
        if rc != SQLITE_OK {
            return Err(sqlite_error(self.db, rc));
        };
        let id = CString::new(candidate_id)
            .map_err(|_| StoreError::Authority("candidate contains NUL".into()))?;
        let bind = unsafe { sqlite3_bind_text(stmt, 1, id.as_ptr(), -1, SQLITE_TRANSIENT) };
        let step = if bind == SQLITE_OK {
            unsafe { sqlite3_step(stmt) }
        } else {
            bind
        };
        unsafe { sqlite3_finalize(stmt) };
        if step == SQLITE_ROW {
            Ok(true)
        } else if step == SQLITE_DONE {
            Ok(false)
        } else {
            Err(sqlite_error(self.db, step))
        }
    }
    pub fn checkpoint(&self) -> Result<(), StoreError> {
        self.exec("PRAGMA wal_checkpoint(TRUNCATE);")
    }
    pub fn backup_to(&self, destination: &Path) -> Result<(), StoreError> {
        if destination.exists() {
            std::fs::remove_file(destination)?;
        }
        if let Some(p) = destination.parent() {
            std::fs::create_dir_all(p)?;
        }
        let path = CString::new(destination.to_string_lossy().as_bytes())
            .map_err(|_| StoreError::Authority("backup path contains NUL".into()))?;
        let mut destination = std::ptr::null_mut();
        let rc = unsafe {
            sqlite3_open_v2(
                path.as_ptr(),
                &mut destination,
                SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE | SQLITE_OPEN_FULLMUTEX,
                std::ptr::null(),
            )
        };
        if rc != SQLITE_OK {
            return Err(sqlite_error(destination, rc));
        }
        let main = CString::new("main").unwrap();
        let backup =
            unsafe { sqlite3_backup_init(destination, main.as_ptr(), self.db, main.as_ptr()) };
        if backup.is_null() {
            let e = sqlite_error(destination, 1);
            unsafe {
                sqlite3_close(destination);
            }
            return Err(e);
        }
        let step = unsafe { sqlite3_backup_step(backup, -1) };
        let finish = unsafe { sqlite3_backup_finish(backup) };
        unsafe {
            sqlite3_close(destination);
        }
        if (step == SQLITE_DONE || step == SQLITE_OK) && finish == SQLITE_OK {
            Ok(())
        } else {
            Err(sqlite_error(
                self.db,
                if finish != SQLITE_OK { finish } else { step },
            ))
        }
    }
    fn exec(&self, sql: &str) -> Result<(), StoreError> {
        let c = CString::new(sql).map_err(|_| StoreError::Authority("sql contains NUL".into()))?;
        let mut err = std::ptr::null_mut();
        let rc = unsafe { sqlite3_exec(self.db, c.as_ptr(), None, std::ptr::null_mut(), &mut err) };
        if rc == SQLITE_OK {
            Ok(())
        } else {
            let msg = if err.is_null() {
                self.error_message()
            } else {
                let m = unsafe { CStr::from_ptr(err) }
                    .to_string_lossy()
                    .into_owned();
                unsafe {
                    sqlite3_free(err.cast());
                }
                m
            };
            Err(StoreError::Sqlite {
                code: rc,
                message: msg,
            })
        }
    }
    fn scalar_text(&self, sql: &str) -> Result<String, StoreError> {
        let c = CString::new(sql).unwrap();
        let mut stmt = std::ptr::null_mut();
        let rc =
            unsafe { sqlite3_prepare_v2(self.db, c.as_ptr(), -1, &mut stmt, std::ptr::null_mut()) };
        if rc != SQLITE_OK {
            return Err(sqlite_error(self.db, rc));
        }
        let rc = unsafe { sqlite3_step(stmt) };
        let value = if rc == SQLITE_ROW {
            let p = unsafe { sqlite3_column_text(stmt, 0) };
            if p.is_null() {
                String::new()
            } else {
                unsafe { CStr::from_ptr(p).to_string_lossy().into_owned() }
            }
        } else {
            String::new()
        };
        unsafe {
            sqlite3_finalize(stmt);
        }
        if rc == SQLITE_ROW {
            Ok(value)
        } else {
            Err(sqlite_error(self.db, rc))
        }
    }
    fn scalar_int(&self, sql: &str) -> Result<i32, StoreError> {
        let c = CString::new(sql).unwrap();
        let mut stmt = std::ptr::null_mut();
        let rc =
            unsafe { sqlite3_prepare_v2(self.db, c.as_ptr(), -1, &mut stmt, std::ptr::null_mut()) };
        if rc != SQLITE_OK {
            return Err(sqlite_error(self.db, rc));
        }
        let rc = unsafe { sqlite3_step(stmt) };
        let value = if rc == SQLITE_ROW {
            unsafe { sqlite3_column_int(stmt, 0) }
        } else {
            0
        };
        unsafe {
            sqlite3_finalize(stmt);
        }
        if rc == SQLITE_ROW {
            Ok(value)
        } else {
            Err(sqlite_error(self.db, rc))
        }
    }
    fn error_message(&self) -> String {
        unsafe {
            CStr::from_ptr(sqlite3_errmsg(self.db))
                .to_string_lossy()
                .into_owned()
        }
    }
}
fn sqlite_error(db: *mut sqlite3, code: c_int) -> StoreError {
    let message = if db.is_null() {
        "sqlite open failed".into()
    } else {
        unsafe {
            CStr::from_ptr(sqlite3_errmsg(db))
                .to_string_lossy()
                .into_owned()
        }
    };
    StoreError::Sqlite { code, message }
}
fn migration(authority: &str) -> &'static str {
    match authority {
        "care" => include_str!("../../../migrations/care/001_initial.sql"),
        "vault" => include_str!("../../../migrations/vault/001_initial.sql"),
        _ => include_str!("../../../migrations/companion/001_initial.sql"),
    }
}

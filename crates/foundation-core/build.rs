fn main() {
    let out = std::env::var_os("OUT_DIR").expect("OUT_DIR");
    let out = std::path::PathBuf::from(out);
    const EXPECTED_SQLITE_SHA256: &str =
        "b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189";
    if let Some(source) = std::env::var_os("COMPANION_SQLITE_SOURCE") {
        let source = std::path::PathBuf::from(source);
        if !source.is_file() {
            panic!(
                "COMPANION_SQLITE_SOURCE does not identify a file: {}",
                source.display()
            );
        }
        let digest = std::process::Command::new("sha256sum")
            .arg(&source)
            .output()
            .expect("sha256sum is required to verify exact SQLite source");
        if !digest.status.success() {
            panic!("failed to calculate SQLite source digest");
        }
        let observed = String::from_utf8_lossy(&digest.stdout)
            .split_whitespace()
            .next()
            .unwrap_or_default()
            .to_owned();
        if observed != EXPECTED_SQLITE_SHA256 {
            panic!(
                "SQLite source digest mismatch: expected {EXPECTED_SQLITE_SHA256}, observed {observed}"
            );
        }
        let object = out.join("sqlite3.o");
        let status = std::process::Command::new("cc")
            .args(["-std=c11", "-O2", "-fPIC", "-DSQLITE_THREADSAFE=1", "-c"])
            .arg(&source)
            .args(["-o"])
            .arg(&object)
            .status()
            .expect("cc is required when COMPANION_SQLITE_SOURCE is set");
        if !status.success() {
            panic!(
                "failed to compile exact SQLite source: {}",
                source.display()
            );
        }
        let archive = out.join("libsqlite3.a");
        let status = std::process::Command::new("ar")
            .args(["crus"])
            .arg(&archive)
            .arg(&object)
            .status()
            .expect("ar is required when COMPANION_SQLITE_SOURCE is set");
        if !status.success() {
            panic!("failed to archive exact SQLite object");
        }
        println!("cargo:rustc-link-search=native={}", out.display());
        println!("cargo:rustc-link-lib=static=sqlite3");
        println!("cargo:rerun-if-changed={}", source.display());
        println!("cargo:rerun-if-changed=build.rs");
        return;
    }
    if std::env::var("COMPANION_NONAUTHORITATIVE_HOST_SQLITE").as_deref() != Ok("1") {
        panic!(
            "exact SQLite 3.53.4 source is mandatory; set COMPANION_SQLITE_SOURCE to the verified amalgamation or explicitly opt into the nonauthoritative host fallback with COMPANION_NONAUTHORITATIVE_HOST_SQLITE=1"
        );
    }
    // Explicit developer-only fallback. This can never satisfy Phase 01
    // acceptance because its runtime identity is host-provided.
    let link = out.join("libsqlite3.so");
    if !link.exists() {
        let _ = std::os::unix::fs::symlink("/lib/x86_64-linux-gnu/libsqlite3.so.0", &link);
    }
    println!("cargo:rustc-link-search=native={}", out.display());
    println!("cargo:rustc-link-lib=dylib=sqlite3");
    println!("cargo:rerun-if-changed=build.rs");
}

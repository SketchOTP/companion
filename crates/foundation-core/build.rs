fn main() {
    let out = std::env::var_os("OUT_DIR").expect("OUT_DIR");
    let out = std::path::PathBuf::from(out);
    if let Some(source) = std::env::var_os("COMPANION_SQLITE_SOURCE") {
        let source = std::path::PathBuf::from(source);
        if !source.is_file() {
            panic!(
                "COMPANION_SQLITE_SOURCE does not identify a file: {}",
                source.display()
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
    // Development fallback for hosts without the private exact-source cache.
    // The resulting host-library identity is deliberately not a 3.53.4 claim.
    let link = out.join("libsqlite3.so");
    if !link.exists() {
        let _ = std::os::unix::fs::symlink("/lib/x86_64-linux-gnu/libsqlite3.so.0", &link);
    }
    println!("cargo:rustc-link-search=native={}", out.display());
    println!("cargo:rustc-link-lib=dylib=sqlite3");
    println!("cargo:rerun-if-changed=build.rs");
}

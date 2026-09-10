//! XDG and filesystem policy. Canonical state fails closed when its placement
//! cannot be proven local, private, and outside the checkout.
use std::fs;
use std::path::{Path, PathBuf};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum PathError {
    #[error("unsafe canonical path: {0}")]
    Unsafe(PathBuf),
    #[error("path is on a network filesystem: {0}")]
    Network(PathBuf),
    #[error("required environment variable is missing: {0}")]
    MissingEnv(&'static str),
    #[error("invalid authority identifier: {0}")]
    InvalidAuthority(String),
    #[error("unsafe permissions or ownership: {0}")]
    Permissions(PathBuf),
    #[error("mount metadata unavailable for {0}")]
    MountUnknown(PathBuf),
    #[error("io: {0}")]
    Io(#[from] std::io::Error),
}

#[derive(Debug, Clone)]
pub struct XdgPaths {
    pub config: PathBuf,
    pub data: PathBuf,
    pub state: PathBuf,
    pub cache: PathBuf,
    pub logs: PathBuf,
    pub runtime: PathBuf,
    pub backups: PathBuf,
    pub exports: PathBuf,
    pub secrets: PathBuf,
}

impl XdgPaths {
    pub fn resolve(app: &str) -> Result<Self, PathError> {
        validate_authority(app)?;
        let home = std::env::var_os("HOME")
            .map(PathBuf::from)
            .ok_or(PathError::MissingEnv("HOME"))?;
        let override_root = std::env::var_os("COMPANION_XDG_ROOT").map(PathBuf::from);
        let config_base = override_root
            .clone()
            .or_else(|| std::env::var_os("XDG_CONFIG_HOME").map(PathBuf::from))
            .unwrap_or_else(|| home.join(".config"));
        let data_base = override_root
            .clone()
            .or_else(|| std::env::var_os("XDG_DATA_HOME").map(PathBuf::from))
            .unwrap_or_else(|| home.join(".local/share"));
        let state_base = override_root
            .clone()
            .or_else(|| std::env::var_os("XDG_STATE_HOME").map(PathBuf::from))
            .unwrap_or_else(|| home.join(".local/state"));
        let cache_base = override_root
            .clone()
            .or_else(|| std::env::var_os("XDG_CACHE_HOME").map(PathBuf::from))
            .unwrap_or_else(|| home.join(".cache"));
        let runtime_base = override_root
            .or_else(|| std::env::var_os("XDG_RUNTIME_DIR").map(PathBuf::from))
            .ok_or(PathError::MissingEnv("XDG_RUNTIME_DIR"))?;
        let result = Self {
            config: config_base.join(app),
            data: data_base.join(app),
            state: state_base.join(app),
            cache: cache_base.join(app),
            logs: state_base.join(app).join("logs"),
            runtime: runtime_base.join(app),
            backups: data_base.join(app).join("backups"),
            exports: data_base.join(app).join("exports"),
            secrets: data_base.join(app).join("secrets"),
        };
        result.validate_all()?;
        Ok(result)
    }
    pub fn ensure(&self) -> Result<(), PathError> {
        for path in [
            &self.config,
            &self.data,
            &self.state,
            &self.cache,
            &self.logs,
            &self.runtime,
            &self.backups,
            &self.exports,
            &self.secrets,
        ] {
            fs::create_dir_all(path)?;
            #[cfg(unix)]
            {
                use std::os::unix::fs::PermissionsExt;
                fs::set_permissions(path, fs::Permissions::from_mode(0o700))?;
            }
            self.validate_private(path)?;
        }
        Ok(())
    }
    pub fn store(&self, authority: &str) -> Result<PathBuf, PathError> {
        validate_authority(authority)?;
        let path = self.data.join(format!("{authority}.sqlite3"));
        self.validate(&path)?;
        Ok(path)
    }
    pub fn validate(&self, path: &Path) -> Result<(), PathError> {
        let absolute = if path.is_absolute() {
            path.to_path_buf()
        } else {
            return Err(PathError::Unsafe(path.to_path_buf()));
        };
        if absolute.exists() && fs::symlink_metadata(&absolute)?.file_type().is_symlink() {
            return Err(PathError::Unsafe(absolute));
        }
        if absolute
            .components()
            .any(|c| matches!(c, std::path::Component::ParentDir))
        {
            return Err(PathError::Unsafe(absolute));
        }
        let parent = absolute.parent().unwrap_or(Path::new("/"));
        let canonical_parent = canonicalize_existing(parent)?;
        let candidate = canonical_parent.join(absolute.file_name().unwrap_or_default());
        let cwd = std::env::current_dir()?.canonicalize()?;
        if candidate.starts_with(&cwd)
            || find_repository_root(&cwd).is_some_and(|root| candidate.starts_with(root))
        {
            return Err(PathError::Unsafe(candidate));
        }
        match mount_kind(&candidate)? {
            Some(kind) if is_network_fs(&kind) => Err(PathError::Network(candidate)),
            Some(_) => Ok(()),
            None => Err(PathError::MountUnknown(candidate)),
        }
    }
    fn validate_all(&self) -> Result<(), PathError> {
        for p in [
            &self.config,
            &self.data,
            &self.state,
            &self.cache,
            &self.logs,
            &self.runtime,
            &self.backups,
            &self.exports,
            &self.secrets,
        ] {
            self.validate(p)?;
        }
        Ok(())
    }
    fn validate_private(&self, path: &Path) -> Result<(), PathError> {
        #[cfg(unix)]
        {
            use std::os::unix::fs::{MetadataExt, PermissionsExt};
            let m = fs::metadata(path)?;
            if m.uid() != unsafe { libc::geteuid() } || (m.permissions().mode() & 0o077) != 0 {
                return Err(PathError::Permissions(path.to_path_buf()));
            }
        }
        Ok(())
    }
}
fn validate_authority(value: &str) -> Result<(), PathError> {
    if value.is_empty()
        || !value
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-' || b == b'_')
    {
        return Err(PathError::InvalidAuthority(value.into()));
    }
    Ok(())
}
fn canonicalize_existing(path: &Path) -> Result<PathBuf, PathError> {
    let mut current = path.to_path_buf();
    while !current.exists() {
        current = current
            .parent()
            .ok_or_else(|| PathError::Unsafe(path.to_path_buf()))?
            .to_path_buf();
    }
    let base = current.canonicalize()?;
    let tail = path.strip_prefix(&current).unwrap_or(Path::new(""));
    Ok(base.join(tail))
}
fn find_repository_root(start: &Path) -> Option<PathBuf> {
    let mut p = Some(start);
    while let Some(v) = p {
        if v.join(".git").exists() {
            return Some(v.to_path_buf());
        }
        p = v.parent();
    }
    None
}
fn mount_kind(path: &Path) -> Result<Option<String>, PathError> {
    let mounts = fs::read_to_string("/proc/mounts")
        .map_err(|_| PathError::MountUnknown(path.to_path_buf()))?;
    let mut best: Option<(usize, String)> = None;
    for line in mounts.lines() {
        let mut p = line.split_whitespace();
        let _ = p.next();
        let Some(m) = p.next() else { continue };
        let Some(k) = p.next() else { continue };
        let m = m.replace("\\040", " ");
        if path.to_string_lossy().starts_with(&m) && best.as_ref().is_none_or(|(n, _)| m.len() > *n)
        {
            best = Some((m.len(), k.into()));
        }
    }
    Ok(best.map(|(_, k)| k))
}
fn is_network_fs(kind: &str) -> bool {
    matches!(
        kind,
        "sshfs" | "fuse.sshfs" | "nfs" | "nfs4" | "cifs" | "smb3" | "9p" | "fuseblk"
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rejects_relative() {
        assert!(validate_authority("../bad").is_err());
    }
    #[test]
    fn rejects_authority() {
        assert!(validate_authority("bad/name").is_err());
    }
}

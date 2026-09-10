use std::fs;
use std::path::{Path, PathBuf};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum PathError {
    #[error("unsafe canonical path: {0}")]
    Unsafe(PathBuf),
    #[error("path is on a network filesystem: {0}")]
    Network(PathBuf),
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
        let home = std::env::var_os("HOME")
            .map(PathBuf::from)
            .unwrap_or_else(|| PathBuf::from("/tmp"));
        let base = std::env::var_os("COMPANION_XDG_ROOT")
            .map(PathBuf::from)
            .unwrap_or_else(|| home.join(".local"));
        let root = base.join("share").join(app);
        let config = std::env::var_os("XDG_CONFIG_HOME")
            .map(PathBuf::from)
            .unwrap_or_else(|| base.join("config"))
            .join(app);
        let data = root.join("data");
        let state = std::env::var_os("XDG_STATE_HOME")
            .map(PathBuf::from)
            .unwrap_or_else(|| base.join("state"))
            .join(app);
        let cache = std::env::var_os("XDG_CACHE_HOME")
            .map(PathBuf::from)
            .unwrap_or_else(|| base.join("cache"))
            .join(app);
        let logs = state.join("logs");
        let runtime = std::env::var_os("XDG_RUNTIME_DIR")
            .map(PathBuf::from)
            .unwrap_or_else(|| state.join("runtime"))
            .join(app);
        let backups = data.join("backups");
        let exports = data.join("exports");
        let secrets = data.join("secrets");
        let result = Self {
            config,
            data,
            state,
            cache,
            logs,
            runtime,
            backups,
            exports,
            secrets,
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
        }
        Ok(())
    }

    pub fn store(&self, authority: &str) -> Result<PathBuf, PathError> {
        let path = self.data.join(format!("{authority}.sqlite3"));
        self.validate(&path)?;
        Ok(path)
    }

    pub fn validate(&self, path: &Path) -> Result<(), PathError> {
        let absolute = if path.is_absolute() {
            path.to_path_buf()
        } else {
            std::env::current_dir()?.join(path)
        };
        let cwd = std::env::current_dir()?
            .canonicalize()
            .unwrap_or_else(|_| std::env::current_dir().unwrap_or_default());
        let repo = find_repository_root(&cwd);
        if absolute.starts_with(&cwd)
            || repo.as_ref().is_some_and(|root| absolute.starts_with(root))
        {
            return Err(PathError::Unsafe(absolute));
        }
        let text = absolute.to_string_lossy();
        if text.contains("sshfs") || mounted_network_path(&absolute) {
            return Err(PathError::Network(absolute));
        }
        Ok(())
    }

    fn validate_all(&self) -> Result<(), PathError> {
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
            self.validate(path)?;
        }
        Ok(())
    }
}

fn find_repository_root(start: &Path) -> Option<PathBuf> {
    let mut current = Some(start);
    while let Some(path) = current {
        if path.join(".git").exists() {
            return Some(path.to_path_buf());
        }
        current = path.parent();
    }
    None
}

fn mounted_network_path(path: &Path) -> bool {
    let Ok(mounts) = fs::read_to_string("/proc/mounts") else {
        return false;
    };
    let mut best: Option<(usize, &str)> = None;
    for line in mounts.lines() {
        let mut parts = line.split_whitespace();
        let _source = parts.next();
        let Some(mount) = parts.next() else {
            continue;
        };
        let Some(kind) = parts.next() else {
            continue;
        };
        let mount = mount.replace("\\040", " ");
        if path.to_string_lossy().starts_with(&mount)
            && best.is_none_or(|(len, _)| mount.len() > len)
        {
            best = Some((mount.len(), kind));
        }
    }
    best.is_some_and(|(_, kind)| {
        matches!(
            kind,
            "sshfs" | "fuse.sshfs" | "nfs" | "nfs4" | "cifs" | "smb3" | "9p"
        )
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_checkout_paths() {
        let root = std::env::current_dir().expect("cwd");
        let policy = XdgPaths {
            config: root.join("config"),
            data: root.join("data"),
            state: root.join("state"),
            cache: root.join("cache"),
            logs: root.join("logs"),
            runtime: root.join("runtime"),
            backups: root.join("backups"),
            exports: root.join("exports"),
            secrets: root.join("secrets"),
        };
        assert!(matches!(
            policy.validate(&root.join("companion.sqlite3")),
            Err(PathError::Unsafe(_))
        ));
    }
}

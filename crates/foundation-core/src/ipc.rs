use libc::{AF_UNIX, SOCK_SEQPACKET, c_int, sockaddr_un};
use std::io;
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum IpcError {
    #[error("socketpair: {0}")]
    Socket(#[source] io::Error),
    #[error("send: {0}")]
    Send(#[source] io::Error),
    #[error("receive: {0}")]
    Receive(#[source] io::Error),
}

pub fn seqpacket_pair() -> Result<(OwnedFd, OwnedFd), IpcError> {
    let mut fds = [0 as c_int; 2];
    // SAFETY: fds points to two valid c_int slots and libc fills them.
    let rc = unsafe {
        libc::socketpair(
            AF_UNIX,
            SOCK_SEQPACKET | libc::SOCK_CLOEXEC,
            0,
            fds.as_mut_ptr(),
        )
    };
    if rc != 0 {
        return Err(IpcError::Socket(io::Error::last_os_error()));
    }
    // SAFETY: successful socketpair transfers ownership of both descriptors.
    Ok((unsafe { OwnedFd::from_raw_fd(fds[0]) }, unsafe {
        OwnedFd::from_raw_fd(fds[1])
    }))
}

pub fn send(fd: &OwnedFd, payload: &[u8]) -> Result<(), IpcError> {
    // SAFETY: payload is a valid byte slice for the duration of the call.
    let rc = unsafe {
        libc::send(
            fd.as_raw_fd(),
            payload.as_ptr().cast(),
            payload.len(),
            libc::MSG_NOSIGNAL,
        )
    };
    if rc < 0 {
        Err(IpcError::Send(io::Error::last_os_error()))
    } else {
        Ok(())
    }
}

pub fn receive(fd: &OwnedFd, max: usize) -> Result<Vec<u8>, IpcError> {
    let mut buffer = vec![0_u8; max];
    // SAFETY: buffer is writable and sized max.
    let rc = unsafe { libc::recv(fd.as_raw_fd(), buffer.as_mut_ptr().cast(), buffer.len(), 0) };
    if rc < 0 {
        return Err(IpcError::Receive(io::Error::last_os_error()));
    }
    buffer.truncate(rc as usize);
    Ok(buffer)
}

pub fn receive_with_credentials(
    fd: &OwnedFd,
    max: usize,
) -> Result<(Vec<u8>, libc::ucred), IpcError> {
    let mut buffer = vec![0_u8; max];
    let mut iov = libc::iovec {
        iov_base: buffer.as_mut_ptr().cast(),
        iov_len: buffer.len(),
    };
    let mut control = [0_u8; 128];
    // SAFETY: all message fields point to live writable buffers for recvmsg.
    let mut msg: libc::msghdr = unsafe { std::mem::zeroed() };
    msg.msg_iov = &mut iov;
    msg.msg_iovlen = 1;
    msg.msg_control = control.as_mut_ptr().cast();
    msg.msg_controllen = control.len();
    // SAFETY: fd and msghdr are valid for the duration of the syscall.
    let rc = unsafe { libc::recvmsg(fd.as_raw_fd(), &mut msg, 0) };
    if rc < 0 {
        return Err(IpcError::Receive(io::Error::last_os_error()));
    }
    let mut cred = None;
    // SAFETY: libc walks the control buffer bounded by msg_controllen.
    let mut header = unsafe { libc::CMSG_FIRSTHDR(&msg) };
    while !header.is_null() {
        // SAFETY: header points inside the control buffer returned by recvmsg.
        if unsafe {
            (*header).cmsg_level == libc::SOL_SOCKET && (*header).cmsg_type == libc::SCM_CREDENTIALS
        } {
            // SAFETY: SCM_CREDENTIALS carries one ucred value.
            let ptr = unsafe { libc::CMSG_DATA(header) }.cast::<libc::ucred>();
            cred = Some(unsafe { *ptr });
            break;
        }
        // SAFETY: advance to the next bounded control message.
        header = unsafe { libc::CMSG_NXTHDR(&msg, header) };
    }
    buffer.truncate(rc as usize);
    cred.map(|value| (buffer, value)).ok_or_else(|| {
        IpcError::Receive(io::Error::new(
            io::ErrorKind::InvalidData,
            "SCM_CREDENTIALS missing",
        ))
    })
}

pub fn enable_passcred(fd: &OwnedFd) -> io::Result<()> {
    let enabled: c_int = 1;
    // SAFETY: pointer and length describe a valid integer option value.
    let rc = unsafe {
        libc::setsockopt(
            fd.as_raw_fd(),
            AF_UNIX,
            libc::SO_PASSCRED,
            (&enabled as *const c_int).cast(),
            std::mem::size_of_val(&enabled) as u32,
        )
    };
    if rc == 0 {
        Ok(())
    } else {
        Err(io::Error::last_os_error())
    }
}

/// Return the kernel-reported peer credentials for a connected Unix socket.
/// For the supervisor-created socketpair this is the producer process, not a
/// message-declared identity. The caller must still bind the PID to its
/// expected generation and account for the documented same-user threat ceiling.
pub fn peer_credentials(fd: &OwnedFd) -> io::Result<libc::ucred> {
    let mut cred = libc::ucred {
        pid: 0,
        uid: 0,
        gid: 0,
    };
    let mut len = std::mem::size_of::<libc::ucred>() as libc::socklen_t;
    // SAFETY: cred and len point to writable storage of the declared size.
    let rc = unsafe {
        libc::getsockopt(
            fd.as_raw_fd(),
            libc::SOL_SOCKET,
            libc::SO_PEERCRED,
            (&mut cred as *mut libc::ucred).cast(),
            &mut len,
        )
    };
    if rc == 0 {
        Ok(cred)
    } else {
        Err(io::Error::last_os_error())
    }
}

#[allow(dead_code)]
fn _socket_address_type_is_available(_: sockaddr_un) {}

"""Pseudo terminal utilities."""

# Bugs: No signal handling.  Doesn't set slave termios and window size.
#       Only tested on Linux.
# See:  W. Richard Stevens. 1992.  Advanced Programming in the
#       UNIX Environment.  Chapter 19.
# Author: Steen Lumholt -- with additions by Guido.

import contextlib
import io
import os
import signal
import sys
import tty
import warnings
from select import select

try:
    import threading
except ImportError:
    import dummy_threading as threading

try:
    from shutil import which
except ImportError:
    from backports.shutil_which import which

if sys.version_info[:2] < (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess

try:
    import psutil
    TIMEOUT = 1
except ImportError:
    psutil = None
    PS_PATH = which('ps')
    PGREP_PATH = which('pgrep')
    TIMEOUT = None if PS_PATH is None else 1

__all__ = ["openpty", "fork", "spawn"]

STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2

CHILD = 0


def openpty():
    """openpty() -> (master_fd, slave_fd)
    Open a pty master/slave pair, using os.openpty() if possible."""

    try:
        return os.openpty()
    except (AttributeError, OSError):
        pass
    master_fd, slave_name = _open_terminal()
    slave_fd = slave_open(slave_name)
    return master_fd, slave_fd


def master_open():
    """master_open() -> (master_fd, slave_name)
    Open a pty master and return the fd, and the filename of the slave end.
    Deprecated, use openpty() instead."""

    try:
        master_fd, slave_fd = os.openpty()
    except (AttributeError, OSError):
        pass
    else:
        slave_name = os.ttyname(slave_fd)
        os.close(slave_fd)
        return master_fd, slave_name

    return _open_terminal()


def _open_terminal():
    """Open pty master and return (master_fd, tty_name)."""
    for x in 'pqrstuvwxyzPQRST':
        for y in '0123456789abcdef':
            pty_name = '/dev/pty' + x + y
            try:
                fd = os.open(pty_name, os.O_RDWR)
            except OSError:
                continue
            return (fd, '/dev/tty' + x + y)
    raise OSError('out of pty devices')


def slave_open(tty_name):
    """slave_open(tty_name) -> slave_fd
    Open the pty slave and acquire the controlling terminal, returning
    opened filedescriptor.
    Deprecated, use openpty() instead."""

    result = os.open(tty_name, os.O_RDWR)
    try:
        from fcntl import ioctl, I_PUSH
    except ImportError:
        return result
    try:
        ioctl(result, I_PUSH, "ptem")
        ioctl(result, I_PUSH, "ldterm")
    except OSError:
        pass
    return result


def fork():
    """fork() -> (pid, master_fd)
    Fork and make the child a session leader with a controlling terminal."""

    try:
        pid, fd = os.forkpty()
    except (AttributeError, OSError):
        pass
    else:
        if pid == CHILD:
            try:
                os.setsid()
            except OSError:
                # os.forkpty() already set us session leader
                pass
        return pid, fd

    master_fd, slave_fd = openpty()
    pid = os.fork()
    if pid == CHILD:
        # Establish a new session.
        os.setsid()
        os.close(master_fd)

        # Slave becomes stdin/stdout/stderr of child.
        os.dup2(slave_fd, STDIN_FILENO)
        os.dup2(slave_fd, STDOUT_FILENO)
        os.dup2(slave_fd, STDERR_FILENO)
        if (slave_fd > STDERR_FILENO):
            os.close(slave_fd)

        # Explicitly open the tty to make it become a controlling tty.
        tmp_fd = os.open(os.ttyname(STDOUT_FILENO), os.O_RDWR)
        os.close(tmp_fd)
    else:
        os.close(slave_fd)

    # Parent and child process.
    return pid, master_fd


def _writen(fd, data):
    """Write all the data to a descriptor."""
    while data:
        n = os.write(fd, data)
        data = data[n:]


def _read(fd):
    """Default read function."""
    return os.read(fd, 1024)


if psutil is None:  # if psutil not installed
    def _is_zombie(pid):
        """Check if pid is in zombie stat."""
        if PS_PATH is None:
            return False
        try:
            proc = subprocess.check_output([PS_PATH, 'axo', 'pid=,stat='])
        except subprocess.CalledProcessError:
            return False
        for line in proc.strip().splitlines():
            _pid, stat = line.strip().decode().split()
            if int(_pid) == pid:
                return ('Z' in stat)
        raise OSError(3, 'No such process')

    def _fetch_child(ppid):
        """Get child processes of a leading process."""
        chld_pid = [ppid]
        if PGREP_PATH is None:
            return chld_pid
        try:
            proc = subprocess.check_output([PGREP_PATH, '-P', str(ppid)])
        except subprocess.CalledProcessError:
            return chld_pid
        for line in proc.strip().splitlines():
            with contextlib.suppress(ValueError):
                chld_pid.extend(_fetch_child(int(line.strip())))
        return chld_pid
else:
    def _is_zombie(pid):
        """Check if pid is in zombie stat."""
        try:
            return (psutil.Process(pid).status() == psutil.STATUS_ZOMBIE)
        except psutil.NoSuchProcess:
            raise OSError(3, 'No such process')

    def _fetch_child(ppid):
        """Get child processes of a leading process."""
        chld_pid = [ppid]
        try:
            for child in psutil.Process(ppid).children(recursive=True):
                chld_pid.append(child.pid)
        except psutil.NoSuchProcess:
            pass
        return chld_pid


def _copy(pid, master_fd, master_read=_read, stdin_read=_read):
    """Parent copy loop.
    Copies
            pty master -> standard output   (master_read)
            standard input -> pty master    (stdin_read)"""
    fds = [master_fd, STDIN_FILENO]
    while True:
        rfds, _, _ = select(fds, [], [], TIMEOUT)
        if _is_zombie(pid):
            raise OSError(5, 'Input/output error')
        if master_fd in rfds:
            data = master_read(master_fd)
            if not data:  # Reached EOF.
                fds.remove(master_fd)
            else:
                os.write(STDOUT_FILENO, data)
        if STDIN_FILENO in rfds:
            data = stdin_read(STDIN_FILENO)
            if not data:
                fds.remove(STDIN_FILENO)
            else:
                _writen(master_fd, data)


def _kill(pid, signal, master_read):
    """Kill a process with a signal."""
    class FileObject(io.IOBase):
        def write(self, data):
            os.write(master_read, bytes(data, 'utf-8', 'replace'))

    file = FileObject(master_read)
    for chld in reversed(_fetch_child(pid)):
        try:
            os.kill(chld, signal)
        except OSError as error:
            with contextlib.suppress(OSError):
                os.kill(chld, signal.SIGTERM)
            message = ('failed to send signal to process %d '
                       'with error message: %s') % (chld, error)
            warnings.showwarning(message, ResourceWarning, __file__, 246, file)


def spawn(argv, master_read=_read, stdin_read=_read, timeout=None, env=None):
    """Create a spawned process."""
    if env is None:
        env = os.environ
    if isinstance(argv, str):
        argv = (argv,)

    pid, master_fd = fork()
    if pid == CHILD:
        os.execvpe(argv[0], argv, env)

    if timeout is not None:
        timer = threading.Timer(timeout, _kill, args=(pid, signal.SIGKILL, master_fd))
        timer.start()

    try:
        mode = tty.tcgetattr(STDIN_FILENO)
        tty.setraw(STDIN_FILENO)
        restore = 1
    except tty.error:    # This is the same as termios.error
        restore = 0

    try:
        _copy(pid, master_fd, master_read, stdin_read)
        # print('copied!')
    except OSError:
        if restore:
            tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)

    os.close(master_fd)
    if timeout is not None:
        timer.cancel()
    return os.waitpid(pid, 0)[1]

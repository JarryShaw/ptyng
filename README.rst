PTYng -- Pseudo-terminal utilities
==================================

Fork of ``pty`` aiming for enhancement of the full ``stdlib`` Python API.

    As encountered in practice, ``pty.spawn`` requires ``KeyboardInterrupt``
    or else to break hanging from ``select.select`` as in ``pty._copy`` then
    raise ``OSError`` to ``pty.spawn`` and to return from the function.

    Thus, ``ptyng`` introduced ``_is_zombie`` to check if the spawned child
    process is already dead (or, a 'zombie'), through which ``pty.spawn``
    will automatically return from function call as normal/trivial scenerios
    expected.

Download
--------

Standalone releases are available on PyPI:
http://pypi.python.org/pypi/ptyng/

Development
-----------

The main development takes place in the Python standard library: see
the `Python developer's guide <http://docs.python.org/devguide/>`_.
In particular, new features should be submitted to the
`Python bug tracker <http://bugs.python.org/>`_.

Documentation
-------------

Refer to the
`standard pty <http://docs.python.org/dev/library/pty.html>`_
documentation.

    ``ptyng.spawn`` now supports ``timeout`` argument. If the timeout
    expires, the spawned child process will be killed and waited for.
    Another ``env`` argument can be used to set the runtime environment
    variables for the spawned child process, default is ``os.environ``.

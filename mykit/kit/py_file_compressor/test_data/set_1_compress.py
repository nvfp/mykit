import io as _io
import sys as _sys
class StreamCapture:
    """Redirects and captures stream content"""
    def __init__(self, fd:int=1):
        r"""
        Initialize the context manager.

        ---

        ## Params
        - `fd`: file descriptors: `0` for stdin, `1` for stdout, and `2` is for stderr.

        ## Demo
        >>> with StreamCapture() as captured:
        >>>     print('foo\n\nbar')
        >>>     print('baz')
        >>> print(repr(captured.value))  # 'foo\n\nbar\nbaz\n'
        """
        self.fd = fd
        if fd in [0, 2]: raise NotImplementedError  # TODO: Remove this once implemented
        if fd not in [0, 1, 2]: raise ValueError(f'Invalid `fd` value: {repr(fd)}.')
        self.holder = _io.StringIO()
        self.old = None
    def __enter__(self):
        if self.fd == 0: self.old = _sys.stdin  # Hasn't tested
        if self.fd == 1: self.old = _sys.stdout
        if self.fd == 2: self.old = _sys.stderr  # Hasn't tested
        self.holder = self.holder
        if self.fd == 0: _sys.stdin = self.holder  # Hasn't tested
        if self.fd == 1: _sys.stdout = self.holder
        if self.fd == 2: _sys.stderr = self.holder  # Hasn't tested

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        ## Restore
        if self.fd == 0: _sys.stdin = self.old  # Hasn't tested
        if self.fd == 1: _sys.stdout = self.old
        if self.fd == 2: _sys.stderr = self.old  # Hasn't tested

    @property
    def value(self):
        """The captured output as a string"""
        return self.holder.getvalue()
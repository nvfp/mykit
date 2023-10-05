import sys as _sys


def get_py_ver() -> str:
    """Get the current Python version in the expected 'Major.minor.patch' format"""
    info = _sys.version_info
    M = info.major  # Major
    m = info.minor  # Minor
    p = info.micro  # Patch
    return f'{M}.{m}.{p}'

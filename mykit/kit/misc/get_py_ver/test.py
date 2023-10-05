import TurboTest as tt
from . import get_py_ver


def should_in_M_m_p_format():
    tt.the_string_matches_the_regex(get_py_ver(), r'^\d+\.\d+\.\d+$')

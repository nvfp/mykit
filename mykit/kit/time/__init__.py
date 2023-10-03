import platform as _platform
import re as _re
from datetime import (
    datetime as _datetime,
    timedelta as _timedelta,
    timezone as _timezone,
)
from typing import (
    Optional as _Optional
)


def get_sexagecimal(secs: float, /, include_ms: bool = False) -> str:
    """
    Converts seconds to sexagesimal format.

    ## Demo
    >>> get_sexagecimal(3661.345)
    '01:01:01'

    """
    sign = '-' if secs < 0 else ''
    secs_abs = abs(secs)
    hours, remainder = divmod(secs_abs, 3600)
    minutes, seconds = divmod(remainder, 60)

    h = str(int(hours)).zfill(2)
    m = str(int(minutes)).zfill(2)

    if include_ms:
        s = f'{seconds:.3f}'.zfill(6)
    else:
        s = str(round(seconds)).zfill(2)

    return sign + ':'.join([h, m, s])


def sexagecimal_to_secs(sexagecimal: str, /) -> float:
    """
    ## Exceptions
    - `ValueError` if `sexagecimal` is invalid

    ## Demo
    - `sexagecimal_to_secs('1.25')` -> `1.25`
    - `sexagecimal_to_secs('01:01.25')` -> `61.25`
    - `sexagecimal_to_secs('1:1:5.25')` -> `3665.25`
    """
    _s = sexagecimal.strip(' ')

    res = _re.match(r'^(?P<sign>\+|-)?(?:(?:(?P<h>\d+):)?(?:(?P<m>[0-5]?\d):))?(?P<s>[0-5]?\d(?:\.\d*)?)$', _s)
    if res is None:
        raise ValueError(f'Invalid sexagecimal: {repr(sexagecimal)}')

    sign = res.group('sign')
    if sign in (None, '+'):
        sign = 1
    else:
        sign = -1

    h = res.group('h')
    if h is None:
        h = 0

    m = res.group('m')
    if m is None:
        m = 0

    s = res.group('s')

    return sign * (int(h)*3600 + int(m)*60 + float(s))


def get_dur(__secs: float, /) -> str:
    """
    Converts a duration in seconds to a string in hours, minutes, and seconds format.

    ## Demo
    >>> get_dur(3600)
    '1 hr'
    >>> get_dur(5400)
    '1 hr 30 mins'
    >>> get_dur(7261)
    '2 hrs 1 min 1 sec'
    """
    
    hours, _r = divmod(__secs, 3600)
    minutes, seconds = divmod(_r, 60)

    hours = int(hours)
    minutes = int(minutes)
    seconds = round(seconds)

    parts = []
    
    if hours > 0:
        if hours == 1:
            parts.append('1 hr')
        else:
            parts.append(f'{hours} hrs')
    
    if minutes > 0:
        if minutes == 1:
            parts.append('1 min')
        else:
            parts.append(f'{minutes} mins')

    if seconds == 0:
        if parts == []:
            parts.append('0 sec')
    elif seconds == 1:
        parts.append('1 sec')
    else:
        parts.append(f'{seconds} secs')

    return ' '.join(parts)


class TimeFmt:
    """
    Time Formats: Various datetime presets

    ### Params
    - `timestamp`: If not specified, the current timestamp will be used.
    - `utc_offset`: Current time, but at the specified `utc_offset` (in hours) for the timezone.
                    `2.5` means UTC+02:30, `0` is UTC+0000, `13` is UTC+13, etc.
                    If `None`, will use local timezone.
    """

    def _get_time(ts, utc_offset, fmt):
        dt = _datetime.now() if ts is None else _datetime.fromtimestamp(ts)
        dt = dt.astimezone() if utc_offset is None else dt.astimezone(_timezone(_timedelta(hours=utc_offset)))
        return dt.strftime(fmt)

    def date(timestamp:_Optional[float]=None, utc_offset:_Optional[float]=None) -> str:
        """`Aug 1, 2023` | See class docstring for parameter descriptions."""
        if _platform.system() == 'Windows' : fmt = '%b %#d, %Y'
        elif _platform.system() == 'Linux' : fmt = '%b %-d, %Y'
        elif _platform.system() == 'Darwin': fmt = '%b %-d, %Y'  # macOS
        else: raise NotImplementedError
        return TimeFmt._get_time(timestamp, utc_offset, fmt)

    def hour(timestamp:_Optional[float]=None, utc_offset:_Optional[float]=None) -> str:
        """`HH:MM:SS` / `03:02:01` | See class docstring for parameter descriptions."""
        return TimeFmt._get_time(timestamp, utc_offset, '%H:%M:%S')

    def sort(timestamp:_Optional[float]=None, utc_offset:_Optional[float]=None) -> str:
        """`YYYYMMDD_HHMMSS` / `20231221_013030` | See class docstring for parameter descriptions."""
        return TimeFmt._get_time(timestamp, utc_offset, '%Y%m%d_%H%M%S')

    def neat(timestamp:_Optional[float]=None, utc_offset:_Optional[float]=None) -> str:
        """`2020 Jan 01, 01:02:03 UTC+0000` (fixed length) | See class docstring for parameter descriptions."""
        return TimeFmt._get_time(timestamp, utc_offset, '%Y %b %d, %H:%M:%S UTC%z')

    ## TODO: make tests for this one
    def full(timestamp:_Optional[float]=None, utc_offset:_Optional[float]=None) -> str:
        """`Monday, Jan 1, 2024, 21:12:34 UTC+0000` | See class docstring for parameter descriptions."""
        if _platform.system() == 'Windows' : fmt = '%A, %b %#d, %H:%M:%S UTC%z'
        elif _platform.system() == 'Linux' : fmt = '%A, %b %-d, %H:%M:%S UTC%z'
        elif _platform.system() == 'Darwin': fmt = '%A, %b %-d, %H:%M:%S UTC%z'  # macOS
        else: raise NotImplementedError
        return TimeFmt._get_time(timestamp, utc_offset, fmt)

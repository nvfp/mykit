import re as _re
import subprocess as _sp
from typing import (
    List as _List,
    Tuple as _Tuple,
    Union as _Union
)


def get_resolution(input_path: str, ffprobe_path: str) -> _Tuple[int, int]:
    """
    image/video resolution.

    `input_path`: absolute path to the input file
    `ffprobe_path`: absolute path to ffprobe executable

    return: `(width, height)`
    """
    cmd = [
        ffprobe_path,
        '-v', 'error',
        '-select_streams', 'v',
        '-of', 'csv=p=0',
        '-show_entries', 'stream=width,height',
        input_path
    ]
    res = _sp.run(cmd, capture_output=True, text=True)
    match = _re.search(r'^(\d+),(\d+)$', res.stdout.strip())
    width, height = int(match.group(1)), int(match.group(2))
    return width, height


def get_audio_sample_rate(input_path: str, ffprobe_path: str) -> float:
    res = _sp.check_output(
        [
            ffprobe_path, '-v', 'error',
            '-select_streams', 'a',
            '-of', 'csv=p=0',
            '-show_entries', 'stream=sample_rate',
            input_path
        ],
        stderr=_sp.STDOUT, text=True
    )
    reg = _re.match(r'^(?P<v>\d+(?:\.\d+)?)', res)
    return float(reg.group('v'))


def get_vid_dur(file: str, ffprobe: str, /) -> float:
    """
    Get video duration in secs.
    Note, video and audio might be different.
    `file`: full path to the input file
    `ffprobe`: ffprobe.exe full path
    """
    stdout = _sp.check_output(
        [
            ffprobe, '-v', 'error',
            '-select_streams', 'v',
            '-of', 'csv=p=0',
            '-show_entries', 'stream=duration',
            file
        ],
        stderr=_sp.STDOUT, text=True
    )
    res = _re.match(r'^(?P<dur>\d+(?:\.\d+)?)', stdout)
    return float(res.group('dur'))

def get_audio_dur(file: str, ffprobe: str, /) -> float:
    """
    Get audio duration in secs.
    Note, video and audio might be different.
    `file`: full path to the input file
    `ffprobe`: ffprobe.exe full path
    """
    stdout = _sp.check_output(
        [
            ffprobe, '-v', 'error',
            '-select_streams', 'a',
            '-of', 'csv=p=0',
            '-show_entries', 'stream=duration',
            file
        ],
        stderr=_sp.STDOUT, text=True
    )
    res = _re.match(r'^(?P<dur>\d+(?:\.\d+)?)', stdout)
    return float(res.group('dur'))


def get_vid_fps(file: str, ffprobe: str, /, *, do_round: bool = False) -> _Union[int, float]:
    """
    Video fps (average frame rate).

    `file`: full path to the input file
    `ffprobe`: ffprobe.exe full path
    `do_round`: round the fps to the nearest integer
    """
    stdout = _sp.check_output(
        [
            ffprobe, '-v', 'error',
            '-select_streams', 'v',
            '-of', 'csv=p=0',
            '-show_entries', 'stream=avg_frame_rate',
            file
        ],
        stderr=_sp.STDOUT, text=True
    )
    res = _re.match(r'^(?P<fps>\d+/\d+)', stdout)
    fps = eval(res.group('fps'), {})
    if do_round:
        return round(fps)
    else:
        return fps


def gen_dyn_vol(__timestamp: _List[_Tuple[float, float]], /, precision: float = 0.0001, vol_round: int = 2) -> str:
    """
    Generate a dynamic volume (with linear interpolation) filter.

    ---

    ## params
    - `precision`: Lower values indicate better quality with fewer artifacts.
    - `vol_round`: To minimize output length.

    ## Demo
    - If `__timestamp = [(0, 1), (5, 0.5), (10, 1)]` -> Start at full volume,
        transition to half volume, reach half volume at the 5-sec mark,
        transition back to full volume, and return back to full volume at the 10-sec mark.
    - If `__timestamp = [(0, 1), (5, 0.5), (8, 0.5), (10, 1)]` -> Start at full volume,
        transition to half volume, reach half volume at the 5-sec mark, remains at half volume until 8-sec mark,
        transition back to full volume, and return back to full volume at the 10-sec mark.

    ## TODO:
    - Add argument for supporting different interpolation types
    """

    ts_round = len(str(abs(precision)).split('.')[1]) if '.' in str(precision) else 0

    keys = []
    for idx, (current_ts, current_vol) in enumerate(__timestamp):

        if idx == 0:
            V = round(current_vol, vol_round)
            T1 = round(current_ts, ts_round)
            T2 = round(current_ts + precision, ts_round)  # This line is necessary to handle potential occurrences of '1 + 0.1 = 1.100000000000003'.
            keys.append(f'{V}*between(t,{T1},{T2})')
        else:
            prev_ts, prev_vol = __timestamp[idx - 1]
            if idx == 1:
                V1 = round(prev_vol, vol_round)
                V2 = round(prev_vol - current_vol, vol_round)
                T_START = round(prev_ts + precision, ts_round)
                INTERVAL = round(current_ts - prev_ts - 2*precision, ts_round)
                T1 = round(prev_ts + 2*precision, ts_round)
                T2 = round(current_ts, ts_round)
                keys.append(
                    f'({V1}-{V2}*(t-{T_START})/{INTERVAL})'
                    f'*between(t,{T1},{T2})'
                )
            else:
                V1 = round(prev_vol, vol_round)
                V2 = round(prev_vol - current_vol, vol_round)
                T_START = round(prev_ts + precision, ts_round)
                INTERVAL = round(current_ts - prev_ts - precision, ts_round)
                T1 = round(prev_ts + precision, ts_round)
                T2 = round(current_ts, ts_round)
                keys.append(
                    f'({V1}-{V2}*(t-{T_START})/{INTERVAL})'
                    f'*between(t,{T1},{T2})'
                )

    keys_str = '+'.join(keys)
    return f"volume='{keys_str}':eval=frame"
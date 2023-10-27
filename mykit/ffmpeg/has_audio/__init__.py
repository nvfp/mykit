import subprocess as _sp


## Born: Oct 27, 2023
def has_audio(ffprobe:str, input_file:str) -> bool:
    """
    Check whether or not the `input_file` has an audio stream.

    ## Params
    - `ffprobe`: absolute path to the ffprobe binary
    - `input_file`: absolute path to the input file
    """
    cmd = [
        ffprobe,
        '-v', 'error',
        '-select_streams', 'a:0',
        '-show_entries', 'stream=channels',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_file
    ]
    res = _sp.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip('\n')
    return False if out == '' else True

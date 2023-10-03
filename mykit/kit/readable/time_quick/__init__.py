

def time_quick(secs: float, /) -> str:
    """
    Convert seconds into minutes-seconds concise-look style

    ## Examples
    - `quick(61.25)` -> `'1m1.2s'`
    """
    m, s = divmod(secs, 60)
    return f'{int(m)}m{s:.1f}s'

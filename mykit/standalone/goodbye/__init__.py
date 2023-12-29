import os, random, time
from datetime import datetime, timedelta, timezone


class Goodbye:  # Born: 2023 Dec 29

    @staticmethod
    def _get_dur(__secs):
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

    def __new__(cls, gmt:float, T_STARTUP:float, Ctxt=None) -> None:
        """
        ## Params
        - `gmt`: GMT offset (in hours). Example: if UTC+0100 -> gmt=1; UTC-0230 -> gmt=-2.5
        - `T_STARTUP`: the timestamp of program's startup.
        - `Ctxt`: for printing in color. This is a function from mykit lib.
        """
        T = datetime.now().astimezone(timezone(timedelta(hours=gmt))).strftime('EXITED NORMALLY @ %H:%M:%S')
        PAD = 2  # number of spaces
        SEP = '─'*((os.get_terminal_size().columns-1-len(T)-PAD)//2)
        FOOTER = f'{SEP} {T} {SEP}'
        print(
            '─'*(os.get_terminal_size().columns-1) + '\n' +
            f'Done! Took about {Goodbye._get_dur(time.time() - T_STARTUP)}.\n' +
            random.choice([
                'Goodbye and see you...', 'Bye, you are awesome!', 'You are cool!',
                'Have a good day!', 'See you, have a great day.', 'Take care, have a great time!',
                'See you again and take care.', 'You are incredible!', 'You are amazing, see you!',
            ])
        )
        if Ctxt is None:
            print(FOOTER)
        else:
            print(Ctxt(FOOTER, '#4fc778'))

from typing import (
    Callable as _Callable
)


class Eventdriven:
    """Simple event-driven implementation"""

    bus = {}  # Container

    def register(name: str, /) -> None:
        if name in Eventdriven.bus:
            raise ValueError(f'Event {repr(name)} already exists.')
        Eventdriven.bus[name] = []

    def call(name: str, /) -> None:
        for fn in Eventdriven.bus[name]:
            fn()

    def listen(to: str, do: _Callable[[], None]) -> None:
        if to not in Eventdriven.bus:
            raise ValueError(f'Event {repr(to)} does not exist.')
        Eventdriven.bus[to].append(do)
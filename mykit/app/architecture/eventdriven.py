from mykit.app.architecture import Architecture as _Architecture

from mykit.app import App  # be careful of circular imports. this is just used for typehint purposes


class Eventdriven(_Architecture):
    """
    Simple event-driven architecture.
    (still in beta)
    """

    bus = {}  # basically a container
    
    def register(name):
        
        if name in Eventdriven.bus:
            raise ValueError('Already exists')
        Eventdriven.bus[name] = []

    def call(name):
        
        for fn in Eventdriven.bus[name]:
            fn()

    def listen(to, do):

        if to not in Eventdriven.bus:
            raise ValueError('Event not exist')
        Eventdriven.bus[to].append(do)
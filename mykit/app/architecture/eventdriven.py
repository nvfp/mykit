from mykit.app.architecture import Architecture as _Architecture

from mykit.app import App  # be careful of circular imports. this is just used for typehint purposes


class Eventdriven(_Architecture):
    """simple event-driven architecture"""

    bus = {}  # basically a container
    
    def register(abstraction):
        
        if fn in bus:
            raise ValueError
        bus[fn] = []

    def call(event):
        
        for fn in Eventdriven.bus[event]:
            fn(app: App)

    def listen(to, do):
        pass
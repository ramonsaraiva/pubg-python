from .events import Event


class Telemetry:

    def __init__(self, data):
        self.events = [Event.instance(event) for event in data]

    def events_from_type(self, _type):
        return [ev for ev in self.events if type(ev).__name__ == _type]
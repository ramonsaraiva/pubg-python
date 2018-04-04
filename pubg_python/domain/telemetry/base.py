from .events import Event


class Telemetry:

    def __init__(self, data):
        self.events = [Event.instance(event) for event in data]
import json

from .data import SHARD_DATA_MAP
from .events import Event


class Telemetry:

    def __init__(self, data, url, shard=None):
        self.shard = shard or ('xbox' if 'xbox-' in url else 'pc')
        self.events = [
            Event.instance(event_data)
            for event_data in self.generate_events_data(data)
        ]

    def generate_events_data(self, data):
        data_class = SHARD_DATA_MAP[self.shard]
        for event in data:
            yield data_class(event)

    def events_from_type(self, _type):
        return [ev for ev in self.events if type(ev).__name__ == _type]

    @classmethod
    def from_json(cls, path, shard='pc'):
        with open(path, 'r') as telemetry_file:
            data = json.load(telemetry_file)
        return cls(data, path, shard)

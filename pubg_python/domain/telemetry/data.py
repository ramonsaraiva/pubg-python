from collections.abc import MutableMapping


class TelemetryData(MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        value = self.store[self.__keytransform__(key)]
        if isinstance(value, dict):
            return self.__class__(value)
        return value

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key


class PCTelemetryData(TelemetryData):
    pass


class XBOXTelemetryData(TelemetryData):

    def __keytransform__(self, key):
        return super().__keytransform__(key).title()


SHARD_DATA_MAP = {
    'xbox': XBOXTelemetryData,
    'pc': PCTelemetryData,
}

from . import exceptions


def requires_shard(f):
    def wrapper(self, *args, **kwargs):
        if self.shard is None:
            raise exceptions.ShardNotDefinedError(
                'A shard is required for this call')
        return f(self, *args, **kwargs)
    return wrapper


def invalidates_cache(f):
    def wrapper(self, *args, **kwargs):
        if self._data:
            self._data = None
        return f(self, *args, **kwargs)
    return wrapper


def fetchy(f):
    def wrapper(self, *args, **kwargs):
        self.fetch()
        return f(self, *args, **kwargs)
    return wrapper

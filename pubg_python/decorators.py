from . import exceptions

def requires_shard(f):
    def wrapper(self, *args, **kwargs):
        if self.shard is None:
            raise exceptions.ShardNotDefinedError(
                'A shard is required for this call')
        return f(self, *args, **kwargs)
    return wrapper


def invalidates_cache(f):
    # TODO: can probably be a class decorator
    def wrapper(self, *args, **kwargs):
        if self._response:
            self._response = None
        return f(self, *args, **kwargs)
    return wrapper
from . import exceptions

def requires_shard(f):
    def wrapper(self, *args, **kwargs):
        if self.shard is None:
            raise exceptions.ShardNotDefinedError(
                'A shard is required for this call')
        return f(self, *args, **kwargs)
    return wrapper


def requires_endpoint(f):
    def wrapper(self, *args, **kwargs):
        if self.endpoint is None:
            raise exceptions.EndpointNotDefinedError(
                'An endpoint is required for this call')
        return f(self, *args, **kwargs)
    return wrapper
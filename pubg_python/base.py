import json

from . import exceptions
from .decorators import requires_shard
from .domain import (
    Domain,
    Match,
    Shard,
)
from .mixins import (
    FilterableQuerySetMixin,
    PaginatedQuerySetMixin,
    RequestMixin,
    SortableQuerySetMixin,
)


class PUBG(RequestMixin):

    API_OK = 200
    API_ERRORS_MAPPING = {
        401: exceptions.UnauthorizedError,
        404: exceptions.NotFoundError,
        415: exceptions.InvalidContentTypeError,
        429: exceptions.RateLimitError,
    }

    def __init__(self, api_key, shard=None):
        super().__init__(api_key)
        self.shard = shard

    @property
    def shard(self):
        return self._shard

    @shard.setter
    def shard(self, value):
        if not isinstance(value, Shard):
            raise exceptions.InvalidShardError('Invalid Shard')
        self._shard = value

    @property
    def shard_url(self):
        url = self.url.copy()
        url.path = 'shards/{}'.format(self.shard.value)
        return url

    @requires_shard
    def matches(self, id=None):
        url = self.shard_url
        url.path.segments.append('matches')
        return MatchQuerySet(self, url)

    def request(self, endpoint):
        response = self.session.get(endpoint)

        if response.status_code != self.API_OK:
            exception = self.API_ERRORS_MAPPING.get(
                response.status_code, exceptions.APIError)
            raise exception()

        return json.loads(response.text)


class BaseQuerySet:
    domain = Domain

    def __init__(self, client, endpoint):
        self.client = client
        self.endpoint = endpoint
        self._data = None

    def __iter__(self):
        data = self.fetch()
        return MultiResponse(
            self, self.domain, data).__iter__()

    def __getitem__(self, key):
        data = self.fetch()
        return MultiResponse(
            self, self.domain, data).__getitem__(key)

    def fetch(self, id=None):
        if self._data is not None:
            return self._data

        if id is not None:
            self.endpoint.path.segments.append(id)
        self._data = self.client.request(self.endpoint)
        return self._data

    def get(self, id):
        return self.domain(self.fetch(id))


class QuerySet(PaginatedQuerySetMixin, SortableQuerySetMixin,
               FilterableQuerySetMixin, BaseQuerySet):
    pass


class MatchQuerySet(QuerySet):
    domain = Match


class MultiResponse:

    def __init__(self, client, domain, data):
        self.client = client
        self.domain = domain
        self.data = data

    def __iter__(self):
        return (self.domain(data) for data in self.data['data'])

    def __getitem__(self, index):
        return self.domain(self.data['data'][index])

    @property
    def links(self):
        if 'links' not in self['data']:
            return None
        return self['data']['links']

    @property
    def next_url(self):
        links = self.links
        if links and 'next' in self.links:
            return links['next']
        return None

    @property
    def last_url(self):
        links = self.links
        if links and 'prev' in self.links:
            return links['prev']
        return None

    def next(self):
        next_url = self.next_url
        if next_url is None:
            return None
        self.data = self.client.request(next_url)
        return self

    def prev(self):
        prev_url = self.prev_url
        if prev_url is None:
            return None
        self.data = self.client.request(prev_url)
        return self

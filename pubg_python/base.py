import json

from .decorators import requires_shard
from .domain import (
    Domain,
    Match,
    Shard,
)
from .exceptions import InvalidShardError
from .mixins import (
    FilterableQuerySetMixin,
    PaginatedQuerySetMixin,
    RequestMixin,
    SortableQuerySetMixin,
)


class PUBG(RequestMixin):

    def __init__(self, api_key, shard=None):
        super().__init__(api_key)
        self.shard = shard

    @property
    def shard(self):
        return self._shard

    @shard.setter
    def shard(self, value):
        if not isinstance(value, Shard):
            raise InvalidShardError('Invalid Shard')
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
        return MatchQuerySet(self.session, url)


class BaseQuerySet:
    path = None
    domain = Domain

    def __init__(self, session, endpoint):
        self.session = session
        self.endpoint = endpoint
        self._response = None

    def __iter__(self):
        return MultiResponse(
            self.domain, self.fetch(), self.session).__iter__()

    def __getitem__(self, key):
        return MultiResponse(
            self.domain, self.fetch(), self.session).__getitem__(key)

    def fetch(self, id=None):
        if self._response is not None:
            return self._response

        if id is not None:
            self.endpoint.path.segments.append(id)
        self._response = self.session.get(self.endpoint)
        return self._response

    def get(self, id):
        response = self.fetch(id)
        return self.domain(json.loads(response.text))


class QuerySet(PaginatedQuerySetMixin, SortableQuerySetMixin,
               FilterableQuerySetMixin, BaseQuerySet):
    domain = Domain


class MatchQuerySet(QuerySet):
    path = 'matches'
    domain = Match


class MultiResponse:

    def __init__(self, domain, response, session):
        self.domain = domain
        self.response = response
        self.session = session
        self.data = json.loads(self.response.text)

    def __iter__(self):
        return (self.domain(data) for data in self.data['data'])

    def __getitem__(self, key):
        return self.domain(self.data['data'][key])

    def has_links(self):
        return 'links' in self.data

    def has_next(self):
        return self.has_links() and 'next' in self.data['links']

    def has_prev(self):
        return self.has_links() and 'next' in self.data['links']

    def next(self):
        if not self.has_next():
            return None
        response = self.session.get(self.data['links']['next'])
        return MultiResponse(self.domain, response, self.session)

    def prev(self):
        if not self.has_prev():
            return None
        response = self.session.get(self.data['links']['prev'])
        return MultiResponse(self.domain, response, self.session)
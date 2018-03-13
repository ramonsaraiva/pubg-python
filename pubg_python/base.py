import json
from enum import Enum

from .decorators import (
    requires_shard,
    requires_endpoint,
)
from .domain import (
    Domain,
    Match,
)
from .exceptions import InvalidShardError
from .mixins import (
    FilterableQuerySetMixin,
    PaginatedQuerySetMixin,
    RequestMixin,
    SortableQuerySetMixin,
)


class Shard(Enum):
    PC_AS = 'pc-as'  # Asia
    PC_EU = 'pc-eu'  # Europe
    PC_KAKAO = 'pc-kakao'  # ?
    PC_KRJP = 'pc-krjp'  # Korea/Japan
    PC_NA = 'pc-na'  # North America
    PC_OC = 'pc-oc'  # Oceania
    PC_SA = 'pc-sa'  # South and Central America
    PC_SEA = 'pc-sea'  # South East Asia
    XBOX_AS = 'xbox-as'  # Asia
    XBOX_EU = 'xbox-eu'  # Europe
    XBOX_NA = 'xbox-na'  # North America
    XBOX_OC = 'xbox-oc'  # Oceania


class PUBG(RequestMixin):

    def __init__(self, api_key, shard=None, gzip=False):
        super().__init__(api_key, gzip)
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
        return MatchQuerySet(self.session, url, lookup=id)


class BaseQuerySet:
    path = None
    domain = Domain

    def __init__(self, session, endpoint, lookup=None):
        self.session = session
        self.endpoint = endpoint
        self.lookup = lookup
        
        self.endpoint.path.segments.append(self.path)
        if self.lookup:
            self.endpoint.path.segments.append(self.lookup)

    def fetch(self):
        response = self.session.get(self.endpoint)
        if self.lookup:
            return self.domain(json.loads(response.text))
        return MultiResponse(
            self.domain, response, self.session)


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
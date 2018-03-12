import json
import urllib.parse
from enum import Enum

import furl
import requests

from .decorators import (
    requires_shard,
    requires_endpoint,
)
from .exceptions import (
    InvalidShardError,
    PUBGResponseError,
)
from .mixins import PUBGRequestMixin


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


class PUBG(PUBGRequestMixin):

    def __init__(self, api_key, shard=None, gzip=False):
        super().__init__(api_key, gzip)
        self.shard = shard
        self.endpoint = None

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
        url = furl.furl(self.URL)
        url.path = 'shards/{}'.format(self.shard.value)
        return url

    @requires_shard
    def matches(self, id=None):
        self.endpoint = self.shard_url
        self.endpoint.path.segments.append('matches')
        if id:
            self.endpoint.path.segments.append(id)
        return self

    @requires_endpoint
    def sort(self, sort_key, ascending=True):
        sort_key = sort_key if ascending else '-{}'.format(sort_key)
        self.endpoint.args['sort'] = sort_key
        return self

    @requires_endpoint
    def limit(self, value):
        self.endpoint.args['page[limit]'] = value
        return self

    @requires_endpoint
    def offset(self, value):
        self.endpoint.args['page[offset]'] = value
        return self

    @requires_endpoint
    def fetch(self):
        response = self.session.get(self.endpoint)
        return PUBGResponse(response, self.session)


class PUBGResponse():

    def __init__(self, response, session):
        self.response = response
        self.session = session
        self.data = json.loads(response.text)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        if not value or value.status_code != 200:
            raise PUBGResponseError('Something went wrong with your request')
        self._response = value

    def has_links(self):
        return 'links' in self.data

    def has_next(self):
        return self.has_links() and 'next' in self.data['links']

    def has_prev(self):
        return self.has_links() and 'next' in self.data['links']

    def next_response(self, endpoint):
        return PUBGResponse(self.session.get(endpoint), self.session)

    def next(self):
        if not self.has_next():
            return None
        return self.next_response(self.data['links']['next'])

    def prev(self):
        if not self.has_prev():
            return None
        return self.next_response(self.data['links']['prev'])
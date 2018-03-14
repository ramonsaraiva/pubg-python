import requests

from enum import Enum

import furl

from .decorators import invalidates_cache
from .domain import Filter
from .exceptions import InvalidFilterError


class RequestMixin:

    BASE_URL = 'https://api.playbattlegrounds.com/'

    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': api_key,
            'Accept': 'application/vnd.api+json'
        })
        self.url = furl.furl(self.BASE_URL)


class PaginatedQuerySetMixin:

    @invalidates_cache
    def limit(self, value):
        self.endpoint.args['page[limit]'] = value
        return self

    @invalidates_cache
    def offset(self, value):
        self.endpoint.args['page[offset]'] = value
        return self


class SortableQuerySetMixin:

    @invalidates_cache
    def sort(self, sort_key, ascending=True):
        sort_key = sort_key if ascending else '-{}'.format(sort_key)
        self.endpoint.args['sort'] = sort_key
        return self


class FilterableQuerySetMixin:

    @invalidates_cache
    def filter(self, filter_key, filter_value):
        if not isinstance(filter_key, Filter):
            raise InvalidFilterError("Invalid Filter")
        if isinstance(filter_value, Enum):
            filter_value = filter_value.value

        self.endpoint.args['filter[{}]'.format(filter_key.value)] = filter_value
        return self
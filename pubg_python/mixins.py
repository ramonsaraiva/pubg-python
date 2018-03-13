import requests

import furl


class RequestMixin:

    BASE_URL = 'https://api.playbattlegrounds.com/'

    def __init__(self, api_key, gzip=False):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': api_key,
            'Accept': 'application/vnd.api+json'
        })
        if gzip:
            self.session.headers['Accept-Encoding'] = 'gzip'
        self.url = furl.furl(self.BASE_URL)


class PaginatedQuerySetMixin:

    def limit(self, value):
        self.endpoint.args['page[limit]'] = value
        return self

    def offset(self, value):
        self.endpoint.args['page[offset]'] = value
        return self


class SortableQuerySetMixin:

    def sort(self, sort_key, ascending=True):
        sort_key = sort_key if ascending else '-{}'.format(sort_key)
        self.endpoint.args['sort'] = sort_key
        return self


class FilterableQuerySetMixin:

    def filter(self, filter_key, filter_value):
        self.endpoint.args['filter[{}]'.format(filter_key)] = filter_value
        return self
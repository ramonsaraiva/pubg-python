from .decorators import (
    fetchy,
    invalidates_cache,
)
from .domain.base import Domain
from .mixins import (
    FilterableQuerySetMixin,
    PaginatedQuerySetMixin,
    SortableQuerySetMixin,
)


class QuerySet(FilterableQuerySetMixin, SortableQuerySetMixin,
               PaginatedQuerySetMixin):

    def __init__(self, client, endpoint):
        self.client = client
        self.endpoint = endpoint.copy()
        self._data = None

    @property
    def has_data(self):
        return self._data and 'data' in self._data

    @fetchy
    def __iter__(self):
        return (Domain.instance({'data': data}) for data in self._data['data'])

    @fetchy
    def __getitem__(self, key):
        return Domain.instance({'data': self._data['data'][key]})

    @invalidates_cache
    def get(self, id=None):
        # get can be a fetchy filter in the future
        if id:
            self.endpoint.path.segments.append(id)
        self.fetch()
        del self.endpoint.path.segments[-1]  # dirty?
        return Domain.instance(self._data)

    def fetch(self):
        if self._data:
            return
        self._data = self.client.request(self.endpoint)

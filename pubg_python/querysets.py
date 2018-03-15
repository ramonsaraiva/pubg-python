from .decorators import (
    fetchy,
    invalidates_cache,
)
from .mixins import (
    FilterableQuerySetMixin,
    PaginatedQuerySetMixin,
    SortableQuerySetMixin,
)


class QuerySet(FilterableQuerySetMixin, SortableQuerySetMixin,
               PaginatedQuerySetMixin):

    def __init__(self, domain, client, endpoint):
        self.domain = domain
        self.client = client
        self.endpoint = endpoint.copy()
        self._data = None

    @property
    def has_data(self):
        return self._data and 'data' in self._data

    @fetchy
    def __iter__(self):
        return (self.domain(data) for data in self._data['data'])

    @fetchy
    def __getitem__(self, key):
        dataset = self._data['data'][key]
        if isinstance(dataset, list):
            return [self.domain(data) for data in dataset]
        return self.domain(dataset)

    @invalidates_cache
    def get(self, id):
        self.endpoint.path.segments.append(id)
        self.fetch()
        del self.endpoint.path.segments[-1]  # dirty?
        return self.domain(self._data)

    def fetch(self):
        if self._data:
            return
        self._data = self.client.request(self.endpoint)

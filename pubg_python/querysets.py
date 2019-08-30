from .decorators import (
    fetchy,
    invalidates_cache,
)
from .exceptions import RequiredFilterError
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


class SeasonsQuerySet(QuerySet):
    # TODO: redesign the way clients/querysets/data works
    # because the API has new endpoints with a different design
    # than the initial versions

    @invalidates_cache
    def get(self, id=None, game_mode=None):
        if id:
            if not game_mode:
                raise RequiredFilterError(
                    'gameMode is needed when querying a specific season.')

            additional_segments = [id, 'gameMode', game_mode, 'players']
            for segment in additional_segments:
                self.endpoint.path.segments.append(segment)
            return self

        self.fetch()
        aaa = [
            {'data': data}
            for data in self._data['data']
        ]
        import pdb; pdb.set_trace()
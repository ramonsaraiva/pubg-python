from .decorators import invalidates_cache
from .exceptions import InvalidFilterError


class PaginatedQuerySetMixin:

    @property
    def links(self):
        if not self.has_data:
            return None

        if 'links' not in self._data:
            return None
        return self._data['links']

    @property
    def next_url(self):
        links = self.links
        if links and 'next' in self.links:
            return links['next']
        return None

    @property
    def prev_url(self):
        links = self.links
        if links and 'prev' in self.links:
            return links['prev']
        return None

    @invalidates_cache
    def limit(self, value):
        self.endpoint.args['page[limit]'] = value
        return self

    @invalidates_cache
    def offset(self, value):
        self.endpoint.args['page[offset]'] = value
        return self

    @invalidates_cache
    def page(self, value):
        self.endpoint.args['page[number]'] = value
        return self

    def next(self):
        if not self.has_data:
            return self

        next_url = self.next_url
        if next_url:
            self.endpoint = next_url
            self._data = None
        else:
            self._data['data'] = []
        return self

    def prev(self):
        if not self.has_data:
            return self

        prev_url = self.prev_url
        if prev_url:
            self.endpoint = prev_url
            self._data = None
        else:
            self._data['data'] = []
        return self


class SortableQuerySetMixin:

    @invalidates_cache
    def sort(self, sort_key, ascending=True):
        sort_key = sort_key if ascending else '-{}'.format(sort_key)
        self.endpoint.args['sort'] = sort_key
        return self


class FilterableQuerySetMixin:

    FILTER_MAPPING = {
        'created_at_start': 'createdAt-start',
        'created_at_end': 'createdAt-end',
        'player_ids': 'playerIds',
        'player_names': 'playerNames',
        'match_ids': 'matchIds',
        'game_mode': 'gameMode',
    }

    FILTER_MULTIPLES = (
        'player_ids',
        'player_names',
        'match_ids'
    )

    @invalidates_cache
    def filter(self, **kwargs):
        for kw in kwargs:
            if kw not in self.FILTER_MAPPING:
                raise InvalidFilterError('Invalid filter')

            if kw in self.FILTER_MULTIPLES:
                if not isinstance(kwargs[kw], list):
                    raise InvalidFilterError('Invalid filter value')
                value = ','.join(kwargs[kw])
            else:
                value = kwargs[kw]

            self.endpoint.args[
                'filter[{}]'.format(self.FILTER_MAPPING[kw])] = value
        return self

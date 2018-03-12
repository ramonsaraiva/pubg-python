# pubg-python

A python wrapper for the PUBG developer API

[PUBG Developer API Official Documentation](https://developer.playbattlegrounds.com/docs/en/introduction.html)

*This is a MVP and the package is currently under development, please feel free to contribute*

*Initial version still needs to be uploaded to PyPI*

## Usage

### Specifying a shard

The PUBG API shards data by platform and region, and therefore requires a shard to be specified in the URL for most requests.

```python
from pubg_pytho import PUBG, Shard

api = PUBG('<api-key>', Shard.PC_NA)
```

A list of shards can be found [here](https://developer.playbattlegrounds.com/docs/en/making-requests.html#regions) and the wrapper constants [here](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/base.py)

## Retrieving a list of matches

Retrieving a list of matches is as simple as this:

```python
matches = api.matches().fetch()
```

### Limits and Offsets
Offsetting 5 matches and limitting by 10

```python
matches = api.matches.limit(10).offset(5).fetch()
```

### Sorting

`sort` defaults to ascending, you can use `ascending=False` for a descending sort

```python
matches = api.matches.limit(10).sort('createdAt')
matches = api.matches.limit(10).sort('createdAt', ascending=False)
```

### Pagination

Paginating is as easy as calling `next()` and `prev()`

```python
matches = api.matches.limit(1000)
next_matches = matches.next()
previous_matches = matches.prev()
```
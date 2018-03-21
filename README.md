# pubg-python

A python wrapper for the PUBG Developer API

[PUBG Developer API Official Documentation](https://developer.playbattlegrounds.com/docs/en/introduction.html)

*This is a MVP and the package is currently under development, please feel free to contribute*

## PyPI release

PUBG developer API is scheduled to go live in early April, `pubg-python` initial version will be uploaded to PyPI once that happens.

## Usage

### Specifying a shard

The PUBG API shards data by platform and region, and therefore requires a shard to be specified in the URL for most requests.

```python
from pubg_python import PUBG, Shard

api = PUBG('<api-key>', Shard.PC_NA)
```

A list of shards can be found [here](https://developer.playbattlegrounds.com/docs/en/making-requests.html#regions) and the wrapper constants [here](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain.py)

## Retrieving a list of matches

Retrieving a list of matches is as simple as this:

```python
matches = api.matches()
```

## Retrieving a single match

Retrieving a single match is also a piece of cake:

```python
match = api.matches().get(12345)
```

## Playing around with the match data

A simple example of how you can manipulate the data:
The domain is all specified [here](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain.py)

```python
match = api.matches().get(12345)

print(match.duration)
print(match.game_mode)

for roster in match.rosters:
    print(roster.participants)
    print(roster.won)

    for participant in roster.participants:
        print(participant.actor)
```

### Limits and Offsets

Offsetting 5 matches and limitting by 10

```python
matches = api.matches().limit(10).offset(5)
```

### Sorting

`sort` defaults to ascending, you can use `ascending=False` for a descending sort

```python
matches = api.matches().limit(10).sort('createdAt')
matches = api.matches().limit(10).sort('createdAt', ascending=False)
```

### Filtering

A list of filters can be found [here](https://developer.playbattlegrounds.com/docs/en/matches.html#/Matches/get_matches)

```python
from pubg_python import GameMode

squad_matches = api.matches().filter(game_mode=GameMode.SQUAD)
solo_matches = api.matches().filter(game_mode=GameMode.SOLO)
after_2018_before_2019 = api.matches().filter(
    created_at_start='2018-01-01T00:00:00Z',
    created_at_end='2019-01-01T00:00:00Z'
)
```

You don't need to use the `Enum`s if you don't want to:

```python
squad_matches = api.matches().filter(game_mode='squad')
solo_matches = api.matches().filter(game_mode='solo')
```

And you can also chain filters:

```python
squad_queryset = api.matches().filter(game_mode='squad')
squad_after_2018 = squad_queryset.filter(created_at_start='2018-01-01T00:00:00Z')
```

### Pagination

Use `next()` for the next page and `prev()` for the previous one:

```python
matches = api.matches()
next_matches = matches.next()
previous_matches = matches.prev()
```

### I want them all!

Be aware of rate limits:

```python
matches = api.matches()
while matches:
    for match in matches:
        print(match)
    matches = matches.next()
```

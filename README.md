# pubg-python

A python wrapper for the PUBG Developer API

[PUBG Developer API Official Documentation](https://documentation.playbattlegrounds.com/en/introduction.html)

## Installation

To install the wrapper, simply use `pip`

```
pip install pubg-python
```

or `pipenv`


```
pipenv install pubg-python
```

## Usage

### Specifying a shard

The PUBG API shards data by platform and region, and therefore requires a shard to be specified in the URL for most requests.

```python
from pubg_python import PUBG, Shard

api = PUBG('<api-key>', Shard.PC_NA)
```

A list of shards can be found [here](https://documentation.playbattlegrounds.com/en/making-requests.html#regions) and the wrapper constants [here](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain.py)

## Players

### Retrieving a single player

```python
player = api.players().get('account.3654e255b77b409e87b10dcb086ab00d')

for match in player.matches:
    match_data = api.matches().get(match.id)
```

### Retrieving a list of players filtering by names

```python
players = api.players().filter(player_names=['Name1', 'Name2'])
```

### Retrieving a list of players filtering by ids

```python
players = api.players().filter(player_ids=['276f5bcb-a831-4e8c-a610-d2073692069e'])
```

## Matches

### Retrieving a single match

Retrieving a single match is also a piece of cake:

```python
match = api.matches().get('276f5bcb-a831-4e8c-a610-d2073692069e')
```

## Playing around with data

An example of how you can manipulate the data:
The domain is all specified [here](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain.py)

```python
players = api.players().filter(players_names['epickitten'])
player = players[0]

player.matches
>> [<Match bd6aae34-be05-4094-981c-083285c7e861>, <Match 276f5bcb-a831-4e8c-a610-d2073692069e>, ..]

match = api.matches().get(player.matches[0].id)

match.game_mode
>> 'solo'

match.duration
>> 1899

match.rosters
>> [<Roster d542eaee-cd02-4f4e-ad7f-ed5ea71a17cf>, <Roster e9f0962a-ebd4-4d86-b134-95783b713800>, ..]

roster = match.rosters[0]

roster.participants
>> [<Participant 7cc76d1b-a80e-4997-8eb8-d4b3c1ed4f44>]

participant = roster.participans[0]

participant.name
>> 'urdaddyYO'

participant.damage_dealt
>> 291.08

participant.kills
>> 2

participant.ride_distance
>> 3204.53467

participant.walk_distance
>> 2262.81714

participant.time_survived
>> 1367

participant.player_id
>> account.edb9910f1e9c4f3b9addb87d9329b57c

player = api.players().get(participant.player_id)

player
>> account.edb9910f1e9c4f3b9addb87d9329b57c

player.matches
>> [<Match b3dcd7e8-2270-4fdd-8389-af77acf2d6c2>, <Match 2ebb1a9c-ab5e-4264-971f-df77a00918a9>, ..]
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

A list of filters can be found [here](https://documentation.playbattlegrounds.com/en/matches.html#/Matches/get_matches)

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

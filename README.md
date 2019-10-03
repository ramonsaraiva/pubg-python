# pubg-python

![pypi](https://img.shields.io/pypi/pyversions/pubg-python)
![wheel](https://img.shields.io/pypi/wheel/pubg-python)

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

A list of shards can be found [here](https://documentation.playbattlegrounds.com/en/making-requests.html#regions) and the wrapper constants [here](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)


## Samples

* Samples
  * [Official docs](https://documentation.playbattlegrounds.com/en/samples.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)

### A sample of matches can be retrieved as a starting point

```python
sample = api.samples().get()
for match in sample.matches:
    print(match.id)
```

### Samples can also be filtered by a creation date

```python
sample = api.samples().filter(created_at_start='2018-01-01T00:00:00Z').get()
for match in sample.matches:
    print(match.id)
```


## Players

* Players
  * [Official docs](https://documentation.playbattlegrounds.com/en/players.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)

### Retrieving a single player

```python
player = api.players().get('account.3654e255b77b409e87b10dcb086ab00d')

for match in player.matches:
    match_data = api.matches().get(match.id)
```

### Retrieving a list of players filtering by names

```python
players = api.players().filter(player_names=['Name1', 'Name2'])

for player in players:
    player_id = player.id
```

### Retrieving a list of players filtering by ids

```python
players = api.players().filter(player_ids=['account.3654e255b77b409e87b10dcb086ab00d'])

for player in players:
    player_name = player.name
```

## Matches

* Matches
  * [Official docs](https://documentation.playbattlegrounds.com/en/matches.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)

### Retrieving a single match

```python
match = api.matches().get('276f5bcb-a831-4e8c-a610-d2073692069e')
```

### Retrieving a list of matches filtering by ids

**Still unavailable in the API**

```python
match_ids = [
    '276f5bcb-a831-4e8c-a610-d2073692069e',
    'fasf9082-21de-dkle-13ke-qlamd13nab3a',
]
matches = api.matches().filter(match_ids=match_ids)
for match in matches:
    print(match)
```

## Telemetry

* Telemetry events
  * [Official docs](https://documentation.playbattlegrounds.com/en/telemetry-events.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/telemetry/events.py)
* Event objects
  * [Official docs](https://documentation.playbattlegrounds.com/en/telemetry-objects.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/telemetry/objects.py)

### Processing a match Telemetry data

```python
match = api.matches().get('276f5bcb-a831-4e8c-a610-d2073692069e')
asset = match.assets[0]
telemetry = api.telemetry(asset.url)

print(len(telemetry.events))
>> 16871
```

### Filtering specific events in a telemetry object

Sometimes you're interested in a set of very specific events, so there is a helper function to filter those for you:

```python
match = api.matches().get('276f5bcb-a831-4e8c-a610-d2073692069e')
asset = match.assets[0]
telemetry = api.telemetry(asset.url)

player_kill_events = telemetry.events_from_type('LogPlayerKill')
player_position_events = telemetry.events_from_type('LogPlayerPosition')
```

### Loading a local Telemetry file

If you want to load a previously downloaded telemetry file, there is a helper
method to create a Telemetry object from it:

```python
from pubg_python import Telemetry

telemetry = Telemetry.from_json('telemetry.json', shard='pc')
```

`shard` defaults to `pc` but you need to specify if you're loading a `xbox` telemetry file.

## Tournaments

* Tournaments
  * [Official docs](https://documentation.playbattlegrounds.com/en/tournaments-endpoint.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)


### Retrieving a single tournament

```python
tournament = api.tournaments().get('na-ppc')
```

### Retrieving a list of tournaments

```python
tournaments = api.tournaments()
for tournament in tournaments:
    print(tournament)
```

## Seasons

* Seasons
  * [Official docs](https://documentation.pubg.com/en/seasons-endpoint.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)

### Retrieving the list of seasons

```python
seasons = api.seasons()
```

### Retrieving seasons information for a list of players

```python
players_seasons = api.seasons(
    season_id='division.bro.official.2018-09', game_mode='solo'
).filter(player_ids=['epickitten'])
```

It's also possible to retrieve lifetime stats, instead of a season_id:

```python
players_seasons = api.seasons(
    season_id='lifetime', game_mode='solo'
).filter(player_ids=['epickitten'])
```

### Retrieving season data for a specific player

```python
season_data = api.seasons(
    'division.bro.official.2018-09' , player_id='epickitten').get()
```

It's also possible to retrieve lifetime stats, instead of a season_id:

```python
season_data = api.seasons(
    'lifetime' , player_id='epickitten').get()
```

## Weapon Mastery

* Weapon Mastery
  * [Official docs](https://documentation.pubg.com/en/weapon-mastery-endpoint.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)

### Retrieving a weapon mastery data

```python
players = api.players().filter(player_names=['epickitten'])[0]
player = players[0]
wm = api.weapon_mastery(player.id).get()
print(wm.weapon_summaries)
```

## Leaderboards

* Leaderboards
  * [Official docs](https://documentation.pubg.com/en/leaderboards-endpoint.html)
  * [Data structure](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)

### Retrieving a leaderboard

```python
# Leaderboards stats are only available for PC players
api.shard = Shard.STEAM
solo_leaderboard = api.leaderboards(game_mode='solo').page(0).get()
solo_fpp_leaderboard = api.leaderboards(game_mode='solo-fpp').page(0).get()
duo_leaderboard = api.leaderboards(game_mode='duo').page(0).get()
duo_fpp_leaderboard = api.leaderboards(game_mode='duo-fpp').page(0).get()
squad_leaderboard = api.leaderboards(game_mode='squad').page(0).get()
squad_fpp_leaderboard = api.leaderboards(game_mode='squad-fpp').page(0).get()
```

`page` is always required, even when querying the first leaderboard page.

## Playing around with data

An example of how you can manipulate the data:
The domain is all specified [here](https://github.com/ramonsaraiva/pubg-python/blob/master/pubg_python/domain/base.py)

```python
players = api.players().filter(player_names=['epickitten'])
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

### Ratelimits

Each application has a limited amount of requests allowed per minute.
The ratelimit is managed through HTTP headers (`X-Ratelimit-Limit`, `X-Ratelimit-Reset`, etc..).
In order to facilitate heavy tasks, it is possible to retrieve those values from the `RateLimitError`. The values available in the exception instance are `rl_limit` (integer) and `rl_reset` (datetime).

An example snippet that would use this information in favor of processing something big:

```python
api = PUBG('my-super-secret-key', Shard.STEAM)

while True:
    try:
        print('Processing samples...')
        api.samples().get()
    except RateLimitError as error:
        sleep_seconds = (error.rl_reset - datetime.now()).total_seconds()
        if sleep_seconds > 0:
            print('Reached my limit! sleeping for {}'.format(sleep_seconds))
            time.sleep(sleep_seconds)
```

### Limits and Offsets

**Currently disabled from the official API**

Offsetting 5 matches and limitting by 10

```python
matches = api.matches().limit(10).offset(5)
```

### Sorting

**Currently disabled from the official API**

`sort` defaults to ascending, you can use `ascending=False` for a descending sort

```python
matches = api.matches().limit(10).sort('createdAt')
matches = api.matches().limit(10).sort('createdAt', ascending=False)
```

### Filtering

Some endpoints allow you to apply filters, for example, filtering players by names:

```python
players = api.players().filter(player_names=['Name1', 'Name2'])
```

Or filtering players by ids:

```python
players = api.players().filter(player_ids=['account.3654e255b77b409e87b10dcb086ab00d'])
```

### Pagination

Use `next()` for the next page and `prev()` for the previous one:

```python
matches = api.matches()
next_matches = matches.next()
previous_matches = matches.prev()
```

## Changelog

[CHANGELOG.md](https://github.com/ramonsaraiva/pubg-python/blob/master/CHANGELOG.md)

import os
from unittest import TestCase

from pubg_python import PUBG, Shard
from pubg_python.exceptions import (
    UnauthorizedError,
    InvalidShardError,
)


class TestApi(TestCase):
    def test_unauthorized(self):
        api = PUBG('', Shard.PC_NA)
        self.assertRaises(UnauthorizedError, api.players().get, '')

    def test_noshard(self):
        self.assertRaises(InvalidShardError, PUBG, '', 'NA')

    def test_player(self):
        api = PUBG(os.environ.get('PUBGapi'), Shard.PC_NA)
        players = api.players().filter(player_names=['shroud'])
        for player in players:
            player_id = player.id
        player = api.players().get(player_id)
        self.assertTrue(player.name)
        self.assertTrue(player.created_at)
        self.assertTrue(player.shard_id)
        self.assertTrue(player.title_id)
        self.assertTrue(player.updated_at)
        # Returns None
        # self.assertTrue(player.stats)
        # Returns an empty string
        # self.assertTrue(player.patch_version)

    def test_match(self):
        api = PUBG(os.environ.get('PUBGapi'), Shard.PC_NA)
        players = api.players().filter(player_names=['shroud'])
        for player in players:
            player_id = player.id
        player = api.players().get(player_id)
        match = api.matches().get(player.matches[0])
        self.assertTrue(match.map)
        self.assertTrue(match.created_at)
        self.assertTrue(match.duration)
        self.assertTrue(match.game_mode)
        self.assertTrue(match.title_id)
        self.assertTrue(match.shard_id)
        # Returns none
        # self.assertTrue(match.stats)
        # Returns an empty string
        # self.assertTrue(match.patch_version)
        # Returns none
        # self.assertTrue(match.tags)

        roster = match.rosters[0]
        self.assertTrue(roster.shard_id)
        self.assertTrue(roster.won)
        self.assertTrue(roster.stats)

        participant = roster.participants[0]
        self.assertTrue(participant.shard_id)
        self.assertTrue(participant.stats)
        # Returns none
        # self.assertTrue(participant.actor)

        # Stats

        # Minimum 0 according to api
        self.assertGreaterEqual(participant.dbnos, 0)
        self.assertGreaterEqual(participant.assists, 0)
        self.assertGreaterEqual(participant.boosts, 0)
        self.assertGreaterEqual(participant.damage_dealt, 0)
        self.assertGreaterEqual(participant.headshot_kills, 0)
        self.assertGreaterEqual(participant.heals, 0)
        self.assertGreaterEqual(participant.kills, 0)
        self.assertGreaterEqual(participant.last_kill_points, 0)
        self.assertGreaterEqual(participant.last_win_points, 0)
        self.assertGreaterEqual(participant.longest_kill, 0)
        self.assertGreaterEqual(participant.most_damage, 0)
        self.assertGreaterEqual(participant.revives, 0)
        self.assertGreaterEqual(participant.ride_distance, 0)
        self.assertGreaterEqual(participant.road_kills, 0)
        self.assertGreaterEqual(participant.team_kills, 0)
        self.assertGreaterEqual(participant.vehicle_destroys, 0)
        self.assertGreaterEqual(participant.weapons_acquired, 0)
        self.assertGreaterEqual(participant.boosts, 0)
        self.assertGreaterEqual(participant.damage_dealt, 0)

        # Between 1 and 100 according to api
        self.assertTrue(1 <= participant.kill_place <= 100)
        self.assertTrue(1 <= participant.win_place <= 100)

        # Between 0 and 99 according to api
        self.assertTrue(0 <= participant.kill_streaks <= 99)

        # Should be an number according to api
        self.assertTrue(type(participant.kill_points_delta) == float)
        self.assertTrue(type(participant.win_points_delta) == float)

        self.assertTrue(participant.name)
        self.assertTrue(participant.player_id)
        self.assertTrue(participant.time_survived)
        self.assertTrue(participant.walk_distance)
        self.assertTrue(participant.death_type)

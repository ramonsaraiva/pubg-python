from unittest import TestCase
from pubg_python.domain.telemetry.events import LogParachuteLanding
from pubg_python.domain.telemetry.objects import Character, Common


class ParachuteLandingTests(TestCase):
    data_json = {
        "character": {
            "name": "test",
            "teamId": 22,
            "health": 100,
            "location": {
                    "x": 665619.75,
                    "y": 114621.828125,
                    "z": 1911.15185546875
            },
            "ranking": 0,
            "accountId": "account.1234567890",
            "isInBlueZone": False,
            "isInRedZone": False,
            "zone": ["kameshki"]
        },
        "distance": 328.51821899414063,
        "common": {"isGame": 0.10000000149011612},
        "_D": "2019-03-10T23:31:50.564Z",
        "_T": "LogParachuteLanding"
    }

    character_json = {
        "name": "test",
        "teamId": 22,
        "health": 100,
        "location": {
                "x": 665619.75,
                "y": 114621.828125,
                "z": 1911.15185546875
        },
        "ranking": 0,
        "accountId": "1234567890",
        "isInBlueZone": False,
        "isInRedZone": False,
        "zone": ["kameshki"]
    }

    def setUp(self):
        self.actual = LogParachuteLanding(self.data_json)

    def test_parachute_landing(self):

        # expected = {
        #     "character": Character(self.character_json),
        #     "distance": 328.51821899414063,
        #     "event": "LogParachuteLanding",
        #     "timestamp": "2019-03-10T23:31:50.564Z",
        #     "common": Common({"isGame": 0.10000000149011612})
        # }

        self.assertIsInstance(self.actual.character, Character)
        self.assertIs(type(self.actual.distance), float)
        self.assertIs(type(self.actual.timestamp), str)
        self.assertEqual(self.actual.event, "LogParachuteLanding")
        self.assertIsInstance(self.actual.common, Common)

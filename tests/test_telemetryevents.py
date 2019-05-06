from unittest import TestCase
from pubg_python.domain.telemetry.events import LogParachuteLanding
from pubg_python.domain.telemetry.objects import Character, Common


class ParachuteLandingTests(TestCase):

    def setUp(self):
        self.data_json = {
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

    def test_parachute_landing(self):

        actual = LogParachuteLanding(self.data_json)

        self.assertIsInstance(actual.character, Character)
        self.assertIs(type(actual.distance), float)
        self.assertIs(type(actual.timestamp), str)
        self.assertEqual(actual.event, "LogParachuteLanding")
        self.assertIsInstance(actual.common, Common)

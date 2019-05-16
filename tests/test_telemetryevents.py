from unittest import TestCase
from pubg_python.domain.telemetry.events import LogParachuteLanding, LogItemPickupFromCarepackage
from pubg_python.domain.telemetry.objects import Character, Common, Item


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


class ItemPickupFromCarepackageTest(TestCase):

    def setUp(self):
        self.data_json = {
            "character": {
                "name": "Big_Erock",
                "teamId": 26,
                "health": 100,
                "location": {
                    "x": 496815.59375,
                    "y": 441357.90625,
                    "z": 755.76995849609375
                },
                "ranking": 0,
                "accountId": "account.80a96f67fbd44c65b6d3c9aa6c6be3cc",
                "isInBlueZone": False,
                "isInRedZone": False,
                "zone": []
            },
            "item": {
                "itemId": "Item_Head_G_01_Lv3_C",
                "stackCount": 1,
                "category": "Equipment",
                "subCategory": "Headgear",
                "attachedItems": []
            },
            "common": {"isGame": 1.5},
            "_D": "2019-05-15T00:14:32.168Z",
            "_T": "LogItemPickupFromCarepackage"
        }

    def test_item_pickup_carepackage(self):

        actual = LogItemPickupFromCarepackage(self.data_json)

        self.assertIsInstance(actual.character, Character)
        self.assertIsInstance(actual.item, Item)
        self.assertIsInstance(actual.common, Common)
        self.assertEqual(actual.event, "LogItemPickupFromCarepackage")

from .data import TelemetryData
from .resources import (
    ITEM_MAP,
    VEHICLE_MAP,
)


class Object:

    def __init__(self, data):
        self._data = data if isinstance(data, TelemetryData) else {}
        self.from_dict()

    def from_dict(self):
        pass


class Common(Object):

    def from_dict(self):
        super().from_dict()
        self.match_id = self._data.get('matchId')
        self.map_name = self._data.get('mapName')
        self.is_game = self._data.get('isGame')


class Location(Object):

    def from_dict(self):
        super().from_dict()
        self.x = self._data.get('x')
        self.y = self._data.get('y')
        self.z = self._data.get('z')


class Item(Object):

    def from_dict(self):
        super().from_dict()
        self.item_id = self._data.get('itemId')
        self.stack_count = self._data.get('stackCount')
        self.category = self._data.get('category')
        self.sub_category = self._data.get('subCategory')
        self.attached_items = [
            _id for _id in self._data.get('attachedItems', [])]

    def __str__(self):
        return self.name

    @property
    def name(self):
        return ITEM_MAP.get(self.item_id, 'Undefined')


class ItemPackage(Object):

    def from_dict(self):
        super().from_dict()
        self.item_package_id = self._data.get('itemPackageId')
        self.location = Location(self._data.get('location', {}))
        self.items = [
            Item(data) for data in self._data.get('items', [])]


class Character(Object):

    def from_dict(self):
        super().from_dict()
        self.name = self._data.get('name')
        self.team_id = self._data.get('teamId')
        self.health = self._data.get('health')
        self.location = Location(self._data.get('location', {}))
        self.ranking = self._data.get('ranking')
        self.account_id = self._data.get('accountId')


class Vehicle(Object):

    def from_dict(self):
        super().from_dict()
        self.vehicle_type = self._data.get('vehicleType')
        self.vehicle_id = self._data.get('vehicleId')
        self.health_percent = self._data.get('healthPercent')
        self.fuel_percent = self._data.get('fuelPercent')

    def __str__(self):
        return self.name

    @property
    def name(self):
        return VEHICLE_MAP.get(self.vehicle_id, 'Undefined')


class GameState(Object):

    def from_dict(self):
        super().from_dict()
        self.elapsed_time = self._data.get('elapsedTime')
        self.num_alive_teams = self._data.get('numAliveTeams')
        self.num_join_players = self._data.get('numJoinPlayers')
        self.num_start_players = self._data.get('numStartPlayers')
        self.num_alive_players = self._data.get('numAlivePlayers')
        self.safety_zone_position = self._data.get('safetyZonePosition')
        self.safety_zone_radius = self._data.get('safetyZoneRadius')
        self.poison_gas_warning_position = self._data.get(
            'poisonGasWarningPosition')
        self.poison_gas_warning_radius = self._data.get(
            'poisonGasWarningRadius')
        self.red_zone_position = self._data.get('redZonePosition')
        self.red_zone_radius = self._data.get('redZoneRadius')

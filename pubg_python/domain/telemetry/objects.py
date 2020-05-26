import json

from .data import TelemetryData
from .resources import (
    ITEM_MAP,
    VEHICLE_MAP,
)


class BaseObject:

    def deserialize(self, data):
        raise NotImplementedError

    def __init__(self, data):
        self._data = self.deserialize(data)
        self.from_dict()

    def from_dict(self):
        pass


class Object(BaseObject):

    def deserialize(self, data):
        # TODO: process nested objects as telemetry data
        return data if isinstance(data, (TelemetryData, dict)) else {}


class StringifiedObject(BaseObject):

    def deserialize(self, data):
        return json.loads(data)


class Common(Object):

    def from_dict(self):
        super().from_dict()
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
        self.is_in_blue_zone = self._data.get('isInBlueZone')
        self.is_in_red_zone = self._data.get('isInRedZone')
        self.zone = self._data.get('zone', [])


class Vehicle(Object):

    def from_dict(self):
        super().from_dict()
        self.vehicle_type = self._data.get('vehicleType')
        self.vehicle_id = self._data.get('vehicleId')
        self.vehicle_unique_id = self._data.get('vehicleUniqueId')
        self.vehicle_is_wheels_in_air = self._data.get('isWheelsInAir')
        self.vehicle_is_in_water_volume = self._data.get('isInWaterVolume')
        self.vehicle_is_engine_on = self._data.get('isEngineOn')
        self.health_percent = self._data.get('healthPercent')
        self.altitude_abs = self._data.get('altitudeAbs')
        self.altitude_rel = self._data.get('altitudeRel')
        self.velocity = self._data.get('velocity')

        # TODO: update feulPercent when fixed in API
        self.fuel_percent = self._data.get('feulPercent')

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
        self.black_zone_position = self._data.get('blackZonePosition')
        self.black_zone_radius = self._data.get('blackZoneRadius')


class BlueZone(Object):

    def from_dict(self):
        self.circle_algorithm = self._data.get('circleAlgorithm')
        self.land_ratio = self._data.get('landRatio')
        self.phase_num = self._data.get('phaseNum')
        self.poison_gas_dps = self._data.get('poisonGasDamagePerSecond')
        self.radius_rate = self._data.get('radiusRate')
        self.release_duration = self._data.get('releaseDuration')
        self.spread_ratio = self._data.get('spreadRatio')
        self.warning_duration = self._data.get('warningDuration')


class BlueZoneCustomOptions(StringifiedObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bz = []
        for bz_data in self._data:
            self._bz.append(BlueZone(bz_data))

    def __getitem__(self, index):
        return self._bz[index]

    def __len__(self):
        return len(self._bz)


class Stats(Object):

    def from_dict(self):
        super().from_dict()
        self.kill_count = self._data.get('killCount')
        self.distance_on_foot = self._data.get('distanceOnFoot')
        self.distance_on_swim = self._data.get('distanceOnSwim')
        self.distance_on_vehicle = self._data.get('distanceOnVehicle')
        self.distance_on_parachute = self._data.get('distanceOnParachute')
        self.distance_on_freefall = self._data.get('distanceOnFreefall')


class GameResult(Object):

    def from_dict(self):
        super().from_dict()
        self.rank = self._data.get('rank')
        self.game_result = self._data.get('gameResult')
        self.team_id = self._data.get('teamId')
        self.stats = Stats(self._data.get('stats', {}))
        self.account_id = self._data.get('accountId')

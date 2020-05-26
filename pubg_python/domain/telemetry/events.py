from . import objects


class Event:

    def __init__(self, data):
        self._data = data
        self.from_dict()

    def from_dict(self):
        self.event = self._data['_T']
        self.timestamp = self._data['_D']
        self.common = objects.Common(self._data.get('common', {}))

    @staticmethod
    def instance(data):
        return globals()[data['_T']](data)


class LogPlayerLogin(Event):

    def from_dict(self):
        super().from_dict()
        self.account_id = self._data.get('accountId')


class LogPlayerLogout(Event):

    def from_dict(self):
        self.account_id = self._data.get('accountId')


class LogPlayerCreate(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))


class LogPlayerPosition(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.vehicle = objects.Vehicle(self._data.get('vehicle', {}))
        self.elapsed_time = self._data.get('elapsedTime')
        self.num_alive_players = self._data.get('numAlivePlayers')


class LogWeaponFireCount(Event):

    def from_dict(self):
        self.character = objects.Character(self._data.get('character', {}))
        self.weapon_id = self._data.get('weaponId')
        self.fire_count = self._data.get('fireCount')


class LogPlayerAttack(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.fire_weapon_stack_count = self._data.get('fireWeaponStackCount')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.attack_type = self._data.get('attackType')
        self.weapon = objects.Item(self._data.get('weapon', {}))
        self.vehicle = objects.Vehicle(self._data.get('vehicle', {}))


class LogPlayerTakeDamage(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.victim = objects.Character(self._data.get('victim', {}))
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_reason = self._data.get('damageReason')
        self.damage = self._data.get('damage')
        self.damage_causer_name = self._data.get('damageCauserName')
        self.is_through_penetrable_wall = self._data.get(
            'isThroughPenetrableWall')


class LogPlayerUseFlareGun(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.fire_weapon_stack_count = self._data.get('fireWeaponStackCount')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.attack_type = self._data.get('attackType')
        self.weapon = objects.Item(self._data.get('weapon', {}))


class LogPlayerUseThrowable(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.fire_weapon_stack_count = self._data.get('fireWeaponStackCount')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.attack_type = self._data.get('attackType')
        self.weapon = objects.Item(self._data.get('weapon', {}))


class LogPlayerDestroyBreachableWall(Event):

    def from_dict(self):
        super().from_dict()
        self.attacker = objects.Character(self._data.get('character', {}))
        self.weapon = objects.Item(self._data.get('weapon', {}))


class LogPlayerKill(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.killer = objects.Character(self._data.get('killer', {}))
        self.victim = objects.Character(self._data.get('victim', {}))
        self.victim_weapon = self._data.get('victimWeapon')
        self.victim_weapon_additional_info = self._data.get(
            'victimWeaponAdditionalInfo')
        self.assistant = objects.Character(self._data.get('assistant', {}))
        self.dbno_id = self._data.get('dBNOId')
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_causer_name = self._data.get('damageCauserName')
        self.damage_causer_additional_info = self._data.get(
            'damageCauserAdditionalInfo', [])
        self.damage_reason = self._data.get('damageReason')
        self.distance = self._data.get('distance')
        self.victim_game_result = objects.GameResult(
            self._data.get('victimGameResult', {}))
        self.is_through_penetrable_wall = self._data.get(
            'isThroughPenetrableWall')


class LogParachuteLanding(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.distance = self._data.get('distance')


class LogItem(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.item = objects.Item(self._data.get('item', {}))


class LogItemPickup(LogItem):
    pass


class LogItemDrop(LogItem):
    pass


class LogItemEquip(LogItem):
    pass


class LogItemUnequip(LogItem):
    pass


class LogItemUse(LogItem):
    pass


class LogItemBundle(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.parent_item = objects.Item(self._data.get('parentItem', {}))
        self.child_item = objects.Item(self._data.get('childItem', {}))


class LogItemAttach(LogItemBundle):
    pass


class LogItemDetach(LogItemBundle):
    pass


class LogItemPickupFromCarepackage(LogItemPickup):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.item = objects.Item(self._data.get('item', {}))


class LogItemPickupFromLootBox(LogItemPickup):

    def from_dict(self):
        super().from_dict()
        self.creator_id = self._data.get('creatorAccountId')
        self.team_id = self._data.get('ownerTeamId')


class LogHeal(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.item = objects.Item(self._data.get('item', {}))
        self.heal_amount = self._data.get('healAmount')


class LogObjectDestroy(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.object_type = self._data.get('objectType')
        self.object_location = objects.Location(
            self._data.get('objectLocation', {}))


class LogObjectInteraction(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.object_type = self._data.get('objectType')
        self.object_type_status = self._data.get('objectTypeStatus')
        self.object_type_additional_info = self._data.get(
            'objectTypeAdditionalInfo')
        self.object_type_count = self._data.get('objectTypeCount')


class LogVaultStart(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))


class LogVehicle(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.vehicle = objects.Vehicle(self._data.get('vehicle', {}))


class LogVehicleRide(LogVehicle):

    def from_dict(self):
        super().from_dict()
        self.seat_index = self._data.get('seatIndex')
        self.fellow_passengers = [
            objects.Character(data)
            for data in self._data.get('fellowPassengers', [])
        ]


class LogVehicleLeave(LogVehicle):

    def from_dict(self):
        super().from_dict()
        self.ride_distance = self._data.get('rideDistance')
        self.seat_index = self._data.get('seatIndex')
        self.max_speed = self._data.get('maxSpeed')
        self.fellow_passengers = [
            objects.Character(data)
            for data in self._data.get('fellowPassengers', [])
        ]


class LogVehicleDestroy(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.vehicle = objects.Vehicle(self._data.get('vehicle', {}))
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_causer_name = self._data.get('damageCauserName')
        self.distance = self._data.get('distance')


class LogCarePackageEvent(Event):

    def from_dict(self):
        super().from_dict()
        self.item_package = objects.ItemPackage(
            self._data.get('itemPackage', {}))


class LogCarePackageSpawn(LogCarePackageEvent):
    pass


class LogCarePackageLand(LogCarePackageEvent):
    pass


class LogMatchDefinition(Event):

    def from_dict(self):
        super().from_dict()
        self.match_id = self._data.get('MatchId')
        self.ping_quality = self._data.get('PingQuality')
        self.season_state = self._data.get('SeasonState')


class LogBlackZoneEnded(Event):

    def from_dict(self):
        super().from_dict()
        self.survivors = [
            objects.Character(data)
            for data in self._data.get('characters', [])
        ]


class LogMatchEvent(Event):

    def from_dict(self):
        super().from_dict()
        self.characters = [
            objects.Character(data)
            for data in self._data.get('characters', [])
        ]


class LogMatchStart(LogMatchEvent):

    def from_dict(self):
        super().from_dict()
        # blueZoneCustomOptions data is a stringified array of objects
        # /en/telemetry-objects.html#bluezonecustomoptions
        self.blue_zone_custom_options = objects.BlueZoneCustomOptions(
            self._data.get('blueZoneCustomOptions'))
        self.camera_view_behaviour = self._data.get('cameraViewBehaviour')
        self.is_custom_game = self._data.get('isCustomGame')
        self.is_event_mode = self._data.get('isEventMode')
        self.map_name = self._data.get('mapName')
        self.team_size = self._data.get('teamSize')
        self.weather_id = self._data.get('weatherId')


class LogMatchEnd(LogMatchEvent):
    pass


class LogGameStatePeriodic(Event):

    def from_dict(self):
        super().from_dict()
        self.game_state = objects.GameState(self._data.get('gameState', {}))


class LogSwim(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))


class LogSwimStart(LogSwim):
    pass


class LogSwimEnd(LogSwim):

    def from_dict(self):
        super().from_dict()
        self.swim_distance = self._data.get('swimDistance')
        self.max_swim_depth_of_water = self._data.get('maxSwimDepthOfWater')


class LogArmorDestroy(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.victim = objects.Character(self._data.get('victim', {}))
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_reason = self._data.get('damageReason')
        self.damage_causer_name = self._data.get('damageCauserName')
        self.item = objects.Item(self._data.get('item', {}))
        self.distance = self._data.get('distance')


class LogWheelDestroy(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.vehicle = objects.Vehicle(self._data.get('vehicle', {}))
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_causer_name = self._data.get('damageCauserName')


class LogPlayerMakeGroggy(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.victim = objects.Character(self._data.get('victim', {}))
        self.victim_weapon = self._data.get('victimWeapon')
        self.victim_weapon_additional_info = self._data.get(
            'victimWeaponAdditionalInfo')
        self.damage_reason = self._data.get('damageReason')
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_causer_name = self._data.get('damageCauserName')
        self.damage_causer_additional_info = self._data.get(
            'damageCauserAdditionalInfo', [])
        self.distance = self._data.get('distance')
        self.is_attacker_in_vehicle = self._data.get('isAttackerInVehicle')
        self.dbno_id = self._data.get('dBNOId')


class LogPlayerRevive(Event):

    def from_dict(self):
        super().from_dict()
        self.reviver = objects.Character(self._data.get('reviver', {}))
        self.victim = objects.Character(self._data.get('victim', {}))
        self.dbno_id = self._data.get('dBNOId')


class LogRedZoneEnded(Event):

    def from_dict(self):
        super().from_dict()
        self.drivers = self._data.get('drivers', [])


class LogPhaseChange(Event):

    def from_dict(self):
        super().from_dict()
        self.phase = self._data.get('phase')

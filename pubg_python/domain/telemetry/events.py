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
        self.result = self._data.get('Result')
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
        self.elapsed_time = self._data.get('elapsedTime')
        self.num_alive_players = self._data.get('numAlivePlayers')


class LogPlayerAttack(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
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


class LogPlayerKill(Event):

    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.killer = objects.Character(self._data.get('killer', {}))
        self.victim = objects.Character(self._data.get('victim', {}))
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_reason = self._data.get('damageReason')
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


class LogVehicle(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))
        self.vehicle = objects.Vehicle(self._data.get('vehicle', {}))


class LogVehicleRide(LogVehicle):
    pass


class LogVehicleLeave(LogVehicle):
    pass


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
        self.match_id = self._data.get('matchId')
        self.ping_quality = self._data.get('pingQuality')


class LogMatchEvent(Event):

    def from_dict(self):
        super().from_dict()
        self.characters = [
            objects.Character(data)
            for data in self._data.get('characters', [])
        ]


class LogMatchStart(LogMatchEvent):
    pass


class LogMatchEnd(LogMatchEvent):
    pass


class LogGameStatePeriodic(Event):

    def from_dict(self):
        super().from_dict()
        self.game_state = objects.GameState(self._data.get('gameState', {}))


class LogSwimStart(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))


class LogSwimEnd(Event):

    def from_dict(self):
        super().from_dict()
        self.character = objects.Character(self._data.get('character', {}))


class LogArmorDestroy(Event):
    """docstring for LogArmorDestroy"""
    def from_dict(self):
        super().from_dict()
        self.attack_id = self._data.get('attackId')
        self.attacker = objects.Character(self._data.get('attacker', {}))
        self.vehicle = objects.Vehicle(self._data.get('vehicle', {}))
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_causer_name = self._data.get('damageCauserName')
        self.distance = self._data.get('distance')
        self.item = objects.Item(self._data.get('item', {}))
        self.victim = objects.Character(self._data.get('victim', {}))
        self.damage_reason = self._data.get('damageReason')


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
        self.damage_type_category = self._data.get('damageTypeCategory')
        self.damage_causer_name = self._data.get('damageCauserName')
        self.distance = self._data.get('distance')
        self.is_attacker_in_vehicle = self._data.get('isAttackerInVehicle')
        self.dbno_id = self._data.get('dBNOId')


class LogPlayerRevive(Event):
    def from_dict(self):
        super().from_dict()
        self.reviver = objects.Character(self._data.get('reviver', {}))
        self.victim = objects.Character(self._data.get('victim', {}))

from pubg_python.base import Telemetry
from pubg_python.domain.telemetry.events import (
    LogPlayerLogin,
    LogPlayerLogout,
    LogPlayerCreate,
    LogPlayerPosition,
    LogWeaponFireCount,
    LogPlayerAttack,
    LogPlayerTakeDamage,
    LogPlayerKill,
    LogParachuteLanding,
    LogItemPickup,
    LogItemDrop,
    LogItemEquip,
    LogItemUnequip,
    LogItemUse,
    LogItemAttach,
    LogItemDetach,
    LogItemPickupFromCarepackage,
    LogItemPickupFromLootBox,
    LogHeal,
    LogObjectDestroy,
    LogObjectInteraction,
    LogVaultStart,
    LogVehicleRide,
    LogVehicleLeave,
    LogVehicleDestroy,
    LogCarePackageSpawn,
    LogCarePackageLand,
    LogMatchDefinition,
    LogMatchStart,
    LogMatchEnd,
    LogGameStatePeriodic,
    LogSwimStart,
    LogSwimEnd,
    LogArmorDestroy,
    LogWheelDestroy,
    LogPlayerMakeGroggy,
    LogPlayerRevive,
    LogRedZoneEnded,
    LogPhaseChange,
    LogPlayerUseThrowable
)
from pubg_python.domain.telemetry.objects import (
    Location,
    Item,
    ItemPackage,
    Character,
    Vehicle,
    GameState,
    BlueZone,
    BlueZoneCustomOptions,
    GameResult
)
from pubg_python.domain.telemetry.resources import (
    ITEM_MAP,
    VEHICLE_MAP,
    DAMAGE_CAUSER_MAP,
    DAMAGE_TYPE_MAP,
    ATTACK_TYPE,
    DAMAGE_REASON,
    MAP_NAME,
    WEATHER_MAP,
    OBJECT_TYPE,
    OBJECT_TYPE_STATUS
)

telemetry = Telemetry.from_json('tests/telemetry_response.json')
ITEM_MAP_VALUES = ITEM_MAP.values()
VEHICLE_MAP_VALUES = VEHICLE_MAP.values()


def test_log_player_login():
    events = telemetry.events_from_type('LogPlayerLogin')
    data = events[0]
    assert isinstance(data, LogPlayerLogin)


def test_log_player_logout():
    events = telemetry.events_from_type('LogPlayerLogout')
    data = events[0]
    assert isinstance(data, LogPlayerLogout)


def test_log_player_create():
    events = telemetry.events_from_type('LogPlayerCreate')
    data = events[0]
    assert isinstance(data, LogPlayerCreate)
    assert isinstance(data.character, Character)


def test_log_player_position():
    events = telemetry.events_from_type('LogPlayerPosition')
    for i in events:
        if isinstance(i.vehicle, Vehicle):
            data = i
            break
    assert isinstance(data, LogPlayerPosition)
    assert isinstance(data.character, Character)
    assert isinstance(data.vehicle, Vehicle)
    if data.vehicle.vehicle_id:
        assert str(data.vehicle) in VEHICLE_MAP_VALUES
    assert isinstance(data.elapsed_time, int)
    assert isinstance(data.num_alive_players, int)


def test_log_weapon_fire_count():
    events = telemetry.events_from_type('LogWeaponFireCount')
    data = events[0]
    assert isinstance(data, LogWeaponFireCount)
    assert isinstance(data.character, Character)
    assert isinstance(data.fire_count, int)
    assert data.weapon_id in ITEM_MAP


def test_log_player_attack():
    events = telemetry.events_from_type('LogPlayerAttack')
    for e in events:
        if e.weapon.item_id != '':
            data = e
            break
    assert isinstance(data, LogPlayerAttack)
    assert isinstance(data.attacker, Character)
    assert isinstance(data.weapon, Item)
    assert isinstance(data.vehicle, Vehicle)
    assert isinstance(data.attack_id, int)
    if data.vehicle.vehicle_id:
        assert str(data.vehicle) in VEHICLE_MAP_VALUES
    assert str(data.weapon) in ITEM_MAP_VALUES
    assert data.attack_type in ATTACK_TYPE


def test_log_player_take_damage():
    events = telemetry.events_from_type('LogPlayerTakeDamage')
    data = events[0]
    assert isinstance(data, LogPlayerTakeDamage)
    assert isinstance(data.attacker, Character)
    assert isinstance(data.victim, Character)
    assert data.damage > 0
    assert data.damage_type_category in DAMAGE_TYPE_MAP
    assert data.damage_reason in DAMAGE_REASON
    assert data.damage_causer_name in DAMAGE_CAUSER_MAP


def test_log_player_kill():
    events = telemetry.events_from_type('LogPlayerKill')
    data = events[50]
    assert isinstance(data, LogPlayerKill)
    assert isinstance(data.killer, Character)
    assert isinstance(data.victim, Character)
    assert isinstance(data.assistant, Character)
    assert isinstance(data.victim_game_result, GameResult)
    assert isinstance(data.attack_id, int)
    assert isinstance(data.dbno_id, int)
    assert isinstance(data.distance, float)
    assert all(x in ITEM_MAP for x in data.victim_weapon_additional_info)
    assert all(x in ITEM_MAP for x in data.damage_causer_additional_info)
    assert data.damage_type_category in DAMAGE_TYPE_MAP
    assert data.damage_causer_name in DAMAGE_CAUSER_MAP
    assert data.damage_reason in DAMAGE_REASON
    if data.victim_weapon:
        cut_idx = data.victim_weapon.index('_C_') + 2
        assert data.victim_weapon[:cut_idx] in DAMAGE_CAUSER_MAP


def test_log_parachute_landing():
    events = telemetry.events_from_type('LogParachuteLanding')
    data = events[50]
    assert isinstance(data, LogParachuteLanding)
    assert isinstance(data.character, Character)
    assert isinstance(data.distance, float)


def test_log_item_pickup():
    events = telemetry.events_from_type('LogItemPickup')
    data = events[0]
    assert isinstance(data, LogItemPickup)
    assert isinstance(data.character, Character)
    assert isinstance(data.item, Item)
    assert str(data.item) in ITEM_MAP_VALUES


def test_log_item_drop():
    events = telemetry.events_from_type('LogItemDrop')
    data = events[0]
    assert isinstance(data, LogItemDrop)
    assert isinstance(data.character, Character)
    assert isinstance(data.item, Item)
    assert str(data.item) in ITEM_MAP_VALUES


def test_log_item_equip():
    events = telemetry.events_from_type('LogItemEquip')
    data = events[0]
    assert isinstance(data, LogItemEquip)
    assert isinstance(data.character, Character)
    assert isinstance(data.item, Item)
    assert str(data.item) in ITEM_MAP_VALUES


def test_log_item_unequip():
    events = telemetry.events_from_type('LogItemUnequip')
    data = events[0]
    assert isinstance(data, LogItemUnequip)
    assert isinstance(data.character, Character)
    assert isinstance(data.item, Item)
    assert str(data.item) in ITEM_MAP_VALUES


def test_log_item_use():
    events = telemetry.events_from_type('LogItemUse')
    data = events[0]
    assert isinstance(data, LogItemUse)
    assert isinstance(data.character, Character)
    assert isinstance(data.item, Item)
    assert str(data.item) in ITEM_MAP_VALUES


def test_log_item_attach():
    events = telemetry.events_from_type('LogItemAttach')
    data = events[0]
    assert isinstance(data, LogItemAttach)
    assert isinstance(data.character, Character)
    assert isinstance(data.parent_item, Item)
    assert isinstance(data.child_item, Item)
    assert str(data.parent_item) in ITEM_MAP_VALUES
    assert str(data.child_item) in ITEM_MAP_VALUES


def test_log_item_detach():
    events = telemetry.events_from_type('LogItemDetach')
    data = events[0]
    assert isinstance(data, LogItemDetach)
    assert isinstance(data.character, Character)
    assert isinstance(data.parent_item, Item)
    assert isinstance(data.child_item, Item)
    assert str(data.parent_item) in ITEM_MAP_VALUES
    assert str(data.child_item) in ITEM_MAP_VALUES


def test_log_item_pickup_from_care_package():
    events = telemetry.events_from_type('LogItemPickupFromCarepackage')
    data = events[0]
    assert isinstance(data, LogItemPickupFromCarepackage)
    assert isinstance(data.character, Character)
    assert isinstance(data.item, Item)
    assert str(data.item) in ITEM_MAP_VALUES


def test_log_item_pickup_from_loot_box():
    events = telemetry.events_from_type('LogItemPickupFromLootBox')
    data = events[0]
    assert isinstance(data, LogItemPickupFromLootBox)
    assert isinstance(data.creator_id, str)
    assert isinstance(data.team_id, int)


def test_log_heal():
    events = telemetry.events_from_type('LogHeal')
    data = events[0]
    assert isinstance(data, LogHeal)
    assert isinstance(data.heal_amount, int)


def test_log_object_destroy():
    events = telemetry.events_from_type('LogObjectDestroy')
    data = events[0]
    assert isinstance(data, LogObjectDestroy)
    assert isinstance(data.character, Character)
    assert isinstance(data.object_location, Location)
    assert data.object_type in OBJECT_TYPE


def test_log_object_intercation():
    events = telemetry.events_from_type('LogObjectInteraction')
    data = events[0]
    assert isinstance(data, LogObjectInteraction)
    assert isinstance(data.character, Character)
    assert isinstance(data.object_type_count, int)
    assert data.object_type in OBJECT_TYPE
    assert data.object_type_status in OBJECT_TYPE_STATUS


def test_log_vault_start():
    events = telemetry.events_from_type('LogVaultStart')
    data = events[0]
    assert isinstance(data, LogVaultStart)
    assert isinstance(data.character, Character)


def test_log_vehicle_ride():
    events = telemetry.events_from_type('LogVehicleRide')
    for idx, ev in enumerate(events):
        if ev.fellow_passengers and ev.vehicle.fuel_percent != 0:
            data = events[idx]
            break
    else:
        assert False
    assert isinstance(data, LogVehicleRide)
    assert isinstance(data.character, Character)
    assert isinstance(data.vehicle, Vehicle)
    if data.vehicle.health_percent != 100:
        assert isinstance(data.vehicle.health_percent, float)
    assert isinstance(data.vehicle.fuel_percent, float)
    assert isinstance(data.vehicle.vehicle_id, str)
    assert isinstance(data.vehicle.vehicle_unique_id, int)
    assert isinstance(data.vehicle.vehicle_is_wheels_in_air, bool)
    assert isinstance(data.vehicle.vehicle_is_in_water_volume, bool)
    assert isinstance(data.seat_index, int)
    assert str(data.vehicle) in VEHICLE_MAP_VALUES


def test_log_vehicle_leave():
    events = telemetry.events_from_type('LogVehicleLeave')
    for idx, ev in enumerate(events):
        if ev.fellow_passengers and ev.vehicle.fuel_percent != 0:
            data = events[idx]
            break
    else:
        assert False
    assert isinstance(data, LogVehicleLeave)
    assert isinstance(data.character, Character)
    assert isinstance(data.vehicle, Vehicle)
    if data.vehicle.health_percent != 100:
        assert isinstance(data.vehicle.health_percent, float)
    assert isinstance(data.vehicle.fuel_percent, float)
    assert isinstance(data.vehicle.vehicle_id, str)
    assert isinstance(data.vehicle.vehicle_unique_id, int)
    assert isinstance(data.vehicle.vehicle_is_wheels_in_air, bool)
    assert isinstance(data.vehicle.vehicle_is_in_water_volume, bool)
    assert isinstance(data.fellow_passengers[0], Character)
    assert isinstance(data.seat_index, int)
    assert isinstance(data.ride_distance, float)
    assert isinstance(data.max_speed, float)
    assert str(data.vehicle) in VEHICLE_MAP_VALUES


def test_log_vehicle_destroy():
    events = telemetry.events_from_type('LogVehicleDestroy')
    data = events[0]
    assert isinstance(data, LogVehicleDestroy)
    assert isinstance(data.attacker, Character)
    assert isinstance(data.vehicle, Vehicle)
    assert isinstance(data.attack_id, int)
    assert isinstance(data.distance, float)
    assert data.damage_type_category in DAMAGE_TYPE_MAP
    assert data.damage_causer_name in DAMAGE_CAUSER_MAP
    assert str(data.vehicle) in VEHICLE_MAP_VALUES


def test_log_care_package_spawn():
    events = telemetry.events_from_type('LogCarePackageSpawn')
    data = events[0]
    assert isinstance(data, LogCarePackageSpawn)
    assert isinstance(data.item_package, ItemPackage)


def test_log_care_package_land():
    events = telemetry.events_from_type('LogCarePackageLand')
    data = events[0]
    assert isinstance(data, LogCarePackageLand)
    assert isinstance(data.item_package, ItemPackage)


def test_log_match_definition():
    events = telemetry.events_from_type('LogMatchDefinition')
    data = events[0]
    assert isinstance(data, LogMatchDefinition)
    assert isinstance(data.match_id, str)
    if data.ping_quality:
        assert isinstance(data.ping_quality, str)
    assert isinstance(data.season_state, str)


def test_log_match_start():
    events = telemetry.events_from_type('LogMatchStart')
    data = events[0]
    assert isinstance(data, LogMatchStart)
    assert isinstance(data.characters, list)
    assert isinstance(data.characters[0], Character)
    assert isinstance(data.blue_zone_custom_options, BlueZoneCustomOptions)
    assert isinstance(data.camera_view_behaviour, str)
    assert isinstance(data.is_custom_game, bool)
    assert isinstance(data.is_event_mode, bool)
    assert isinstance(data.team_size, int)
    if len(data.blue_zone_custom_options) == 0:
        stringified = """
            [{"phaseNum":0,"startDelay":120,"warningDuration":300,
              "releaseDuration":300,
              "poisonGasDamagePerSecond":0.40000000596046448,
              "radiusRate":0.34999999403953552,"spreadRatio":0.5,
              "landRatio":0.55000001192092896,"circleAlgorithm":0}]
        """.replace('\n', ' ')
        data.blue_zone_custom_options = BlueZoneCustomOptions(stringified)
    blue_zone = data.blue_zone_custom_options[0]
    isinstance(blue_zone, BlueZone)
    isinstance(blue_zone.circle_algorithm, int)
    isinstance(blue_zone.land_ratio, float)
    isinstance(blue_zone.phase_num, int)
    isinstance(blue_zone.poison_gas_dps, float)
    isinstance(blue_zone.radius_rate, float)
    isinstance(blue_zone.release_duration, int)
    isinstance(blue_zone.spread_ratio, float)
    isinstance(blue_zone.warning_duration, int)
    assert data.weather_id in WEATHER_MAP
    assert data.map_name in MAP_NAME


def test_log_match_end():
    events = telemetry.events_from_type('LogMatchEnd')
    data = events[0]
    assert isinstance(data, LogMatchEnd)
    assert isinstance(data.characters, list)
    assert isinstance(data.characters[0], Character)


def test_log_game_state_periodic():
    events = telemetry.events_from_type('LogGameStatePeriodic')
    data = events[0]
    assert isinstance(data, LogGameStatePeriodic)
    assert isinstance(data.game_state, GameState)


def test_log_swim_start():
    events = telemetry.events_from_type('LogSwimStart')
    data = events[0]
    assert isinstance(data, LogSwimStart)
    assert isinstance(data.character, Character)


def test_log_swim_end():
    events = telemetry.events_from_type('LogSwimEnd')
    data = events[0]
    assert isinstance(data, LogSwimEnd)
    assert isinstance(data.character, Character)
    assert isinstance(data.swim_distance, float)
    assert isinstance(data.max_swim_depth_of_water, float)


def test_log_armor_destroy():
    events = telemetry.events_from_type('LogArmorDestroy')
    data = events[0]
    assert isinstance(data, LogArmorDestroy)
    assert isinstance(data.attacker, Character)
    assert isinstance(data.victim, Character)
    assert isinstance(data.item, Item)
    assert isinstance(data.attack_id, int)
    assert isinstance(data.distance, float)
    assert data.damage_type_category in DAMAGE_TYPE_MAP
    assert data.damage_reason in DAMAGE_REASON
    assert data.damage_causer_name in DAMAGE_CAUSER_MAP
    assert data.item.item_id in ITEM_MAP


def test_log_wheel_destroy():
    events = telemetry.events_from_type('LogWheelDestroy')
    data = events[0]
    assert isinstance(data, LogWheelDestroy)
    assert isinstance(data.attacker, Character)
    assert isinstance(data.vehicle, Vehicle)
    assert isinstance(data.attack_id, int)
    assert data.damage_type_category in DAMAGE_TYPE_MAP
    assert data.damage_causer_name in DAMAGE_CAUSER_MAP


def test_log_player_make_groggy():
    events = telemetry.events_from_type('LogPlayerMakeGroggy')
    data = events[25]
    assert isinstance(data, LogPlayerMakeGroggy)
    assert isinstance(data.attacker, Character)
    assert isinstance(data.victim, Character)
    assert isinstance(data.attack_id, int)
    assert isinstance(data.is_attacker_in_vehicle, bool)
    assert isinstance(data.dbno_id, int)
    assert isinstance(data.distance, float)
    assert all(x in ITEM_MAP for x in data.victim_weapon_additional_info)
    assert all(x in ITEM_MAP for x in data.damage_causer_additional_info)
    assert data.damage_type_category in DAMAGE_TYPE_MAP
    assert data.damage_causer_name in DAMAGE_CAUSER_MAP
    assert data.damage_reason in DAMAGE_REASON
    if not data.victim_weapon:
        assert True
    else:
        cut_idx = data.victim_weapon.index('_C_') + 2
        assert data.victim_weapon[:cut_idx] in DAMAGE_CAUSER_MAP


def test_log_player_revive():
    events = telemetry.events_from_type('LogPlayerRevive')
    data = events[0]
    assert isinstance(data, LogPlayerRevive)
    assert isinstance(data.reviver, Character)
    assert isinstance(data.victim, Character)
    assert isinstance(data.dbno_id, int)


def test_log_red_zone_ended():
    events = telemetry.events_from_type('LogRedZoneEnded')
    data = events[0]
    assert isinstance(data, LogRedZoneEnded)
    assert isinstance(data.drivers, list)


def test_log_phase_change():
    events = telemetry.events_from_type('LogPhaseChange')
    data = events[0]
    assert isinstance(data, LogPhaseChange)
    assert isinstance(data.phase, int)


def test_log_player_use_throwable():
    events = telemetry.events_from_type('LogPlayerUseThrowable')
    data = events[0]
    assert isinstance(data, LogPlayerUseThrowable)
    assert isinstance(data.attacker, Character)
    assert isinstance(data.weapon, Item)
    assert isinstance(data.fire_weapon_stack_count, int)
    assert data.attack_type in ATTACK_TYPE

import json
import os
import unittest

from unittest.mock import MagicMock

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types
from pywink.devices.key import WinkKey
from pywink.devices.powerstrip import WinkPowerStripOutlet, WinkPowerStrip
from pywink.devices.piggy_bank import WinkPorkfolioBalanceSensor, WinkPorkfolioNose
from pywink.devices.siren import WinkSiren
from pywink.devices.eggtray import WinkEggtray
from pywink.devices.remote import WinkRemote
from pywink.devices.fan import WinkFan, WinkGeZwaveFan
from pywink.devices.binary_switch import WinkBinarySwitch
from pywink.devices.hub import WinkHub
from pywink.devices.light_bulb import WinkLightBulb
from pywink.devices.thermostat import WinkThermostat
from pywink.devices.shade import WinkShade
from pywink.devices.sprinkler import WinkSprinkler
from pywink.devices.button import WinkButton
from pywink.devices.gang import WinkGang
from pywink.devices.camera import WinkCanaryCamera
from pywink.devices.air_conditioner import WinkAirConditioner
from pywink.devices.propane_tank import WinkPropaneTank
from pywink.devices.scene import WinkScene
from pywink.devices.robot import WinkRobot
from pywink.devices.water_heater import WinkWaterHeater


class BaseTests(unittest.TestCase):

    def setUp(self):
        super(BaseTests, self).setUp()
        self.api_interface = MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if (os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_all_devices_are_available(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        for device in devices:
            self.assertTrue(device.available())

    def test_all_devices_have_pubnub_channel(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        for device in devices:
            self.assertIsNotNone(device.pubnub_channel)

    def test_all_devices_have_pubnub_key(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        for device in devices:
            self.assertIsNotNone(device.pubnub_key)

    def test_all_devices_have_object_id(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        for device in devices:
            self.assertIsNotNone(device.object_id())
            self.assertRegex(device.object_id(), "^[0-9]{3,7}$")

    def test_all_devices_state_should_not_be_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        for device in devices:
            self.assertIsNotNone(device.state())

    def test_all_devices_name_is_not_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        for device in devices:
            self.assertIsNotNone(device.name())

    def test_all_devices_state_is_not_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        for device in devices:
            self.assertIsNotNone(device.state())

    def test_all_devices_battery_is_valid(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        skip_types = [WinkFan, WinkGeZwaveFan, WinkPorkfolioBalanceSensor, WinkPorkfolioNose, WinkBinarySwitch, WinkHub,
                      WinkLightBulb, WinkThermostat, WinkKey, WinkPowerStrip, WinkPowerStripOutlet,
                      WinkRemote, WinkShade, WinkSprinkler, WinkButton, WinkGang, WinkCanaryCamera,
                      WinkAirConditioner, WinkScene, WinkRobot, WinkWaterHeater]
        for device in devices:
            if device.manufacturer_device_model() == "leaksmart_valve":
                self.assertIsNotNone(device.battery_level())
            elif type(device) in skip_types:
                self.assertIsNone(device.battery_level())
            elif device.manufacturer_device_model() == "wink_relay_sensor":
                self.assertIsNone(device.battery_level())
            elif device.device_manufacturer() == "dropcam":
                self.assertIsNone(device.battery_level())
            elif device.model_name() == "Nest Cam":
                self.assertIsNone(device.battery_level())
            elif device._last_reading.get('external_power'):
                self.assertIsNone(device.battery_level())
            else:
                self.assertIsNotNone(device.battery_level())

    def test_all_devices_manufacturer_device_model_state_is_valid(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        skip_types = [WinkKey, WinkPorkfolioBalanceSensor, WinkPorkfolioNose, WinkPowerStripOutlet,
                      WinkSiren, WinkEggtray, WinkRemote, WinkPowerStrip, WinkAirConditioner, WinkPropaneTank]
        devices_with_no_device_model = ["GoControl Thermostat", "New Shortcut", "Test robot", "August lock"]
        for device in devices:
            if type(device) in skip_types:
                self.assertIsNone(device.manufacturer_device_model())
            elif device.name() in devices_with_no_device_model:
                self.assertIsNone(device.manufacturer_device_model())
            else:
                self.assertIsNotNone(device.manufacturer_device_model())

    def test_all_devices_manufacturer_device_id_state_is_valid(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        skip_types = [WinkKey, WinkPowerStrip, WinkPowerStripOutlet, WinkPorkfolioBalanceSensor, WinkPorkfolioNose,
                      WinkSiren, WinkEggtray, WinkRemote, WinkButton, WinkAirConditioner, WinkPropaneTank,
                      WinkGeZwaveFan]
        skip_manufactuer_device_models = ["linear_wadwaz_1",  "linear_wapirz_1", "aeon_labs_dsb45_zwus", "wink_hub", "wink_hub2", "sylvania_sylvania_ct",
                                          "ge_bulb", "quirky_ge_spotter", "schlage_zwave_lock", "home_decorators_home_decorators_fan",
                                          "sylvania_sylvania_rgbw", "somfy_bali", "wink_relay_sensor", "wink_project_one", "kidde_smoke_alarm",
                                          "wink_relay_switch", "leaksmart_valve", "home_decorators_home_decorators_light_bulb", "dome_dmwv1"]
        skip_names = ["GoControl Thermostat", "GE Zwave Switch", "New Shortcut", "Test robot"]
        for device in devices:
            if device.name() in skip_names:
                self.assertIsNone(device.manufacturer_device_id())
            elif device.manufacturer_device_model() in skip_manufactuer_device_models:
                self.assertIsNone(device.manufacturer_device_id())
            elif type(device) in skip_types:
                self.assertIsNone(device.manufacturer_device_id())
            else:
                self.assertIsNotNone(device.manufacturer_device_id())

    def test_all_devices_device_manufacturer_is_valid(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        device_with_no_manufacturer = ["GoControl Thermostat", "New Shortcut", "Test robot", "August lock"]
        for device in devices:
            if type(device) is WinkKey:
                self.assertIsNone(device.device_manufacturer())
            elif device.name() in device_with_no_manufacturer:
                self.assertIsNone(device.device_manufacturer())
            elif type(device) is WinkPowerStripOutlet:
                self.assertIsNone(device.device_manufacturer())
            else:
                self.assertIsNotNone(device.device_manufacturer())

    def test_all_devices_model_name_is_valid(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.ALL_SUPPORTED_DEVICES)
        devices_with_no_model_name = ["GoControl Thermostat", "New Shortcut", "Test robot", "August lock"]
        for device in devices:
            if type(device) is WinkKey:
                self.assertIsNone(device.model_name())
            elif device.name() in devices_with_no_model_name:
                self.assertIsNone(device.model_name())
            elif type(device) is WinkPowerStripOutlet:
                self.assertIsNone(device.model_name())
            else:
                self.assertIsNotNone(device.model_name())

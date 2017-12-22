import json
import os
import unittest

from unittest.mock import MagicMock

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types


class ThermostatTests(unittest.TestCase):

    def setUp(self):
        super(ThermostatTests, self).setUp()
        self.api_interface = MagicMock()

    def test_thermostat_state(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/nest.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.state(), "heat_only")

    def test_thermostat_fan_modes(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.fan_modes(), ["on", "auto"])

    def test_thermostat_hvac_modes(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.hvac_modes(), ["heat_only", "cool_only", "auto", "aux"])

    def test_thermostat_users_away(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/nest.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        thermostat2 = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[1]
        self.assertTrue(thermostat.away())
        self.assertEqual(thermostat2.away(), None)

    def test_thermostat_users_away_generic(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.away() is None)

    def test_thermostat_profile(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/ecobee_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.away())

    def test_thermostat_current_fan_mode(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_fan_mode(), "auto")

    def test_thermostat_current_units(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_units().get('temperature'), "f")

    def test_thermostat_current_temperature(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_temperature(), 20.0)

    def test_thermostat_current_external_temperature(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_external_temperature(), 16.1)

    def test_thermostat_current_humidity(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_humidity(), 40)

    def test_thermostat_smart_temperature(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/ecobee_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_smart_temperature(), 21.5)

    def test_thermostat_max_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/ecobee_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_max_set_point(), 25.555555555555557)

    def test_thermostat_min_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/ecobee_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_min_set_point(), 21.666666666666668)

    def test_thermostat_current_humidifier_mode(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_humidifier_mode(), "auto")

    def test_thermostat_current_dehumidifier_mode(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_dehumidifier_mode(), "auto")

    def test_thermostat_current_humidifier_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_humidifier_set_point(), 0.2)

    def test_thermostat_current_dehumidifier_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.current_dehumidifier_set_point(), 0.6)

    def test_thermostat_min_min_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.min_min_set_point(), 7.222222222222222)

    def test_thermostat_min_max_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.min_max_set_point(), 7.222222222222222)

    def test_thermostat_max_min_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.max_min_set_point(), 37.22222222222222)

    def test_thermostat_max_max_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.max_max_set_point(), 37.22222222222222)

    def test_thermostat_eco_target(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/nest.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertFalse(thermostat.eco_target())

    def test_thermostat_occupied(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/ecobee_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertFalse(thermostat.occupied())

    def test_thermostat_deadband(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/ecobee_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertEqual(thermostat.deadband(), 2.7777777777777777)

    def test_thermostat_fan_active(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.fan_on())

    def test_thermostat_has_fan(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.has_fan())
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/ecobee_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.has_fan())
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/nest.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertFalse(thermostat.has_fan())
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/go_control_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.has_fan())

    def test_thermostat_is_on(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.is_on())

    def test_thermostat_heat_on(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertTrue(thermostat.heat_on())

    def test_thermostat_cool_on(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/sensi_thermostat.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        thermostat = get_devices_from_response_dict(response_dict, device_types.THERMOSTAT)[0]
        self.assertFalse(thermostat.cool_on())

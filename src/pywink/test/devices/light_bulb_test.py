import json
import os
import unittest

from unittest.mock import MagicMock

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types
from pywink.devices.light_group import WinkLightGroup

JSON_DATA = {}


class LightBulbTests(unittest.TestCase):

    def setUp(self):
        super(LightBulbTests, self).setUp()
        self.api_interface = MagicMock()

    def test_bulb_brightness(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/lightify_rgbw_bulb.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        bulb = get_devices_from_response_dict(response_dict, device_types.LIGHT_BULB)[0]
        self.assertEqual(bulb.brightness(), 0.02)

    def test_bulb_hsb_color(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/lightify_rgbw_bulb.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        bulb = get_devices_from_response_dict(response_dict, device_types.LIGHT_BULB)[0]
        self.assertTrue(bulb.supports_hue_saturation())
        self.assertEqual(bulb.color_model(), "hsb")
        self.assertEqual(bulb.color_hue(), 0.0)
        self.assertEqual(bulb.color_saturation(), 1.0)

    def test_bulb_xy_color(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/hue_bulb.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        bulb = get_devices_from_response_dict(response_dict, device_types.LIGHT_BULB)[0]
        self.assertEqual(bulb.color_model(), "xy")
        self.assertTrue(bulb.supports_xy_color())
        self.assertEqual(bulb.color_xy(), [0.4571, 0.4097])

    def test_bulb_color_temperature(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/lightify_rgbw_bulb.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        bulb = get_devices_from_response_dict(response_dict, device_types.LIGHT_BULB)[0]
        self.assertTrue(bulb.supports_temperature())
        self.assertEqual(bulb.color_temperature_kelvin(), 2755)

    def test_light_groups_are_created_correctly(self):
        all_devices = os.listdir('{}/api_responses/groups/'.format(os.path.dirname(__file__)))
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/groups/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/groups/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        JSON_DATA["data"] = device_list
        all_groups = get_devices_from_response_dict(JSON_DATA, device_types.GROUP)
        self.assertEqual(3, len(all_groups))
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        self.assertEqual(1, len(groups))
        self.assertTrue(isinstance(groups[0], WinkLightGroup))

    def test_light_group_state_is_correct(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertFalse(light_group.state())

    def test_light_group_is_available(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertTrue(light_group.available())

    def test_light_group_brightness(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertEqual(light_group.brightness(), 1)

    def test_light_group_color_model(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertEqual(light_group.color_model(), "hsb")

    def test_light_group_supports_hsb_and_temperature(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertTrue(light_group.supports_temperature())
        self.assertTrue(light_group.supports_hue_saturation())

    def test_light_group_saturation(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertEqual(light_group.color_saturation(), 0.13)

    def test_light_group_hue(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertEqual(light_group.color_hue(), 0.11)

    def test_light_group_color_temperature_kelvin(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/light_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        light_group = groups[0]
        self.assertEqual(light_group.color_temperature_kelvin(), 2326)

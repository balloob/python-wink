import json
import os
import unittest

from unittest.mock import MagicMock

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types


class GeZwaveFanTests(unittest.TestCase):

    def setUp(self):
        super(GeZwaveFanTests, self).setUp()
        self.api_interface = MagicMock()
        device_list = []
        self.response_dict = {}
        _json_file = open('{}/api_responses/ge_zwave_fan.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        self.response_dict["data"] = device_list

    def test_fan_speeds(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        has_speeds = fan.fan_speeds()
        self.assertEqual(len(has_speeds), 3)
        speeds = ['low', 'medium', 'high']
        for speed in has_speeds:
            self.assertTrue(speed in speeds)

    def test_fan_directions(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        has_directions = fan.fan_directions()
        self.assertEqual(len(has_directions), 0)

    def test_fan_timer_range(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        has_timer_range = fan.fan_timer_range()
        self.assertEqual(len(has_timer_range), 0)

    def test_fan_speed_is_medium(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        self.assertEqual(fan.current_fan_speed(), "medium")

    def test_fan_state(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        self.assertFalse(fan.state())

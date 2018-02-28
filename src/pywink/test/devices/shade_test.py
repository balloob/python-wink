import json
import os
import unittest

from unittest.mock import MagicMock

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types
from pywink.devices.shade_group import WinkShadeGroup

JSON_DATA = {}


class ShadeTests(unittest.TestCase):

    def setUp(self):
        super(ShadeTests, self).setUp()
        self.api_interface = MagicMock()

    def test_shade_groups_are_created_correctly(self):
        all_devices = os.listdir(
            '{}/api_responses/groups/'.format(os.path.dirname(__file__)))
        device_list = []
        for json_file in all_devices:
            if os.path.isfile(
                    '{}/api_responses/groups/{}'.format(os.path.dirname(__file__),
                                                        json_file)):
                _json_file = open(
                    '{}/api_responses/groups/{}'.format(os.path.dirname(__file__),
                                                        json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        JSON_DATA["data"] = device_list
        all_groups = get_devices_from_response_dict(JSON_DATA, device_types.GROUP)
        self.assertEqual(3, len(all_groups))
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/shade_group.json'.format(
            os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        self.assertEqual(1, len(groups))
        self.assertTrue(isinstance(groups[0], WinkShadeGroup))

    def test_light_group_state_is_correct(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/shade_group.json'.format(
            os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        shade_group = groups[0]
        self.assertEqual(shade_group.state(), 0.0)

    def test_light_group_is_available(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/shade_group.json'.format(
            os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        shade_group = groups[0]
        self.assertTrue(shade_group.available())
import json
import os
import unittest

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types
from pywink.devices.binary_switch_group import WinkBinarySwitchGroup

JSON_DATA = {}


class BinarySwitchTests(unittest.TestCase):

    def test_state_should_be_false(self):
        with open('{}/api_responses/ge_zwave_switch.json'.format(os.path.dirname(__file__))) as binary_switch_file:
            response_dict = json.load(binary_switch_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.BINARY_SWITCH)

        switch = devices[0]
        self.assertFalse(switch.state())

    def test_switch_groups_are_created_correctly(self):
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
        _json_file = open('{}/api_responses/groups/switch_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        self.assertEqual(1, len(groups))
        self.assertTrue(isinstance(groups[0], WinkBinarySwitchGroup))

    def test_switch_group_state_is_correct(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/switch_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        switch_group = groups[0]
        self.assertFalse(switch_group.state())

    def test_switch_group_availble(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/groups/switch_group.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        groups = get_devices_from_response_dict(response_dict, device_types.GROUP)
        switch_group = groups[0]
        self.assertTrue(switch_group.available())

    def test_last_event(self):
        with open('{}/api_responses/leaksmart_valve.json'.format(os.path.dirname(__file__))) as binary_switch_file:
            response_dict = json.load(binary_switch_file)
        response_dict = {"data": [response_dict]}
        binary_switches = get_devices_from_response_dict(response_dict, device_types.BINARY_SWITCH)
        for switch in binary_switches:
            if switch.model_name() == "leakSMART Valve":
                self.assertEqual(switch.last_event(), "monthly_cycle_success")
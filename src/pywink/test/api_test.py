# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import socket
from threading import Thread
import unittest
import os

# Third-party imports...
import requests
from mock import patch

from pywink.api import *
from pywink.devices import types as device_types
from pywink.api import WinkApiInterface
from pywink.devices.sensor import WinkSensor
from pywink.devices.hub import WinkHub
from pywink.devices.piggy_bank import WinkPorkfolioBalanceSensor, WinkPorkfolioNose
from pywink.devices.key import WinkKey
from pywink.devices.remote import WinkRemote
from pywink.devices.powerstrip import WinkPowerStrip, WinkPowerStripOutlet
from pywink.devices.light_bulb import WinkLightBulb
from pywink.devices.binary_switch import WinkBinarySwitch
from pywink.devices.lock import WinkLock
from pywink.devices.eggtray import WinkEggtray
from pywink.devices.garage_door import WinkGarageDoor
from pywink.devices.shade import WinkShade
from pywink.devices.siren import WinkSiren
from pywink.devices.fan import WinkFan
from pywink.devices.thermostat import WinkThermostat
from pywink.devices.button import WinkButton
from pywink.devices.gang import WinkGang
from pywink.devices.smoke_detector import WinkSmokeDetector, WinkSmokeSeverity, WinkCoDetector, WinkCoSeverity
from pywink.devices.sprinkler import WinkSprinkler
from pywink.devices.camera import WinkCanaryCamera
from pywink.devices.air_conditioner import WinkAirConditioner
from pywink.devices.propane_tank import WinkPropaneTank
from pywink.devices.scene import WinkScene
from pywink.devices.robot import WinkRobot

USERS_ME_WINK_DEVICES = {}


class ApiTests(unittest.TestCase):


    def setUp(self):
        global USERS_ME_WINK_DEVICES
        super(ApiTests, self).setUp()
        all_devices = os.listdir('{}/devices/api_responses/'.format(os.path.dirname(__file__)))
        device_list = []
        for json_file in all_devices:
            _json_file = open('{}/devices/api_responses/{}'.format(os.path.dirname(__file__), json_file))
            device_list.append(json.load(_json_file))
            _json_file.close()
        USERS_ME_WINK_DEVICES["data"] = device_list
        self.port = get_free_port()
        start_mock_server(self.port)
        self.api_interface = MockApiInterface()

    def test_bad_status_codes(self):
        try:
            WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port) + "/401/"
            get_all_devices()
        except Exception as e:
            self.assertTrue(type(e), WinkAPIException)
        try:
            WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port) + "/404/"
            get_all_devices()
        except Exception as e:
            self.assertTrue(type(e), WinkAPIException)

    def test_set_bearer_token(self):
        self.assertIsNone(get_set_access_token())
        set_bearer_token("THIS_IS_A_TEST")
        self.assertEqual("THIS_IS_A_TEST", get_set_access_token())
        self.assertTrue(is_token_set())

    def test_get_subscription_key(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        get_all_devices()
        self.assertIsNotNone(get_subscription_key())

    def test_get_all_devices_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_all_devices()
        self.assertEqual(len(devices), 63)
        lights = get_light_bulbs()
        for light in lights:
            self.assertTrue(isinstance(light, WinkLightBulb))
        sensors = get_sensors()
        sensors.extend(get_door_bells())
        for sensor in sensors:
            self.assertTrue(isinstance(sensor, WinkSensor))
        smoke_detectors = get_smoke_and_co_detectors()
        for device in smoke_detectors:
            self.assertTrue(isinstance(device, WinkSmokeDetector) or isinstance(device, WinkSmokeSeverity) or
                            isinstance(device, WinkCoDetector) or isinstance(device, WinkCoSeverity))
        keys = get_keys()
        for key in keys:
            self.assertTrue(isinstance(key, WinkKey))
        switches = get_switches()
        for switch in switches:
            self.assertTrue(isinstance(switch, WinkBinarySwitch))
        locks = get_locks()
        for lock in locks:
            self.assertTrue(isinstance(lock, WinkLock))
        eggtrays = get_eggtrays()
        for eggtray in eggtrays:
            self.assertTrue(isinstance(eggtray, WinkEggtray))
        garage_doors = get_garage_doors()
        for garage_door in garage_doors:
            self.assertTrue(isinstance(garage_door, WinkGarageDoor))
        powerstrip = get_powerstrips()
        self.assertEqual(len(powerstrip), 3)
        for device in powerstrip:
            self.assertTrue(isinstance(device, WinkPowerStrip) or isinstance(device, WinkPowerStripOutlet))
        shades = get_shades()
        for shade in shades:
            self.assertTrue(isinstance(shade, WinkShade))
        sirens = get_sirens()
        for siren in sirens:
            self.assertTrue(isinstance(siren, WinkSiren))
        keys = get_keys()
        for key in keys:
            self.assertTrue(isinstance(key, WinkKey))
        porkfolio = get_piggy_banks()
        self.assertEqual(len(porkfolio), 2)
        for device in porkfolio:
            self.assertTrue(isinstance(device, WinkPorkfolioBalanceSensor) or isinstance(device, WinkPorkfolioNose))
        thermostats = get_thermostats()
        for thermostat in thermostats:
            self.assertTrue(isinstance(thermostat, WinkThermostat))
        hubs = get_hubs()
        for hub in hubs:
            self.assertTrue(isinstance(hub, WinkHub))
        fans = get_fans()
        for fan in fans:
            self.assertTrue(isinstance(fan, WinkFan))
        buttons = get_buttons()
        for button in buttons:
            self.assertTrue(isinstance(button, WinkButton))
        acs = get_air_conditioners()
        for ac in acs:
            self.assertTrue(isinstance(ac, WinkAirConditioner))
        propane_tanks = get_propane_tanks()
        for tank in propane_tanks:
            self.assertTrue(isinstance(tank, WinkPropaneTank))

    def test_get_sensor_and_binary_switch_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        sensor_types = [WinkSensor, WinkHub, WinkPorkfolioBalanceSensor, WinkKey, WinkRemote,
                        WinkGang, WinkSmokeDetector, WinkSmokeSeverity,
                        WinkCoDetector, WinkCoSeverity, WinkButton, WinkRobot]
        # No way to validate scene is activated, so skipping.
        skip_types = [WinkPowerStripOutlet, WinkCanaryCamera, WinkScene]
        devices = get_all_devices()
        old_states = {}
        for device in devices:
            if type(device) in skip_types:
                continue
            device.api_interface = self.api_interface
            if type(device) in sensor_types:
                old_states[device.object_id() + device.name()] = device.state()
            elif isinstance(device, WinkPorkfolioNose):
                device.set_state("FFFF00")
            elif device.state() is False or device.state() is True:
                old_states[device.object_id()] = device.state()
                device.set_state(not device.state())
            device.update_state()
        for device in devices:
            if type(device) in skip_types:
                continue
            if isinstance(device, WinkPorkfolioNose):
                self.assertEqual(device.state(), "FFFF00")
            elif type(device) in sensor_types:
                self.assertEqual(device.state(), old_states.get(device.object_id() + device.name()))
            elif device.object_id() in old_states:
                self.assertEqual(not device.state(), old_states.get(device.object_id()))

    def test_get_light_bulbs_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_light_bulbs()
        old_states = {}
        # Set states
        for device in devices:
            device.api_interface = self.api_interface
            # Test HSB and powered
            if device.supports_hue_saturation():
                old_states[device.object_id()] = device.state()
                device.set_state(not device.state(), 0.5, color_hue_saturation=[0.5, 0.5])
            # Test temperature and powered
            elif not device.supports_hue_saturation() and device.supports_temperature():
                old_states[device.object_id()] = device.state()
                device.set_state(not device.state(), 0.5, color_kelvin=2500)
            # Test Brightness and powered
            else:
                old_states[device.object_id()] = device.state()
                device.set_state(not device.state(), 0.5)
        # Check states
        for device in devices:
            # Test HSB and powered
            if device.supports_hue_saturation():
                self.assertEqual([old_states.get(device.object_id()), 0.5, [0.5, 0.5]],
                                 [not device.state(), device.brightness(), [device.color_saturation(), device.color_hue()]])
            # Test temperature and powered
            elif not device.supports_hue_saturation() and device.supports_temperature():
                self.assertEqual([not old_states.get(device.object_id()), 0.5, 2500], [device.state(), device.brightness(), device.color_temperature_kelvin()])
            # Test Brightness and powered
            else:
                self.assertEqual([old_states.get(device.object_id()), 0.5], [not device.state(), device.brightness()])

    def test_get_shade_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_shades()
        for device in devices:
            device.api_interface = self.api_interface
            device.set_state(1.0)
            device.update_state()
        for device in devices:
            self.assertEqual(1.0, device.state())

    def test_get_garage_door_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_garage_doors()
        for device in devices:
            device.api_interface = self.api_interface
            device.set_state(1)
            device.update_state()
        for device in devices:
            self.assertEqual(1, device.state())

    def test_get_powerstrip_outlets_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        skip_types = [WinkPowerStrip]
        devices = get_powerstrips()
        old_states = {}
        for device in devices:
            if type(device) in skip_types:
                continue
            device.api_interface = self.api_interface
            if device.state() is False or device.state() is True:
                old_states[device.object_id()] = device.state()
                device.set_state(not device.state())
                device.update_state()
        for device in devices:
            if device.object_id() in old_states:
                self.assertEqual(not device.state(), old_states.get(device.object_id()))

    def test_get_siren_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_sirens()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            old_states[device.object_id()] = device.state()
            device.set_state(not device.state())
            device.set_mode("strobe")
            device.set_auto_shutoff(120)
            device.update_state()
        self.assertEqual(not device.state(), old_states.get(device.object_id()))
        self.assertEqual(device.mode(), "strobe")
        self.assertEqual(device.auto_shutoff(), 120)

    def test_get_lock_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_locks()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            old_states[device.object_id()] = device.state()
            device.set_state(not device.state())
            device.set_alarm_sensitivity(0.22)
            device.set_alarm_mode("alert")
            device.set_alarm_state(False)
            device.set_vacation_mode(True)
            device.set_beeper_mode(True)
            device.update_state()
        self.assertEqual(not device.state(), old_states.get(device.object_id()))
        self.assertEqual(device.alarm_mode(), "alert")
        self.assertFalse(device.alarm_enabled())
        self.assertTrue(device.vacation_mode_enabled())
        self.assertTrue(device.beeper_enabled())

    def test_get_air_conditioner_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_air_conditioners()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            old_states[device.object_id()] = device.state()
            device.set_operation_mode("cool_only")
            device.set_temperature(70)
            device.set_schedule_enabled(False)
            device.set_ac_fan_speed(0.5)
        for device in devices:
            self.assertEqual(device.state(), "cool_only")
            self.assertEqual(70, device.current_max_set_point())
            self.assertFalse(device.schedule_enabled())
            self.assertEqual(0.5, device.current_fan_speed())

    def test_get_camera_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_cameras()

    def test_get_thermostat_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_thermostats()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            old_states[device.object_id()] = device.state()
            if device.name() == "Home Hallway Thermostat":
                device.set_operation_mode("off")
            else:
                device.set_operation_mode("auto")
            device.set_away(True)
            if device.has_fan():
                device.set_fan_mode("auto")
            device.set_temperature(10, 50)
        for device in devices:
            if device.name() == "Home Hallway Thermostat":
                self.assertFalse(device.is_on())
            else:
                self.assertEqual(device.current_hvac_mode(), "auto")
            self.assertTrue(device.away())
            if device.has_fan():
                self.assertEqual(device.current_fan_mode(), "auto")
            self.assertEqual(10, device.current_min_set_point())
            self.assertEqual(50, device.current_max_set_point())

    def test_get_camera_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_cameras()
        old_states = {}
        for device in devices:
            if isinstance(device, WinkCanaryCamera):
                device.api_interface = self.api_interface
                device.set_mode("away")
                device.set_privacy(True)
                device.update_state()
        if isinstance(device, WinkCanaryCamera):
            self.assertEqual(device.state(), "away")
            self.assertTrue(device.private())

    def test_get_fan_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_fans()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            device.set_fan_speed("auto")
            device.set_fan_direction("reverse")
            device.set_fan_timer(300)
            device.update_state()
        self.assertEqual(device.current_fan_speed(), "auto")
        self.assertEqual(device.current_fan_direction(), "reverse")
        self.assertEqual(device.current_timer(), 300)


    def test_get_propane_tank_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_propane_tanks()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            device.set_tare(5.0)
            device.update_state()
        self.assertEqual(device.tare(), 5.0)



class MockServerRequestHandler(BaseHTTPRequestHandler):
    USERS_ME_WINK_DEVICES_PATTERN = re.compile(r'/users/me/wink_devices')
    BAD_STATUS_PATTERN = re.compile(r'/401/')
    NOT_FOUND_PATTERN = re.compile(r'/404/')
    REFRESH_TOKEN_PATTERN = re.compile(r'/oauth2/token')
    DEVICE_SPECIFIC_PATTERN = re.compile(r'/*/[0-9]*')

    def do_GET(self):
        if re.search(self.BAD_STATUS_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.unauthorized)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            return
        elif re.search(self.NOT_FOUND_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.not_found)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            return
        elif re.search(self.USERS_ME_WINK_DEVICES_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            # Add response content.
            response_content = json.dumps(USERS_ME_WINK_DEVICES)
            self.wfile.write(response_content.encode('utf-8'))
            return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()


class MockApiInterface():

    def set_device_state(self, device, state, id_override=None, type_override=None):
        """
        :type device: WinkDevice
        """
        object_id = id_override or device.object_id()
        device_object_type = device.object_type()
        object_type = type_override or device_object_type
        return_dict = {}
        for dict_device in USERS_ME_WINK_DEVICES.get('data'):
            _object_id = dict_device.get("object_id")
            if _object_id == object_id:
                if device_object_type == "powerstrip":
                    set_state = state["outlets"][0]["desired_state"]["powered"]
                    dict_device["outlets"][0]["last_reading"]["powered"] = set_state
                    dict_device["outlets"][1]["last_reading"]["powered"] = set_state
                    return_dict["data"] = dict_device
                elif device_object_type == "outlet":
                    index = device.index()
                    set_state = state["outlets"][index]["desired_state"]["powered"]
                    dict_device["outlets"][index]["last_reading"]["powered"] = set_state
                    return_dict["data"] = dict_device
                else:
                    if "nose_color" in state:
                        dict_device["nose_color"] = state.get("nose_color")
                    elif "tare" in state:
                        dict_device["tare"] = state.get("tare")
                    else:
                        for key, value in state.get('desired_state').items():
                            dict_device["last_reading"][key] = value
                    return_dict["data"] = dict_device
        return return_dict

    def get_device_state(self, device, id_override=None, type_override=None):
        """
        :type device: WinkDevice
        """
        object_id = id_override or device.object_id()
        return_dict = {}
        for device in USERS_ME_WINK_DEVICES.get('data'):
            _object_id = device.get("object_id")
            if _object_id == object_id:
                return_dict["data"] = device
        return return_dict

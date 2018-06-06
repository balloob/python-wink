from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import socket
from threading import Thread
import unittest
import os

# Third-party imports...
from unittest.mock import MagicMock, Mock

from pywink.api import *
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
from pywink.devices.fan import WinkFan, WinkGeZwaveFan
from pywink.devices.thermostat import WinkThermostat
from pywink.devices.button import WinkButton
from pywink.devices.gang import WinkGang
from pywink.devices.smoke_detector import WinkSmokeDetector, WinkSmokeSeverity, WinkCoDetector, WinkCoSeverity
from pywink.devices.camera import WinkCanaryCamera
from pywink.devices.air_conditioner import WinkAirConditioner
from pywink.devices.propane_tank import WinkPropaneTank
from pywink.devices.scene import WinkScene
from pywink.devices.robot import WinkRobot
from pywink.devices.water_heater import WinkWaterHeater

USERS_ME_WINK_DEVICES = {}
GROUPS = {}


class ApiTests(unittest.TestCase):

    def setUp(self):
        global USERS_ME_WINK_DEVICES, GROUPS
        super(ApiTests, self).setUp()
        all_devices = os.listdir('{}/devices/api_responses/'.format(os.path.dirname(__file__)))
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/devices/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/devices/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        USERS_ME_WINK_DEVICES["data"] = device_list
        all_devices = os.listdir('{}/devices/api_responses/groups'.format(os.path.dirname(__file__)))
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/devices/api_responses/groups/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/devices/api_responses/groups/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        GROUPS["data"] = device_list
        self.port = get_free_port()
        start_mock_server(self.port)
        self.api_interface = MockApiInterface()

    def test_local_control_enabled_by_default(self):
        self.assertTrue(ALLOW_LOCAL_CONTROL)

    def test_that_disable_local_control_works(self):
        from pywink.api import ALLOW_LOCAL_CONTROL
        disable_local_control()
        self.assertFalse(ALLOW_LOCAL_CONTROL)

    def test_set_user_agent(self):
        from pywink.api import API_HEADERS
        set_user_agent("THIS IS A TEST")
        self.assertEqual("THIS IS A TEST", API_HEADERS["User-Agent"])

    def test_set_bearer_token(self):
        from pywink.api import API_HEADERS, LOCAL_API_HEADERS
        set_bearer_token("THIS IS A TEST")
        self.assertEqual("Bearer THIS IS A TEST", API_HEADERS["Authorization"])


    def test_get_authorization_url(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        url = get_authorization_url("TEST", "127.0.0.1")
        comparison_url = "%s/oauth2/authorize?client_id=TEST&redirect_uri=127.0.0.1" % ("http://localhost:" + str(self.port))
        self.assertEqual(comparison_url, url)

    def test_bad_status_codes(self):
        try:
            WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port) + "/401/"
            wink_api_fetch()
        except Exception as e:
            self.assertTrue(type(e), WinkAPIException)
        try:
            WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port) + "/404/"
            wink_api_fetch()
        except Exception as e:
            self.assertTrue(type(e), WinkAPIException)

    def test_get_subscription_key(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        get_all_devices()
        self.assertIsNotNone(get_subscription_key())

    def test_get_all_devices_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_all_devices()
        self.assertEqual(len(devices), 77)
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
            self.assertTrue(isinstance(fan, WinkFan) or isinstance(fan, WinkGeZwaveFan))
        buttons = get_buttons()
        for button in buttons:
            self.assertTrue(isinstance(button, WinkButton))
        acs = get_air_conditioners()
        for ac in acs:
            self.assertTrue(isinstance(ac, WinkAirConditioner))
        propane_tanks = get_propane_tanks()
        for tank in propane_tanks:
            self.assertTrue(isinstance(tank, WinkPropaneTank))
        water_heaters = get_water_heaters()
        for water_heater in water_heaters:
            self.assertTrue(isinstance(water_heater, WinkWaterHeater))

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
            # Test xy color and powered
            if device.supports_xy_color():
                old_states[device.object_id()] = device.state()
                device.set_state(not device.state(), color_xy=[0.5, 0.5])
            # Test HSB and powered
            elif device.supports_hue_saturation():
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
            # Test xy color and power
            if device.supports_xy_color():
                self.assertEqual([not old_states.get(device.object_id()), [0.5, 0.5]], [device.state(), device.color_xy()])
            # Test HSB and powered
            elif device.supports_hue_saturation():
                self.assertEqual([old_states.get(device.object_id()), 0.5, [0.5, 0.5]],
                                 [not device.state(), device.brightness(), [device.color_saturation(), device.color_hue()]])
            # Test temperature and powered
            elif not device.supports_hue_saturation() and device.supports_temperature():
                self.assertEqual([not old_states.get(device.object_id()), 0.5, 2500], [device.state(), device.brightness(), device.color_temperature_kelvin()])
            # Test Brightness and powered
            else:
                self.assertEqual([old_states.get(device.object_id()), 0.5], [not device.state(), device.brightness()])

    def test_get_switch_group_updated_state_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_binary_switch_groups()
        for device in devices:
            device.api_interface = self.api_interface
            # The Mock API only changes the "powered" true_count and false_count
            device.set_state(False)
            device.update_state()
        for device in devices:
            self.assertFalse(device.state())

    def test_get_light_group_updated_state_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_light_groups()
        for device in devices:
            device.api_interface = self.api_interface
            # The Mock API only changes the "powered" true_count and false_count
            device.set_state(True)
            device.update_state()
        for device in devices:
            self.assertTrue(device.state())

    def test_all_devices_local_control_id_is_not_decimal(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_all_devices()
        for device in devices:
            if device.local_id() is not None:
                _temp = float(device.local_id())
                _temp2 = int(device.local_id())
                self.assertEqual(_temp, _temp2)

    def test_local_control_get_state_is_being_called(self):
        mock_api_object = Mock()
        mock_api_object.local_get_state = MagicMock()
        mock_api_object.get_device_state = MagicMock()
        devices = get_light_bulbs()
        devices[0].api_interface = mock_api_object
        devices[0].update_state()
        mock_api_object.local_get_state.assert_called_with(devices[0])

    def test_local_control_set_state_is_being_called(self):

        def Any(cls):
            class Any(cls):
                def __eq__(self, other):
                    return True
            return Any()

        mock_api_object = Mock()
        mock_api_object.local_set_state = MagicMock()
        mock_api_object.set_device_state = MagicMock()
        devices = get_light_bulbs()
        devices[0].api_interface = mock_api_object
        devices[0].set_state(True)
        mock_api_object.local_set_state.assert_called_with(devices[0], Any(str))

    def test_local_control_get_state_is_not_being_called(self):
        mock_api_object = Mock()
        mock_api_object.local_get_state = MagicMock()
        mock_api_object.get_device_state = MagicMock()
        devices = get_piggy_banks()
        devices[0].api_interface = mock_api_object
        devices[0].update_state()
        mock_api_object.get_device_state.assert_called_with(devices[0])

    def test_local_control_set_state_is_not_being_called(self):

        def Any(cls):
            class Any(cls):
                def __eq__(self, other):
                    return True
            return Any()

        mock_api_object = Mock()
        mock_api_object.local_set_state = MagicMock()
        mock_api_object.set_device_state = MagicMock()
        devices = get_thermostats()
        devices[0].api_interface = mock_api_object
        devices[0].set_operation_mode("auto")
        mock_api_object.set_device_state.assert_called_with(devices[0], Any(str))

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
            device.set_siren_volume("medium")
            device.set_chime_volume("medium")
            device.set_siren_sound("test_sound")
            device.set_chime("test_sound", 10)
            device.set_chime_strobe_enabled(True)
            device.set_siren_strobe_enabled(False)
            device.update_state()
        self.assertEqual(not device.state(), old_states.get(device.object_id()))
        self.assertEqual(device.mode(), "strobe")
        self.assertEqual(device.auto_shutoff(), 120)
        self.assertEqual(device.siren_volume(), "medium")
        self.assertEqual(device.chime_volume(), "medium")
        self.assertEqual(device.chime_mode(), "test_sound")
        self.assertEqual(device.siren_sound(), "test_sound")
        self.assertTrue(device.chime_strobe_enabled())
        self.assertFalse(device.strobe_enabled())
        self.assertEqual(device.chime_cycles(), 10)

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

    def test_get_water_heater_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_water_heaters()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            old_states[device.object_id()] = device.state()
            device.set_operation_mode("heat_pump")
            device.set_temperature(70)
            device.set_vacation_mode(True)
        for device in devices:
            self.assertEqual(device.state(), "heat_pump")
            self.assertEqual(70, device.current_set_point())
            self.assertTrue(device.vacation_mode_enabled())

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
        for device in devices:
            if isinstance(device, WinkCanaryCamera):
                self.assertEqual(device.state(), "away")
                self.assertTrue(device.private())

    def test_get_fan_updated_states_from_api(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_fans()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            if isinstance(device, WinkGeZwaveFan):
                device.set_state(True, "high")
            else:
                device.set_state(True, "auto")
                device.set_fan_direction("reverse")
                device.set_fan_timer(300)
            device.update_state()
        for device in devices:
            if isinstance(device, WinkGeZwaveFan):
                self.assertEqual(device.current_fan_speed(), "high")
            else:
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

    def test_set_all_device_names(self):
        WinkApiInterface.BASE_URL = "http://localhost:" + str(self.port)
        devices = get_all_devices()
        old_states = {}
        for device in devices:
            device.api_interface = self.api_interface
            device.set_name("TEST_NAME")
            device.update_state()
        for device in devices:
            self.assertTrue(device.name().startswith("TEST_NAME"))


class MockServerRequestHandler(BaseHTTPRequestHandler):
    USERS_ME_WINK_DEVICES_PATTERN = re.compile(r'/users/me/wink_devices')
    BAD_STATUS_PATTERN = re.compile(r'/401/')
    NOT_FOUND_PATTERN = re.compile(r'/404/')
    REFRESH_TOKEN_PATTERN = re.compile(r'/oauth2/token')
    DEVICE_SPECIFIC_PATTERN = re.compile(r'/*/[0-9]*')
    GROUPS_PATTERN = re.compile(r'/groups')

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
        elif re.search(self.GROUPS_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            # Add response content.
            response_content = json.dumps(GROUPS)
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
        if "name" in str(state):
            for dict_device in USERS_ME_WINK_DEVICES.get('data'):
                _object_id = dict_device.get("object_id")
                if _object_id == object_id:
                    if device_object_type == "outlet":
                        index = device.index()
                        set_state = state["outlets"][index]["name"]
                        dict_device["outlets"][index]["name"] = set_state
                        return_dict["data"] = dict_device
                    else:
                        dict_device["name"] = state.get("name")
            for dict_device in GROUPS.get('data'):
                _object_id = dict_device.get("object_id")
                if _object_id == object_id:
                    dict_device["name"] = state.get("name")
        elif object_type != "group":
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
        else:
            for dict_device in GROUPS.get('data'):
                _object_id = dict_device.get("object_id")
                if _object_id == object_id:
                    set_state = state["desired_state"]["powered"]
                    if set_state:
                        dict_device["reading_aggregation"]["powered"]["true_count"] = 1
                        dict_device["reading_aggregation"]["powered"]["false_count"] = 0
                    else:
                        dict_device["reading_aggregation"]["powered"]["true_count"] = 0
                        dict_device["reading_aggregation"]["powered"]["false_count"] = 1
                    return_dict["data"] = dict_device

        return return_dict

    def local_set_state(self, device, state, id_override=None, type_override=None):
        return self.set_device_state(device, state, id_override, type_override)

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

    def local_get_state(self, device, id_override=None, type_override=None):
        return self.get_device_state(device, id_override, type_override)


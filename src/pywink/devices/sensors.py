# -*- coding: utf-8 -*-
from pywink.devices.base import WinkDevice


class _WinkCapabilitySensor(WinkDevice):

    def __init__(self, device_state_as_json, api_interface, capability, unit, objectprefix="sensor_pods"):
        super(_WinkCapabilitySensor, self).__init__(device_state_as_json, api_interface,
                                                    objectprefix=objectprefix)
        self._capability = capability
        self.unit = unit

    def __repr__(self):
        return "<Wink sensor {name} {dev_id} {reading}{unit}>".format(name=self.name(),
                                                                      dev_id=self.device_id(),
                                                                      reading=self._last_reading.get(self._capability),
                                                                      unit='' if self.unit is None else self.unit)

    def state(self):
        return self._last_reading.get('connection', False)

    def last_reading(self):
        return self._last_reading.get(self._capability)

    def capability(self):
        return self._capability

    def name(self):
        name = self.json_state.get('name', "Unknown Name")
        if self._capability != "opened":
            name += " " + self._capability
        return name

    @property
    def battery_level(self):
        if not self._last_reading.get('external_power', None):
            return self._last_reading.get('battery', None)
        else:
            return None

    def device_id(self):
        root_name = self.json_state.get('sensor_pod_id', None)
        return '{}+{}'.format(root_name, self._capability)

    def update_state(self, require_desired_state_fulfilled=False):
        """ Update state with latest info from Wink API. """
        root_name = self.json_state.get('sensor_pod_id', self.name())
        response = self.api_interface.get_device_state(self, root_name)
        self._update_state_from_response(response,
                                         require_desired_state_fulfilled=require_desired_state_fulfilled)


class WinkSensorPod(_WinkCapabilitySensor):
    """ represents a wink.py sensor
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:
    """
    CAPABILITY = 'opened'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkSensorPod, self).__init__(device_state_as_json, api_interface,
                                            self.CAPABILITY, self.UNIT)

    def __repr__(self):
        return "<Wink sensor %s %s %s>" % (self.name(),
                                           self.device_id(), self.state())

    def state(self):
        if 'opened' in self._last_reading:
            return self._last_reading['opened']
        return False

    def device_id(self):
        return self.json_state.get('sensor_pod_id', self.name())


class WinkHumiditySensor(_WinkCapabilitySensor):

    CAPABILITY = 'humidity'
    UNIT = '%'

    def __init__(self, device_state_as_json, api_interface):
        super(WinkHumiditySensor, self).__init__(device_state_as_json, api_interface,
                                                 self.CAPABILITY,
                                                 self.UNIT)

    def humidity_percentage(self):
        """
        :return: The relative humidity detected by the sensor (0% to 100%)
        :rtype: int
        """
        # Relay returns humidity as a decimal
        if self.last_reading() < 1.0:
            return int(round(self.last_reading() * 100))
        else:
            return self.last_reading()

    def pubnub_update(self, json_response):
        # Pubnub returns the humidity as a decimal
        # converting to a percentage
        hum = json_response["last_reading"]["humidity"] * 100
        json_response["last_reading"]["humidity"] = hum
        self.json_state = json_response


class WinkBrightnessSensor(_WinkCapabilitySensor):

    CAPABILITY = 'brightness'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkBrightnessSensor, self).__init__(device_state_as_json, api_interface,
                                                   self.CAPABILITY,
                                                   self.UNIT)

    def brightness_boolean(self):
        """
        :return: True if light is detected.  False if light is below detection threshold (varies by device)
        :rtype: bool
        """
        return self.last_reading()


class WinkSoundPresenceSensor(_WinkCapabilitySensor):

    CAPABILITY = 'loudness'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkSoundPresenceSensor, self).__init__(device_state_as_json, api_interface,
                                                      self.CAPABILITY,
                                                      self.UNIT)

    def loudness_boolean(self):
        """
        :return: True if sound is detected.  False if sound is below detection threshold (varies by device)
        :rtype: bool
        """
        return self.last_reading()


class WinkTemperatureSensor(_WinkCapabilitySensor):

    CAPABILITY = 'temperature'
    UNIT = u'\N{DEGREE SIGN}'

    def __init__(self, device_state_as_json, api_interface):
        super(WinkTemperatureSensor, self).__init__(device_state_as_json, api_interface,
                                                    self.CAPABILITY,
                                                    self.UNIT)

    def temperature_float(self):
        """
        :return: A float indicating the temperature.  Units are determined by the sensor.
        :rtype: float
        """
        return self.last_reading()


class WinkVibrationPresenceSensor(_WinkCapabilitySensor):

    CAPABILITY = 'vibration'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkVibrationPresenceSensor, self).__init__(device_state_as_json, api_interface,
                                                          self.CAPABILITY,
                                                          self.UNIT)

    def vibration_boolean(self):
        """
        :return: Returns True if vibration is detected.
        :rtype: bool
        """
        return self.last_reading()


class WinkLiquidPresenceSensor(_WinkCapabilitySensor):

    CAPABILITY = 'liquid_detected'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkLiquidPresenceSensor, self).__init__(device_state_as_json, api_interface,
                                                       self.CAPABILITY,
                                                       self.UNIT)

    def liquid_boolean(self):
        """
        :return: Returns True if liquid is detected.
        :rtype: bool
        """
        return self.last_reading()


class WinkMotionSensor(_WinkCapabilitySensor):

    CAPABILITY = 'motion'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkMotionSensor, self).__init__(device_state_as_json, api_interface,
                                               self.CAPABILITY,
                                               self.UNIT)

    def motion_boolean(self):
        """
        :return: Returns True if motion is detected.
        :rtype: bool
        """
        return self.last_reading()


class WinkPresenceSensor(_WinkCapabilitySensor):

    CAPABILITY = 'presence'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkPresenceSensor, self).__init__(device_state_as_json, api_interface,
                                                 self.CAPABILITY,
                                                 self.UNIT)

    def presence_boolean(self):
        """
        :return: Returns True if presence is detected.
        :rtype: bool
        """
        return self.last_reading()


class WinkProximitySensor(_WinkCapabilitySensor):

    CAPABILITY = 'proximity'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkProximitySensor, self).__init__(device_state_as_json, api_interface,
                                                  self.CAPABILITY,
                                                  self.UNIT)

    def proximity_float(self):
        """
        :return: A float indicating the proximity.
        :rtype: float
        """
        return self.last_reading()


class WinkCurrencySensor(_WinkCapabilitySensor):

    CAPABILITY = 'balance'
    UNIT = 'USD'

    def __init__(self, device_state_as_json, api_interface):
        super(WinkCurrencySensor, self).__init__(device_state_as_json, api_interface,
                                                 self.CAPABILITY,
                                                 self.UNIT, 'piggy_bank')

    @property
    def available(self):
        """
        connection variable isn't stable.
        Porkfolio can be offline, but updates will continue to occur.
        always returning True to avoid this issue.
        """
        return True

    def device_id(self):
        root_name = self.json_state.get('piggy_bank_id', self.name())
        return '{}+{}'.format(root_name, self._capability)

    def balance(self):
        """
        :return: Returns the balance in cents.
        :rtype: int
        """
        return self.last_reading()

    def update_state(self, require_desired_state_fulfilled=False):
        """ Update state with latest info from Wink API. """
        root_name = self.json_state.get('piggy_bank_id', self.name())
        response = self.api_interface.get_device_state(self, root_name)
        self._update_state_from_response(response,
                                         require_desired_state_fulfilled=require_desired_state_fulfilled)


class WinkSmokeDetector(_WinkCapabilitySensor):

    CAPABILITY = 'smoke_detected'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkSmokeDetector, self).__init__(device_state_as_json, api_interface,
                                                self.CAPABILITY,
                                                self.UNIT, 'smoke_detectors')

    def smoke_detected_boolean(self):
        """
        :return: Returns True if smoke is detected.
        :rtype: bool
        """
        return self.last_reading()

    def device_id(self):
        root_name = self.json_state.get('smoke_detector_id', None)
        return '{}+{}'.format(root_name, self._capability)

    def update_state(self, require_desired_state_fulfilled=False):
        """ Update state with latest info from Wink API. """
        root_name = self.json_state.get('smoke_detector_id', self.name())
        response = self.api_interface.get_device_state(self, root_name)
        self._update_state_from_response(response,
                                         require_desired_state_fulfilled=require_desired_state_fulfilled)


class WinkCoDetector(_WinkCapabilitySensor):

    CAPABILITY = 'co_detected'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkCoDetector, self).__init__(device_state_as_json, api_interface,
                                             self.CAPABILITY,
                                             self.UNIT, 'smoke_detectors')

    def co_detected_boolean(self):
        """
        :return: Returns True if CO is detected.
        :rtype: bool
        """
        return self.last_reading()

    def device_id(self):
        root_name = self.json_state.get('smoke_detector_id', None)
        return '{}+{}'.format(root_name, self._capability)

    def update_state(self, require_desired_state_fulfilled=False):
        """ Update state with latest info from Wink API. """
        root_name = self.json_state.get('smoke_detector_id', self.name())
        response = self.api_interface.get_device_state(self, root_name)
        self._update_state_from_response(response,
                                         require_desired_state_fulfilled=require_desired_state_fulfilled)

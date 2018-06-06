from pywink.devices.base import WinkDevice


# pylint: disable=too-many-public-methods
class WinkFan(WinkDevice):
    """
    Represents a Wink fan.
    """
    json_state = {}

    def fan_speeds(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        fan_speeds = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'mode':
                fan_speeds = field.get('choices')
        return fan_speeds

    def fan_directions(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        fan_directions = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'direction':
                fan_directions = field.get('choices')
        return fan_directions

    def fan_timer_range(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        fan_timer_range = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'timer':
                fan_timer_range = field.get('range')
        return fan_timer_range

    def current_fan_speed(self):
        return self._last_reading.get('mode', "lowest")

    def current_fan_direction(self):
        return self._last_reading.get('direction', None)

    def current_timer(self):
        return self._last_reading.get('timer', None)

    def state(self):
        return self._last_reading.get('powered', False)

    def set_state(self, state, speed=None):
        """
        :param state: bool
        :param speed: a string one of ["lowest", "low",
            "medium", "high", "auto"] defaults to last speed
        :return: nothing
        """
        speed = speed or self.current_fan_speed()
        if state:
            desired_state = {"powered": state, "mode": speed}
        else:
            desired_state = {"powered": state}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_fan_direction(self, direction):
        """
        :param direction: a string one of ["forward", "reverse"]
        :return: nothing
        """
        desired_state = {"direction": direction}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_fan_timer(self, timer):
        """
        :param timer: an int between fan_timer_range
        :return: nothing
        """
        desired_state = {"timer": timer}

        resp = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(resp)


# pylint: disable=too-many-public-methods
class WinkGeZwaveFan(WinkFan):
    """
    Represents a GE-Z-Wave In wall fan switch. Wink recognizes this as a light
    bulb dimmer switch but in reality it is a fan with 3 speeds.
    """
    _to_brightness = {
        "lowest": 0.33,
        "low": 0.33,
        "medium": 0.66,
        "high": 1.0,
        "auto": 0.66
    }

    _to_speed = {
        0.33: "low",
        0.66: "medium",
        1.0: "high"
    }

    def fan_speeds(self):
        return ["low", "medium", "high"]

    def fan_directions(self):
        return []

    def fan_timer_range(self):
        return []

    def current_fan_speed(self):
        return self._to_speed[self._last_reading.get('brightness', 0.33)]

    def current_fan_direction(self):
        return None

    def current_timer(self):
        return None

    def set_state(self, state, speed=None):
        """
        :param state: bool
        :param speed: a string one of ["lowest", "low",
            "medium", "high", "auto"] defaults to last speed
        :return: nothing
        """
        desired_state = {"powered": state}
        if state:
            brightness = self._to_brightness.get(speed or self.current_fan_speed(), 0.33)
            desired_state.update({'brightness': brightness})

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_fan_direction(self, direction):
        pass

    def set_fan_timer(self, timer):
        pass

from pywink.devices.base import WinkDevice


class WinkShadeGroup(WinkDevice):
    """
    Represents a Wink shade group.
    """

    def state(self):
        """
        Groups states is calculated by Wink in the positions "average" field.
        """
        return self.reading_aggregation().get("position").get("average")

    def reading_aggregation(self):
        return self.json_state.get("reading_aggregation")

    def available(self):
        count = self.reading_aggregation().get("connection").get("true_count")
        if count > 0:
            return True
        return False

    def set_state(self, state):
        """
        :param state:   a number of 1 ('open') or 0 ('close')
        :return: nothing
        """
        values = {"desired_state": {"position": state}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

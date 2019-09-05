import json
import requests as rq


class SnipsHomeManager:
    """
    Whereas the "action-home-manager" describes the logic and handles the interactions with snips,
    the SnipsHomeManager manages functions that carry out the intents specified by the user.
    The "action-home-manager" will call the appropriate functions from SnipsHomeManager who makes the
    appropriate API request. The SnipsHomeManager in this case is made mostly of calls to the Hass API
    to manage lights and switches.

    The functions in this manager depend on a corresponding naming convention for the Hass entities.
    E.g. each light entity must follow "light.roomname_light"
    """
    def __init__(self, autho, header):
        print("Created the snips home manager")
        self.autho = autho  # Hass API key
        self.header = header  # Header required for REST API
        self.api_address = 'http://192.168.0.136:8123/api/'

    def light_on(self, room):
        """
        Ask Hass to turn on a specific light.
        :param room: String, name of the room
        :return: None
        """
        url = self.api_address + 'services/light/turn_on'
        body = {
            "entity_id": "light.{}_light".format(room)
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_on_all(self):
        """
        Ask Hass to turn on every light entity
        :return: None
        """
        url = self.api_address + 'services/light/turn_on'
        body = {
            "entity_id": "all"
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_off(self, room):
        """
        Asks Hass to turn off a specific light
        :param room: String, room to turn lights off
        :return: None
        """
        url = self.api_address + 'services/light/turn_off'
        body = {
            "entity_id": "light.{}_light".format(room)
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_off_all(self):
        """
        Ask Hass to turn off all of the lights
        :return:
        """
        url = self.api_address + 'services/light/turn_off'
        body = {
            "entity_id": "all",
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_color(self, room, color):
        url = self.api_address + 'services/light/turn_on'
        body = {
            "entity_id": "light.{}_light".format(room),
            "color_name": color
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_color_all(self, color):
        url = self.api_address + 'services/light/turn_on'
        body = {
            "entity_id": "all",
            "color_name": color
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_brightness(self, room, brightness):
        url = self.api_address + 'services/light/turn_on'
        body = {
            "entity_id": "light.{}_light".format(room),
            "brightness": brightness
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_brightness_all(self, brightness):
        url = self.api_address + 'services/light/turn_on'
        body = {
            "entity_id": "all",
            "brightness": brightness
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def shift_light_up(self, room, percent):
        url = self.api_address + 'states/bedroom_light'
        request = rq.get(url, headers=self.header)
        print(request.text)


    # def shift_light_up_all(self, room, percent):
    #
    #
    # def shift_light_down(self, room, percent):
    #
    #
    # def shift_light_down_all(self, room, percent):

import json
import requests as rq


class SnipsHomeManager:
    def __init__(self, autho, header):
        print("Creted the snips home manager")
        self.autho = autho
        self.header = header
        self.api_address = 'http://192.168.0.136:8123/api/'

    def light_on(self, room):
        url = self.api_address + 'services/light/turn_on'
        body = {
            "entity_id": "light.{}_light".format(room)
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_on_all(self):
        url = self.api_address + 'services/light/turn_on'
        request = rq.post(url, headers=self.header)

    def light_off(self, room):
        url = self.api_address + 'services/light/turn_off'
        body = {
            "entity_id": "light.{}_light".format(room)
        }
        json_body = json.dumps(body)
        request = rq.post(url, data=json_body, headers=self.header)

    def light_off_all(self):
        url = self.api_address + 'services/light/turn_off'
        request = rq.post(url, headers=self.header)
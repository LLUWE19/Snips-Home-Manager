#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "192.168.0.136"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_LIGHT_ON = "turnOn"
INTENT_LIGHT_OFF = "turnOff"
INTENT_LIGHT_COLOR = "setColor"
INTENT_LIGHT_BRIGHTNESS = "setBrightness"
INTENT_LIGHTS_UP = "shiftUp"
INTENT_LIGHTS_DOWN = "shiftDown"
INTENT_SET_SCENE = "setScene"


class HomeManager(object):
    def __init__(self):
        print("Loading HomeManager")
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except:
            self.config = None
            print("[Warning] No config file")
        self.autho = self.config['secret']['http_api_token']
        print(self.autho)
        self.header = {
            'Authorization': self.autho,
            "Content-Type": "application/json",
        }
        # start listening to MQTT
        self.start_blocking()

    def turn_light_on(self, hermes, intent_message):
        print("[WARNING] Implement turn_light_on")
        sentence = "Heard ya"
        hermes.publish_end_session(intent_message.session_id, sentence)

    def turn_light_off(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(intent_message.session_id, sentence)
        print("[WARNING] Implement turn_light_off")

    def set_light_color(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(intent_message.session_id, sentence)
        print("[WARNING] Implement set_light_color")

    def set_light_brightness(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(intent_message.session_id, sentence)
        print("[WARNING] Implement set_light_brightness")

    def shift_lights_up(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(intent_message.session_id, sentence)
        print("[WARNING] Implement shift_lights_up")

    def shift_lights_down(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(intent_message.session_id, sentence)
        print("[WARNING] Implement shift_lights_down")

    def set_a_scene(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(intent_message.session_id, sentence)
        print("[WARNING] Implement set_a_scene")

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            print("Debug")
            h.subscribe_intent(INTENT_LIGHT_ON, self.turn_light_on) \
                .subscribe_intent(INTENT_LIGHT_OFF, self.turn_light_off) \
                .subscribe_intent(INTENT_LIGHT_COLOR, self.set_light_color) \
                .subscribe_intent(INTENT_LIGHT_BRIGHTNESS, self.set_light_brightness) \
                .start()


if __name__ == "__main__":
    HomeManager()


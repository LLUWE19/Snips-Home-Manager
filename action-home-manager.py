#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIG_INI = "config.ini.default"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_LIGHT_ON = "LLUWE19:turnOn"
INTENT_LIGHT_OFF = "LLUWE19:turnOff"
INTENT_LIGHT_COLOR = "LLUWE19:setColor"
INTENT_LIGHT_BRIGHTNESS = "LLUWE19:setBrightness"
INTENT_LIGHTS_UP = "LLUWE19:shiftUp"
INTENT_LIGHTS_DOWN = "LLUWE19:shiftDown"
INTENT_SET_SCENE = "LLUWE19:setScene"


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
        hermes.publish_end_session(session_id, sentence)

    def turn_light_off(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(session_id, sentence)
        print("[WARNING] Implement turn_light_off")

    def set_light_color(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(session_id, sentence)
        print("[WARNING] Implement set_light_color")

    def set_light_brightness(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(session_id, sentence)
        print("[WARNING] Implement set_light_brightness")

    def shift_lights_up(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(session_id, sentence)
        print("[WARNING] Implement shift_lights_up")

    def shift_lights_down(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(session_id, sentence)
        print("[WARNING] Implement shift_lights_down")

    def set_a_scene(self, hermes, intent_message):
        sentence = "Heard ya"
        hermes.publish_end_session(session_id, sentence)
        print("[WARNING] Implement set_a_scene")

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            print("Debug")
            h \
                .subscribe_intents(INTENT_LIGHT_ON, self.turn_light_on) \
                .subscribe_intents(INTENT_LIGHT_OFF, self.turn_light_off) \
                .subscribe_intents(INTENT_LIGHT_COLOR, self.set_light_color) \
                .subscribe_intents(INTENT_LIGHT_BRIGHTNESS, self.set_light_brightness) \
                .subscribe_intents(INTENT_LIGHTS_UP, self.shift_lights_up) \
                .subscribe_intents(INTENT_LIGHTS_DOWN, self.shift_lights_down) \
                .subscribe_intents(INTENT_SET_SCENE, self.set_a_scene) \
                .start()


if __name__ == "__main__":
    HomeManager()

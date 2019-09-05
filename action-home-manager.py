#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from snips-home-manager import SnipsHomeManager
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
        self.steward = SnipsHomeManager(self.autho, self.header)
        # start listening to MQTT
        self.start_blocking()

    def turn_light_on(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            sentence = "Turning on the "
            for room in rooms:
                print("Turning on ", room)
                sentence += " " + room
                self.steward.light_on(room)
            sentence += " lights"
        else:
            sentence = "Turning on all the lights"
            self.steward.light_on_all()
        hermes.publish_end_session(intent_message.session_id, sentence)

    def turn_light_off(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            sentence = "Turning off the "
            for room in rooms:
                self.steward.light_off(room)
                sentence += " " + room
            sentence += " lights"
        else:
            self.steward.light_off_all()
            sentence = "Turning off all the lights"
        hermes.publish_end_session(intent_message.session_id, sentence)

    def set_light_color(self, hermes, intent_message, rooms):
        color = self.extract_color(intent_message)
        if len(rooms) > 0:
            sentence = "changing  "
            for room in rooms:
                sentence += " " + room
            sentence += " lights to " + color
        else:
            sentence = "changing color for all lights "
        hermes.publish_end_session(intent_message.session_id, sentence)

    def set_light_brightness(self, hermes, intent_message, rooms):
        percent = self.extract_percentage(intent_message, None)
        if percent is None:
            sentence = "Did not specify the brightness"
            hermes.publish_end_session(intent_message.session_id, sentence)
        if len(rooms) > 0:
            sentence = "Setting  "
            for room in rooms:
                sentence += " " + room
            sentence += " lights to " + percent
        else:
            sentence = "Setting light brightness to " + percent
        hermes.publish_end_session(intent_message.session_id, sentence)

    def shift_lights_up(self, hermes, intent_message, rooms):
        percent = self.extract_percentage(intent_message, 20)
        if len(rooms) > 0:
            sentence = "Shifting lights up in the  "
            for room in rooms:
                sentence += " " + room
        else:
            sentence = "Shifting lights up "
        hermes.publish_end_session(intent_message.session_id, sentence)

    def shift_lights_down(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            sentence = "shifting light down in the  "
            for room in rooms:
                sentence += " " + room
        else:
            sentence = "shifting lights down"
        hermes.publish_end_session(intent_message.session_id, sentence)

    def set_a_scene(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            sentence = "Setting scene in "
            for room in rooms:
                sentence += " " + room
        else:
            sentence = "Setting a scene "
        hermes.publish_end_session(intent_message.session_id, sentence)

    def master_intent_callback(self,hermes, intent_message):
        rooms = self.extract_house_rooms(intent_message)
        intent_name = intent_message.intent.intent_name
        if ':' in intent_name:
            intent_name = intent_name.split(":")[1]
        if intent_name == INTENT_LIGHT_ON:
            self.turn_light_on(hermes, intent_message, rooms)
        if intent_name == INTENT_LIGHT_OFF:
            self.turn_light_off(hermes, intent_message, rooms)
        if intent_name == INTENT_LIGHT_COLOR:
            self.set_light_color(hermes, intent_message, rooms)
        if intent_name == INTENT_LIGHT_BRIGHTNESS:
            self.set_light_brightness(hermes, intent_message, rooms)
        if intent_name == INTENT_LIGHTS_UP:
            self.shift_lights_up(hermes, intent_message, rooms)
        if intent_name == INTENT_LIGHTS_DOWN:
            self.shift_lights_down(hermes, intent_message, rooms)
        if intent_name == INTENT_SET_SCENE:
            self.set_a_scene(hermes, intent_message, rooms)

    def extract_house_rooms(self, intent_message):
        house_rooms = []
        if intent_message.slots.house_room:
            for room in intent_message.slots.house_room.all():
                type(room.value)
                house_rooms.append(room.value)
        return house_rooms

    def extract_percentage(self, intent_message, default_percentage):
        percentage = default_percentage
        if intent_message.slots.percent:
            percentage = intent_message.slots.percent.first().value
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        return percentage

    def extract_color(self, intent_message):
        color_code = None
        if intent_message.slots.color:
            color_code = intent_message.slots.color.first().value
        return color_code

    def extract_scene(self, intent_message):
        scene_code = None
        if intent_message.slots.scene:
            scene_code = intent_message.slots.scene.first().value
        return scene_code

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            print("Start Blocking")
            h.subscribe_intents(self.master_intent_callback).start()


if __name__ == "__main__":
    HomeManager()


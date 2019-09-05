#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from snips_home_manager import SnipsHomeManager
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

INTENT_TV_ON = "putTvOn"
INTENT_TV_OFF = "putTvOff"

INTENT_ARRIVE_HOME = "arriveHome"
INTENT_LEAVE_HOME = "leaveHome"
INTENT_GIVE_ANSWER = "giveAnswer"
INTENT_GIVE_PERCENTAGE = "givePercentage"
INTENT_GIVE_COLOR = "giveColor"

FILTER_ARRIVE_HOME = [INTENT_GIVE_ANSWER, INTENT_GIVE_PERCENTAGE, INTENT_GIVE_COLOR]

# contexts = ["arrive_home", "at_home", "leaving_home", "out_home"]

contexts = {
    "arrive_home": False,
    "at_home": False,
    "leaving_home": False,
    "out_home": False
}


class HomeManager(object):
    """
    The HomeManager is used to manage the disucssion between Snips and Hass via MQTT (using Hermes).
    The HomeManager listens for intents and implements the logic to carry out required actions. The HomeManager passes
    on the actual task of calling Hass services and communicating with Hass onto the "SnipsHomeManager" who makes calls
    to the Hass REST API via HTTP.
    """
    def __init__(self):
        print("Loading HomeManager")
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except:
            self.config = None
            print("[Warning] No config file")
        self.autho = self.config['secret']['http_api_token']
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
        self.terminate_feedback(hermes, intent_message, sentence)

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
        self.terminate_feedback(hermes, intent_message, sentence)

    def set_light_color(self, hermes, intent_message, rooms):
        color = self.extract_color(intent_message)
        if len(rooms) > 0:
            sentence = "changing  "
            for room in rooms:
                sentence += " " + room
                self.steward.light_color(room, color)
            sentence += " lights to " + color
        else:
            self.steward.light_color_all(color)
            sentence = "changing color for all lights "
        self.terminate_feedback(hermes, intent_message, sentence)

    def set_light_brightness(self, hermes, intent_message, rooms):
        percent = self.extract_percentage(intent_message, None)
        if percent is None:
            sentence = "Did not specify the brightness"
            self.terminate_feedback(hermes, intent_message, sentence)
        if len(rooms) > 0:
            sentence = "Setting  "
            for room in rooms:
                self.steward.light_brightness(room, percent)
                sentence += " " + room
            sentence += " lights to " + str(percent)
        else:
            self.steward.light_brightness_all(percent)
            sentence = "Setting light brightness to " + str(percent)
        self.terminate_feedback(hermes, intent_message, sentence)

    def shift_lights_up(self, hermes, intent_message, rooms):
        percent = self.extract_percentage(intent_message, 20)
        if len(rooms) > 0:
            sentence = "Shifting lights up in the  "
            for room in rooms:
                self.steward.shift_light_up(room, percent)
                sentence += " " + room
        else:
            #self.steward.shift_light_up_all(percent)
            sentence = "Can only shift a specific light "
        self.terminate_feedback(hermes, intent_message, sentence)

    def shift_lights_down(self, hermes, intent_message, rooms):
        percent = self.extract_percentage(intent_message, 20)
        if len(rooms) > 0:
            sentence = "shifting light down in the  "
            for room in rooms:
                self.steward.shift_light_down(room, percent)
                sentence += " " + room
        else:
            #self.steward.shift_light_down_all(percent)
            sentence = "Can only shift a specific light"
        self.terminate_feedback(hermes, intent_message, sentence)

    def set_a_scene(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            sentence = "Setting scene in "
            for room in rooms:
                sentence += " " + room
        else:
            sentence = "Setting a scene "
        self.terminate_feedback(hermes, intent_message, sentence)

    def turn_tv_on(self, hermes, intent_message):
        self.steward.tv_on()
        sentence = "tee vee on"
        self.terminate_feedback(hermes, intent_message, sentence)

    def turn_tv_off(self, hermes, intent_message):
        self.steward.tv_off()
        sentence = "tee vee off"
        self.terminate_feedback(hermes, intent_message, sentence)

    def arrive_home(self, hermes, intent_message):
        print("User has arrived home")
        sentence = "welcome home do you want the lights on"
        global CONTEXT_ARRIVE_HOME
        CONTEXT_ARRIVE_HOME = True
        self.terminate_feedback(hermes, intent_message, sentence)

    def master_intent_callback(self,hermes, intent_message):
        rooms = self.extract_house_rooms(intent_message)
        intent_name = intent_message.intent.intent_name
        print("[DEBUG] " + intent_name)
        if ':' in intent_name:
            intent_name = intent_name.split(":")[1]
            print("[DEBUG] " + intent_name)
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
        if intent_name == INTENT_TV_ON:
            self.turn_tv_on(hermes, intent_message)
        if intent_name == INTENT_TV_OFF:
            self.turn_tv_off(hermes, intent_message)
        if intent_name == INTENT_ARRIVE_HOME:
            self.arrive_home(hermes, intent_message)

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

    def terminate_feedback(self, hermes, intent_message, sentence):
        hermes.publish_end_session(intent_message.session_id, sentence)
        

if __name__ == "__main__":
    HomeManager()


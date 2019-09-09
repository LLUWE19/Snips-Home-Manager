#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from snips_home_manager import SnipsHomeManager
from intent_processor import IntentProcessor
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "192.168.0.136"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

"""Register intents"""
INTENT_LIGHT_ON = "turnOn"
INTENT_LIGHT_OFF = "turnOff"
INTENT_LIGHT_COLOR = "setColor"
INTENT_LIGHT_BRIGHTNESS = "setBrightness"
INTENT_LIGHTS_UP = "shiftUp"
INTENT_LIGHTS_DOWN = "shiftDown"
INTENT_SET_SCENE = "setScene"
INTENT_GIVE_ANSWER = "giveAnswer"  # yes or no
INTENT_TV_ON = "putTvOn"
INTENT_TV_OFF = "putTvOff"

INTENT_ARRIVE_HOME = "arriveHome"
INTENT_LEAVE_HOME = "leaveHome"


FILTER_ARRIVE_HOME = [INTENT_GIVE_ANSWER, ]



last_question = None


class HomeManager(object):
    """
    The HomeManager is used to manage the disucssion between Snips and Hass via MQTT (using Hermes).
    The HomeManager listens for intents and implements the logic to carry out required actions. The HomeManager passes
    on the actual task of calling Hass services and communicating with Hass onto the "SnipsHomeManager" who makes calls
    to the Hass REST API.
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
        self.intent_processor = IntentProcessor()
        # Manage the calls to the Hass API
        self.steward = SnipsHomeManager(self.autho, self.header)
        self.last_question = None
        self.contexts = {
            "arrive_home": False,
            "at_home": False,
            "leaving_home": False,
            "out_home": False
        }
        self.questions = {
            "lights on": "do you want the lights on",
            "light_color": "what color do you want the lights",
            "light_brightness": "how bright do you want the light",
            "tv_on": "do you want the tv on"
        }
        # start listening to MQTT
        self.start_blocking()



    def arrive_home(self, hermes, intent_message):
        print("User has arrived home")
        sentence = "welcome home. " + self.questions['tv_on']
        self.contexts['arrive_home'] = True
        self.terminate_feedback(hermes, intent_message, sentence, "arrive_home")

    def welcome_home_handler(self, hermes, intent_message, last_answer):
        if self.last_question == self.questions['tv_on']:
            answer = self.extract_answer(intent_message)
            if answer:
                self.steward.light_on_all()
                sentence = self.questions['light_color']
                self.terminate_feedback(hermes, intent_message, sentence, "arrive_home")
        elif self.last_question == self.questions['light_color']:

    def master_intent_callback(self,hermes, intent_message):
        """
        A register for intent callback functions. Any intent from Snips
        will be processed here e.g. extracting and counting rooms and passing on to the corresponding
        callback function.
        """
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
        if intent_name == INTENT_GIVE_ANSWER and self.contexts['arrive_home']:
            self.welcome_home_handler(hermes, intent_message, INTENT_GIVE_ANSWER)


    def start_blocking(self):
        """
        Start listening to intents on the MQTT broker.
        Any Snips intent will be pass to the master callback function to be processed.
        """
        with Hermes(MQTT_ADDR) as h:
            print("Start Blocking")
            h.subscribe_intents(self.master_intent_callback).start()

    def terminate_feedback(self, hermes, intent_message, sentence, context):
        """
        After an intent is processed in the callback function, terminate_feedback will make a decision
        whether to continue or end a conversation.

        (Currently only ends a conversation)
        :param context:
        :param hermes:
        :param intent_message:
        :param sentence:
        :return:
        """
        if context == "arrive_home" and sentence == "welcome home. do you want the lights on":
            hermes.publish_continue_session(intent_message.session_id, sentence, [INTENT_GIVE_ANSWER])
        elif context == "arrive_home" and sentence == "":


            hermes.publish_end_session(intent_message.session_id, sentence)


if __name__ == "__main__":
    HomeManager()


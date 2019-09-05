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

    def turn_light_on(self, hermes, intent_message, rooms):
        """
        Call back function to manage turning on the lights.
        Will turn on a few lights in specified rooms, or will turn every light on
        :param rooms: Room names extracted from the intent slots
        :return: None, calls terminate_feedback to manage the conversation
        """
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


    def extract_house_rooms(self, intent_message):
        """
        Extract the rooms or entities from the given intents slots
        :return: A list of rooms to manage devices in
        """
        house_rooms = []
        if intent_message.slots.house_room:
            for room in intent_message.slots.house_room.all():
                type(room.value)
                house_rooms.append(room.value)
        return house_rooms

    def extract_percentage(self, intent_message, default_percentage):
        """
        Extract the percentage value from the given intents slots
        :return: A float percentage value
        """
        percentage = default_percentage
        if intent_message.slots.percent:
            percentage = intent_message.slots.percent.first().value
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        return percentage

    def extract_color(self, intent_message):
        """
        Extract the color value from the given intents slots
        :return: A human readable color value
        """
        color_code = None
        if intent_message.slots.color:
            color_code = intent_message.slots.color.first().value
        return color_code

    def extract_scene(self, intent_message):
        """
        Extract the scene from the given intents slots
        :return: A code describing which scene to call
        """
        scene_code = None
        if intent_message.slots.scene:
            scene_code = intent_message.slots.scene.first().value
        return scene_code

    def extract_answer(self, intent_message):
        """
        Extract a yes or no answer from the given intent slot
        :return: A boolean describing yes or no
        """
        final_answer = None
        if intent_message.slots.answer:
            answer = intent_message.slots.color.first().value
            if answer == "yes":
                final_answer = True
            else:
                final_answer = False

        return final_answer

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


class CallbackProcessor:
    def __init__(self):




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
        color = self.intent_processor.extract_color(intent_message)
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
        percent = self.intent_processor.extract_percentage(intent_message, None)
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
        percent = self.intent_processor.extract_percentage(intent_message, 20)
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
        percent = self.intent_processor.extract_percentage(intent_message, 20)
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
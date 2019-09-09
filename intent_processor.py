

class IntentProcessor:

    def __init__(self):
        print("Made an intent processor")


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
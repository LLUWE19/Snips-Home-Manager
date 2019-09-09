## Snips Home Manager
The snips Home manager is a Snips skill used to manage the lights and switches in the living lab.

The home manager was adapted from the snipshue light skill, but changed to make Hass REST API calls rather than talk to the phillips hue. 

The basic intents to control lights in this skill currently include:

- turnOn
- turnOff
- setBrightness
- setColor
- shiftUp
- shiftDown
- setScene (not implemented)

There are also intents to turn the tv on or off
- tvOn
- tvOff

These intents can be used to issue commands like "hey snips, turn the lights on" or "hey snips, shift the lights up" or "hey snips, make the bedroom light blue"

The intents to manage multi turn dialogue include:

- arriveHome
- leaveHome
- giveAnswer

These intents are intended to be used to engage in a multi-turn dialgoue with snips. E.g. 

User: "hey Snips, im home". 
Snips: "Welcome home, do you want the lights on?"
User: "Yes"
Snips: "Okay, how bright do you want the lights?"
User: "50 percent"
Snips: "Okay, what color do you want the light?"
User: "White"
Snips: "Okay, did you want the TV on?"
User: "Yes please"
Snips: "Okay, welcome home"




Home manager is currently testing how to integrate single line commands like turn on the lights, and multi-turn dialogue which will ask if you want to turn on the lights and a series of other questions. The issue is with intents, and how to reuse intents in a different situation e.g. conversations or commands. Using multiple intents with similar slots might introduce clashes like ending a converstaion sooner or starting a converstaion instead of making a command.

(If only using single line commands snips actions are likely easier programmed in the intent_scripts.yaml file)

These are the steps for installation:

1. Need an assistant from the snips console that has the same intents. As described in the code.
2. Need to link this repository to the assistant in the actions section of the assistants console.
3. In a command promt or powershell, use the sam install assistants command and select the right assistant.
4. After installation the action- file may need to be turned into an executable. Open a putty terminal to access the pi, cd to var/sys/snips/skills/Snips-home-manager and use chmod command on the action file.
5. Go back to command prompt and use the sam install actions command. It will run and say everything is already up to date and the permissions warning should have disapeared.
6. Use sam watch in the command line, and use sudo tail -f /var/log/syslog in the putty terminal to watch and debug during testing.

If code needs to be changed then need follow some extra steps as snips will not overwrite the old action files.

1. Make the change to the action code.
2. Upload the new action code to the github.
3. In the putty terminal, delete the directory inside var/sys/snips/skills/.
4. In the command prompt use sam install actions to install the updated skill.
5. Use chmod in the putty terminal to make the action file executable again.
6. Go back to the command prompt and sam install actions again.
7. Use sam watch in the command line, and use sudo tail -f /var/log/syslog in the putty terminal to watch and debug during testing.

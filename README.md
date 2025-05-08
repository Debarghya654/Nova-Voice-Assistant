# Nova-Voice-Assistant

Objective:
The project creates a desktop-based voice assistant using Python with a graphical user interface (GUI), built with PyQt5. It integrates speech recognition and text-to-speech capabilities.

Libraries Used:
1. PyQt5: For creating the GUI.
2. speech_recognition: To capture and process voice commands.
3. pyttsx3: For converting text to speech.
4. datetime: For handling date and time-related functionalities.
5. webbrowser: To open websites (e.g., Google).
6. json: For saving and loading settings and reminders.

Voice Profiles:
Supports switching between male and female voices for the assistant (using pyttsx3 engine).

Assistant Initialization:
1. VoiceAssistant class initializes the assistant, sets its voice, and loads previous settings and reminders.
2. The assistant greets the user upon startup and begins listening for voice commands.

Settings Management:
1. Stores user settings (name and voice preference) in a JSON file (nova_settings.json).
2. The assistant can change the voice (male/female) and update the settings file accordingly.

Reminder System:
1. Users can set, view, and delete reminders. Reminders are saved in nova_reminders.json.
2. A timer checks every minute for any due reminders and reads them aloud.

Main GUI Components:
1. Output Label: Displays the assistant's responses.
2. Command Log: A text area that logs all commands and responses.
3. Listen Button: When clicked, starts listening for voice commands.
4. Reminder List: Displays the list of reminders, where users can double-click to delete a reminder.

Command Processing:
1. Commands include greetings, changing voice, telling the time, opening websites (e.g., Google), telling jokes, setting reminders, and exiting the assistant.
2. Custom handling of time-based reminders with specific formats like "remind me at 5 PM."

Speech Recognition:
The assistant listens for voice commands using a microphone, processes the speech using Google's speech recognition API, and handles different commands accordingly.

Reminders:
1. Reminders are set through voice commands, saved in a list, and displayed in the GUI.
2. The assistant reads due reminders aloud at the specified time.

Exit Functionality:
The assistant can exit gracefully when receiving a command like "exit" or "stop."

Error Handling:
Handles cases where the assistant doesn't understand a command, or if the connection to the API fails.

User Interaction:
The assistant speaks to the user using text-to-speech and listens for commands, providing a seamless voice-based interaction experience.

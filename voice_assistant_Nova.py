# voice_assistant_gui.py

import sys
import os
import json
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QListWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime

engine = pyttsx3.init()
voices = engine.getProperty('voices')
voice_profiles = {
    'nova_female': [v for v in voices if 'female' in v.name.lower()],
    'nova_male': [v for v in voices if 'male' in v.name.lower()]
}

recognizer = sr.Recognizer()
SETTINGS_FILE = "nova_settings.json"
REMINDERS_FILE = "nova_reminders.json"

class VoiceAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.assistant_name = "Nova"
        self.user_name = "User"
        self.current_voice = 'nova_female'
        self.set_voice(self.current_voice)

        self.reminders = []
        self.load_settings()
        self.load_reminders()

        self.setWindowTitle(f"{self.assistant_name} - Voice Assistant")
        self.setGeometry(100, 100, 400, 400)
        self.init_ui()
        self.speak(f"Hello {self.user_name}, {self.assistant_name} is ready.")

        self.reminder_timer = QTimer()
        self.reminder_timer.timeout.connect(self.read_due_reminders)
        self.reminder_timer.start(60000)  # check every 1 min

    def set_voice(self, profile):
        options = voice_profiles.get(profile)
        if options:
            engine.setProperty('voice', options[0].id)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                self.user_name = data.get('user_name', self.user_name)
                self.current_voice = data.get('voice', self.current_voice)
                self.set_voice(self.current_voice)

    def save_settings(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({
                'user_name': self.user_name,
                'voice': self.current_voice
            }, f)

    def load_reminders(self):
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, 'r') as f:
                self.reminders = json.load(f)

    def save_reminders(self):
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(self.reminders, f)

    def init_ui(self):
        self.output_label = QLabel(f"Welcome to your assistant, {self.assistant_name}")
        self.command_log = QTextEdit()
        self.command_log.setReadOnly(True)

        self.listen_button = QPushButton("🎤 Listen")
        self.listen_button.clicked.connect(self.run_assistant)

        self.reminder_list = QListWidget()
        for r in self.reminders:
            self.reminder_list.addItem(f"{r['time']} - {r['text']}")
        self.reminder_list.itemDoubleClicked.connect(self.delete_reminder)

        layout = QVBoxLayout()
        layout.addWidget(self.output_label)
        layout.addWidget(self.command_log)
        layout.addWidget(self.listen_button)
        layout.addWidget(QLabel("Reminders (double-click to delete):"))
        layout.addWidget(self.reminder_list)

        self.setLayout(layout)

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()
        self.output_label.setText(text)

    def listen(self):
        with sr.Microphone() as source:
            self.output_label.setText("Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='en-US')
            self.command_log.append(f"You: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Please repeat.")
            return ""
        except sr.RequestError:
            self.speak("API connection failed.")
            return ""

    def process_command(self, command):
        if "hello" in command:
            self.speak(f"Hello {self.user_name}, I'm {self.assistant_name}. How can I help you?")
        elif "my name is" in command:
            name = command.split("my name is")[-1].strip().title()
            if name:
                self.user_name = name
                self.save_settings()
                self.speak(f"Nice to meet you, {self.user_name}.")
        elif "change voice" in command:
            self.current_voice = 'nova_male' if self.current_voice == 'nova_female' else 'nova_female'
            self.set_voice(self.current_voice)
            self.save_settings()
            self.speak("Voice updated.")
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}")
        elif "open google" in command:
            self.speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "tell me a joke" in command:
            self.speak("Why don't scientists trust atoms? Because they make up everything!")
        elif "remind me at" in command:
            try:
                time_part = command.split("remind me at")[-1].split("to")[0].strip()
                reminder_part = command.split("to")[-1].strip()
                reminder_time = datetime.datetime.strptime(time_part, "%I %p").strftime("%H:%M")
                reminder_entry = {"time": reminder_time, "text": reminder_part}
                self.reminders.append(reminder_entry)
                self.save_reminders()
                self.reminder_list.addItem(f"{reminder_time} - {reminder_part}")
                self.speak(f"Reminder set for {time_part} to {reminder_part}")
            except Exception as e:
                self.speak("I couldn't understand the reminder format. Please say something like 'remind me at 5 PM to call John'")
        elif "exit" in command or "stop" in command:
            self.speak("Goodbye!")
            sys.exit()
        else:
            self.speak("I'm not sure how to help with that.")

    def delete_reminder(self, item):
        text = item.text()
        self.reminders = [r for r in self.reminders if f"{r['time']} - {r['text']}" != text]
        self.save_reminders()
        self.reminder_list.takeItem(self.reminder_list.row(item))
        self.speak(f"Deleted reminder: {text}")

    def read_due_reminders(self):
        now = datetime.datetime.now().strftime("%H:%M")
        due = [r for r in self.reminders if r['time'] == now]
        for r in due:
            self.speak(f"Reminder: {r['text']}")

    def run_assistant(self):
        command = self.listen()
        if command:
            self.process_command(command)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = VoiceAssistant()
    assistant.show()
    sys.exit(app.exec_())

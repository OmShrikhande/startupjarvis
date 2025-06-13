import sys
import subprocess
import pyttsx3
import psutil
import datetime
import speech_recognition as sr
import webbrowser
import os
import random
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QGraphicsDropShadowEffect, QHBoxLayout, QTextEdit)
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter, QBrush, QRadialGradient
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

# === Voice Engine Setup ===
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

# === Command Listener ===
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            command = r.recognize_google(audio).lower()
            return command
        except Exception:
            return None

# === System Info ===
def get_system_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f"🧠 CPU: {cpu}%   📀 RAM: {ram}%   ⏰ Time: {now}"

# === Weather Info ===
def get_weather():
    try:
        api_key = "your_openweather_api_key"
        city = "Pune"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        return f"{city} weather is {desc} with {temp}°C"
    except:
        return "Unable to fetch weather info."

# === Voice Thread ===
class VoiceCommandThread(QThread):
    command_received = pyqtSignal(str)

    def run(self):
        while True:
            command = listen_command()
            if command and "jarvis" in command:
                self.command_received.emit(command)

# === Main Launcher ===
class JarvisLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Om Jarvis Launcher")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui()

        speak("Jarvis online and awaiting your orders, Sir.")
        self.voice_thread = VoiceCommandThread()
        self.voice_thread.command_received.connect(self.handle_voice_command)
        self.voice_thread.start()

    def init_ui(self):
        layout = QVBoxLayout()

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setStyleSheet("background: rgba(0,0,0,0.4); color: cyan; font-size: 14px; border: none;")
        layout.addWidget(self.chat_box)

        title = QLabel("OM JARVIS LAUNCHER")
        title.setFont(QFont("Consolas", 26, QFont.Bold))
        title.setStyleSheet("color: cyan;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.sys_label = QLabel()
        self.sys_label.setStyleSheet("color: white; font-size: 14px;")
        self.sys_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sys_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sys_info)
        self.timer.start(1000)

        btn_layout = QHBoxLayout()
        buttons = [
            ("VS Code", lambda: self.launch_app("C:/Users/OM/AppData/Local/Programs/Microsoft VS Code/Code.exe")),
            ("Chrome", lambda: self.launch_app("C:/Program Files/Google/Chrome/Application/chrome.exe")),
            ("Brave", lambda: self.launch_app("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")),
            ("ToDo", lambda: self.launch_app("C:/Users/OM/Desktop/docs/Failur.txt")),
            ("Aptitude", lambda: self.launch_app("C:/Users/OM/Desktop/docs/quantitative-aptitude-for-competitive-examinations-by-rs-aggarwal-reprint-2017.pdf")),
            ("Projects", lambda: self.launch_app("explorer.exe C:/xampp/htdocs")),
            ("Exit", self.close_app)
        ]

        for text, action in buttons:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(action)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0d0d0d;
                    color: cyan;
                    border: 2px solid cyan;
                    padding: 10px;
                    border-radius: 12px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: cyan;
                    color: black;
                }
            """)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QColor("cyan"))
            shadow.setOffset(0)
            btn.setGraphicsEffect(shadow)
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QRadialGradient(self.width()/2, self.height()/2, self.width())
        gradient.setColorAt(0, QColor("#001f33"))
        gradient.setColorAt(1, QColor("#000000"))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

    def update_sys_info(self):
        self.sys_label.setText(get_system_info())

    def log_chat(self, text):
        self.chat_box.append(f"<b>Jarvis:</b> {text}")

    def handle_voice_command(self, command):
        print(f"Voice command received: {command}")
        command = command.replace("jarvis", "").strip()
        self.log_chat(f"Command: {command}")

        if "chrome" in command:
            self.respond_and_launch("Opening Chrome", "C:/Program Files/Google/Chrome/Application/chrome.exe")
        elif "brave" in command:
            self.respond_and_launch("Opening Brave", "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
        elif "code" in command or "vs" in command:
            self.respond_and_launch("Launching VS Code", "C:/Users/OM/AppData/Local/Programs/Microsoft VS Code/Code.exe")
        elif "project" in command:
            self.respond_and_launch("Opening projects", "explorer.exe C:/xampp/htdocs")
        elif "todo" in command:
            self.respond_and_launch("Opening to-do list", "C:/Users/OM/Desktop/docs/Failur.txt")
        elif "aptitude" in command:
            self.respond_and_launch("Opening aptitude notes", "C:/Users/OM/Desktop/docs/quantitative-aptitude-for-competitive-examinations-by-rs-aggarwal-reprint-2017.pdf")
        elif "youtube" in command:
            self.respond("Launching YouTube")
            webbrowser.open("https://youtube.com")
        elif "spotify" in command or "music" in command:
            self.respond("Playing music")
            webbrowser.open("https://open.spotify.com")
        elif "shutdown" in command:
            self.respond("Shutting down system")
            subprocess.call("shutdown /s /t 5")
        elif "lock screen" in command or "log off" in command:
            self.respond("Locking screen")
            subprocess.call("rundll32.exe user32.dll,LockWorkStation")
        elif "volume up" in command:
            subprocess.call(["nircmd.exe", "changesysvolume", "2000"])
        elif "volume down" in command:
            subprocess.call(["nircmd.exe", "changesysvolume", "-2000"])
        elif "weather" in command:
            info = get_weather()
            self.respond(info)
        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            self.respond(f"The time is {now}")
        elif "joke" in command:
            joke = random.choice([
                "Why don’t scientists trust atoms? Because they make up everything!",
                "I would tell you a construction pun, but I’m still working on it.",
                "Why do Java developers wear glasses? Because they don't see sharp."
            ])
            self.respond(joke)
        elif "whatsapp" in command:
            self.respond_and_launch("Opening WhatsApp", "C:/Users/OM/AppData/Local/WhatsApp/WhatsApp.exe")
        elif "telegram" in command:
            self.respond_and_launch("Opening Telegram", "C:/Users/OM/AppData/Roaming/Telegram Desktop/Telegram.exe")
        elif "exit" in command or "quit" in command:
            self.close_app()
        elif "run" in command or "start" in command:
            app_name = command.replace("run", "").replace("start", "").strip()
            self.respond_and_launch(f"Trying to start {app_name}", app_name)
        else:
            self.respond("Sorry, I couldn't understand.")

    def respond(self, text):
        speak(text)
        self.log_chat(text)

    def respond_and_launch(self, speech, path):
        speak(speech)
        self.log_chat(speech)
        self.launch_app(path)

    def launch_app(self, path):
        try:
            if path.lower().endswith(('.txt', '.pdf')):
                os.startfile(path)
            else:
                subprocess.Popen(path if isinstance(path, list) else path.split())
        except Exception as e:
            self.log_chat(f"Error launching {path}: {e}")
            speak("Failed to launch application.")

    def close_app(self):
        self.respond("Goodbye, Sir.")
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = JarvisLauncher()
    launcher.showFullScreen()
    sys.exit(app.exec_())
import sys
import subprocess
import pyttsx3
import speech_recognition as sr
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QMovie, QFont, QColor


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Waiting for your command, sir.")
        print("Listening...")

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=7)
            command = r.recognize_google(audio).lower()
            print("Recognized:", command)
            return command
        except sr.WaitTimeoutError:
            speak("No command received. Try again, sir.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            speak("Internet or recognition service error.")
            return ""


class JarvisLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Om Jarvis Launcher")
        self.showFullScreen()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

        # Set animated GIF background
        gif = QMovie(r"C:\Users\OM\Desktop\1it9YM.gif")  # change path if needed
        self.bg_label.setMovie(gif)
        gif.start()

        self.init_ui()

        # Delay voice command to let GUI finish loading
        QTimer.singleShot(2000, self.handle_voice_command)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)

        title = QLabel("🔱 OM JARVIS LAUNCHER 🔱")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ffff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor("#00ffff"))
        shadow.setOffset(0, 0)
        title.setGraphicsEffect(shadow)

        layout.addWidget(title)

        button_row = QHBoxLayout()
        button_row.setSpacing(20)

        buttons = [
            ("VS Code", lambda: self.launch('vs', "Launching Visual Studio Code")),
            ("Chrome", lambda: self.launch('chrome', "Launching Chrome")),
            ("Brave", lambda: self.launch('brave', "Launching Brave")),
            ("ToDo", lambda: self.launch('todo', "Opening ToDo Notes")),
            ("Aptitude", lambda: self.launch('aptitude', "Opening Aptitude PDF")),
            ("Projects", lambda: self.launch('projects', "Opening Projects Folder")),
            ("Exit", self.close_launcher)
        ]

        for label, action in buttons:
            btn = QPushButton(label)
            btn.setFont(QFont("Segoe UI", 14))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(action)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 0, 0, 180);
                    border: 2px solid #00ffff;
                    border-radius: 10px;
                    color: #00ffff;
                    padding: 12px 22px;
                }
                QPushButton:hover {
                    background-color: #00ffff;
                    color: black;
                }
            """)
            glow = QGraphicsDropShadowEffect()
            glow.setBlurRadius(25)
            glow.setColor(QColor("#00ffff"))
            glow.setOffset(0, 0)
            btn.setGraphicsEffect(glow)

            button_row.addWidget(btn)

        layout.addLayout(button_row)

        panel = QWidget(self)
        panel.setStyleSheet("background-color: rgba(0, 0, 0, 130); border-radius: 20px;")
        panel.setGeometry(self.width() // 10, self.height() // 2, self.width() - self.width() // 5, 160)
        panel.lower()

        container = QWidget(self)
        container.setLayout(layout)
        container.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        if hasattr(self, 'bg_label'):
            self.bg_label.setGeometry(0, 0, self.width(), self.height())

    def launch(self, key, message):
        speak(message)
        try:
            paths = {
                'vs': r'C:\Users\OM\AppData\Local\Programs\Microsoft VS Code\Code.exe',
                'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
                'todo': r'C:\Users\OM\Desktop\docs\Failur.txt',
                'aptitude': r'C:\Users\OM\Desktop\docs\quantitative-aptitude-for-competitive-examinations-by-rs-aggarwal-reprint-2017.pdf',
                'projects': r'C:\xampp\htdocs',
            }
            if key == 'projects':
                subprocess.Popen(['explorer', paths[key]])
            else:
                subprocess.Popen([paths[key]], shell=True)
        except Exception as e:
            speak("Error opening application.")

    def close_launcher(self):
        speak("Goodbye sir.")
        self.close()

    def handle_voice_command(self):
        command = listen_command()
        if "chrome" in command:
            self.launch("chrome", "Launching Chrome, sir.")
        elif "brave" in command:
            self.launch("brave", "Launching Brave, sir.")
        elif "code" in command or "vs" in command:
            self.launch("vs", "Launching VS Code, sir.")
        elif "aptitude" in command:
            self.launch("aptitude", "Opening Aptitude Book, sir.")
        elif "to do" in command or "todo" in command:
            self.launch("todo", "Opening ToDo List, sir.")
        elif "projects" in command:
            self.launch("projects", "Opening Projects, sir.")
        elif "exit" in command or "close" in command:
            self.close_launcher()
        else:
            speak("Command not recognized, sir.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = JarvisLauncher()
    jarvis.show()
    sys.exit(app.exec())

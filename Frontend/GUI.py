from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit,
    QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
)
from PyQt5.QtGui import (
    QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
)
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

# Environment setup
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

# Utility functions
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(Query):
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you"]
    if any(Query.lower().startswith(word) for word in question_words):
        if not Query.endswith("?"):
            Query = Query.strip() + "?"
    else:
        if not Query.endswith("."):
            Query = Query.strip() + "."
    return Query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', 'w', encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', 'r', encoding='utf-8') as file:
        return file.read()

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', 'w', encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', 'r', encoding='utf-8') as file:
        return file.read()

# def MicButtonInitialized():
#     SetMicrophoneStatus("False")

# def MicButtonClosed():
#     SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    return rf'{GraphicsDirPath}\{Filename}'

def TempDirectoryPath(Filename):
    return rf'{TempDirPath}\{Filename}'

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', 'w', encoding='utf-8') as file:
        file.write(Text)

# ---------------- CHAT SECTION ----------------
class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)

        self.setStyleSheet("background-color: black;")

        self.gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(350, 200))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(200)

    def loadMessages(self):
        global old_chat_message
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()
        except:
            return

        if not messages or str(old_chat_message) == str(messages):
            return

        self.addMessage(message=messages, color='White')
        old_chat_message = messages

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except:
            pass

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

# ---------------- INITIAL SCREEN ----------------
# ---------------- INITIAL SCREEN ----------------
class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)

        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(800, 450))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)

        # ✅ START WITH MIC OFF
        self.toggled = False
        self.update_icon()

        # Click event
        self.icon_label.mousePressEvent = self.toggle_icon

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px;")

        content_layout.addWidget(gif_label)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        self.setLayout(content_layout)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(200)

    # ✅ FIXED ICON + STATUS SYNC
    def update_icon(self):
        if self.toggled:
            # Mic ON
            pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
            SetMicrophoneStatus("True")
        else:
            # Mic OFF
            pixmap = QPixmap(GraphicsDirectoryPath('Mic_off.png'))
            SetMicrophoneStatus("False")

        self.icon_label.setPixmap(pixmap.scaled(60, 60))

    # ✅ CLEAN TOGGLE
    def toggle_icon(self, event=None):
        self.toggled = not self.toggled
        self.update_icon()

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except:
            pass

# ---------------- MESSAGE SCREEN ----------------
class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(ChatSection())

# ---------------- TOP BAR ----------------
class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)

        # Title
        title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet("color: black; font-size: 18px;")

        # Buttons
        home_button = QPushButton("Home")
        message_button = QPushButton("Chat")

        # Navigation actions
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Styling
        home_button.setStyleSheet("background-color: white; color: black; padding: 5px 15px;")
        message_button.setStyleSheet("background-color: white; color: black; padding: 5px 15px;")

        # Layout arrangement
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(home_button)
        layout.addWidget(message_button)

        self.setStyleSheet("background-color: white;")

# ---------------- MAIN WINDOW ----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Jarvis AI")
        self.resize(1200, 800)

        stacked_widget = QStackedWidget()
        stacked_widget.addWidget(InitialScreen())
        stacked_widget.addWidget(MessageScreen())

        top_bar = CustomTopBar(self, stacked_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(top_bar)
        main_layout.addWidget(stacked_widget)

        self.setCentralWidget(main_widget)

# ---------------- RUN ----------------
def GraphicalUserInterface():
    app = QApplication(sys.argv)

    # FULL BLACK UI FIX
    app.setStyleSheet("""
    QMainWindow, QWidget {
        background-color: black;
    }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
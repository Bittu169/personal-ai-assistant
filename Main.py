from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# ---------------- ENV ----------------
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

DefaultMessage = f'''{Username}: Hello {Assistantname}, How are you?
{Assistantname}: I am doing well. How may I help you?'''

subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# ---------------- DEFAULT CHAT ----------------
def ShowDefaultChatIfNoChats():
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as File:
            if len(File.read()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                    file.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
                    file.write(DefaultMessage)
    except:
        pass

# ---------------- INITIAL ----------------
def InitialExecution():
    ShowDefaultChatIfNoChats()

# ---------------- MAIN EXECUTION ----------------
# def MainExecution():
#     TaskExecution = False
#     ImageExecution = False
#     ImageGenerationQuery = ""

#     try:
#         # Listening
#         SetAssistantStatus("Listening ...")
#         Query = SpeechRecognition()
#         print("User Query:", Query)

#         # Safety check
#         if not Query or Query.strip() == "":
#             return

#         # Show user query
#         ShowTextToScreen(f"{Username} : {Query}")

#         # Thinking
#         SetAssistantStatus("Thinking ...")
#         Decision = FirstLayerDMM(Query)
#         print("Decision:", Decision)

#         G = any(i.startswith("general") for i in Decision)
#         R = any(i.startswith("realtime") for i in Decision)

#         Mearged_query = " and ".join(
#             ["-".join(i.split()[1:]) for i in Decision if i.startswith(("general", "realtime"))]
#         )

#         # -------- AUTOMATION --------
#         for queries in Decision:
#             if not TaskExecution and any(queries.startswith(func) for func in Functions):
#                 run(Automation(list(Decision)))
#                 TaskExecution = True

#         # -------- IMAGE --------
#         for queries in Decision:
#             if "generate " in queries:
#                 ImageGenerationQuery = str(queries)
#                 ImageExecution = True

#         if ImageExecution:
#             try:
#                 with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
#                     file.write(f"{ImageGenerationQuery},True")

#                 subprocess.Popen(['python', r'Backend\ImageGeneration.py'])
#             except Exception as e:
#                 print("Image error:", e)

#         # -------- RESPONSE --------
#         if R:
#             SetAssistantStatus("Searching ...")
#             Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
#         else:
#             SetAssistantStatus("Thinking ...")
#             Answer = ChatBot(QueryModifier(Query))

#         print("Answer:", Answer)

#         # Show + Speak
#         ShowTextToScreen(f"{Assistantname} : {Answer}")
#         SetAssistantStatus("Answering ...")
#         TextToSpeech(Answer)

#     except Exception as e:
#         print("MainExecution Error:", e)

#     finally:
#         # 🔥 KEEP LISTENING (continuous mode)
#         SetAssistantStatus("Listening ...")

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    try:
        # ❗ STOP if mic turned OFF before starting
        if GetMicrophoneStatus() != "True":
            return

        SetAssistantStatus("Listening ...")
        Query = SpeechRecognition()

        # ❗ STOP immediately if mic turned OFF during listening
        if GetMicrophoneStatus() != "True":
            SetAssistantStatus("Available...")
            return

        if not Query or Query.strip() == "":
            return

        print("User Query:", Query)
        ShowTextToScreen(f"{Username} : {Query}")

        SetAssistantStatus("Thinking ...")
        Decision = FirstLayerDMM(Query)
        print("Decision:", Decision)

        # ❗ STOP again before heavy processing
        if GetMicrophoneStatus() != "True":
            SetAssistantStatus("Available...")
            return

        G = any(i.startswith("general") for i in Decision)
        R = any(i.startswith("realtime") for i in Decision)

        Mearged_query = " and ".join(
            ["-".join(i.split()[1:]) for i in Decision if i.startswith(("general", "realtime"))]
        )

        # -------- AUTOMATION --------
        for queries in Decision:
            if not TaskExecution and any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

        # -------- IMAGE --------
        for queries in Decision:
            if "generate " in queries:
                ImageExecution = True
                ImageGenerationQuery = str(queries)

        if ImageExecution:
            try:
                with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
                    file.write(f"{ImageGenerationQuery},True")

                subprocess.Popen(['python', r'Backend\ImageGeneration.py'])
            except Exception as e:
                print("Image error:", e)

        # ❗ STOP before answering
        if GetMicrophoneStatus() != "True":
            SetAssistantStatus("Available...")
            return

        # -------- RESPONSE --------
        if R:
            SetAssistantStatus("Searching ...")
            Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        else:
            Answer = ChatBot(QueryModifier(Query))

        print("Answer:", Answer)

        # ❗ FINAL STOP CHECK
        if GetMicrophoneStatus() != "True":
            SetAssistantStatus("Available...")
            return

        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)

    except Exception as e:
        print("MainExecution Error:", e)

    finally:
        # Only continue if mic still ON
        if GetMicrophoneStatus() == "True":
            SetAssistantStatus("Listening ...")
        else:
            SetAssistantStatus("Available...")

# ---------------- THREAD ----------------
def FirstThread():
    while True:
        try:
            status = GetMicrophoneStatus()
            print("Mic Status:", status)

            if status == "True":
                MainExecution()

            else:
                if GetAssistantStatus() != "Available...":
                    SetAssistantStatus("Available...")

            sleep(0.2)

        except Exception as e:
            print("Thread Error:", e)
            sleep(0.5)

# ---------------- GUI ----------------
def SecondThread():
    GraphicalUserInterface()

# ---------------- RUN ----------------
if __name__ == "__main__":
    InitialExecution()

    thread = threading.Thread(target=FirstThread, daemon=True)
    thread.start()

    SecondThread()
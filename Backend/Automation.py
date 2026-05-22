# Import required libraries
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# ---------------- ENV ----------------
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# ---------------- CONFIG ----------------
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

client = Groq(api_key=GroqAPIKey)

messages = []

SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ.get('Username')}, You're a content writer."
}]

# ---------------- GOOGLE SEARCH ----------------
def GoogleSearch(Topic):
    search(Topic)
    return True

# ---------------- CONTENT GENERATION ----------------
def Content(Topic):

    def OpenNotepad(File):
        subprocess.Popen(['notepad.exe', File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            stream=True
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    filename = rf"Data\{Topic.lower().replace(' ', '')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(filename)
    return True

# ---------------- YOUTUBE ----------------
def YouTubeSearch(Topic):
    webbrowser.open(f"https://www.youtube.com/results?search_query={Topic}")
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

# ---------------- OPEN APP ----------------
def OpenApp(app):
    try:
        # Try opening installed app
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except:
        try:
            print(f"App not found locally. Opening in browser: {app}")

            # Known websites mapping (fast & accurate)
            sites = {
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com",
                "facebook": "https://www.facebook.com",
                "instagram": "https://www.instagram.com",
                "whatsapp": "https://web.whatsapp.com",
                "gmail": "https://mail.google.com",
                "twitter": "https://twitter.com",
                "linkedin": "https://www.linkedin.com"
            }

            app_lower = app.lower()

            # Direct open if known
            if app_lower in sites:
                webopen(sites[app_lower])
            else:
                # Fallback → Google search (always works)
                webopen(f"https://www.google.com/search?q={app}")

        except Exception as e:
            print("Browser Open Error:", e)

        return True

# ---------------- CLOSE APP ----------------
def CloseApp(app):
    try:
        if "chrome" not in app:
            close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

# ---------------- SYSTEM CONTROL ----------------
def System(command):
    actions = {
        "mute": "volume mute",
        "unmute": "volume mute",
        "volume up": "volume up",
        "volume down": "volume down"
    }

    if command in actions:
        keyboard.press_and_release(actions[command])

    return True

# ---------------- COMMAND EXECUTION ----------------
async def TranslateAndExecute(commands: list[str]):
    tasks = []

    for command in commands:
        try:
            if command.startswith("open "):
                tasks.append(asyncio.to_thread(OpenApp, command.removeprefix("open ")))

            elif command.startswith("close "):
                tasks.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))

            elif command.startswith("play "):
                tasks.append(asyncio.to_thread(PlayYoutube, command.removeprefix("play ")))

            elif command.startswith("content "):
                tasks.append(asyncio.to_thread(Content, command.removeprefix("content ")))

            elif command.startswith("google search "):
                tasks.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")))

            elif command.startswith("youtube search "):
                tasks.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))

            elif command.startswith("system "):
                tasks.append(asyncio.to_thread(System, command.removeprefix("system ")))

            else:
                print(f"No Function Found: {command}")

        except Exception as e:
            print("Command Error:", e)

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        yield result

# ---------------- AUTOMATION ----------------
async def Automation(commands: list[str]):
    async for _ in TranslateAndExecute(commands):
        pass
    return True
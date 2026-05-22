from serpapi import GoogleSearch as SerpAPI
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# -------------------- LOAD ENV --------------------
env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
SerpAPIKey = env_vars.get("SerpAPIKey")

client = Groq(api_key=GroqAPIKey)

# -------------------- SYSTEM PROMPT --------------------
System = f"""
You are {Assistantname}, an AI assistant.

You DO NOT have real-time data by default.
You MUST use the provided search results to answer queries.

Rules:
- Always use the given search data
- NEVER say "I don't have real-time access"
- Keep answers short and direct
- Reply only in English
"""

# -------------------- INIT STORAGE --------------------
if not os.path.exists("Data"):
    os.makedirs("Data")

try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open("Data/ChatLog.json", "w") as f:
        dump([], f)
    messages = []

# -------------------- SEARCH FUNCTION --------------------
def PerformSearch(query):
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SerpAPIKey
        }

        search = SerpAPI(params)
        results = search.get_dict()

        if "organic_results" not in results:
            return f"No search results found for '{query}'."

        Answer = f"Search results for '{query}':\n[start]\n"

        for result in results["organic_results"][:5]:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            Answer += f"{title}\n{snippet}\n\n"

        Answer += "[end]"
        return Answer

    except Exception as e:
        return f"Search Error: {e}"

# -------------------- CLEAN OUTPUT --------------------
def AnswerModifier(answer):
    lines = answer.split('\n')
    return '\n'.join([line for line in lines if line.strip()])

# -------------------- TIME INFO --------------------
def Information():
    now = datetime.datetime.now()
    return (f"Current Info:\n"
            f"Date: {now.strftime('%d %B %Y')}\n"
            f"Time: {now.strftime('%H:%M:%S')}")

# -------------------- MAIN ENGINE --------------------
def RealtimeSearchEngine(prompt):
    global messages

    # Load previous chat
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)

    messages.append({"role": "user", "content": prompt})

    # Get search data
    search_data = PerformSearch(prompt)

    # System + Search context
    system_messages = [
        {"role": "system", "content": System},
        {"role": "system", "content": f"Use this real-time data to answer:\n{search_data}"},
        {"role": "system", "content": Information()}
    ]

    # Generate response
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=system_messages + messages,
        temperature=0.3,
        max_tokens=1024,
        stream=True
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")

    messages.append({"role": "assistant", "content": Answer})

    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer)

# -------------------- RUN --------------------
if __name__ == "__main__":
    while True:
        user_input = input("Enter your query: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = RealtimeSearchEngine(user_input)
        print("\n" + response + "\n")
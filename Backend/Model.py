import cohere  #Import the cohere Library for AI services
from rich import print #Import the rich library to enhance terminal outputs 
from dotenv import dotenv_values #Import the dotenv library to load environment variables from a .env file
import os
# #Load environment variables from the .env file
# env_vars = dotenv_values(".env")

# #Retrive API key
# CohereApiKey = env_vars.get("KEY")

# #Create a Cohere client using the retrieved API key
# co = cohere.Client(api_key = CohereApiKey)



# 1. Get the path to the folder where Model.py is located (Backend folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Point to the .env file in the PARENT folder (JARVIS AI folder)
env_path = os.path.join(current_dir, "..", ".env")

# 3. Load environment variables from the specific path
env_vars = dotenv_values(env_path)

# 4. Retrieve API key using the EXACT name seen in your .env file screenshot
CohereApiKey = env_vars.get("CohereApiKey")

# 5. Check and initialize
if CohereApiKey is None:
    print(f"[bold red]❌ Error:[/bold red] Could not find 'CohereApiKey' in {env_path}")
else:
    # .strip() removes any accidental spaces from the .env file
    co = cohere.Client(api_key=CohereApiKey.strip())
    print("[bold green]✅ Cohere Client initialized successfully![/bold green]")

#define a list of recognized functions keywords for task categorization
funcs = {
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "remaindar"
}

messages = [] #Initialize an empty list to store conversation messages

#Define a preamble string that can be used to provide context or instructions for the AI model.
# preamble = """
# You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
# You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open application'.
# *** Do not answer any query, just decide what kind of query is given to you. ***
# -> Respond with 'general (query)' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any realtime data.
# -> Respond with 'realtime (query)' if a query can not be answered by a llm model (because they don't have realtime data) and requires search.
# -> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open notepad', etc.
# -> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc.
# -> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but only for music.
# -> Respond with 'generate image (image prompt)' if a query is requesting to generate a photo or image like 'generate image of a cat'.
# -> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down, etc. but if the query is asking for status.
# -> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything similar.
# -> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search.
# -> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search on youtube.
# *** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp'. ***
# *** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'. ***
# *** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
# """ 

preamble = """
You are a highly accurate Query Classification Model.

Your ONLY job is to classify the user query into one of the predefined categories.
DO NOT answer the query.

----------------------
CATEGORIES:

1. general (query)
- Casual conversation
- Opinions
- Greetings
- Simple chat
Examples:
"hello"
"how are you"
"do you like pizza"

2. realtime (query)
- Any factual question about people, places, current info
- Questions that typically require searching or updated knowledge
Examples:
"who is narendra modi"
"what is today's date"
"latest news about AI"
"weather in kolkata"

3. open (application/website)
Examples:
"open facebook"
"open youtube"
"open chrome and instagram"

4. close (application)
Examples:
"close chrome"
"close notepad"

5. play (song name)
Examples:
"play let her go"
"play afsanay"

6. generate image (prompt)
Examples:
"generate image of a cat"

7. system (task)
Examples:
"volume up"
"mute system"

8. content (topic)
Examples:
"write an essay on AI"
"generate python code for sorting"

9. google search (topic)
- Explicitly says search on google

10. youtube search (topic)
- Explicitly says search on youtube

11. remainder (task)
Examples:
"remind me to call mom at 5pm"

----------------------

RULES:

- If query is greeting or casual → general
- If query is asking INFORMATION about a person, place, or fact → realtime
- If query contains MULTIPLE tasks → split properly
Example:
"open facebook and instagram"
→ open facebook, open instagram

- If user says bye → exit

- If unsure → default to general

----------------------

OUTPUT FORMAT (STRICT):

Return ONLY:
category query

Examples:
general hello
realtime narendra modi
open facebook
open facebook, open instagram

DO NOT explain anything.
"""

ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi"},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome , open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date. remainder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general How Are You?"}
]

#Define main function on decision amking on queries
def FirstLayerDMM(prompt: str = "test"):

    #Add the user's query to the messages list with the role of "user"
    messages.append({"role": "user", "content": "f{prompt}"})

    #Create a streaming chat session with the cohere model
    stream = co.chat_stream(
        model = "command-r-plus-08-2024",
        #model = "command-r-plus", #specify the cohere model to use for generating responses
        message = prompt, #Pass the user's query as the message to the model
        temperature = 0.7, #set the creativity level of the model
        chat_history = ChatHistory, #Provide the conversation history to the model for context
        prompt_truncation = "OFF", #Disable prompt truncation to ensure the entire conversation history is considered by the model
        connectors = [], #No additional connectors are used
        preamble = preamble #Provide the preamble for additional context or instructions to the model

    )

    response = "" #Initialize an empty string to store the model's response

    for event in stream:
        if event.event_type == "text-generation" :
            response += event.text

    response = response.replace("\n", " ").split(",") #Clean up the response by replacing newlines with spaces and trimming whitespace

    response = [ i.strip() for i in response] #Trim whitespace from each part of the response

    temp = []

    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
    
    response = temp #Filter the response to include only recognized function keywords
    if "(query)" in response:
        newrespomse = FirstLayerDMM(prompt=prompt)
        return newrespomse
    else :
        return response
    
#Entry point for the script
if __name__ == "__main__":

    while True:
        print(FirstLayerDMM(input(">>> ")))

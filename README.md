# JARVIS AI 🤖

JARVIS AI is a personal desktop assistant designed to handle everything from real-time web searches to speech processing, automation, and image generation. Built with a robust **Python backend** and a modern, fluid **PyQt5 GUI frontend**, JARVIS brings a sci-fi inspired interface right to your desktop.

---

## 🛠️ Project Structure

Based on the project's architecture, the workspace is organized as follows:

```text
JARVIS AI/
├── .venv/                  # Virtual environment
├── Backend/                # Core AI logic and engine
│   ├── Automation.py       # Desktop & browser automation tasks
│   ├── Chatbot.py          # LLM core for conversation parsing
│   ├── ImageGeneration.py  # AI text-to-image pipeline
│   ├── Model.py            # Local or API model configurations
│   ├── RealtimeSearchEngi… # Live web scraping & search engine parsing
│   ├── SpeechToText.py     # Voice recognition pipeline (STT)
│   └── TextToSpeech.py     # Voice synthesis pipeline (TTS)
├── Data/                   # Local storage, memory caches, or assets
├── Frontend/               # GUI application source files
├── .env                    # Secure environment keys & API configurations
├── .gitignore              # Git exclusion files
├── Main.py                 # Application entry point
├── README.md               # Project documentation
└── Requirements.txt        # System dependencies
```
## 🚀 Features
* **🗣️ Advanced Speech Processing:**

  * **Speech-to-Text (STT):** High-accuracy voice recognition for hands-free commanding.

  * **Text-to-Speech (TTS):** Dynamic, fluid, and natural-sounding voice responses.

* **🧠 Intelligent Chatbot Engine:** Context-aware conversations driven by advanced language models.

* **🌐 Real-Time Search Engine Integration:** Fetches up-to-the-minute web answers to queries instantly.

* **🖼️ AI Image Generation:** Native generation of visual assets directly from textual prompts.

* **⚙️ System & Web Automation:** Automates routine desktop workflows, browser interactions, and tasks.

* **🎨 Dynamic PyQt5 Dashboard:** A modern UI layered with smooth custom animations, dynamic styling, and complex layout management.

## 📸 Demo & Screenshots

Here is a preview of the JARVIS AI dashboard in action:

![JARVIS AI Desktop Interface](https://github.com/Bittu169/personal-ai-assistant/blob/228cc86b383aa3a3d772cab6c02f61583fcf050b/Screenshot%202026-05-22%20191627.png)
![JARVIS AI Desktop Interface](Frontend/screenshots/demo.png)

## 💻 Tech Stack
**Backend:**
* **Python 3.x**
* Custom sub-modules for AI generation, web scraping, and automation.

**Frontend Framework (PyQt5):**

The interactive dashboard uses deep implementations of the following **PyQt5** modules:

* **QtWidgets:** Advanced layouts **(QGridLayout, QHBoxLayout, QVBoxLayout)**, stacked views **(QStackedWidget)**, custom frames, and input fields.

* **QtGui:** Rich styling, custom painting components **(QPainter)**, custom fonts, and animated GIF renderers **(QMovie)**.

* **QtCore:** Low-level system timers **(QTimer)**, event loops, and core core mechanics.

## ⚙️ Setup and Installation
**1. Clone the Repository**
```Bash
git clone [https://github.com/your-username/jarvis-ai.git](https://github.com/Bittu169/personal-ai-assistant.git)
cd jarvis-ai
```
**2. Set Up the Virtual Environment**
```Bash
# Create environment
python -m venv .venv

# Activate environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```
**3. Install Dependencies**
```Bash
pip install -r Requirements.txt
```
**4. Environment Variables**

Create a .env file in the root directory (as shown in the structure) and populate it with your respective API credentials:

```Code snippet
# Example Environment Layout
API_KEY="your_llm_or_generation_api_key"
SEARCH_ENGINE_ID="your_search_engine_identifier"
```
## 🏃‍♂️ Running the Assistant

To spin up the user interface and initialize the backend processing engines simultaneously, run the main initialization script:

```Bash
python Main.py
```

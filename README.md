# Voice-Controlled AI Agent

I built this project as part of my internship assignment at Mem0 AI. The idea was to create an agent that you can literally talk to — it listens to what you say, figures out what you want, and actually does it on your computer.

Took me a while to get everything working together but honestly learned a lot building this.

---

## What it does

You speak a command (or type it), and the agent:
- Converts your speech to text
- Understands what you're asking for
- Takes the actual action — creates files, writes code, summarizes text, or just chats with you
- Shows everything that happened in a clean UI

---

## How I built it

I kept the architecture simple — four files, each doing one job:

```
Your voice → stt.py → intent.py → tools.py → app.py (shows results)
```

**stt.py** — takes the audio file and sends it to Groq's Whisper model. Whisper converts it to text. That's it.

**intent.py** — takes that text and asks LLaMA 3.3 what the user wants. I prompt the model to reply only in JSON so I can easily extract things like the filename, programming language, etc.

**tools.py** — actually does the work based on what intent.py detected. Creates files, generates code, summarizes, or chats.

**app.py** — puts everything together in a Gradio UI so you can see what's happening at each step.

---

## Why I used Groq instead of running models locally

Honestly, my laptop can't run Whisper or LLaMA locally without it taking forever. Running Whisper on CPU takes like 30-60 seconds per request which makes the whole thing unusable.

Groq gives free API access and runs both models in under a second. So I used that. The code is written in a way that you could swap it out for Ollama or any local model by just changing a few lines.

---

## Tech stack

- **Python** — main language
- **Gradio** — for the UI, easiest way to build a web interface in pure Python
- **Groq API** — for both Whisper (speech to text) and LLaMA 3.3 (intent + responses)
- **python-dotenv** — to keep the API key out of the code

---

## Project structure

```
voice-agent/
├── app.py              # UI and main pipeline
├── stt.py              # Speech to text
├── intent.py           # Intent classification
├── tools.py            # File ops, code gen, summarize, chat
├── output/             # All generated files go here
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Abhayy-Raj/voice-agent.git
cd voice-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Groq API key

Sign up free at https://console.groq.com, go to API Keys, and create a new key.

### 5. Add your API key

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_key_here
```

### 6. Run it

```bash
python app.py
```

Open your browser at `http://127.0.0.1:7860`

---

## Supported commands

The agent understands four types of commands:

| What you say | What happens |
|---|---|
| "Create a file called notes.txt" | Creates an empty file in output/ |
| "Write a Python function for bubble sort" | Generates the code and saves it |
| "Summarize this: [your text here]" | Returns a short summary |
| "What is machine learning?" | Answers conversationally |

You can also just type the command instead of speaking if you prefer.

---

## Safety

All files created by the agent go into the `output/` folder only. I added a check in tools.py using `os.path.basename()` so there's no way for a command to create files outside that folder by accident.

---

## Things I'd improve with more time

- Add support for compound commands like "summarize this and save it to a file"
- Add a confirmation popup before executing file operations
- Try running it with a local Ollama model to remove the API dependency
- Add conversation memory so it remembers previous commands in the same session

---

## Challenges I ran into

The biggest headache was version conflicts between Gradio, gradio-client, and huggingface-hub. Took a while to figure out the right combination. Also the LLaMA model I was using (llama3-70b-8192) got decommissioned mid-development so had to switch to llama-3.3-70b-versatile.

Other than that, getting the JSON output from the LLM to be consistent was tricky. Sometimes the model would add extra text around the JSON. Solved it by being very explicit in the system prompt.

---

## Demo

[YouTube Demo Link] — will update this after recording

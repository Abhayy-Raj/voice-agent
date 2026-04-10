# 🎙️ Voice-Controlled Local AI Agent

A voice-controlled AI agent that transcribes audio, detects user intent, and executes local actions — all through a clean browser UI.

---

## 📌 What It Does

Speak a command → the agent:
1. **Transcribes** your audio to text (via Groq Whisper)
2. **Classifies the intent** (via LLaMA 3 on Groq)
3. **Executes the action** (creates files, writes code, summarizes, or chats)
4. **Shows everything** in a Gradio web UI

---

## 🏗️ Architecture

```
Audio Input (mic / file)
        │
        ▼
  ┌─────────────┐
  │   stt.py    │  Groq Whisper API → transcribed text
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │  intent.py  │  LLaMA 3 (Groq) → intent + metadata (JSON)
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │   tools.py  │  Executes: create_file / write_code / summarize / general_chat
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │   app.py    │  Gradio UI displays all results
  └─────────────┘
```

### Supported Intents

| Intent | What It Does |
|---|---|
| `create_file` | Creates an empty file in `output/` |
| `write_code` | Generates code with LLM and saves to `output/` |
| `summarize` | Summarizes provided text |
| `general_chat` | Answers questions conversationally |

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|---|---|---|
| UI | Gradio | Easiest Python-native web UI, no HTML/JS needed |
| Speech-to-Text | Groq Whisper API | Fast and accurate; local Whisper was too slow on CPU |
| LLM (Intent + Tools) | LLaMA 3 70B via Groq | Free, fast, strong reasoning ability |
| Language | Python 3.10+ | As required |

### ⚠️ Hardware Note — Why Groq Instead of Local Models

Running Whisper or LLaMA locally requires a GPU with at least 8–16 GB VRAM. Since this machine uses a CPU-only setup, running these models locally results in very slow inference (30–60 seconds per request). Groq provides free API access with near-instant responses (< 1 second), making it the practical choice. The architecture is identical — swapping to a local Ollama model requires only changing one line in each file.

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/AbhayyRaj/voice-agent.git
cd voice-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a free Groq API key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for free
3. Go to **API Keys** → Create a new key
4. Copy the key

### 5. Add your API key

```bash
# Copy the example file
cp .env.example .env

# Open .env and replace the placeholder with your actual key
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

### 6. Run the app

```bash
python app.py
```

Open your browser at: **http://localhost:7860**

---

## 💬 Example Commands to Try

| Say This | Expected Intent |
|---|---|
| "Create a file called notes.txt" | `create_file` |
| "Write a Python function for bubble sort and save it" | `write_code` |
| "Summarize this: Artificial intelligence is transforming industries..." | `summarize` |
| "What is machine learning?" | `general_chat` |

---

## 📁 Project Structure

```
voice-agent/
├── app.py              # Gradio UI + main pipeline
├── stt.py              # Speech-to-text (Groq Whisper)
├── intent.py           # Intent classification (LLaMA 3)
├── tools.py            # Tool execution (file ops, code gen, summarize, chat)
├── output/             # ← All generated files go here (auto-created)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .env                # Your actual API key (NOT committed to git)
├── .gitignore
└── README.md
```

---

## 🔒 Safety

- All file creation and code writing is **restricted to the `output/` folder**
- Path traversal attacks are blocked in `tools.py` via `os.path.basename()`
- The `.env` file is in `.gitignore` and will never be committed

---

## ✨ Bonus Features Implemented

- ✅ **Graceful degradation** — errors at any stage are caught and shown in the UI
- ✅ **Clean intent fallback** — unknown intents default to `general_chat`
- ✅ **Human-readable output** — all results shown with icons and clear labels

---

## 📄 License

MIT

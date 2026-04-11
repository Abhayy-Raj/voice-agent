# intent.py
# handles intent detection for the voice agent

import os
import json
from groq import Groq

SUPPORTED_INTENTS = ["create_file", "write_code", "summarize", "general_chat"]

INTENT_DESCRIPTIONS = {
    "create_file": "User wants to create a file or folder",
    "write_code": "User wants to generate and save code to a file",
    "summarize": "User wants to summarize a piece of text",
    "general_chat": "General question or conversation"
}

SYSTEM_PROMPT = """
You are an intent classifier for a voice-controlled AI agent.
Your job is to analyze a user command and return a structured JSON response.

Supported intents:
- create_file: User wants to create an empty file or folder
- write_code: User wants you to generate code and save it to a file
- summarize: User wants to summarize a piece of text they provided
- general_chat: Any general question, greeting, or conversation

You must respond ONLY with valid JSON in this exact format:
{
  "intent": "<one of the supported intents>",
  "filename": "<suggested filename if applicable, else null>",
  "language": "<programming language if write_code, else null>",
  "content": "<the text to summarize if summarize intent, else null>",
  "description": "<brief human-readable description of what you will do>"
}

Rules:
- For write_code, always suggest a filename with the correct extension (e.g., retry.py)
- For create_file, suggest a filename or folder name
- For summarize, extract the text content from the command
- For general_chat, set filename, language, and content to null
- Never include anything outside the JSON block
"""


def detect_intent(transcribed_text: str) -> dict:
    # TODO: maybe add retry logic here if groq times out
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcribed_text}
        ],
        temperature=0.2
    )

    try:
        result = json.loads(resp.choices[0].message.content.strip())
    except json.JSONDecodeError:
        return {"intent": "general_chat", "filename": None, "language": None, "content": None, "description": "fallback"}

    if result.get("intent") not in SUPPORTED_INTENTS:
        result["intent"] = "general_chat"

    return result
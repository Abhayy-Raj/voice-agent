"""
stt.py - Speech-to-Text Module
Uses Groq's Whisper API to transcribe audio files to text.
"""

import os
from groq import Groq


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file to text using Groq's Whisper model.

    Args:
        file_path: Path to the audio file (.wav or .mp3)

    Returns:
        Transcribed text as a string
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            response_format="text"
        )

    return transcription.strip()

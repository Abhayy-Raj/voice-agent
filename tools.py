"""
tools.py - Tool Execution Module
Handles all actions: file creation, code generation, summarization, and chat.
All file outputs are restricted to the output/ folder for safety.
"""

import os
from groq import Groq


# Safety: All generated files go here only
OUTPUT_DIR = "output"


def ensure_output_dir():
    """Create the output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def safe_path(filename: str) -> str:
    """
    Build a safe file path inside the output/ directory.
    Strips any path traversal attempts (e.g., ../../etc).
    """
    # Take only the basename to prevent directory traversal
    safe_name = os.path.basename(filename)
    return os.path.join(OUTPUT_DIR, safe_name)


def create_file(filename: str) -> dict:
    """
    Create an empty file inside the output/ folder.

    Args:
        filename: Name of the file to create

    Returns:
        A dict with keys: success (bool), path (str), message (str)
    """
    ensure_output_dir()

    if not filename:
        return {"success": False, "path": None, "message": "No filename provided."}

    file_path = safe_path(filename)

    # Don't overwrite if file already exists
    if os.path.exists(file_path):
        return {
            "success": False,
            "path": file_path,
            "message": f"File '{file_path}' already exists."
        }

    with open(file_path, "w") as f:
        f.write("")  # Create empty file

    return {
        "success": True,
        "path": file_path,
        "message": f"File '{file_path}' created successfully."
    }


def write_code(filename: str, language: str, user_command: str) -> dict:
    """
    Generate code using LLM and write it to a file in output/.

    Args:
        filename:     Target filename (e.g., retry.py)
        language:     Programming language (e.g., Python)
        user_command: The original user instruction

    Returns:
        A dict with keys: success (bool), path (str), code (str), message (str)
    """
    ensure_output_dir()

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
Write clean, well-commented {language} code based on this request:
"{user_command}"

Rules:
- Only output the raw code, no markdown, no backticks, no explanation
- Add docstrings and inline comments to explain the logic
- Make the code production-ready and readable
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    generated_code = response.choices[0].message.content.strip()

    # Save to output folder
    if not filename:
        filename = f"generated_code.{_get_extension(language)}"

    file_path = safe_path(filename)

    with open(file_path, "w") as f:
        f.write(generated_code)

    return {
        "success": True,
        "path": file_path,
        "code": generated_code,
        "message": f"Code written to '{file_path}' successfully."
    }


def summarize_text(text: str) -> dict:
    """
    Summarize the provided text using the LLM.

    Args:
        text: The text content to summarize

    Returns:
        A dict with keys: success (bool), summary (str), message (str)
    """
    if not text:
        return {"success": False, "summary": None, "message": "No text provided to summarize."}

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
Summarize the following text clearly and concisely in 3-5 sentences:

\"\"\"{text}\"\"\"

Return only the summary, no preamble.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    summary = response.choices[0].message.content.strip()

    return {
        "success": True,
        "summary": summary,
        "message": "Text summarized successfully."
    }


def general_chat(user_message: str) -> dict:
    """
    Handle general conversation with the AI.

    Args:
        user_message: The user's message or question

    Returns:
        A dict with keys: success (bool), response (str), message (str)
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, friendly voice assistant. Keep responses concise and conversational."
            },
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content.strip()

    return {
        "success": True,
        "response": reply,
        "message": "Response generated."
    }


def _get_extension(language: str) -> str:
    """Map language name to file extension."""
    extensions = {
        "python":     "py",
        "javascript": "js",
        "typescript": "ts",
        "java":       "java",
        "c":          "c",
        "c++":        "cpp",
        "go":         "go",
        "rust":       "rs",
        "html":       "html",
        "css":        "css",
        "bash":       "sh",
    }
    return extensions.get(language.lower(), "txt") if language else "txt"

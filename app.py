import os
import gradio as gr
from dotenv import load_dotenv

from stt import transcribe_audio
from intent import detect_intent
from tools import create_file, write_code, summarize_text, general_chat

# Load environment variables from .env file
load_dotenv()


#  INTENT ICONS 
INTENT_ICONS = {
    "create_file":  "📁",
    "write_code":   "💻",
    "summarize":    "📝",
    "general_chat": "💬"
}

INTENT_LABELS = {
    "create_file":  "Create File",
    "write_code":   "Write Code",
    "summarize":    "Summarize Text",
    "general_chat": "General Chat"
}


# CORE PIPELINE

def run_pipeline(audio_path: str, text_command: str) -> tuple:
    """
    Full pipeline: audio OR text → transcription → intent → tool execution.
    """

    # ── Decide input source ─────────────────────────────────────────────
    # If user typed something, use that. Otherwise use audio.
    if text_command and text_command.strip():
        transcription = text_command.strip()

    elif audio_path is not None:
        try:
            transcription = transcribe_audio(audio_path)
        except Exception as e:
            return f" Transcription failed: {str(e)}", "", "", ""

        if not transcription:
            return " Could not understand the audio. Please try again.", "", "", ""

    else:
        return "Please record audio or type a command.", "", "", ""

    #Step 2: Detect Intent 
    try:
        intent_data = detect_intent(transcription)
    except Exception as e:
        return transcription, f"Intent detection failed: {str(e)}", "", ""

    intent        = intent_data.get("intent", "general_chat")
    filename      = intent_data.get("filename")
    language      = intent_data.get("language")
    content       = intent_data.get("content")
    description   = intent_data.get("description", "")

    icon  = INTENT_ICONS.get(intent, "🤖")
    label = INTENT_LABELS.get(intent, intent)
    intent_display = f"{icon} {label}\n\n{description}"

    # ── Step 3: Execute Tool ────────────────────────────────────────────
    action_taken = ""
    final_output = ""

    if intent == "create_file":
        result = create_file(filename or "new_file.txt")
        action_taken = f"📁 Creating file: `{filename}`"
        final_output = result["message"]

    elif intent == "write_code":
        result = write_code(filename or "output.py", language or "Python", transcription)
        action_taken = f"💻 Generating {language or 'Python'} code → `{result.get('path', '')}`"
        if result["success"]:
            final_output = f"✅ {result['message']}\n\n```{language or 'python'}\n{result['code']}\n```"
        else:
            final_output = f"❌ {result['message']}"

    elif intent == "summarize":
        text_to_summarize = content or transcription
        result = summarize_text(text_to_summarize)
        action_taken = "📝 Summarizing provided text"
        final_output = result.get("summary", result["message"])

    elif intent == "general_chat":
        result = general_chat(transcription)
        action_taken = "💬 Generating conversational response"
        final_output = result.get("response", result["message"])

    else:
        action_taken = "⚠️ Unknown intent"
        final_output = "Sorry, I did not understand that command. Please try again."

    return transcription, intent_display, action_taken, final_output


#   GRADIO UI 

def build_ui():
    """Build and return the Gradio interface."""

    custom_css = """
    /* ── Base & Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    body, .gradio-container {
        font-family: 'DM Sans', sans-serif !important;
        background: #0a0a0f !important;
        color: #e8e8f0 !important;
    }

    /* ── Header ── */
    .app-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
        border-bottom: 1px solid #1e1e2e;
        margin-bottom: 1.5rem;
    }
    .app-header h1 {
        font-family: 'Space Mono', monospace !important;
        font-size: 2rem;
        color: #a78bfa;
        letter-spacing: -0.03em;
        margin: 0;
    }
    .app-header p {
        color: #6b6b8a;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }

    /* ── Panels ── */
    .panel-label {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        color: #a78bfa;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* ── Input Section ── */
    .input-section {
        background: #111118;
        border: 1px solid #1e1e2e;
        border-radius: 12px;
        padding: 1.5rem;
    }

    /* ── Output Cards ── */
    .output-card {
        background: #111118;
        border: 1px solid #1e1e2e;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
    }

    /* ── Gradio textbox override ── */
    .gr-textbox textarea, .gr-textbox input {
        background: #0d0d14 !important;
        border: 1px solid #2a2a3e !important;
        color: #e8e8f0 !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Button ── */
    .gr-button-primary {
        background: linear-gradient(135deg, #7c3aed, #a78bfa) !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.05em !important;
        color: white !important;
        padding: 0.7rem 1.5rem !important;
    }
    .gr-button-primary:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }

    /* ── Audio component ── */
    .gr-audio {
        background: #0d0d14 !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
    }
    """

    with gr.Blocks(
        title="Voice AI Agent"
    ) as demo:

        # Header
        gr.HTML("""
        <div class="app-header">
            <h1>🎙️ Voice AI Agent</h1>
            <p>Speak a command — the agent will transcribe, understand, and act.</p>
        </div>
        """)

        # Input Row
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML('<div class="panel-label">Audio Input</div>')
                audio_input = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label=""
                )

        with gr.Row():
            with gr.Column(scale=4):
                gr.HTML('<div class="panel-label">✍️ Or Type a Command</div>')
                text_input = gr.Textbox(
                    label="",
                    placeholder='e.g. "Create a file called notes.txt" or "What is machine learning?"',
                    lines=1
                )
            with gr.Column(scale=1):
                run_btn = gr.Button("▶  Run Agent", variant="primary")

        #Output Row
        gr.HTML('<div style="height: 1rem;"></div>')

        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML('<div class="panel-label">Transcription</div>')
                transcription_out = gr.Textbox(
                    label="",
                    lines=3,
                    interactive=False,
                    placeholder="Transcribed text will appear here..."
                )

            with gr.Column(scale=1):
                gr.HTML('<div class="panel-label">Detected Intent</div>')
                intent_out = gr.Textbox(
                    label="",
                    lines=3,
                    interactive=False,
                    placeholder="Detected intent will appear here..."
                )

        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML('<div class="panel-label">Action Taken</div>')
                action_out = gr.Textbox(
                    label="",
                    lines=2,
                    interactive=False,
                    placeholder="Action details will appear here..."
                )

            with gr.Column(scale=1):
                gr.HTML('<div class="panel-label">Final Output</div>')
                output_out = gr.Markdown(
                    value="",
                )

       
        

        #Wire up the button 
        run_btn.click(
            fn=run_pipeline,
            inputs=[audio_input, text_input],
            outputs=[transcription_out, intent_out, action_out, output_out]
        )


    return demo


#ENTRY POINT
if __name__ == "__main__":
    # Sanity check for API key
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️  Warning: GROQ_API_KEY not found in environment. Please add it to your .env file.")

    demo = build_ui()
    demo.launch(
        server_name="127.0.0.1",
    server_port=7860,
    share=False
    )

"""
utils/session.py
Manages Streamlit session state for TalentScout chatbot.
"""

import streamlit as st

# ─── Stages ─────────────────────────────────────────────────────────────────
STAGES = [
    {"id": "greeting",    "label": "Greeting",    "icon": "👋"},
    {"id": "basic_info",  "label": "Basic Info",  "icon": "📋"},
    {"id": "tech_stack",  "label": "Tech Stack",  "icon": "💻"},
    {"id": "assessment",  "label": "Assessment",  "icon": "🧪"},
    {"id": "complete",    "label": "Complete",    "icon": "✅"},
]

# ─── Exit Keywords ───────────────────────────────────────────────────────────
EXIT_KEYWORDS = {
    "bye", "goodbye", "exit", "quit", "end", "stop",
    "see you", "farewell", "done", "finish", "that's all",
}


def init_session():
    """Initialise all session-state keys with defaults."""
    defaults = {
        "messages":        [],          # [{"role": "user"|"assistant", "content": str}]
        "api_messages":    [],          # messages sent to Anthropic API (may include META)
        "stage":           0,           # current pipeline stage index
        "candidate":       {            # collected candidate profile
            "name":        "",
            "email":       "",
            "phone":       "",
            "location":    "",
            "experience":  "",
            "position":    "",
            "tech_stack":  "",
        },
        "ended":           False,       # conversation finished flag
        "initialized":     False,       # first greeting sent?
        "chips":           [],          # quick-reply suggestions
        "tech_questions":  [],          # generated technical questions
        "answers":         [],          # candidate answers to tech questions
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_session():
    """Clear all session state to restart the conversation."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session()


def is_exit_intent(text: str) -> bool:
    """Return True if the user's message contains an exit keyword."""
    lowered = text.lower().strip().rstrip(".,!?")
    words = set(lowered.split())
    return bool(words & EXIT_KEYWORDS) or lowered in EXIT_KEYWORDS

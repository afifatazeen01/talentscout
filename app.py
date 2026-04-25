"""
TalentScout - AI Hiring Assistant
Main Streamlit application entry point.
"""

import streamlit as st
from utils.session import init_session
from utils.ui import render_sidebar, render_chat, render_input_area
from utils.styles import inject_css

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentScout | AI Hiring Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_session()

# ─── Layout ─────────────────────────────────────────────────────────────────
sidebar_col, chat_col = st.columns([1, 2.4])

with sidebar_col:
    render_sidebar()

with chat_col:
    render_chat()
    render_input_area()

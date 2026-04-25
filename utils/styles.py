"""
utils/styles.py
Injects custom CSS into the Streamlit app for a polished, dark-themed UI.
"""

import streamlit as st


def inject_css():
    st.markdown(
        """
<style>
/* ── Google Fonts ────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

/* ── Root palette ────────────────────────────────────── */
:root {
    --bg:        #0d0f14;
    --surface:   #161a23;
    --surface2:  #1e2330;
    --border:    #2a3040;
    --accent:    #4f7cff;
    --accent2:   #7c5cfc;
    --gold:      #f0b429;
    --text:      #e8ecf4;
    --muted:     #8892a4;
    --success:   #2ed47a;
    --danger:    #ff5a5f;
    --radius:    14px;
}

/* ── Global resets ───────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ───────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1.5rem 0 1.5rem !important; max-width: 100% !important; }

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    padding: 1rem !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Chat messages ───────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.25rem 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"] .stMarkdown,
.user-bubble {
    background: linear-gradient(135deg, #4f7cff, #7c5cfc) !important;
    color: #fff !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 0.75rem 1rem !important;
    max-width: 78% !important;
    margin-left: auto !important;
    font-size: 0.92rem !important;
}

/* Assistant bubble */
.bot-bubble {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 0.75rem 1rem !important;
    max-width: 82% !important;
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
}

/* ── Input box ───────────────────────────────────────── */
[data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(79,124,255,0.15) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    background: transparent !important;
}

/* ── Buttons (chips) ─────────────────────────────────── */
.stButton > button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    padding: 4px 14px !important;
    transition: all 0.2s !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(79,124,255,0.06) !important;
}

/* Primary send button */
.primary-btn > button {
    background: linear-gradient(135deg, #4f7cff, #7c5cfc) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
}

/* ── Stage progress bar ──────────────────────────────── */
.stage-bar {
    display: flex;
    gap: 6px;
    align-items: center;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.stage-pill {
    flex: 1;
    height: 5px;
    border-radius: 3px;
    background: var(--surface2);
    transition: background 0.4s;
}
.stage-pill.done   { background: var(--success); }
.stage-pill.active { background: var(--accent); }

/* ── Profile card ────────────────────────────────────── */
.profile-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 1rem;
    font-size: 0.82rem;
}
.profile-card h4 {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted);
    margin-bottom: 0.7rem;
}
.profile-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.8rem;
}
.profile-row:last-child { border-bottom: none; }
.p-label { color: var(--muted); }
.p-value { color: var(--text); font-weight: 500; text-align: right; max-width: 60%; }

/* ── Notice / alert ──────────────────────────────────── */
.notice {
    background: rgba(240,180,41,0.08);
    border: 1px solid rgba(240,180,41,0.25);
    border-radius: 10px;
    padding: 0.65rem 0.9rem;
    font-size: 0.75rem;
    color: #f0b429;
    margin-top: 0.5rem;
}

/* ── Status dot ──────────────────────────────────────── */
.status-online {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 6px var(--success);
    margin-right: 6px;
}

/* ── Dividers ────────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Metric ──────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface2);
    border-radius: var(--radius);
    padding: 0.75rem 1rem;
    border: 1px solid var(--border);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.7rem !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-size: 1.4rem !important; }

/* ── Spinner ─────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Success / end banner ────────────────────────────── */
.end-banner {
    background: linear-gradient(135deg, rgba(46,212,122,0.1), rgba(79,124,255,0.1));
    border: 1px solid var(--success);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
    margin-top: 1rem;
}
.end-banner h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--success);
    margin-bottom: 0.5rem;
}
</style>
""",
        unsafe_allow_html=True,
    )

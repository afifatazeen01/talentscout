"""
utils/ui.py
Rendering functions for sidebar, chat messages, and input area.
Uses Groq API (groq_api.py) instead of Anthropic.
"""

import streamlit as st
from utils.session import STAGES, reset_session, is_exit_intent
from utils.groq_api import chat


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _stage_bar(current: int):
    pills_html = '<div class="stage-bar">'
    for i in range(len(STAGES)):
        cls = "done" if i < current else ("active" if i == current else "")
        pills_html += f'<div class="stage-pill {cls}" title="{STAGES[i]["label"]}"></div>'
    pills_html += "</div>"
    st.markdown(pills_html, unsafe_allow_html=True)


def _profile_card(candidate: dict):
    filled = {k: v for k, v in candidate.items() if v}
    if not filled:
        st.markdown(
            '<p style="color:var(--muted);font-size:0.8rem;">Profile will appear as you share your details.</p>',
            unsafe_allow_html=True,
        )
        return

    labels = {
        "name": "Full Name", "email": "Email", "phone": "Phone",
        "location": "Location", "experience": "Experience",
        "position": "Desired Role", "tech_stack": "Tech Stack",
    }
    rows = "".join(
        f'<div class="profile-row">'
        f'<span class="p-label">{labels.get(k, k)}</span>'
        f'<span class="p-value">{v}</span></div>'
        for k, v in filled.items()
    )
    st.markdown(
        f'<div class="profile-card"><h4>Candidate Profile</h4>{rows}</div>',
        unsafe_allow_html=True,
    )


# ─── Sidebar ──────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        # Branding
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:1.2rem">
                <div style="font-size:2rem">🎯</div>
                <div>
                    <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;line-height:1">TalentScout</div>
                    <div style="font-size:0.68rem;letter-spacing:1px;color:var(--muted);text-transform:uppercase">AI Hiring Assistant</div>
                </div>
            </div>
            <div style="font-size:0.75rem;color:var(--muted);margin-bottom:1rem">
                <span class="status-online"></span>Alex is online &nbsp;·&nbsp;
                <span style="color:#f0b429;font-size:0.68rem">⚡ Groq LLaMA-3.3-70B</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Stage label + progress bar
        st.markdown(
            f'<div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:6px">'
            f'Stage {st.session_state.stage + 1} of {len(STAGES)} — '
            f'{STAGES[st.session_state.stage]["icon"]} {STAGES[st.session_state.stage]["label"]}'
            f'</div>',
            unsafe_allow_html=True,
        )
        _stage_bar(st.session_state.stage)

        # Stage checklist
        for i, s in enumerate(STAGES):
            icon = "✅" if i < st.session_state.stage else ("🔵" if i == st.session_state.stage else "⬜")
            color = "var(--text)" if i == st.session_state.stage else "var(--muted)"
            st.markdown(
                f'<div style="font-size:0.8rem;padding:3px 0;color:{color}">{icon} {s["label"]}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<hr>", unsafe_allow_html=True)

        # Live profile card
        st.markdown(
            '<div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:8px">Live Profile</div>',
            unsafe_allow_html=True,
        )
        _profile_card(st.session_state.candidate)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Stats
        filled_count = sum(1 for v in st.session_state.candidate.values() if v)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Fields", f"{filled_count}/7")
        with col2:
            st.metric("Messages", len(st.session_state.messages))

        st.markdown("<hr>", unsafe_allow_html=True)

        # Privacy notice
        st.markdown(
            '<div class="notice">🔒 Data handled per GDPR standards. Not stored permanently.</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔄 Start New Session", use_container_width=True):
            reset_session()
            st.rerun()


# ─── Chat Area ────────────────────────────────────────────────────────────────

def render_chat():
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding-bottom:1rem;
             border-bottom:1px solid var(--border);margin-bottom:1rem">
            <span style="font-size:1.4rem">💬</span>
            <div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.2rem">Screening Interview</div>
                <div style="font-size:0.72rem;color:var(--muted)">Powered by Groq · LLaMA-3.3-70B · TalentScout</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Auto-greet on first load
    if not st.session_state.initialized:
        with st.spinner("Alex is joining…"):
            text, meta = chat("START_SCREENING_SESSION")
        _apply_meta(meta)
        st.session_state.messages.append({"role": "assistant", "content": text})
        st.session_state.initialized = True
        st.rerun()

    # Render message history
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="🎯"):
                st.markdown(
                    f'<div class="bot-bubble">{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])

    # End banner
    if st.session_state.ended:
        st.markdown(
            """
            <div class="end-banner">
                <h2>Screening Complete ✅</h2>
                <p style="color:var(--muted);font-size:0.88rem">
                    Thank you for your time! Our hiring team will review your profile
                    and reach out within <strong>3–5 business days</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─── Input Area ───────────────────────────────────────────────────────────────

def render_input_area():
    if st.session_state.ended:
        return

    chips = st.session_state.get("chips", [])
    if chips:
        st.markdown(
            '<div style="font-size:0.7rem;color:var(--muted);margin-bottom:4px">Quick replies:</div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(len(chips))
        for i, chip in enumerate(chips):
            with cols[i]:
                if st.button(chip, key=f"chip_{i}_{chip}"):
                    _handle_user_input(chip)
                    st.rerun()

    user_input = st.chat_input("Type your message…", key="chat_input")
    if user_input:
        _handle_user_input(user_input)
        st.rerun()


# ─── Core handler ─────────────────────────────────────────────────────────────

def _handle_user_input(text: str):
    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.chips = []

    assistant_text, meta = chat(text)

    if is_exit_intent(text):
        meta["ended"] = True

    _apply_meta(meta)
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})


def _apply_meta(meta: dict):
    if "stage" in meta:
        st.session_state.stage = min(int(meta["stage"]), len(STAGES) - 1)
    if "collected" in meta:
        for k, v in meta["collected"].items():
            if v and k in st.session_state.candidate:
                st.session_state.candidate[k] = v
    if "ended" in meta:
        st.session_state.ended = bool(meta["ended"])
    if "chips" in meta:
        st.session_state.chips = meta.get("chips", [])

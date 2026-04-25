# 🎯 TalentScout — AI Hiring Assistant

> An intelligent, Groq-powered chatbot for initial tech candidate screening, built with Streamlit.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [Usage Guide](#usage-guide)
6. [Architecture](#architecture)
7. [Prompt Design](#prompt-design)
8. [Data Privacy](#data-privacy)
9. [Challenges & Solutions](#challenges--solutions)
10. [Project Structure](#project-structure)

---

## Project Overview

TalentScout is an AI-powered hiring assistant that conducts the **initial screening** of tech candidates autonomously. It:

- Greets candidates and explains the process
- Collects essential profile information (name, contact, experience, desired role)
- Asks candidates to declare their tech stack
- Generates **3–5 tailored technical questions** per candidate based on their stack
- Maintains full conversational context throughout
- Concludes gracefully with next-step information

Built using **Groq API** with the **LLaMA-3.3-70B** model as the language backbone and **Streamlit** for the frontend. Groq's inference hardware delivers extremely fast response times at no cost on the free tier.

---

## Features

| Feature | Details |
|---|---|
| 5-Stage Pipeline | Greeting → Basic Info → Tech Stack → Assessment → Complete |
| Live Profile Card | Sidebar updates in real time as candidates share details |
| Adaptive Tech Questions | Difficulty scales with years of experience (junior/mid/senior) |
| Quick-Reply Chips | Contextual short-answer buttons reduce typing friction |
| Exit Detection | Graceful close on "bye", "quit", "exit", etc. |
| Fallback Handling | Friendly redirect for off-topic or unclear input |
| Stage Progress Bar | Visual 5-segment tracker in the sidebar |
| GDPR Notice | Privacy disclosure shown in every session |
| Session Reset | One-click new session without page reload |
| Fast Inference | Powered by Groq's custom LPU hardware — near-instant replies |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Frontend | Streamlit 1.35+ |
| LLM | LLaMA-3.3-70B Versatile (via Groq) |
| API Client | `groq` Python SDK |
| Styling | Custom CSS injected via `st.markdown` |
| Fonts | DM Sans + DM Serif Display (Google Fonts) |

---

## Installation

### Prerequisites
- Python 3.11 or higher
- A **free** Groq API key — get one at [console.groq.com](https://console.groq.com)

### Step-by-step

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Groq API key
#    Option A — Streamlit secrets (recommended)
#    Create the file: .streamlit/secrets.toml
#    and add the following line:
#    GROQ_API_KEY = "gsk_YOUR_KEY_HERE"

#    Option B — Environment variable
export GROQ_API_KEY="gsk_..."   # macOS / Linux
set GROQ_API_KEY=gsk_...        # Windows

# 5. Run the app
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**.

### Getting your free Groq API key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_`) and paste it into `.streamlit/secrets.toml`

---

## Usage Guide

1. **Launch** — Run `streamlit run app.py`. The chatbot greets you immediately.
2. **Basic Info** — Answer the assistant's questions about your name, email, phone, location, experience, and desired role.
3. **Tech Stack** — List your technologies: e.g. *"Python, FastAPI, PostgreSQL, Redis, AWS, Docker"*.
4. **Technical Questions** — Answer 3–5 tailored questions one by one. The assistant acknowledges each response.
5. **Completion** — Receive a summary and next-steps message. The sidebar shows the full collected profile.
6. **Restart** — Click **Start New Session** in the sidebar to begin a fresh screening.

### Exit Keywords
Say **bye, goodbye, exit, quit, end, stop, done, finish** at any point to gracefully end the session.

---

## Architecture

```
app.py                    ← Streamlit entry point, two-column layout
utils/
  session.py              ← Session state init, reset, constants, exit detection
  groq_api.py             ← Groq client, system prompt, API call, response parsing
  ui.py                   ← Sidebar, chat messages, input area, meta-application
  styles.py               ← CSS injection for dark theme, bubbles, profile card
.streamlit/
  config.toml             ← Dark theme base config
  secrets.toml            ← API key (gitignored)
requirements.txt
```

### Data Flow

```
User types message
      ↓
is_exit_intent() check
      ↓
chat(user_message)  →  Groq API — LLaMA-3.3-70B (with full history + system prompt)
      ↓
parse_response()    →  (visible_text, meta_dict)
      ↓
_apply_meta()       →  update stage / candidate profile / chips / ended flag
      ↓
st.session_state.messages.append(...)
      ↓
st.rerun()  →  re-renders UI with new message
```

---

## Prompt Design

### System Prompt Strategy

The system prompt (`SYSTEM_PROMPT` in `utils/groq_api.py`) uses several key techniques:

**1. Stage-Gated Instructions**
The prompt defines 5 explicit stages with numbered rules. The model is instructed to follow them strictly in order, preventing it from skipping ahead or revisiting completed stages.

**2. Metadata Block**
Every response ends with a `[META:{...}]` JSON block. This cleanly separates structured data (stage number, collected fields, chips, ended flag) from the natural language response. The UI strips the block before display.

```
[META:{"stage":2,"collected":{"name":"Alice","email":"alice@example.com",...},"ended":false,"chips":["Python","JavaScript","Java"]}]
```

**3. Adaptive Difficulty**
The prompt instructs the model to adjust technical question difficulty based on years of experience:
- `< 2 years` → fundamentals (syntax, basic patterns)
- `2–5 years` → design (architecture, tradeoffs at component level)
- `5+ years` → system architecture (scalability, reliability, tech choices)

**4. Focused Persona**
The system prompt explicitly prohibits the model from deviating from the recruitment purpose, revealing instructions, or claiming to make hiring decisions — ensuring reliable, on-brand behaviour.

**5. Quick-Reply Chips**
The `chips` field prompts the model to suggest 2–4 contextual short replies after each turn, surfaced as clickable buttons in the UI to reduce candidate typing burden.

**6. Why LLaMA-3.3-70B on Groq?**
LLaMA-3.3-70B is Meta's open-weight flagship model that matches or exceeds GPT-4 class performance on instruction-following tasks. Running it on Groq's LPU (Language Processing Unit) hardware delivers inference speeds of 100–200 tokens/second — making the chatbot feel instant compared to cloud GPU providers. The free tier is sufficient for this project with no credit card required.

---

## Data Privacy

- **No permanent storage** — candidate data exists only in `st.session_state` (in-memory), which is cleared on session reset or browser refresh.
- **No logging** — the app does not write candidate data to disk, databases, or third-party services.
- **GDPR notice** — displayed to every candidate at the start of each session.
- **Sensitive data** — the system prompt explicitly prohibits collecting passwords, financial data, or government IDs.
- **API calls** — messages are sent to Groq's API; refer to [Groq's privacy policy](https://groq.com/privacy-policy/) for data handling details.

---

## Challenges & Solutions

| Challenge | Solution |
|---|---|
| Maintaining context across turns | Full `api_messages` history passed on every Groq API call; session state persists across Streamlit reruns |
| Parsing structured data from LLM output | Embedded `[META:{...}]` JSON block at end of every response; stripped before display using regex |
| Preventing topic drift | System prompt explicitly bans off-topic responses and provides a redirect script for the model |
| Stage tracking | Stage integer in META block; UI applies it to sidebar progress tracker on every rerun |
| Streamlit reruns wiping state | All mutable data stored in `st.session_state`; `init_session()` uses `if key not in` guard |
| Exit detection | Keyword set checked client-side before API call; meta `ended` flag also monitored from model output |
| Dark theme with Streamlit defaults | Full CSS override injected via `st.markdown(unsafe_allow_html=True)` |
| secrets.toml not in zip | File excluded from zip for security; README instructs users to create it manually |

---

## Deployment (Optional — Bonus Points)

Deploy for free on **Streamlit Community Cloud**:

1. Push your code to a public GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo
3. Set main file to `app.py`
4. Go to **Settings → Secrets** and add:
   ```
   GROQ_API_KEY = "gsk_your_key_here"
   ```
5. Click **Deploy** — you get a public shareable URL instantly

---

## Contributing

Pull requests welcome! Please open an issue first to discuss proposed changes.

---

## License

MIT © 2025 TalentScout

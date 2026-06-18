# SPEC.md — AI Resume Critique App

> **Status:** Pre-implementation specification  
> **Last updated:** 2026-06-13  
> **Skill level:** Beginner-friendly

---

## 1. Project Overview

A Streamlit web app that lets a user paste their resume, enter a target job role, and optionally paste a job description. On clicking a button, the app sends the inputs to the Anthropic Claude API and returns a structured, five-section critique. The user can then download the critique as a Markdown file.

This project is designed as a portfolio piece: the code should be simple, well-commented, and easy to understand by a beginner or a hiring manager reading it on GitHub.

---

## 2. Goals

| Goal | Detail |
|------|--------|
| **Functional** | Working resume critique powered by Claude |
| **Beginner-readable** | Every non-obvious line has a comment explaining *why*, not just *what* |
| **GitHub-ready** | Clean repo structure, `.gitignore`, `.env.example`, `README.md` |
| **Deployable** | Works locally via `.env` and on Streamlit Cloud via `st.secrets` with no code changes |
| **Privacy-aware** | User is informed before submission that their text is sent to a third-party API |

---

## 3. Tech Stack

| Tool | Version / Notes |
|------|----------------|
| Python | 3.10+ |
| Streamlit | Latest stable (`streamlit`) |
| Anthropic SDK | Latest stable (`anthropic`) |
| python-dotenv | Latest stable (`python-dotenv`) |
| Claude model | `claude-sonnet-4-6` (good balance of quality and cost) |

---

## 4. Project File Structure

```
resume-critiquer/
│
├── app.py                  # Main Streamlit application (all UI + logic)
├── prompt.py               # Builds the prompt string sent to Claude
│
├── requirements.txt        # All pip dependencies
├── .env                    # Local API key — NOT committed to Git
├── .env.example            # Safe template to commit — no real keys
├── .gitignore              # Excludes .env, __pycache__, etc.
│
├── SPEC.md                 # This file
└── README.md               # Setup instructions and project description
```

**Why two files (`app.py` + `prompt.py`)?**  
Separating the prompt into its own file keeps `app.py` focused on UI, and makes the prompt easy to find, read, and improve later — a good habit even for small projects.

---

## 5. User Interface

### 5a. Layout (single page, top to bottom)

```
┌─────────────────────────────────────────────────┐
│  🧠  AI Resume Critiquer                         │  ← st.title
│  Get structured feedback on your resume          │  ← st.caption
├─────────────────────────────────────────────────┤
│  ⚠️  Privacy notice (collapsed by default)       │  ← st.expander
├─────────────────────────────────────────────────┤
│  Target Role *                                   │  ← st.text_input
│  [ Software Engineer                          ]  │
├─────────────────────────────────────────────────┤
│  Your Resume *                                   │  ← st.text_area (tall)
│  [ Paste your resume here...                  ]  │
│  [                                            ]  │
├─────────────────────────────────────────────────┤
│  Job Description (optional)                      │  ← st.text_area (shorter)
│  [ Paste the job posting here...             ]   │
├─────────────────────────────────────────────────┤
│  [ 🔍 Analyse My Resume ]                        │  ← st.button (primary)
├─────────────────────────────────────────────────┤
│  ── Critique Results ──                          │  ← st.divider + st.subheader
│  (rendered Markdown from Claude)                 │  ← st.markdown
│                                                  │
│  [ ⬇ Download as Markdown ]                      │  ← st.download_button
└─────────────────────────────────────────────────┘
```

### 5b. Privacy Notice (inside expander, collapsed by default)

> **Your data & privacy**  
> When you click "Analyse My Resume", the text you enter is sent to Anthropic's API to generate your critique. Anthropic's standard [usage policies](https://www.anthropic.com/legal/usage-policy) apply. Do not include sensitive personal information such as your home address, national ID numbers, or financial details.

### 5c. Validation Rules

| Condition | Behaviour |
|-----------|-----------|
| Role field is empty | `st.warning("Please enter a target role.")` — do not call API |
| Resume field is empty | `st.warning("Please paste your resume text.")` — do not call API |
| Resume is fewer than 50 characters | `st.warning("Your resume seems too short. Please paste the full text.")` |
| Both fields valid | Show `st.spinner("Analysing your resume...")` while calling API |

---

## 6. Critique Output Format

Claude is instructed to return **exactly** the following five-section Markdown structure. This makes the output predictable and easy to render.

```markdown
## 📋 Overall Summary & Score

**Score: X / 10**

[2–3 sentence overall assessment of the resume's current strength for the target role.]

---

## ✅ Strengths

- [Strength 1]
- [Strength 2]
- [Strength 3]

---

## ⚠️ Weaknesses & Gaps

- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

---

## ✏️ Specific Rewrite Suggestions

**[Section or bullet being improved]**
- *Before:* "[original text]"
- *After:* "[improved version]"

(Repeat for 2–4 suggestions)

---

## 🎯 ATS & Keyword Fit

[Assessment of how well the resume is optimised for Applicant Tracking Systems for this role.
Include 3–5 specific keywords or phrases the resume should add or emphasise.]
```

---

## 7. Prompt Design

The prompt is built in `prompt.py` by a function called `build_prompt(resume, role, job_description)`.

**System prompt** (sets Claude's persona and output rules):
```
You are an expert career coach and resume reviewer with 10+ years of experience 
helping candidates land roles in competitive industries. You give honest, 
constructive, and specific feedback. Always return your critique in exactly the 
Markdown format specified by the user — no extra commentary before or after.
```

**User prompt structure:**
1. State the target role
2. Provide the resume text (inside a code fence to prevent formatting bleed)
3. Optionally include the job description
4. Paste the exact output format template and instruct Claude to fill it in

---

## 8. API Key Handling

The app must work in two environments without changing any code:

### Local development
- Developer creates a `.env` file (not committed) containing:
  ```
  ANTHROPIC_API_KEY=sk-ant-...
  ```
- `python-dotenv` loads this automatically at startup.

### Streamlit Cloud deployment
- Developer adds `ANTHROPIC_API_KEY` in the Streamlit Cloud dashboard under **Secrets**.
- Streamlit makes this available via `st.secrets`.

### Resolution order in `app.py`

```python
import os
from dotenv import load_dotenv
import streamlit as st

# Load .env file if it exists (does nothing if file is absent)
load_dotenv()

# Try Streamlit secrets first (works on Streamlit Cloud),
# then fall back to the environment variable (works locally).
api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))

if not api_key:
    st.error("No API key found. See README for setup instructions.")
    st.stop()
```

---

## 9. Error Handling

| Error scenario | User-facing message |
|----------------|---------------------|
| API key missing | `st.error` with link to README setup section; `st.stop()` halts the app |
| `anthropic.AuthenticationError` | "Invalid API key. Please check your `.env` file." |
| `anthropic.RateLimitError` | "Claude is busy right now. Please wait a moment and try again." |
| Any other exception | "Something went wrong: [error message]. Please try again." |

All errors use `st.error()` and are shown in the results area, never as a crash.

---

## 10. Download Feature

After a successful critique is rendered:

```python
st.download_button(
    label="⬇ Download as Markdown",
    data=critique_text,          # the raw Markdown string from Claude
    file_name="resume_critique.md",
    mime="text/markdown",
)
```

No server-side file saving is needed — Streamlit handles the download entirely in the browser.

---

## 11. Data & Privacy

- **No data is stored.** The app holds user input only in Streamlit's session state for the duration of the browser session.
- **No database, no logging.** The app does not write anything to disk or any external service beyond the single API call.
- **Third-party API.** Resume text is sent to Anthropic. This is disclosed in the privacy notice (Section 5b).
- **`.env` is gitignored.** The API key never touches the repository.

---

## 12. `.gitignore` Contents

```
# Environment variables — never commit your API key
.env

# Python cache files
__pycache__/
*.pyc
*.pyo

# Virtual environment folders
venv/
.venv/
env/

# OS files
.DS_Store
Thumbs.db

# Streamlit local config
.streamlit/secrets.toml
```

---

## 13. `requirements.txt`

```
streamlit
anthropic
python-dotenv
```

---

## 14. README Outline

The `README.md` should cover (in plain language):

1. **What this project is** — one-paragraph description
2. **Demo screenshot** — placeholder note: "add screenshot after first run"
3. **Tech stack** — bulleted list
4. **Setup (local)**
   - Clone the repo
   - Create a virtual environment
   - `pip install -r requirements.txt`
   - Copy `.env.example` to `.env` and add your Anthropic API key
   - `streamlit run app.py`
5. **Setup (Streamlit Cloud)**
   - Fork/push to GitHub
   - Connect on share.streamlit.io
   - Add `ANTHROPIC_API_KEY` under Secrets
6. **How to use the app** — three bullet steps
7. **Project structure** — the file tree from Section 4
8. **Privacy note** — one sentence
9. **Author / licence** — MIT licence

---

## 15. Out of Scope for MVP

These features are intentionally excluded to keep the project simple and shippable:

| Feature | Reason deferred |
|---------|-----------------|
| PDF / DOCX upload | Adds file-parsing complexity |
| Tone selector | Decided against in spec interview |
| Formatting & readability section | Decided against in spec interview |
| User accounts / history | Requires a database |
| Streaming response | Nice UX but complicates beginner code |
| Multiple resume versions | Out of scope |
| Cost / token usage display | Minor complexity for MVP |

---

## 16. Implementation Order

When building the app, follow this order to get something working as fast as possible:

1. Create the file structure and `requirements.txt`
2. Write `.env.example` and `.gitignore`
3. Write `prompt.py` — the prompt builder function
4. Write `app.py` — wire up the UI with placeholder output first
5. Add the Claude API call and connect it to the UI
6. Test locally with a sample resume
7. Add error handling
8. Add the download button
9. Write `README.md`
10. Push to GitHub

---

*End of specification.*

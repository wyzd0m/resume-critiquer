# 🧠 AI Resume Critiquer

![CI](https://github.com/wyzd0m/resume-critiquer/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)
![Claude](https://img.shields.io/badge/Powered%20by-Claude%20Sonnet-8A2BE2)

A Streamlit web app that gives you structured, AI-powered feedback on your resume — powered by Claude.

Paste your resume, enter a target role, and get a five-section critique with an overall score, strengths, weaknesses, specific rewrite suggestions, and ATS keyword tips.

---

## 🚀 Live Demo

**[▶ Try it now → resume-critiquer-aggjcbhxsuur2rbxxh8dyn.streamlit.app](https://resume-critiquer-aggjcbhxsuur2rbxxh8dyn.streamlit.app/)**

> 📸 *Screenshot coming soon*

---

## 🛠 Tech Stack

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — web UI
- [Anthropic Claude API](https://docs.anthropic.com/) — AI critique (`claude-sonnet-4-6`)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — loads your API key from `.env`

---

## 📖 How to Use

> **You will need your own Anthropic API key.**  
> Get one at [console.anthropic.com](https://console.anthropic.com) — a $5 credit top-up covers 80+ critiques at ~$0.06 each. Your key is sent directly to Anthropic and is **never stored** by this app.

1. Open the live app and paste your Anthropic API key into the **sidebar**
2. Enter the job role you're targeting (e.g. *Software Engineer*)
3. Paste your resume as plain text
4. Optionally paste the job description for more targeted feedback
5. Click **Analyse My Resume**
6. Read your critique, then download it as a Markdown file

---

## ☁️ Deploy Your Own (Free)

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your fork
3. Under **Settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
4. Hit **Deploy** — no code changes needed

---

## 📁 Project Structure

```
resume-critiquer/
│
├── app.py                  # Main Streamlit app (UI + API call)
├── prompt.py               # Builds the prompt sent to Claude
│
├── requirements.txt        # pip dependencies
├── .env                    # Your API key — NOT committed to Git
├── .env.example            # Safe template — placeholder values only
├── .gitignore              # Excludes .env, caches, venv, etc.
│
├── Makefile                # Shortcuts: make install / make run
├── .github/workflows/      # GitHub Actions CI (auto-lints on push)
│
├── SPEC.md                 # Full project specification
└── README.md               # This file
```

---

## 🔒 Privacy

Resume text is sent to Anthropic's API to generate feedback. This app stores nothing — no database, no logging, no key retention. See [Anthropic's usage policy](https://www.anthropic.com/legal/usage-policy).

---

## 📄 Licence

MIT — free to use, modify, and share.

---

*Built with [Claude](https://claude.ai)*

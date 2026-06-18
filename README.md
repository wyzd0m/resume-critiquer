# 🧠 AI Resume Critiquer

![CI](https://github.com/wyzd0m/resume-critiquer/actions/workflows/ci.yml/badge.svg)

A Streamlit web app that gives you structured, AI-powered feedback on your resume — powered by Claude.

Paste your resume, enter a target role, and get a five-section critique with an overall score, strengths, weaknesses, specific rewrite suggestions, and ATS keyword tips.

> 📸 **Demo screenshot:** *(add after first run)*

---

## 🛠 Tech Stack

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — web UI
- [Anthropic Claude API](https://docs.anthropic.com/) — AI critique (`claude-sonnet-4-6`)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — loads your API key from `.env`

---

## 📖 How to Use

1. Enter the job role you're targeting (e.g. *Software Engineer*)
2. Paste your resume as plain text
3. Optionally paste the job description for more targeted feedback
4. Click **Analyse My Resume**
5. Read your critique, then download it as a Markdown file

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

Resume text is sent to Anthropic's API to generate feedback. This app stores nothing — no database, no logging. See [Anthropic's usage policy](https://www.anthropic.com/legal/usage-policy).

---

## 📄 Licence

MIT — free to use, modify, and share.

---

*Built with [Claude](https://claude.ai)*

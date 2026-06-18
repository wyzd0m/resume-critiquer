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

## ⚡ Quick Start (Local)

### 1. Clone the repo

```bash
git clone https://github.com/wyzd0m/resume-critiquer.git
cd resume-critiquer
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Mac / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# or, if you have make:
make install
```

### 4. Add your Anthropic API key

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your real key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get a free key at [console.anthropic.com](https://console.anthropic.com/).

### 5. Run the app

```bash
streamlit run app.py
# or:
make run
```

> **No `.env` file?** No problem — when the app opens, paste your API key directly into the sidebar. Great for a quick test without any setup.

---

## ☁️ Deploy to Streamlit Cloud (free)

1. Push this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo
3. Under **Settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
4. Click **Deploy** — no code changes needed

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

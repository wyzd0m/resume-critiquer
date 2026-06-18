import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

from prompt import build_prompt

# ── Page config (must be the first Streamlit command) ─────────────────────────
st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="🧠",
    layout="centered",
)

# ── Load API key ───────────────────────────────────────────────────────────────
# Load .env file if it exists (only useful on local development)
load_dotenv()

# Priority order for finding the API key:
#   1. Streamlit Cloud secrets  (for deployed apps)
#   2. .env file / environment variable  (for local development)
#   3. Sidebar input  (for quick testing with no setup at all)
api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))

# If no key was found automatically, show a sidebar field so the user can paste
# their own key — this is the expected flow for anyone using the live demo.
if not api_key:
    with st.sidebar:
        st.markdown("### 🔑 Your Anthropic API Key")
        st.markdown(
            "This app is powered by Claude and requires your own API key.\n\n"
            "**Get one at [console.anthropic.com](https://console.anthropic.com)** — "
            "a $5 top-up covers 80+ critiques.\n\n"
            "Your key is sent directly to Anthropic and is **never stored** by this app."
        )
        api_key = st.text_input(
            "Paste your API key",
            type="password",       # hides the key while typing
            placeholder="sk-ant-...",
        )
        if not api_key:
            st.info("👆 Paste your key above to get started.")

# ── Title & caption ────────────────────────────────────────────────────────────
st.title("🧠 AI Resume Critiquer")
st.caption("Get structured feedback on your resume — powered by Claude")

# ── Privacy notice (collapsed by default so it doesn't clutter the page) ──────
with st.expander("⚠️ Privacy Notice — read before submitting"):
    st.markdown(
        """
        **Your data & privacy**

        When you click *Analyse My Resume*, the text you enter is sent to
        Anthropic's API to generate your critique.
        Anthropic's standard [usage policies](https://www.anthropic.com/legal/usage-policy) apply.

        Do not include sensitive personal information such as your home address,
        national ID numbers, or financial details.
        """
    )

# ── Input fields ───────────────────────────────────────────────────────────────
target_role = st.text_input(
    "Target Role *",
    placeholder="e.g. Software Engineer, Product Manager, Data Analyst",
)

resume_text = st.text_area(
    "Your Resume *",
    placeholder="Paste your resume here...",
    height=300,
)

# Show a live character count so the user knows how much text they've pasted
if resume_text:
    st.caption(f"{len(resume_text):,} characters")

job_description = st.text_area(
    "Job Description (optional)",
    placeholder="Paste the job posting here to get more targeted feedback...",
    height=150,
)

# ── Analyse button ─────────────────────────────────────────────────────────────
# Disable the button until an API key is available so the user gets clear feedback
analyse_clicked = st.button(
    "🔍 Analyse My Resume",
    type="primary",
    disabled=not api_key,
)

if not api_key:
    st.caption("⚠️ Paste your Anthropic API key in the sidebar to enable analysis.")

# ── Validation & API call ──────────────────────────────────────────────────────
if analyse_clicked:
    # Check required fields before spending any API credits
    if not target_role.strip():
        st.warning("Please enter a target role.")
    elif not resume_text.strip():
        st.warning("Please paste your resume text.")
    elif len(resume_text.strip()) < 50:
        st.warning("Your resume seems too short. Please paste the full text.")
    else:
        # Everything looks good — call the Claude API
        try:
            with st.spinner("Analysing your resume..."):
                # Build the prompts using the helper in prompt.py
                system_prompt, user_prompt = build_prompt(
                    resume_text, target_role, job_description
                )

                # Create the Anthropic client with our key
                client = anthropic.Anthropic(api_key=api_key)

                # Send the request to Claude
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=2048,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )

                # Pull the text out of Claude's response
                critique_text = message.content[0].text

                # Save to session_state so results survive page re-renders
                # (e.g. clicking the Download button would otherwise clear them)
                st.session_state["critique"] = critique_text

        except anthropic.AuthenticationError:
            st.error("❌ Invalid API key. Please check your `.env` file or sidebar input.")
            st.stop()
        except anthropic.RateLimitError:
            st.error("⏳ Claude is busy right now. Please wait a moment and try again.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}. Please try again.")
            st.stop()

# ── Display results ────────────────────────────────────────────────────────────
# We read from session_state so the critique stays visible after interactions
if "critique" in st.session_state:
    st.divider()
    st.subheader("📄 Critique Results")
    st.markdown(st.session_state["critique"])

    # Let the user save the critique as a Markdown file
    st.download_button(
        label="⬇ Download as Markdown",
        data=st.session_state["critique"],
        file_name="resume_critique.md",
        mime="text/markdown",
    )

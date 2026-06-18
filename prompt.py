def build_prompt(resume: str, role: str, job_description: str = "") -> tuple[str, str]:
    """
    Build the system and user prompts to send to Claude.

    Keeping the prompt in its own file means app.py stays focused on the UI,
    and it's easy to find and tweak the wording here without touching anything else.

    Args:
        resume:          The user's resume text (plain text, pasted by the user).
        role:            The target job title (e.g. "Software Engineer").
        job_description: Optional job posting text for more tailored feedback.

    Returns:
        A (system_prompt, user_prompt) tuple ready to pass straight to the API.
    """

    # ── System prompt ──────────────────────────────────────────────────────────
    # This sets Claude's persona and tells it to stick strictly to our format.
    system_prompt = (
        "You are an expert career coach and resume reviewer with 10+ years of experience "
        "helping candidates land roles in competitive industries. You give honest, "
        "constructive, and specific feedback. Always return your critique in exactly the "
        "Markdown format specified by the user — no extra commentary before or after."
    )

    # ── Output template ────────────────────────────────────────────────────────
    # We give Claude the exact Markdown skeleton to fill in.
    # A fixed format makes the output predictable and easy to render in Streamlit.
    output_template = """\
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
Include 3–5 specific keywords or phrases the resume should add or emphasise.]"""

    # ── User prompt ────────────────────────────────────────────────────────────
    # We wrap the resume in a code fence so Claude doesn't misread any special
    # characters or formatting inside the resume as instructions.
    user_prompt = f"""Please critique the following resume for the role of **{role}**.

Resume:

```
{resume}
```
"""

    # Only include the job description section if the user actually provided one
    if job_description.strip():
        user_prompt += f"""
Job Description (use this to tailor your feedback):

```
{job_description}
```
"""

    # Finally, give Claude the output template and tell it to fill it in exactly
    user_prompt += f"""
Return your critique using **exactly** this Markdown structure. \
Do not add any text before or after it:

{output_template}
"""

    return system_prompt, user_prompt

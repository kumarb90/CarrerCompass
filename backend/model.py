import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_json(text: str):
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except Exception:
        return None


def analyze_resume_and_jd(resume: str, jd: str):
    prompt = f"""
You are a senior recruiter at Amazon and an expert career advisor.

First, clearly identify what type of role this job is.
Choose ONE:
- Marketing / MBA
- Cloud / IT Support
- Software Engineering
- Management / Operations

Then compare the resume against the job role.

STRICT RULES:
- If the job is Marketing / MBA, your advice MUST be marketing-focused.
- Do NOT talk about coding for marketing roles.
- Resume suggestions MUST be specific and actionable.
- Always return at least 4 resume suggestions.
- Always return at least 4 relevant courses.
- Do NOT return empty lists.
- Do NOT include explanations outside JSON.

Return ONLY valid JSON in this exact format:

{{
  "role_type": "Marketing / MBA | Cloud / IT Support | Software Engineering | Management / Operations",
  "score": number between 0 and 10,
  "improvement_tip": "one clear professional sentence",
  "resume_suggestions": [
    "suggestion 1",
    "suggestion 2",
    "suggestion 3",
    "suggestion 4"
  ],
  "courses": [
    "course 1",
    "course 2",
    "course 3",
    "course 4"
  ]
}}

JOB DESCRIPTION:
{jd}

RESUME:
{resume}
"""
    response = model.generate_content(prompt)
    data = extract_json(response.text)

    if not data:
        return {
            "score": 3.0,
            "improvement_tip": "The resume is not aligned with the job role and requires significant tailoring.",
            "resume_suggestions": [
                "Rewrite the resume summary to align with the target role.",
                "Highlight role-relevant skills instead of unrelated experience.",
                "Reframe projects to emphasize business or customer impact.",
                "Maintain a separate resume version for this role."
            ],
            "courses": [
                "Marketing Fundamentals",
                "Business Strategy Basics",
                "Customer-Centric Decision Making",
                "Data-Driven Marketing"
            ]
        }

    return {
        "score": float(data.get("score", 3.0)),
        "improvement_tip": data.get("improvement_tip", ""),
        "resume_suggestions": data.get("resume_suggestions", []),
        "courses": data.get("courses", [])
    }

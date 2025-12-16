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

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    return None


def suggest_jobs_from_resume(resume: str):
    prompt = f"""
You are a career assistant.

Based on the resume below, suggest 5 suitable jobs.

Return ONLY JSON in this exact format:
{{
  "jobs": [
    {{
      "company": "Company Name",
      "role": "Job Role",
      "description": "Short description",
      "apply_link": "https://example.com/apply"
    }}
  ]
}}

RESUME:
{resume}
"""

    response = model.generate_content(prompt)
    raw = extract_json(response.text)

    jobs = []

    if raw and "jobs" in raw:
        for j in raw["jobs"]:
            jobs.append({
                "company": j.get("company", "Company"),
                "role": j.get("role") or j.get("title") or "Relevant Role",
                "description": j.get("description") or j.get("summary") or "",
                "apply_link": j.get("apply_link") or j.get("link") or "https://www.linkedin.com/jobs"
            })

    if not jobs:
        jobs = [
            {
                "company": "LinkedIn",
                "role": "Software / IT Role",
                "description": "Suggested based on your resume skills.",
                "apply_link": "https://www.linkedin.com/jobs"
            }
        ]

    return {"jobs": jobs}

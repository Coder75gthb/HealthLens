import json
import re
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

def _safe_json(text: str):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group())
        raise ValueError("Invalid JSON from model")

def generate_lifestyle_blueprint(
    disease: str,
    risk_percent: float,
    trend: str,
    age: int,
    bmi: float,
    smoker: bool,
    activity_level: str
):
    prompt = f"""
You are generating a personalized lifestyle blueprint.

USER CONTEXT:
- Condition of concern: {disease}
- Current risk level: {risk_percent}%
- Risk trend from simulation: {trend}
- Age: {age}
- BMI: {bmi}
- Smoking status: {"Yes" if smoker else "No"}
- Physical activity level: {activity_level}

TASK:
Create a detailed, practical lifestyle blueprint.
Every recommendation MUST explain why it matters for THIS user.

STRICT RULES:
- Do NOT give generic health advice
- Tie explanations to risk level or trend
- No medical or diagnostic claims
- Avoid absolute words like must/always/never
- Be realistic and sustainable

Return STRICT JSON ONLY:

{{
  "context_summary": "...",
  "food_strategy": {{
    "why_it_matters": "...",
    "focus": [],
    "limit": [],
    "practical_swaps": []
  }},
  "exercise_plan": {{
    "why_it_matters": "...",
    "aerobic": {{
      "type": "",
      "duration": "",
      "frequency": ""
    }},
    "strength": {{
      "type": "",
      "frequency": ""
    }}
  }},
  "sleep_recovery": {{
    "why_it_matters": "...",
    "target_duration": "",
    "habits": []
  }},
  "daily_micro_habits": {{
    "why_it_matters": "...",
    "actions": []
  }},
  "avoid_overfocus": {{
    "why_it_matters": "...",
    "items": []
  }},
  "confidence": "low | medium | high"
}}
"""

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    raw = completion.choices[0].message.content
    return _safe_json(raw)

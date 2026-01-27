import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
import re

# -------------------------------------------------
# ENV LOADING
# -------------------------------------------------
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)

# -------------------------------------------------
# MODEL (VERIFIED + STABLE)
# -------------------------------------------------
MODEL_NAME = "llama-3.1-8b-instant"  # DO NOT CHANGE

# -------------------------------------------------
# JSON SAFETY PARSER (CRITICAL)
# -------------------------------------------------
def safe_json_parse(text: str) -> Dict[str, Any]:
    """
    Extracts JSON even if model adds extra text.
    """
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group())
        raise ValueError("No valid JSON found")

# -------------------------------------------------
# FOOD INSIGHT ENGINE (HARD GUARDED)
# -------------------------------------------------
def analyze_food(food: str) -> Dict[str, Any]:

    prompt = f"""
You are a practical nutrition expert.

Food: {food}

STRICT INSTRUCTIONS (NO EXCEPTIONS):
- Do NOT use generic phrases like:
  "provides energy", "may lack balance", "eat in moderation"
- Be SPECIFIC to the food
- Mention typical preparation & ingredients
- Mention realistic positives AND negatives
- Minimum:
  • 2 good_points
  • 2 concerns
  • 2 better_alternatives
- No diseases
- No medical claims
- No judgement words like healthy/unhealthy

Return ONLY valid JSON in EXACT format:

{{
  "good_points": ["..."],
  "concerns": ["..."],
  "better_alternatives": ["..."],
  "confidence": "high | medium | low"
}}
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw_output = completion.choices[0].message.content
    print("RAW FOOD MODEL OUTPUT:\n", raw_output)

    parsed = safe_json_parse(raw_output)

    # FINAL HARD VALIDATION (NO GENERIC OUTPUT ALLOWED)
    if (
        len(parsed.get("good_points", [])) < 2
        or len(parsed.get("concerns", [])) < 2
        or len(parsed.get("better_alternatives", [])) < 2
    ):
        raise RuntimeError("Model returned weak/generic output")

    return parsed

# -------------------------------------------------
# PUBLIC API (USED BY STREAMLIT)
# -------------------------------------------------
def get_food_insights(food: str) -> Dict[str, Any]:
    try:
        profile = analyze_food(food)
    except Exception as e:
        print("FOOD ENGINE FAILURE:", e)

        # LAST-RESORT FALLBACK (VERY RARE NOW)
        profile = {
            "good_points": [
                "Commonly eaten dish with familiar taste",
                "Provides satiety due to richness"
            ],
            "concerns": [
                "Can be calorie dense depending on preparation",
                "Often contains high amounts of fat or sugar"
            ],
            "better_alternatives": [
                "Choose lighter preparation methods",
                "Pair with vegetables or whole grains"
            ],
            "confidence": "low",
        }

    return {
        "food": food,
        "what_is_good": profile["good_points"],
        "what_to_watch_out_for": profile["concerns"],
        "healthier_swaps_or_tips": profile["better_alternatives"],
        "confidence": profile["confidence"],
    }

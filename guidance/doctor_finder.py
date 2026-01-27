# guidance/doctor_finder.py

from urllib.parse import quote_plus


# -----------------------------
# Disease → Specialist mapping
# -----------------------------
DISEASE_SPECIALIST_MAP = {
    "diabetes": "Endocrinologist",
    "hypertension": "Cardiologist",
    "heart_disease": "Cardiologist",
    "ckd": "Nephrologist",
}


def get_highest_risk_disease(risk_summary):
    """
    Determines which disease has the highest actionable risk.
    Expects unified_risk_engine output.
    """

    highest = None
    highest_risk = 0.0

    for disease, data in risk_summary.items():
        if disease == "ckd":
            risk = data["current_risk"]
            severity = data["severity"]
        else:
            risk = data["risk_percent"]
            severity = data["severity"]

        if severity in ["Moderate", "High", "Very High"] and risk > highest_risk:
            highest_risk = risk
            highest = disease

    return highest


def generate_doctor_links(disease, location):
    """
    Generates safe redirect links for doctor discovery.
    No ranking, no recommendations.
    """

    specialist = DISEASE_SPECIALIST_MAP.get(disease)

    if not specialist:
        return None

    query = quote_plus(f"{specialist} near {location}")

    return {
        "specialist": specialist,
        "google_maps": f"https://www.google.com/maps/search/{query}",
        "practo": f"https://www.practo.com/search/doctors?q={query}",
    }


def doctor_guidance(risk_summary, location):
    """
    Main doctor discovery interface.
    """

    disease = get_highest_risk_disease(risk_summary)

    if not disease:
        return {
            "show_guidance": False,
            "message": "Based on the current risk assessment, consulting a specialist is not required at this stage.",
        }

    links = generate_doctor_links(disease, location)

    return {
        "show_guidance": True,
        "trigger_disease": disease,
        "recommended_specialist": links["specialist"],
        "message": (
            "Based on your risk profile, it may be helpful to consult a specialist "
            "for further evaluation. This is not a diagnosis."
        ),
        "links": links,
    }

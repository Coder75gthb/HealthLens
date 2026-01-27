# interaction_engine/hypertension_risk.py

def estimate_hypertension_risk(
    age,
    bmi,
    systolic_bp=None,
    smoker=False,
    physical_activity="moderate"
):
    """
    Rule-based hypertension risk estimation.
    Preventive, not diagnostic.
    """

    risk = 10.0  # base population risk

    # Blood pressure contribution
    if systolic_bp:
        if systolic_bp >= 160:
            risk += 40
        elif systolic_bp >= 140:
            risk += 30
        elif systolic_bp >= 130:
            risk += 20
        elif systolic_bp >= 120:
            risk += 10

    # Age
    if age >= 60:
        risk += 15
    elif age >= 45:
        risk += 10

    # BMI
    if bmi >= 30:
        risk += 15
    elif bmi >= 25:
        risk += 8

    # Smoking
    if smoker:
        risk += 8

    # Physical activity
    if physical_activity == "low":
        risk += 8
    elif physical_activity == "high":
        risk -= 5

    # Clamp
    risk = max(0, min(100, risk))

    # Severity
    if risk < 30:
        severity = "Low"
    elif risk < 60:
        severity = "Moderate"
    else:
        severity = "High"

    # Confidence (depends on BP availability)
    confidence = 0.8 if systolic_bp else 0.6

    return {
        "risk_percent": round(risk, 1),
        "severity": severity,
        "confidence": confidence
    }

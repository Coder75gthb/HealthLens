# guidance/test_doctor_finder.py

from guidance.doctor_finder import doctor_guidance


# -----------------------------
# Case 1: High heart disease risk
# -----------------------------
risk_summary_high = {
    "diabetes": {
        "risk_percent": 42.0,
        "severity": "Moderate",
        "confidence": 0.8,
    },
    "heart_disease": {
        "risk_percent": 68.0,
        "severity": "High",
        "confidence": 0.85,
    },
    "hypertension": {
        "risk_percent": 55.0,
        "severity": "Moderate",
        "confidence": 0.8,
    },
    "ckd": {
        "current_risk": 60.0,
        "severity": "High",
        "confidence": 0.9,
    },
}

result_1 = doctor_guidance(risk_summary_high, location="Delhi")

print("\n=== Case 1: High Risk ===")
for k, v in result_1.items():
    print(f"{k}: {v}")


# -----------------------------
# Case 2: All low risk
# -----------------------------
risk_summary_low = {
    "diabetes": {
        "risk_percent": 10.0,
        "severity": "Low",
        "confidence": 0.5,
    },
    "heart_disease": {
        "risk_percent": 12.0,
        "severity": "Low",
        "confidence": 0.6,
    },
    "hypertension": {
        "risk_percent": 15.0,
        "severity": "Low",
        "confidence": 0.6,
    },
    "ckd": {
        "current_risk": 12.0,
        "severity": "Low",
        "confidence": 0.4,
    },
}

result_2 = doctor_guidance(risk_summary_low, location="Mumbai")

print("\n=== Case 2: Low Risk ===")
for k, v in result_2.items():
    print(f"{k}: {v}")


import math

# -----------------------------
# Helper functions
# -----------------------------
def clamp(val, low=0, high=85):
    return max(low, min(val, high))


def severity_label(risk):
    if risk < 25:
        return "Low"
    elif risk < 50:
        return "Moderate"
    elif risk < 70:
        return "High"
    else:
        return "Very High"


def confidence_from_risk(risk):
    # Higher risk → slightly higher confidence
    return round(0.55 + (risk / 200), 2)


# -----------------------------
# MAIN RISK ENGINE
# -----------------------------
def risk_engine(
    *,
    age,
    bmi,
    smoker,
    physical_activity,
    bp=None,
    glucose=None,
    cholesterol=None,
    diabetes_model=None,   # optional (not dominant)
    heart_model=None       # optional (not dominant)
):
    results = {}

    # -----------------------------
    # Normalize inputs
    # -----------------------------
    smoker = bool(smoker)
    activity = physical_activity.lower()

    systolic_bp = bp if bp is not None else None
    glucose = glucose if glucose is not None else None
    cholesterol = cholesterol if cholesterol is not None else None

    # Smooth age factor (NO jumps)
    age_factor_diabetes = max(0, (age - 18)) * 0.6
    age_factor_heart = max(0, (age - 18)) * 0.7
    age_factor_htn = max(0, (age - 25)) * 0.5

    # =====================================================
    # DIABETES
    # =====================================================
    diabetes_risk = 8 + age_factor_diabetes

    # BMI
    if bmi >= 30:
        diabetes_risk += 14
    elif bmi >= 25:
        diabetes_risk += 6

    # Lifestyle
    if smoker:
        diabetes_risk += 10
    if activity == "low":
        diabetes_risk += 6

    # Glucose (only if provided)
    if glucose is not None:
        if glucose >= 160:
            diabetes_risk += 30
        elif glucose >= 126:
            diabetes_risk += 20

    diabetes_risk = clamp(diabetes_risk)

    results["diabetes"] = {
        "risk_percent": round(diabetes_risk, 1),
        "severity": severity_label(diabetes_risk),
        "confidence": confidence_from_risk(diabetes_risk),
    }

    # =====================================================
    # HEART DISEASE
    # =====================================================
    heart_risk = 6 + age_factor_heart

    # Smoking (strong signal)
    if smoker:
        heart_risk += 18

    # BMI
    if bmi >= 30:
        heart_risk += 10

    # Physical activity
    if activity == "low":
        heart_risk += 6

    # BP (only if provided)
    if systolic_bp is not None:
        if systolic_bp >= 140:
            heart_risk += 25
        elif systolic_bp >= 130:
            heart_risk += 12

    # Cholesterol (only if provided)
    if cholesterol is not None and cholesterol >= 240:
        heart_risk += 12

    heart_risk = clamp(heart_risk)

    results["heart_disease"] = {
        "risk_percent": round(heart_risk, 1),
        "severity": severity_label(heart_risk),
        "confidence": confidence_from_risk(heart_risk),
    }

    # =====================================================
    # HYPERTENSION (RULE BASED)
    # =====================================================
    hypertension_risk = age_factor_htn

    if bmi >= 30:
        hypertension_risk += 10
    if smoker:
        hypertension_risk += 8

    if systolic_bp is not None:
        if systolic_bp >= 140:
            hypertension_risk += 40
        elif systolic_bp >= 130:
            hypertension_risk += 25

    hypertension_risk = clamp(hypertension_risk)

    results["hypertension"] = {
        "risk_percent": round(hypertension_risk, 1),
        "severity": severity_label(hypertension_risk),
        "confidence": confidence_from_risk(hypertension_risk),
    }

    # =====================================================
    # CKD (DERIVED – NOT INDEPENDENT)
    # =====================================================
    ckd_risk = (
        0.3 * diabetes_risk +
        0.4 * hypertension_risk +
        0.2 * age_factor_diabetes
    )

    ckd_risk = clamp(ckd_risk)

    results["ckd"] = {
        "risk_percent": round(ckd_risk, 1),
        "severity": severity_label(ckd_risk),
        "confidence": confidence_from_risk(ckd_risk),
    }

    return results


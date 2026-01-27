# interaction_engine/ckd_risk.py

def clamp(value, min_val=0.0, max_val=0.85):
    return max(min(value, max_val), min_val)


def base_lifestyle_risk(age, bmi, smoker, physical_activity):
    """
    Low baseline CKD risk from demographics + lifestyle alone
    """
    risk = 0.05

    if age >= 45:
        risk += 0.05
    if bmi and bmi >= 30:
        risk += 0.05
    if smoker:
        risk += 0.03
    if physical_activity == "low":
        risk += 0.03

    return risk


def compute_ckd_risk(
    *,
    age,
    bmi,
    smoker,
    physical_activity,
    diabetes_risk,
    hypertension_risk,
):
    """
    Computes current CKD risk (0–1 scale)
    """

    # Layer 1: baseline lifestyle risk
    risk = base_lifestyle_risk(
        age, bmi, smoker, physical_activity
    )

    # Layer 2: comorbidity contributions
    risk += 0.4 * diabetes_risk
    risk += 0.35 * hypertension_risk

    # Interaction amplification
    risk += 0.25 * diabetes_risk * hypertension_risk

    return clamp(risk)


def severity_from_risk(risk):
    """
    Maps risk percentage to severity band
    """
    if risk < 0.15:
        return "Low"
    elif risk < 0.35:
        return "Mild"
    elif risk < 0.60:
        return "Moderate"
    elif risk < 0.80:
        return "High"
    else:
        return "Very High"


def project_ckd_risk(
    *,
    current_risk,
    diabetes_trend=0.0,
    hypertension_trend=0.0,
    months=12,
):
    """
    Projects CKD risk forward in time.
    diabetes_trend / hypertension_trend:
        negative = improving
        positive = worsening
    """

    # Base drift from time
    if months == 3:
        drift = 0.01
    elif months == 6:
        drift = 0.025
    else:  # 12 months
        drift = 0.05

    # Comorbidity-driven adjustment
    trend_effect = (
        0.6 * diabetes_trend +
        0.5 * hypertension_trend
    )

    projected = current_risk + drift + trend_effect

    return clamp(projected)


def confidence_score(
    *,
    has_diabetes_risk,
    has_hypertension_risk,
    bp_provided,
    sugar_provided,
    cholesterol_provided,
):
    """
    Confidence depends on data availability, not severity
    """
    score = 0.3

    if has_diabetes_risk:
        score += 0.2
    if has_hypertension_risk:
        score += 0.2
    if bp_provided:
        score += 0.1
    if sugar_provided:
        score += 0.1
    if cholesterol_provided:
        score += 0.1

    return min(score, 1.0)


def get_ckd_risk_summary(
    *,
    age,
    bmi,
    smoker,
    physical_activity,
    diabetes_risk,
    hypertension_risk,
    diabetes_trend=0.0,
    hypertension_trend=0.0,
    bp_provided=False,
    sugar_provided=False,
    cholesterol_provided=False,
):
    """
    Main CKD risk interface function.
    Returns current risk, projections, severity, confidence, and trend.
    """

    # --- Current risk ---
    current_risk = compute_ckd_risk(
        age=age,
        bmi=bmi,
        smoker=smoker,
        physical_activity=physical_activity,
        diabetes_risk=diabetes_risk,
        hypertension_risk=hypertension_risk,
    )

    severity = severity_from_risk(current_risk)

    # --- Projections ---
    risk_3m = project_ckd_risk(
        current_risk=current_risk,
        diabetes_trend=diabetes_trend,
        hypertension_trend=hypertension_trend,
        months=3,
    )

    risk_6m = project_ckd_risk(
        current_risk=current_risk,
        diabetes_trend=diabetes_trend,
        hypertension_trend=hypertension_trend,
        months=6,
    )

    risk_12m = project_ckd_risk(
        current_risk=current_risk,
        diabetes_trend=diabetes_trend,
        hypertension_trend=hypertension_trend,
        months=12,
    )

    # --- Trend label ---
    if risk_12m > current_risk + 0.03:
        trend = "Worsening"
    elif risk_12m < current_risk - 0.03:
        trend = "Improving"
    else:
        trend = "Stable"

    # --- Confidence ---
    conf = confidence_score(
        has_diabetes_risk=diabetes_risk is not None,
        has_hypertension_risk=hypertension_risk is not None,
        bp_provided=bp_provided,
        sugar_provided=sugar_provided,
        cholesterol_provided=cholesterol_provided,
    )

    if conf >= 0.75:
        conf_label = "High"
    elif conf >= 0.45:
        conf_label = "Medium"
    else:
        conf_label = "Low"

    return {
        "current_risk": round(current_risk * 100, 1),
        "severity": severity,
        "confidence": round(conf, 2),
        "confidence_label": conf_label,
        "projections": {
            "3_months": round(risk_3m * 100, 1),
            "6_months": round(risk_6m * 100, 1),
            "12_months": round(risk_12m * 100, 1),
        },
        "trend": trend,
    }

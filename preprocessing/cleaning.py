# preprocessing/cleaning.py

def compute_bmi(height_cm, weight_kg):
    if height_cm is None or weight_kg is None:
        return None
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def clip(value, min_val, max_val):
    if value is None:
        return None
    return max(min(value, max_val), min_val)


def clean_inputs(inputs: dict) -> dict:
    """
    Performs soft medical cleaning.
    Does NOT raise errors.
    """

    cleaned = inputs.copy()

    # ---- BMI handling ----
    if cleaned.get("bmi") is None:
        cleaned["bmi"] = compute_bmi(
            cleaned.get("height"),
            cleaned.get("weight")
        )

    # Clip BMI to realistic human range
    cleaned["bmi"] = clip(cleaned.get("bmi"), 10, 60)

    # ---- Blood Pressure ----
    cleaned["systolic_bp"] = clip(cleaned.get("systolic_bp"), 80, 200)
    cleaned["diastolic_bp"] = clip(cleaned.get("diastolic_bp"), 40, 130)

    # ---- Blood Sugar ----
    cleaned["blood_sugar"] = clip(cleaned.get("blood_sugar"), 50, 400)

    # ---- Cholesterol ----
    cleaned["cholesterol"] = clip(cleaned.get("cholesterol"), 100, 400)

    return cleaned

def generate_explanations(disease, risk_data, inputs):
    explanations = []

    age = inputs.get("age")
    bmi = inputs.get("bmi")
    smoker = inputs.get("smoker")
    activity = inputs.get("physical_activity")
    bp = inputs.get("bp")
    glucose = inputs.get("glucose")
    cholesterol = inputs.get("cholesterol")

    # ---------------- HARD GATES (POINTER 1 FIX) ----------------

    if disease == "hypertension" and bp is None:
        return [
            "Blood pressure data was not provided, so hypertension risk cannot be reliably assessed.",
            "Without systolic BP values, this estimate is intentionally kept low."
        ]

    if disease == "diabetes" and bmi is None and glucose is None:
        return [
            "Key metabolic indicators (BMI or glucose) were not provided.",
            "Diabetes risk is therefore kept conservative."
        ]

    if disease == "heart_disease" and age < 35 and not smoker and cholesterol is None:
        return [
            "At your age, without smoking or cholesterol abnormalities, heart disease risk is naturally low.",
            "This estimate reflects baseline population risk only."
        ]

    # ---------------- AGE (STRICTLY DISEASE AWARE) ----------------

    if age is not None:
        if disease == "diabetes":
            if age < 30:
                explanations.append("Young age strongly lowers baseline diabetes risk.")
            elif age < 45:
                explanations.append("Age contributes mildly to diabetes risk.")
            else:
                explanations.append("Increasing age raises diabetes risk.")

        elif disease == "heart_disease":
            if age < 30:
                explanations.append("Heart disease is uncommon at this age.")
            elif age < 45:
                explanations.append("Age begins to contribute to cardiovascular risk.")
            else:
                explanations.append("Age is a major risk factor for heart disease.")

        elif disease == "ckd":
            if age < 40:
                explanations.append("Kidney disease risk is typically low at younger ages.")
            else:
                explanations.append("Age increases susceptibility to kidney disease.")

    # ---------------- SMOKING ----------------

    if smoker:
        if disease in ["heart_disease", "hypertension", "ckd"]:
            explanations.append("Smoking significantly damages blood vessels and organs.")
        else:
            explanations.append("Smoking increases metabolic risk.")
    else:
        explanations.append("Not smoking substantially reduces risk.")

    # ---------------- BMI ----------------

    if bmi is not None:
        if disease == "diabetes":
            if bmi < 25:
                explanations.append("Healthy BMI strongly protects against insulin resistance.")
            elif bmi < 30:
                explanations.append("Elevated BMI increases diabetes risk.")
            else:
                explanations.append("Obesity is a major diabetes risk factor.")

        elif disease == "heart_disease":
            if bmi >= 30:
                explanations.append("High BMI contributes to cardiovascular strain.")

        elif disease == "ckd":
            if bmi >= 30:
                explanations.append("Obesity indirectly increases kidney disease risk.")

    # ---------------- PHYSICAL ACTIVITY ----------------

    if activity == "low":
        if disease in ["diabetes", "heart_disease"]:
            explanations.append("Low activity increases long-term metabolic and heart risk.")
    elif activity == "high":
        explanations.append("High physical activity is protective.")

    # ---------------- DISEASE-SPECIFIC CLINICAL SIGNALS ----------------

    if disease == "diabetes":
        if glucose is not None:
            if glucose >= 140:
                explanations.append("Elevated glucose strongly indicates diabetes risk.")
            elif glucose >= 110:
                explanations.append("Borderline glucose mildly increases risk.")

    elif disease == "heart_disease":
        if cholesterol is not None and cholesterol >= 240:
            explanations.append("High cholesterol significantly raises heart disease risk.")

    elif disease == "hypertension":
        if bp is not None:
            if bp >= 140:
                explanations.append("Systolic BP is in the hypertensive range.")
            elif bp >= 130:
                explanations.append("Systolic BP is borderline high.")

    elif disease == "ckd":
        if bp is not None and bp >= 140:
            explanations.append("Chronic high BP damages kidney filtration.")
        if glucose is not None and glucose >= 140:
            explanations.append("Diabetes is a leading cause of kidney disease.")

    # ---------------- FINAL SAFETY ----------------

    if not explanations:
        explanations.append("Overall indicators suggest low current risk.")

    return explanations


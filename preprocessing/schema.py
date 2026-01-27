# preprocessing/schema.py

# ---------- USER INPUT FEATURES ----------

MANDATORY_FEATURES = [
    "age",
    "height",
    "weight",
    "bmi",
    "smoker",
    "physical_activity",
    "family_history"
]

OPTIONAL_FEATURES = [
    "systolic_bp",
    "diastolic_bp",
    "blood_sugar",
    "cholesterol"
]

ALL_FEATURES = MANDATORY_FEATURES + OPTIONAL_FEATURES


# ---------- FEATURE TYPES ----------

NUMERIC_FEATURES = [
    "age",
    "height",
    "weight",
    "bmi",
    "systolic_bp",
    "diastolic_bp",
    "blood_sugar",
    "cholesterol"
]

BINARY_FEATURES = [
    "smoker",
    "family_history"
]

ORDINAL_FEATURES = {
    "physical_activity": ["low", "moderate", "high"]
}

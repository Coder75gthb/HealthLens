# preprocessing/column_mapping.py

# -------- RAW DATASET COLUMN → SYSTEM FEATURE --------

DIABETES_COLUMN_MAP = {
    "Age": "age",
    "BMI": "bmi",
    "Smoker": "smoker",
    "PhysActivity": "physical_activity",
    "Diabetes_012": "label",
    "HighBP": "systolic_bp",
    "HighChol": "cholesterol"
}

HEART_COLUMN_MAP = {
    "Age": "age",
    "BMI": "bmi",
    "Smoker": "smoker",
    "PhysActivity": "physical_activity",
    "HeartDiseaseorAttack": "label",
    "HighBP": "systolic_bp",
    "HighChol": "cholesterol"
}

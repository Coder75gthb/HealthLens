# explainability/diabetes_shap.py

import joblib
import shap
import pandas as pd


# 1️⃣ Load trained model & scaler
model = joblib.load("models/diabetes_model.pkl")
scaler = joblib.load("models/diabetes_scaler.pkl")

# 2️⃣ Load background data (small sample)
df = pd.read_csv("data/processed/diabetes_features.csv")

X = df.drop(columns=["label"])
X_scaled = scaler.transform(X)

# Use a small background sample for efficiency
background = X_scaled[:100]

# 3️⃣ Initialize SHAP explainer
explainer = shap.LinearExplainer(
    model,
    background,
    feature_perturbation="interventional"
)

# 4️⃣ Explain ONE sample (for now)
sample = X_scaled[0:1]
shap_values = explainer.shap_values(sample)

# 5️⃣ Package explanation cleanly
explanation = dict(
    zip(X.columns, shap_values[0])
)

# Sort by absolute impact
explanation = dict(
    sorted(explanation.items(), key=lambda x: abs(x[1]), reverse=True)
)

print("Diabetes SHAP explanation (top features):")
for k, v in explanation.items():
    print(f"{k}: {round(v, 4)}")

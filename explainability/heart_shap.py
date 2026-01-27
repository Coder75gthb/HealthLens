# explainability/heart_shap.py

import joblib
import shap
import pandas as pd


# 1️⃣ Load trained model & scaler
model = joblib.load("models/heart_model.pkl")
scaler = joblib.load("models/heart_scaler.pkl")

# 2️⃣ Load processed heart data
df = pd.read_csv("data/processed/heart_features.csv")

X = df.drop(columns=["label"])
X_scaled = scaler.transform(X)

# Background sample (small, stable)
background = X_scaled[:100]

# 3️⃣ SHAP explainer for logistic regression
explainer = shap.LinearExplainer(
    model,
    background
)

# 4️⃣ Explain ONE sample
sample = X_scaled[0:1]
shap_values = explainer.shap_values(sample)

# 5️⃣ Sort & display
explanation = dict(
    zip(X.columns, shap_values[0])
)

explanation = dict(
    sorted(explanation.items(), key=lambda x: abs(x[1]), reverse=True)
)

print("Heart Disease SHAP explanation (top features):")
for k, v in explanation.items():
    print(f"{k}: {round(v, 4)}")

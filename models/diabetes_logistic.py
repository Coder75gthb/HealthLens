# models/diabetes_logistic.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score


# 1️⃣ Load processed data
df = pd.read_csv("data/processed/diabetes_features.csv")


# 2️⃣ Separate features and label
X = df.drop(columns=["label"])

# Convert 3-class label into binary diabetes risk
# 0,1 -> no diabetes | 2 -> diabetes
y = (df["label"] == 2).astype(int)



# 3️⃣ Train-validation split
# We keep it simple and reproducible
X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 4️⃣ Scale numeric features
# Logistic regression is sensitive to feature scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)


# 5️⃣ Train baseline logistic regression
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_scaled, y_train)


# 6️⃣ Evaluate
y_pred = model.predict(X_val_scaled)
y_prob = model.predict_proba(X_val_scaled)[:, 1]

print("Accuracy:", round(accuracy_score(y_val, y_pred), 3))
print("ROC-AUC:", round(roc_auc_score(y_val, y_prob), 3))

# 7️⃣ Inspect feature coefficients

feature_names = X.columns
coefficients = model.coef_[0]

coef_df = pd.DataFrame({
    "feature": feature_names,
    "coefficient": coefficients
}).sort_values(by="coefficient", ascending=False)

print("\nLogistic Regression Feature Coefficients:")
print(coef_df)


# --- Export trained objects for reuse ---
import joblib

joblib.dump(model, "models/diabetes_model.pkl")
joblib.dump(scaler, "models/diabetes_scaler.pkl")

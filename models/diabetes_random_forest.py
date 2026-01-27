# models/diabetes_random_forest.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score


# 1️⃣ Load processed data
df = pd.read_csv("data/processed/diabetes_features.csv")

# 2️⃣ Binary label: diabetes vs not
y = (df["label"] == 2).astype(int)
X = df.drop(columns=["label"])

# 3️⃣ Train-validation split (same as logistic)
X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4️⃣ Random Forest (simple, no tuning)
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)

# 5️⃣ Evaluate
y_pred = model.predict(X_val)
y_prob = model.predict_proba(X_val)[:, 1]

print("Accuracy:", round(accuracy_score(y_val, y_pred), 3))
print("ROC-AUC:", round(roc_auc_score(y_val, y_prob), 3))

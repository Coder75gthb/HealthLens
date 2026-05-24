# HealthLens 🔬

> Preventive, explainable health risk estimation — not a diagnosis.

🔗 **Live Demo:** [Click here](https://healthlens-rvyd7ypgzyywjtsnd9chng.streamlit.app/)

HealthLens is an AI-powered preventive health intelligence web app that estimates your risk for multiple chronic conditions, simulates how that risk may evolve over time, and gives you a personalized, explainable action plan — all from basic lifestyle and clinical inputs.

---

## Disclaimer

This project does **not** provide medical diagnosis or treatment. All outputs are risk estimations for educational and preventive awareness purposes only. Always consult a qualified doctor for medical advice.

---

## What It Does

A user enters basic health parameters — age, BMI, blood glucose, cholesterol, systolic BP, smoking status, alcohol consumption, and physical activity level — and HealthLens runs them through trained ML models to estimate risk across four chronic conditions. The app then explains *why* that risk exists, simulates how it may change over 12 months, and generates a fully personalized lifestyle blueprint powered by an LLM.

---

## Features

**Risk Overview**
- Estimates risk percentage for Diabetes, Heart Disease, Hypertension, and Chronic Kidney Disease (CKD)
- Shows severity level (Low / Medium / High) and model confidence score
- Expandable "Why this risk?" explanation for each condition using SHAP-based feature importance

**Risk Trajectory Simulation**
- Simulates how risk may evolve over the next 12 months
- User can select a condition and a lifestyle scenario (no change, moderate improvement, significant improvement)
- Shows projected risk and average monthly change

**Food Insights**
- User enters any food item in free text
- LLM returns advantages, disadvantages, and condition-specific impact for that food

**Personalized Lifestyle Blueprint**
- LLM-generated blueprint tailored to the user's actual risk level, trend, age, BMI, and lifestyle
- Covers food strategy, exercise plan, sleep & recovery, daily micro-habits, and what not to over-focus on
- Every recommendation is tied back to the user's specific context — no generic advice

---

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend / UI | Streamlit |
| ML Models | Scikit-learn (Logistic Regression, Random Forest) |
| Explainability | SHAP |
| LLM Integration | Groq API (LLaMA 3.1 8B Instant) |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Altair |
| Model Serialization | Joblib |
| Environment | Python 3.11 |

---

## ML Models

Four separate binary classifiers are trained — one per condition:

**Diabetes**
- Features engineered from the PIMA-style diabetes dataset
- Label binarized: classes 0/1 → no diabetes, class 2 → diabetes
- Logistic Regression with `class_weight="balanced"` and StandardScaler
- Random Forest (200 estimators) trained as a comparison model
- Final model selected based on ROC-AUC

**Heart Disease**
- Trained on processed heart disease dataset
- Logistic Regression with StandardScaler and `class_weight="balanced"`
- Feature coefficients extracted and analyzed for interpretability

**Hypertension & CKD**
- Similar pipeline: StandardScaler + Logistic Regression
- All models exported as `.pkl` files via Joblib for reuse in the app

---

## Project Structure

| File / Folder | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `data/raw/` | Original datasets |
| `data/processed/` | Feature-engineered CSVs |
| `models/` | Model training scripts + saved `.pkl` files |
| `interaction_engine/risk_engine.py` | Risk scoring logic |
| `interaction_engine/explanations.py` | SHAP-based explanations |
| `interaction_engine/food_engine.py` | Food insights via Groq |
| `interaction_engine/roadmap_engine.py` | Lifestyle blueprint via Groq |
| `explainability/` | SHAP utilities |
| `guidance/` | Condition-specific guidance content |
| `simulation/` | Risk trajectory simulation logic |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version for Streamlit Cloud |

---

## How to Run Locally

```bash
git clone https://github.com/Coder75gthb/healthlens.git
cd healthlens
pip install -r requirements.txt
```

Create a `.env` file in the root:
GROQ_API_KEY=your_groq_api_key_here

Then run:
```bash
streamlit run app.py
```

---

## Conditions Covered

- Diabetes
- Heart Disease
- Hypertension
- Chronic Kidney Disease (CKD)

---

## Key Design Decisions

- **Explainability over accuracy** — SHAP values are used to explain every prediction so users understand *why* their risk is what it is, not just what it is
- **LLM for personalization** — Rule-based lifestyle advice is generic; the Groq-powered blueprint ties every recommendation to the user's actual numbers
- **Preventive framing** — The app is intentionally positioned as a risk awareness tool, not a diagnostic one, with clear disclaimers throughout
- **Balanced classes** — All models use `class_weight="balanced"` to handle dataset imbalance, prioritizing recall over raw accuracy for health risk use cases



# interaction_engine/test_ckd_logic.py

from interaction_engine.ckd_risk import get_ckd_risk_summary


def print_case(title, result):
    print(f"\n=== {title} ===")
    for k, v in result.items():
        print(f"{k}: {v}")


# Case 1: Young, healthy lifestyle, no comorbidities
case_1 = get_ckd_risk_summary(
    age=25,
    bmi=22,
    smoker=False,
    physical_activity="high",
    diabetes_risk=0.1,
    hypertension_risk=0.1,
    bp_provided=False,
    sugar_provided=False,
    cholesterol_provided=False,
)

print_case("Case 1: Young & Healthy", case_1)


# Case 2: Middle-aged, obese, smoker, moderate diabetes & BP risk
case_2 = get_ckd_risk_summary(
    age=52,
    bmi=32,
    smoker=True,
    physical_activity="low",
    diabetes_risk=0.6,
    hypertension_risk=0.55,
    diabetes_trend=0.05,
    hypertension_trend=0.05,
    bp_provided=True,
    sugar_provided=True,
    cholesterol_provided=True,
)

print_case("Case 2: Multiple Risk Factors", case_2)


# Case 3: Older, diabetes improving, BP controlled
case_3 = get_ckd_risk_summary(
    age=60,
    bmi=28,
    smoker=False,
    physical_activity="moderate",
    diabetes_risk=0.7,
    hypertension_risk=0.4,
    diabetes_trend=-0.05,
    hypertension_trend=-0.05,
    bp_provided=True,
    sugar_provided=True,
    cholesterol_provided=True,
)

print_case("Case 3: Improving Control", case_3)

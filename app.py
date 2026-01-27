import streamlit as st
import joblib

from interaction_engine.risk_engine import risk_engine
from interaction_engine.explanations import generate_explanations
from interaction_engine.food_engine import get_food_insights
from interaction_engine.roadmap_engine import generate_lifestyle_blueprint

import numpy as np
import matplotlib.pyplot as plt


st.markdown("""
<style>

/* =====================
   PREMIUM BLUE ANIMATED BACKGROUND
===================== */
html, body, [class*="stApp"] {
    background: linear-gradient(
        -45deg,
        #0f172a,
        #1e3a8a,
        #0c4a6e,
        #020617
    );
    background-size: 400% 400%;
    animation: gradientMove 16s ease infinite;
}

/* Smooth gradient animation */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* =====================
   GLASS CARD CONTAINER
===================== */
.block-container {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 2.2rem;

    /* very light shadow for depth */
    box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.25);

    /* IMPORTANT: remove heavy glass blur */
    backdrop-filter: none;
}

/* =====================
   INPUT POLISH
===================== */
input, select, textarea {
    background-color: rgba(2, 6, 23, 0.85) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* =====================
   LABELS & TEXT
===================== */
label, p, span {
    color: #e5e7eb !important;
}

/* =====================
   SUBTLE INTERACTIONS
===================== */
div[data-testid="stMetric"],
div[data-testid="stExpander"] {
    transition: transform 0.15s ease;
}

div[data-testid="stMetric"]:hover,
div[data-testid="stExpander"]:hover {
    transform: translateY(-2px);
}

/* =====================
   HEADINGS
===================== */
h1, h2, h3 {
    letter-spacing: 0.5px;
    color: #f8fafc;
}
            
/* ======================================================
   FORCE REMOVE BASEWEB SELECT INNER DIVIDER
====================================================== */

/* Remove left divider inside selectbox */
div[data-baseweb="select"] > div > div > div {
    border-left: none !important;
}

/* Remove any pseudo divider */
div[data-baseweb="select"] *::before,
div[data-baseweb="select"] *::after {
    border: none !important;
    box-shadow: none !important;
}

/* Force flat appearance */
div[data-baseweb="select"] {
    box-shadow: none !important;
    border: none !important;
}

/* Kill inner value separator */
div[data-baseweb="select"] span {
    border: none !important;
}

/* ======================================================
   BLEND LEFT SELECT BOX WITH MAIN INPUT
====================================================== */

/* BaseWeb select main container */
div[data-baseweb="select"] > div {
    background-color: rgba(2, 6, 23, 0.85) !important;
}

/* Inner value container (the left block) */
div[data-baseweb="select"] div {
    background-color: rgba(2, 6, 23, 0.85) !important;
}

/* Remove any separator illusion */
div[data-baseweb="select"] * {
    border: none !important;
    box-shadow: none !important;
}

</style>
            
""", unsafe_allow_html=True)





# =====================================================
# RISK TRAJECTORY SIMULATION FUNCTION (UNCHANGED)
# =====================================================
def simulate_risk_trajectory(
    current_risk,
    disease,
    age,
    bmi,
    smoker,
    activity,
    alcohol,
    scenario
):
    months = np.arange(0, 13)

    base_growth = {
        "diabetes": 0.6,
        "heart_disease": 0.7,
        "hypertension": 0.8,
        "ckd": 0.5,
    }.get(disease, 0.6)

    scenario_factor = {
        "No lifestyle change": 1.0,
        "Moderate improvement": 0.4,
        "Aggressive improvement": -0.3,
    }[scenario]

    lifestyle_penalty = 0
    if smoker:
        lifestyle_penalty += 0.3
    if activity == "low":
        lifestyle_penalty += 0.2
    if bmi >= 30:
        lifestyle_penalty += 0.3

    if alcohol == "Frequent":
        lifestyle_penalty += 0.25
    elif alcohol == "Occasional":
        lifestyle_penalty += 0.1

    age_factor = 0.5 if age < 30 else 1.0 if age <= 50 else 1.2

    monthly_change = (
        base_growth + lifestyle_penalty
    ) * scenario_factor * age_factor

    trajectory = []
    risk = current_risk

    for _ in months:
        trajectory.append(min(max(risk, 0), 85))
        risk += monthly_change

    return months, trajectory

def infer_primary_drivers(age, bmi, smoker, activity,alcohol):
    """
    Roughly interpret which factors are driving risk.
    This is explanatory, not medical.
    """
    drivers = []

    if activity == "low":
        drivers.append(("Physical inactivity", "High"))
    elif activity == "moderate":
        drivers.append(("Physical inactivity", "Moderate"))
    else:
        drivers.append(("Physical inactivity", "Low"))

    if bmi >= 30:
        drivers.append(("BMI", "High"))
    elif bmi >= 25:
        drivers.append(("BMI", "Moderate"))
    else:
        drivers.append(("BMI", "Low"))

    if smoker:
        drivers.append(("Smoking", "Moderate"))
    else:
        drivers.append(("Smoking", "Low"))

    if age >= 50:
        drivers.append(("Age-related factors", "Moderate"))
    else:
        drivers.append(("Age-related factors", "Low"))


    if alcohol == "Frequent":
        drivers.append(("Alcohol consumption", "Moderate"))
    elif alcohol == "Occasional":
        drivers.append(("Alcohol consumption", "Low"))
    else:
        drivers.append(("Alcohol consumption", "Minimal"))


    return drivers






def get_trend(current_risk: float, final_risk: float) -> str:
    """
    Interprets simulation outcome into a simple trend label.
    """
    if abs(final_risk - current_risk) < 0.5:
        return "stable"
    elif final_risk < current_risk:
        return "improving"
    else:
        return "worsening"


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="HealthLens",

    layout="wide"
)


# =====================================================
# LOAD MODELS
# =====================================================
@st.cache_resource(show_spinner=False)

def load_assets():
    return {
        "diabetes": joblib.load("models/diabetes_model.pkl"),
        "heart": joblib.load("models/heart_model.pkl"),
    }

assets = load_assets()


# =====================================================
# INPUTS
# =====================================================
st.title(" HealthLens")
st.caption("Preventive, explainable health risk estimation- not a diagnosis.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age (years)", 18, 100, 25)
    bmi = st.number_input("BMI", 10.0, 60.0, 22.0, 0.1)

with col2:
    smoker = st.selectbox("Smoking Status", ["No", "Yes"])
    alcohol = st.selectbox(
    "Alcohol Consumption",
    ["No / Rare", "Occasional", "Frequent"]
)

    physical_activity = st.selectbox(
        "Physical Activity Level", ["Low", "Moderate", "High"]
    )

with col3:
    bp = st.number_input("Systolic BP (mmHg)", 0, 250, 0)
    glucose = st.number_input("Blood Glucose (mg/dL)", 0, 400, 0)
    cholesterol = st.number_input("Cholesterol (mg/dL)", 0, 400, 0)

st.divider()


# =====================================================
# BMI CALCULATOR (ASSISTIVE TOOL)
# =====================================================
with st.expander(" Calculate BMI (optional)", expanded=False):
    st.caption(
        "Enter height and weight to calculate BMI automatically."
    )

    c1, c2 = st.columns(2)

    with c1:
        height_cm = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=170
        )

    with c2:
        weight_kg = st.number_input(
            "Weight (kg)",
            min_value=30,
            max_value=200,
            value=65
        )

    height_m = height_cm / 100

    if height_m > 0:
        calculated_bmi = weight_kg / (height_m ** 2)

        st.markdown(f"### Your BMI: **{calculated_bmi:.2f}**")

        # BMI category
        if calculated_bmi < 18.5:
            category = "Underweight"
        elif calculated_bmi < 25:
            category = "Normal"
        elif calculated_bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        st.write(f"**Category:** {category}")

        # Optional helper note
        st.caption(
            "BMI is a screening metric, not a diagnosis. "
            "Muscle mass and body composition are not considered."
        )


# =====================================================
# ANALYZE BUTTON
# =====================================================
if st.button("🔍 Analyze My Health Risk", use_container_width=True):
    results = risk_engine(
        age=age,
        bmi=bmi,
        smoker=(smoker == "Yes"),
        physical_activity=physical_activity.lower(),
        bp=bp if bp > 0 else None,
        glucose=glucose if glucose > 0 else None,
        cholesterol=cholesterol if cholesterol > 0 else None,
        diabetes_model=assets["diabetes"],
        heart_model=assets["heart"],
    )
    st.session_state["results"] = results


# =====================================================
# TABS
# =====================================================
tabs = st.tabs([
    "📊 Risk Overview",
    "📈 Simulation",
    "🥗 Food Insights",
    "🧭 Lifestyle Blueprint"
])



# =====================================================
# TAB 1 — RISK OVERVIEW (UNCHANGED)
# =====================================================
with tabs[0]:
    if "results" in st.session_state:
        user_inputs = {
            "age": age,
            "bmi": bmi,
            "smoker": (smoker == "Yes"),
            "physical_activity": physical_activity.lower(),
            "alcohol": alcohol  
        }

        for disease, data in st.session_state["results"].items():
            st.subheader(disease.replace("_", " ").title())

            risk = data["risk_percent"]
            st.progress(int(risk))
            st.write(f"**Risk:** {risk}%")
            st.write(f"**Severity:** {data['severity']}")
            st.write(f"**Confidence:** {data['confidence']}")

            with st.expander("Why this risk?"):
                # Existing explanations
                for p in generate_explanations(disease, data, user_inputs):
                    st.write("•", p)

                # -----------------------------
                # Alcohol-specific reasoning
                # -----------------------------
                if alcohol == "Frequent":
                    st.write(
                        "• **Alcohol consumption:** Frequent intake can subtly "
                        "increase long-term risk by affecting blood pressure stability, "
                        "sleep quality, and metabolic recovery."
                    )
                elif alcohol == "Occasional":
                    st.write(
                        "• **Alcohol consumption:** Occasional intake has a mild "
                        "impact but can contribute to gradual risk increase over time "
                        "if combined with other factors."
                    )
                else:
                    st.write(
                        "• **Alcohol consumption:** Minimal impact at your current "
                        "intake level."
                    )

            st.markdown("---")




# =====================================================
# TAB 2 — 📈 SIMULATION (ENHANCED & INFORMATIVE)
# =====================================================
with tabs[1]:
    if "results" not in st.session_state:
        st.warning("Please analyze your health risk first.")
    else:
        st.subheader("📈 Risk Trajectory Simulation")
        st.caption(
            "How your health risk may evolve over the next 12 months  "
            "compared to doing nothing, and why it behaves this way."
        )

        # -------------------------------------------------
        # Controls
        # -------------------------------------------------
        disease = st.selectbox(
            "Select condition",
            list(st.session_state["results"].keys()),
            format_func=lambda x: x.replace("_", " ").title(),
            key="sim_disease"
        )

        scenario = st.selectbox(
            "Lifestyle scenario",
            [
                "No lifestyle change",
                "Moderate improvement",
                "Aggressive improvement"
            ],
            key="sim_scenario"
        )

        current_risk = st.session_state["results"][disease]["risk_percent"]

        # -------------------------------------------------
        # Run simulations
        # -------------------------------------------------
        months, baseline_trajectory = simulate_risk_trajectory(
            current_risk=current_risk,
            disease=disease,
            age=age,
            bmi=bmi,
            smoker=(smoker == "Yes"),
            activity=physical_activity.lower(),
            alcohol=alcohol,
            scenario="No lifestyle change"
        )

        months, scenario_trajectory = simulate_risk_trajectory(
            current_risk=current_risk,
            disease=disease,
            age=age,
            bmi=bmi,
            smoker=(smoker == "Yes"),
            activity=physical_activity.lower(),
            alcohol=alcohol,
            scenario=scenario
        )

        final_baseline = baseline_trajectory[-1]
        final_scenario = scenario_trajectory[-1]
        net_change = final_scenario - current_risk
        delta_vs_baseline = final_baseline - final_scenario
        monthly_rate = net_change / 12

        # -------------------------------------------------
        # Key numbers
        # -------------------------------------------------
        c1, c2, c3 = st.columns(3)

        c1.metric("Current Risk", f"{current_risk:.1f}%")

        c2.metric(
            "Projected Risk (12 months)",
            f"{final_scenario:.1f}%",
            delta=f"{net_change:.1f}%"
        )

        c3.metric(
            "Average Monthly Change",
            f"{monthly_rate:.2f}% / month"
        )

        # -------------------------------------------------
        # Plot
        # -------------------------------------------------
        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(
            months,
            baseline_trajectory,
            linestyle="--",
            linewidth=1.5,
            label="No lifestyle change"
        )

        ax.plot(
            months,
            scenario_trajectory,
            marker="o",
            linewidth=2,
            label=scenario
        )

        ax.fill_between(
            months,
            baseline_trajectory,
            scenario_trajectory,
            alpha=0.08
        )

        ax.set_xlabel("Months")
        ax.set_ylabel("Risk (%)")
        ax.set_title(
            f"{disease.replace('_', ' ').title()} Risk Projection"
        )

        ax.set_ylim(0, 100)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()

        trend_label = (
            "Improving ↓" if delta_vs_baseline > 0
            else "Worsening ↑" if delta_vs_baseline < 0
            else "Stable →"
        )

        ax.annotate(
            f"{final_scenario:.1f}% ({trend_label})",
            xy=(months[-1], final_scenario),
            xytext=(months[-1] - 3, final_scenario + 6),
            arrowprops=dict(arrowstyle="->", alpha=0.6),
            fontsize=9
        )

        st.pyplot(fig)

        # -------------------------------------------------
        # Interactive inspection
        # -------------------------------------------------
        inspect_month = st.slider(
            "Inspect projected risk at a specific month",
            0, 12, 12
        )

        st.write(
            f"**Month {inspect_month}:** "
            f"Projected risk ≈ "
            f"{scenario_trajectory[inspect_month]:.1f}%"
        )

        # -------------------------------------------------
        # Driver reasoning
        # -------------------------------------------------
        st.markdown("###  What is influencing your risk the most")
        st.caption(
            "These factors have the strongest influence on how your risk changes over time."
        )

        drivers = infer_primary_drivers(
            age=age,
            bmi=bmi,
            smoker=(smoker == "Yes"),
            activity=physical_activity.lower(),
            alcohol=alcohol
        )

        for name, impact in drivers:
            st.write(f"• **{name}**  {impact} impact")

        # -------------------------------------------------
        # Interpretation (personalized)
        # -------------------------------------------------
        st.markdown("###  How to interpret this trend")

        if abs(delta_vs_baseline) < 1:
            st.write(
                "The projected change is small. At your current risk level, "
                "health risks usually shift gradually, so steady habits matter "
                "more than short bursts of effort."
            )
        elif delta_vs_baseline < 3:
            st.write(
                "The improvement is modest but meaningful. "
                "Maintaining these habits over time can slowly bend the risk curve "
                "in a healthier direction."
            )
        else:
            st.write(
                "The improvement is significant. "
                "Sustaining these changes could meaningfully reduce long-term risk "
                "rather than just short-term fluctuations."
            )

        # -------------------------------------------------
        # Disease-aware explanation
        # -------------------------------------------------
        st.markdown("**Why this behaves this way for you**")

        if disease == "diabetes":
            st.write(
                "Diabetes-related risk usually changes gradually because improvements "
                "in glucose regulation and insulin sensitivity take time to stabilize."
            )
        elif disease == "heart_disease":
            st.write(
                "Heart disease risk responds slowly since cardiovascular and metabolic "
                "changes accumulate over months rather than weeks."
            )
        elif disease == "hypertension":
            st.write(
                "Hypertension-related risk can respond earlier to lifestyle changes, "
                "but consistency is required to prevent fluctuations."
            )
        elif disease == "ckd":
            st.write(
                "Kidney-related risk is often less reversible, which is why projected "
                "changes appear more conservative and gradual."
            )

        # -------------------------------------------------
        # Actionable insight
        # -------------------------------------------------
        st.markdown("### What would move this curve faster for YOU")
        st.caption(
            "Based on your current profile, these factors would have the strongest impact."
        )

        if physical_activity.lower() == "low":
            st.write(
                "• Increasing physical activity would likely have the largest "
                "impact on accelerating risk reduction."
            )

        if bmi >= 25:
            st.write(
                "• Improving weight-related factors could amplify long-term gains."
            )

        if smoker == "Yes":
            st.write(
                "• Smoking cessation would substantially improve the projected trajectory."
            )

        st.caption(
            "This simulation reflects trends, not exact outcomes. "
            "Real-world results depend on consistency, duration, and adherence."
        )





# =====================================================
# TAB 3 —  FOOD INSIGHTS (FIXED & SAFE)
# =====================================================
with tabs[2]:

    if "results" not in st.session_state:
        st.warning("Please analyze your health risk first.")
    else:
        st.subheader(" Personalized Food Insights")
        st.caption("Type any food - explanation based, no judgement.")

        food_input = st.text_input(
            "Enter any food (e.g. Maggi, butter chicken, oats with milk)"
        )

        if food_input:
            result = get_food_insights(food_input)

            st.markdown(f"###  About **{food_input.title()}**")

            if result["what_is_good"]:
                st.markdown("####  What’s good")
                for g in result["what_is_good"]:
                    st.write("•", g)

            if result["what_to_watch_out_for"]:
                st.markdown("#### ⚠️ What to watch out for")
                for c in result["what_to_watch_out_for"]:
                    st.write("•", c)

            if result["healthier_swaps_or_tips"]:
                st.markdown("#### 🔁 Smarter swaps / tips")
                for s in result["healthier_swaps_or_tips"]:
                    st.write("•", s)

            st.caption(f"Confidence level: **{result['confidence']}**")


# =====================================================
# TAB 4 —  LIFESTYLE BLUEPRINT (FINAL UI)
# =====================================================
with tabs[3]:
    if "results" not in st.session_state:
        st.warning("Please analyze your health risk first.")
    else:
        st.subheader("Personalized Lifestyle Blueprint")
        st.caption(
            "Contextual guidance explaining what to focus on and why it matters for you."
        )

        disease = st.selectbox(
            "Focus condition",
            list(st.session_state["results"].keys()),
            format_func=lambda x: x.replace("_", " ").title(),
            key="bp_disease"
        )

        current_risk = st.session_state["results"][disease]["risk_percent"]

        # ---- Simulation to derive trend ----
        months, trajectory = simulate_risk_trajectory(
            current_risk=current_risk,
            disease=disease,
            age=age,
            bmi=bmi,
            smoker=(smoker == "Yes"),
            activity=physical_activity.lower(),
            alcohol=alcohol,
            scenario="Moderate improvement"
        )

        trend = get_trend(current_risk, trajectory[-1])

        if st.button("Generate my lifestyle blueprint"):
            blueprint = generate_lifestyle_blueprint(
                disease=disease.replace("_", " "),
                risk_percent=current_risk,
                trend=trend,
                age=age,
                bmi=bmi,
                smoker=(smoker == "Yes"),
                activity_level=physical_activity.lower(),
                
            )

            # ---- Context Summary ----
            st.markdown("### Why this matters for you")
            st.write(blueprint["context_summary"])

            # ---- Food Strategy ----
            with st.expander(" Food Strategy"):
                st.markdown(f"*{blueprint['food_strategy']['why_it_matters']}*")

                st.markdown("**Focus on:**")
                for item in blueprint["food_strategy"]["focus"]:
                    st.write(f"• {item}")

                st.markdown("**Limit:**")
                for item in blueprint["food_strategy"]["limit"]:
                    st.write(f"• {item}")

                st.markdown("**Practical swaps:**")
                for item in blueprint["food_strategy"]["practical_swaps"]:
                    st.write(f"• {item}")

            # ---- Exercise Plan ----
            with st.expander(" Exercise Plan"):
                st.markdown(f"*{blueprint['exercise_plan']['why_it_matters']}*")

                st.markdown("**Aerobic activity:**")
                st.write(f"• Type: {blueprint['exercise_plan']['aerobic']['type']}")
                st.write(f"• Duration: {blueprint['exercise_plan']['aerobic']['duration']}")
                st.write(f"• Frequency: {blueprint['exercise_plan']['aerobic']['frequency']}")

                st.markdown("**Strength training:**")
                st.write(f"• Type: {blueprint['exercise_plan']['strength']['type']}")
                st.write(f"• Frequency: {blueprint['exercise_plan']['strength']['frequency']}")

            # ---- Sleep & Recovery ----
            with st.expander(" Sleep & Recovery"):
                st.markdown(f"*{blueprint['sleep_recovery']['why_it_matters']}*")
                st.write(f"**Target sleep:** {blueprint['sleep_recovery']['target_duration']}")

                for habit in blueprint["sleep_recovery"]["habits"]:
                    st.write(f"• {habit}")

            # ---- Daily Micro-Habits ----
            with st.expander(" Daily Micro-Habits"):
                st.markdown(f"*{blueprint['daily_micro_habits']['why_it_matters']}*")

                for action in blueprint["daily_micro_habits"]["actions"]:
                    st.write(f"• {action}")

            # ---- Avoid Overfocus ----
            with st.expander(" What not to over-focus on"):
                st.markdown(f"*{blueprint['avoid_overfocus']['why_it_matters']}*")

                for item in blueprint["avoid_overfocus"]["items"]:
                    st.write(f"• {item}")

            st.caption(f"Confidence level: {blueprint['confidence']}")



import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
import json

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CoachBot AI", page_icon="🏋️", layout="centered")

# Get API key from Streamlit Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("GOOGLE_API_KEY not found. Add it in Streamlit → App Settings → Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- UI ----------------
st.title("🏋️ CoachBot AI")
st.caption("AI-powered personalized fitness & sports coaching (data + graphs)")

st.divider()

sport = st.text_input("Sport", placeholder="e.g., Football, Cricket, Basketball")
position = st.text_input("Player Position", placeholder="e.g., Striker, Bowler, Guard")
goal = st.text_input("Primary Goal", placeholder="e.g., Build stamina, Strength, Recovery")
injury = st.text_input("Injury / Risk Area", placeholder="e.g., Knee strain, None")
diet = st.selectbox("Diet Preference", ["No Preference", "Vegetarian", "Non-Vegetarian", "Vegan"])

st.divider()

feature = st.selectbox(
    "What would you like to generate?",
    [
        "Full Workout Plan",
        "Recovery & Injury-Safe Training",
        "Weekly Nutrition Plan",
        "Warm-up & Cooldown Routine",
        "Tactical Improvement Tips"
    ]
)

# ---------------- PROMPT LOGIC ----------------
def build_prompt(feature):
    """
    Ask the AI to output structured JSON data instead of paragraphs.
    Each entry includes Day, Workout/Task, Intensity (1-100).
    """
    base = f"""
You are a professional sports coach.

Athlete Profile:
Sport: {sport}
Position: {position}
Goal: {goal}
Injury/Risk Area: {injury}
Diet Preference: {diet}

Follow safe training practices. Avoid medical diagnosis.

Output 7 entries for the week (Monday to Sunday) as JSON.
Format each entry as:
{{"Day": "Monday", "Workout": "Squats, Push-ups", "Intensity": 70}}

Do NOT include any text outside JSON.
"""

    prompts = {
        "Full Workout Plan": base,
        "Recovery & Injury-Safe Training": base.replace("Workout", "Recovery Routine"),
        "Weekly Nutrition Plan": base.replace("Workout", "Meals"),
        "Warm-up & Cooldown Routine": base.replace("Workout", "Warm-up & Cooldown"),
        "Tactical Improvement Tips": base.replace("Workout", "Tactical Tips")
    }

    return prompts[feature]

# ---------------- GENERATION ----------------
if st.button("Generate Plan"):
    if not sport or not goal:
        st.warning("Please enter at least the Sport and Goal.")
    else:
        with st.spinner("CoachBot AI is generating..."):
            try:
                response = model.generate_content(
                    build_prompt(feature),
                    generation_config={"temperature":0.3, "max_output_tokens":800}
                )

                # Parse JSON from AI
                try:
                    plan_data = json.loads(response.text)
                    df = pd.DataFrame(plan_data)
                except Exception:
                    st.error(f"Failed to parse AI output as JSON.\nRaw output:\n{response.text}")
                    st.stop()

                # Show as table
                st.subheader("📋 Weekly Plan Table")
                st.dataframe(df)

                # Show graph if Intensity exists
                if "Intensity" in df.columns:
                    st.subheader("📈 Weekly Intensity Graph")
                    fig, ax = plt.subplots()
                    ax.plot(df["Day"], df["Intensity"], marker="o")
                    ax.set_xlabel("Day")
                    ax.set_ylabel("Intensity")
                    ax.set_title("Weekly Training Load")
                    st.pyplot(fig)

            except Exception as e:
                st.error(f"Error generating plan: {str(e)}")

st.divider()
st.caption("⚠️ AI-generated advice is for educational purposes only.")

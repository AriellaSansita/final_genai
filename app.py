import os
import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key=os.getenv("AIzaSyBv2dnTTYh3CPHmnRCDO8NQeOcAyRIectw"))
model = genai.GenerativeModel("gemini-2.5 Flash")

st.set_page_config(page_title="CoachBot AI", page_icon="🏋️", layout="centered")

# ---------------- UI ----------------
st.title("🏋️ CoachBot AI")
st.caption("AI-powered personalized fitness & sports coaching")

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
    base = f"""
You are a certified professional sports coach and fitness trainer.

Athlete Profile:
Sport: {sport}
Position: {position}
Goal: {goal}
Injury/Risk Area: {injury}
Diet Preference: {diet}

Follow safe training practices. Avoid medical diagnosis.
"""

    prompts = {
        "Full Workout Plan": base + "Generate a detailed and safe weekly workout plan.",
        "Recovery & Injury-Safe Training": base + "Generate a recovery-focused and injury-safe training routine.",
        "Weekly Nutrition Plan": base + "Generate a simple weekly nutrition plan aligned with the goal.",
        "Warm-up & Cooldown Routine": base + "Generate an effective warm-up and cooldown routine.",
        "Tactical Improvement Tips": base + "Provide tactical and performance improvement tips for the position."
    }

    return prompts[feature]

# ---------------- GENERATION ----------------
if st.button("Generate Plan"):
    if not sport or not goal:
        st.warning("Please enter at least the Sport and Goal.")
    else:
        with st.spinner("CoachBot AI is thinking..."):
            response = model.generate_content(
                build_prompt(feature),
                generation_config={
                    "temperature": 0.5,
                    "max_output_tokens": 600
                }
            )

        st.subheader("📋 AI Generated Output")
        st.write(response.text)

st.divider()
st.caption("⚠️ AI-generated advice is for educational purposes only.")

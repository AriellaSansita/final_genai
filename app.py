import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="CoachBot AI", layout="wide")

st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.write("Personalized AI Coach for Young Athletes")

# ---------------- USER INPUT ----------------
sport = st.selectbox("Select Sport", ["Football", "Cricket", "Basketball", "Athletics", "Other"])
position = st.text_input("Player Position")
injury = st.text_input("Injury History / Risk Area (write 'None' if no injury)")
goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"])
diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
intensity = st.selectbox("Training Intensity", ["Low", "Moderate", "High"])
weakness = st.text_input("Biggest Weakness (optional)")
age = st.slider("Age", 10, 25, 15)

# ---------------- FEATURE SELECT ----------------
feature = st.selectbox(
    "Choose Coaching Feature",
    [
        # Mandatory
        "Full Workout Plan",
        "Injury Recovery Plan",
        "Tactical Coaching",
        "Nutrition Plan",
        "Warm-up & Cooldown",
        "Stamina Builder",
        "Mental Focus Training",
        "Hydration Strategy",
        "Skill Drills",
        "Weekly Training Plan",

        # Optional
        "Progress Predictor",
        "Weakness Analyzer",
        "Match Strategy",
        "Pre-Match Routine",
        "Post-Match Recovery",
        "Motivation Coach",
        "Injury Risk Predictor",
        "Mobility & Stretching",
        "Tournament Preparation",
        "Hydration Optimizer"
    ]
)

# ---------------- PROMPT BUILDER ----------------
def build_prompt():
    base = f"""
    You are a professional youth sports coach AI.

    Athlete Profile:
    Sport: {sport}
    Position: {position}
    Age: {age}
    Injury History: {injury}
    Training Intensity: {intensity}
    Diet: {diet}
    Goal: {goal}
    Weakness: {weakness}
    """

    prompts = {
        # Mandatory
        "Full Workout Plan": "Generate a full-body personalized workout plan.",
        "Injury Recovery Plan": "Create a safe recovery training program avoiding injury risk.",
        "Tactical Coaching": "Provide tactical and decision-making coaching tips.",
        "Nutrition Plan": "Generate a weekly athlete nutrition plan.",
        "Warm-up & Cooldown": "Create a warm-up and cooldown routine for injury prevention.",
        "Stamina Builder": "Design a stamina and endurance improvement program.",
        "Mental Focus Training": "Provide mental training and focus strategies for competition.",
        "Hydration Strategy": "Suggest hydration and electrolyte balance strategy.",
        "Skill Drills": "Generate skill improvement drills specific to the athlete.",
        "Weekly Training Plan": "Create a balanced weekly training schedule.",

        # Optional
        "Progress Predictor": "Predict athlete improvement over 4 weeks and adjust training.",
        "Weakness Analyzer": "Analyze weakness and suggest corrective exercises.",
        "Match Strategy": "Generate match-day strategy and positioning advice.",
        "Pre-Match Routine": "Create a pre-match preparation routine.",
        "Post-Match Recovery": "Generate post-match recovery and muscle repair plan.",
        "Motivation Coach": "Provide motivation and discipline coaching.",
        "Injury Risk Predictor": "Identify possible injury risks and prevention strategies.",
        "Mobility & Stretching": "Generate mobility and flexibility routine.",
        "Tournament Preparation": "Create a 2-week tournament preparation plan.",
        "Hydration Optimizer": "Optimize hydration schedule based on training intensity."
    }

    return base + "\nTask: " + prompts[feature]


# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):

    prompt = build_prompt()

    with st.spinner("CoachBot is thinking..."):
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.6,
                    "top_p": 0.9,
                    "max_output_tokens": 800
                }
            )
            st.success("CoachBot Advice Generated")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")


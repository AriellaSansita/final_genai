import streamlit as st
import google.generativeai as genai
import pandas as pd
import random

# ---------------- CONFIG ----------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="CoachBot AI", layout="wide")
st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.write("AI-powered personalized coach for young athletes")

# ---------------- USER INPUT ----------------
sports_list = [
    "Football","Cricket","Basketball","Athletics","Badminton","Tennis",
    "Hockey","Volleyball","Kabaddi","Table Tennis","Swimming","Martial Arts","Other"
]

sport = st.selectbox("Sport", sports_list)

positions_by_sport = {
    "Football": ["Goalkeeper","Defender","Midfielder","Winger","Striker"],
    "Cricket": ["Batsman","Bowler","All-Rounder","Wicket Keeper"],
    "Basketball": ["Point Guard","Shooting Guard","Small Forward","Power Forward","Center"],
    "Athletics": ["Sprinter","Long Distance Runner","Jumper","Thrower"],
    "Badminton": ["Singles Player","Doubles Player"],
    "Tennis": ["Singles Player","Doubles Player"],
    "Hockey": ["Goalkeeper","Defender","Midfielder","Forward"],
    "Volleyball": ["Setter","Libero","Spiker","Blocker"],
    "Kabaddi": ["Raider","Defender","All-Rounder"],
    "Table Tennis": ["Singles Player","Doubles Player"],
    "Swimming": ["Freestyle Specialist","Backstroke Specialist","Butterfly Specialist"],
    "Martial Arts": ["Striker","Grappler","Mixed Fighter"]
}

if sport == "Other":
    sport = st.text_input("Enter Your Sport") or "General Sport"
    position = st.text_input("Enter Position") or "Athlete"
else:
    position = st.selectbox("Player Position", positions_by_sport.get(sport, ["Athlete"]))

injury = st.text_input("Injury History (None if no injury)")
goal = st.selectbox("Primary Goal", ["Stamina","Strength","Speed","Recovery","Skill Improvement"])
diet = st.selectbox("Diet Type", ["Vegetarian","Non-Vegetarian","Vegan"])
intensity = st.selectbox("Training Intensity", ["Low","Moderate","High"])
age = st.slider("Age", 10, 50, 18)
training_days = st.slider("Training Days / Week", 1, 7, 4)
session_duration = st.slider("Session Duration (minutes)", 30, 180, 90)

# ---------------- FEATURES ----------------
features = [
    "Full Workout Plan","Injury Recovery Plan","Weekly Training Plan",
    "Stamina Builder","Nutrition Plan","Hydration Strategy",
    "Warm-up & Cooldown","Tactical Coaching","Mental Focus Training",
    "Skill Drills","Progress Predictor","Match Strategy",
    "Pre-Match Routine","Post-Match Recovery","Injury Risk Predictor",
    "Mobility & Stretching","Tournament Preparation"
]

selected_feature = st.selectbox("Choose Coaching Feature", features)

# ---------------- NUTRITION ----------------
def generate_nutrition():

    carbs = ["Oats","Brown Rice","Quinoa","Sweet Potato","Whole Wheat"]
    protein_veg = ["Lentils","Chickpeas","Tofu","Tempeh","Beans","Paneer"]
    protein_nonveg = ["Eggs","Chicken","Fish"]
    fats = ["Nuts","Seeds","Olive Oil","Peanut Butter"]

    protein = protein_nonveg if diet == "Non-Vegetarian" else protein_veg

    return pd.DataFrame({
        "Meal": ["Breakfast","Lunch","Dinner","Snacks"],
        "Plan": [
            f"{random.choice(carbs)} + {random.choice(protein)}",
            f"Balanced: {random.choice(carbs)}, {random.choice(protein)}, Vegetables",
            f"Recovery: {random.choice(protein)} + Vegetables",
            f"{random.choice(fats)} + Fruit"
        ]
    })

# ---------------- AI PROMPT ----------------
def build_prompt():

    prompt = f"""
You are a professional youth sports coach AI.

Athlete:
Sport: {sport}
Position: {position}
Age: {age}
Goal: {goal}
Injury: {injury}
Intensity: {intensity}
Diet: {diet}
Training Days: {training_days}
Session Duration: {session_duration}

Include ONLY module: {selected_feature}

General Rules:
- Max 220 words
- Bullet points
- Practical and structured
- No motivation fluff
"""

    if selected_feature in ["Full Workout Plan","Weekly Training Plan","Stamina Builder"]:
        prompt += f"""

Workout Rules:
- Total session MUST equal {session_duration} minutes
- Warmup: 10 min
- Cooldown: 10 min
- Remaining time split 50/50 between Cardio and Strength
- Never exceed total time
"""

    if selected_feature == "Pre-Match Routine":
        prompt += """

Pre-Match Rules:
- Single session only (NOT 6 days)
- 20–40 minutes total
- Focus on activation, reaction, sharpness
- No heavy strength blocks
"""

    return prompt

# ---------------- AI CALL ----------------
def get_ai_text(prompt):
    try:
        r = model.generate_content(prompt)
        return r.candidates[0].content.parts[0].text if r and r.candidates else "⚠️ No AI output"
    except Exception as e:
        if "quota" in str(e).lower():
            return "⚠️ API quota exceeded. Try again later."
        return f"Error: {e}"

# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):

    with st.spinner("AI Coach thinking..."):
        output = get_ai_text(build_prompt())

    st.subheader("📋 AI Coaching Output")
    st.write(output)

    if selected_feature == "Weekly Training Plan":
        st.subheader("📅 Weekly Schedule")
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        focus_pool = ["Stamina","Strength","Skill","Mobility","Speed","Recovery","Tactical"]
        schedule = [focus_pool[i] if i < training_days else "Rest" for i in range(7)]
        st.table(pd.DataFrame({"Day": days, "Focus": schedule}).set_index("Day"))

    if selected_feature == "Nutrition Plan":
        st.subheader("🥗 Nutrition Guide")
        st.dataframe(generate_nutrition())

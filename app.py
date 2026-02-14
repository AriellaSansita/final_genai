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

# ---------------- FEATURE DROPDOWN ----------------
features = [
    "Full Workout Plan","Injury Recovery Plan","Weekly Training Plan",
    "Stamina Builder","Nutrition Plan","Hydration Strategy",
    "Warm-up & Cooldown","Tactical Coaching","Mental Focus Training",
    "Skill Drills","Progress Predictor","Match Strategy",
    "Pre-Match Routine","Post-Match Recovery","Injury Risk Predictor",
    "Mobility & Stretching","Tournament Preparation"
]

selected_feature = st.selectbox("Choose Coaching Feature", features)

# ---------------- WORKOUT TABLE ----------------
def generate_workout_table():

    exercises = [
        {"name": "Squats", "type": "strength"},
        {"name": "Lunges", "type": "strength"},
        {"name": "Glute Bridges", "type": "strength"},
        {"name": "Calf Raises", "type": "strength"},
        {"name": "Cycling / Brisk Walk", "type": "cardio"}
    ]

    # ---- FIXED STRUCTURE ----
    warmup = 10
    cooldown = 10
    usable = session_duration - warmup - cooldown

    # Split remaining time evenly
    cardio_block = usable // 2
    strength_block = usable - cardio_block   # ensures perfect total

    rows = []

    strength_exercises = exercises[:-1]
    cardio_exercise = exercises[-1]

    # Even distribution across strength exercises
    time_per_strength = strength_block / len(strength_exercises)

    sets = 1 if intensity == "Low" else 2 if intensity == "Moderate" else 3

    for ex in strength_exercises:
        rows.append({
            "Exercise": ex["name"],
            "Sets": sets,
            "Reps / Time": f"12-15 reps (~{round(time_per_strength)} min)"
        })

    rows.append({
        "Exercise": cardio_exercise["name"],
        "Sets": "-",
        "Reps / Time": f"{cardio_block} min steady pace"
    })

    return pd.DataFrame(rows)


# ---------------- AI PROMPT ----------------
def build_prompt():

    return f"""
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

Rules:
- Max 220 words
- Bullet points
- Practical, structured, realistic
- No motivation fluff
- If arm injury: NO planks, NO pushups, NO jumps, NO arm loading

Workout Rules:
- Total session MUST equal {session_duration} minutes
- Warmup: 10 min
- Cooldown: 10 min
- Remaining time split EVENLY between Cardio and Strength
- Cardio ≈ Strength (50/50 split)
- Never exceed total time
- If arm injury → NO planks, NO pushups, NO arm load, NO jumps
- Every day MUST show exact time split matching above
"""

# ---------------- AI CALL ----------------
def get_ai_text(prompt):
    try:
        r = model.generate_content(prompt)
        if not r or not r.candidates:
            return "⚠️ No AI output"
        return r.candidates[0].content.parts[0].text
    except Exception as e:
        return f"Error: {e}"

# ---------------- NUTRITION ----------------
def generate_nutrition():

    carbs = ["Oats","Brown Rice","Quinoa","Sweet Potato","Whole Wheat"]
    protein_veg = ["Lentils","Chickpeas","Tofu","Tempeh","Beans"]
    protein_nonveg = ["Eggs","Chicken","Fish","Paneer"]
    fats = ["Nuts","Seeds","Olive Oil","Peanut Butter"]

    protein = protein_veg if diet != "Non-Vegetarian" else protein_nonveg

    return pd.DataFrame({
        "Meal":["Breakfast","Lunch","Dinner","Snacks"],
        "Plan":[
            f"{random.choice(carbs)} + {random.choice(protein)}",
            f"Balanced: {random.choice(carbs)}, {random.choice(protein)}, Veggies",
            f"Recovery: {random.choice(protein)} + Veggies",
            f"{random.choice(fats)} + Fruit"
        ]
    })

# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):

    with st.spinner("AI Coach thinking..."):
        output = get_ai_text(build_prompt())

    st.subheader("📋 AI Coaching Output")
    st.write(output)

    if selected_feature == "Full Workout Plan":
        st.subheader("🏋️ Workout Plan")
        st.dataframe(generate_workout_table())

    if selected_feature == "Weekly Training Plan":
        st.subheader("📅 Weekly Schedule")

        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        focus_pool = [
            "Stamina + Cardio","Strength","Skill + Tactical",
            "Mobility","Speed","Technique","Recovery"
        ]

        schedule = [focus_pool[i] if i < training_days else "Rest" for i in range(7)]
        st.table(pd.DataFrame({"Day": days, "Focus": schedule}).set_index("Day"))

    if selected_feature == "Nutrition Plan":
        st.subheader("🥗 Nutrition Guide")
        st.dataframe(generate_nutrition())


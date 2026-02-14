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

    # Decide sets based on intensity
    if intensity == "Low":
        sets = 2
    elif intensity == "Moderate":
        sets = 3
    else:
        sets = 4
    
    for ex in strength_exercises:
        rows.append({
            "Exercise": ex["name"],
            "Sets": sets,
            "Reps / Time": f"12-15 reps (~{time_per_strength} min)"
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
- - If arm injury → STRICT BAN: no planks, no side planks, no bird-dog, no pushups, no arm-supported core, no arm loading, no crawling, no jumping
- If any banned exercise appears → replace with legs-only core (dead bug legs, reverse crunch, hollow hold, leg raises)
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
def generate_workout_table():

    # ----- Strength pool (5 exercises like AI output) -----
    strength_pool = [
        "Squats",
        "Lunges",
        "Glute Bridges",
        "Calf Raises",
        "Step-ups",
        "Wall Sit",
        "Romanian Deadlift (Bodyweight)",
        "Reverse Crunch",
        "Dead Bug (legs only)",
        "Leg Raises",
        "Hollow Hold"
    ]

    cardio_options = [
        "Cycling",
        "Brisk Walk",
        "Treadmill Walk",
        "Elliptical (legs only)",
        "Stationary Bike"
    ]

    # Pick EXACTLY 5 strength exercises (to match AI plan)
    strength_exercises = random.sample(strength_pool, 5)
    cardio_exercise = random.choice(cardio_options)

    # ----- Time Structure -----
    warmup = 10
    cooldown = 10
    usable = session_duration - warmup - cooldown

    # Perfect 50/50 split
    cardio_block = usable // 2
    strength_block = usable - cardio_block

    # Even distribution across 5 exercises
    time_per_strength = round(strength_block / 5, 1)

    # ----- Sets by Intensity -----
    if intensity == "Low":
        sets = 2
    elif intensity == "Moderate":
        sets = 3
    else:
        sets = 4

    rows = []

    # ----- Strength Rows -----
    for ex in strength_exercises:
        rows.append({
            "Exercise": ex,
            "Sets": sets,
            "Reps / Time": f"10-15 reps (~{time_per_strength} min)"
        })

    # ----- Cardio Row -----
    rows.append({
        "Exercise": cardio_exercise,
        "Sets": "-",
        "Reps / Time": f"{cardio_block} min steady pace"
    })

    return pd.DataFrame(rows)

if "last_output" not in st.session_state:
    st.session_state.last_output = ""

# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):
    with st.spinner("AI Coach thinking..."):
        st.session_state.last_output = get_ai_text(build_prompt())
        st.subheader("📋 AI Coaching Output")
        st.write(st.session_state.last_output)

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


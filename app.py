import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

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
weakness = st.text_input("Biggest Weakness (optional)")
age = st.slider("Age", 10, 50, 15)

training_days = st.slider("Training Days / Week", 1, 7, 4)
session_duration = st.slider("Session Duration (minutes)", 20, 180, 60)

# ---------------- SIDEBAR FEATURES ----------------
st.sidebar.header("Select Coaching Features")

all_features = [
    "Full Workout Plan",
    "Injury Recovery Plan",
    "Weekly Training Plan",
    "Stamina Builder",
    "Nutrition Plan",
    "Hydration Strategy",
    "Warm-up & Cooldown"
]

selected_features = [f for f in all_features if st.sidebar.checkbox(f, True)]

if st.sidebar.button("Reset All"):
    st.rerun()

# ---------------- WORKOUT TABLE ----------------
def generate_workout_table():

    exercises = ["Push-ups","Squats","Plank","Lunges","Jogging"]
    inj = injury.lower()

    if "knee" in inj:
        exercises = [e for e in exercises if e not in ["Squats","Lunges"]]
    if "shoulder" in inj:
        exercises = [e for e in exercises if e != "Push-ups"]

    # Prevent empty list crash
    if len(exercises) == 0:
        exercises = ["Light Walking","Mobility Stretch","Breathing Exercise"]

    if intensity == "Low":
        sets = [1]*len(exercises)
        reps = ["10-12"]*len(exercises)
    elif intensity == "Moderate":
        sets = [2]*len(exercises)
        reps = ["12-15"]*len(exercises)
    else:
        sets = [3]*len(exercises)
        reps = ["15-20"]*len(exercises)

    time_per = max(5, session_duration // len(exercises))

    return pd.DataFrame({
        "Exercise": exercises,
        "Sets": sets,
        "Reps / Time": [f"{r} reps / ~{time_per} min" for r in reps]
    })

# ---------------- PROMPT BUILDER ----------------
def build_prompt():
    return f"""
You are an expert youth sports coach AI.

Athlete Profile:
Sport: {sport}
Position: {position}
Age: {age}
Training Days: {training_days}
Session Duration: {session_duration} min
Injury: {injury}
Intensity: {intensity}
Diet: {diet}
Goal: {goal}
Weakness: {weakness}

Provide detailed coaching guidance for:
{", ".join(selected_features)}

Structure clearly with headings and actionable steps.
"""

# ---------------- SAFE GEMINI CALL ----------------
def get_ai_text(prompt):

    try:
        response = model.generate_content(prompt)

        text = ""
        if response and response.candidates:
            content = response.candidates[0].content
            if content and content.parts:
                text = "".join([p.text for p in content.parts if hasattr(p, "text")])

        if not text.strip():
            return "⚠️ AI returned empty response. Try again later."

        return text

    except Exception as e:
        return f"Error: {e}"

# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):

    if not selected_features:
        st.warning("Select at least one feature.")
    else:
        prompt = build_prompt()

        with st.spinner("Generating coaching plan..."):
            output = get_ai_text(prompt)

        st.subheader("📋 AI Coaching Output")
        st.write(output)

        if any(f in selected_features for f in ["Full Workout Plan","Stamina Builder"]):
            st.subheader("🏋️ Workout Plan")
            st.dataframe(generate_workout_table())

        if "Weekly Training Plan" in selected_features:
            days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
            focus = ["Strength","Cardio","Skills","Speed","Mobility","Technique","Agility"]
            focus = focus[:training_days] + ["Rest"]*(7-training_days)
            st.subheader("📅 Weekly Training Schedule")
            st.table(pd.DataFrame({"Day": days, "Focus": focus}))

        if "Nutrition Plan" in selected_features:
            st.subheader("🥗 Nutrition Guide")
            st.dataframe(pd.DataFrame({
                "Meal":["Breakfast","Lunch","Dinner","Snacks"],
                "Focus":["Carbs+Protein","Balanced","Protein Rich","Fruits+Nuts"]
            }))

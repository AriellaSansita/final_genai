import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import time
from google.api_core.exceptions import ResourceExhausted

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

# ---------------- SIDEBAR ----------------
st.sidebar.header("Select Coaching Features")

features = [
    "Full Workout Plan","Injury Recovery Plan","Tactical Coaching","Nutrition Plan",
    "Warm-up & Cooldown","Stamina Builder","Mental Focus Training","Hydration Strategy",
    "Skill Drills","Weekly Training Plan","Progress Predictor","Weakness Analyzer",
    "Match Strategy","Pre-Match Routine","Post-Match Recovery","Motivation Coach",
    "Injury Risk Predictor","Mobility & Stretching","Tournament Preparation","Hydration Optimizer"
]

selected_features = [f for f in features if st.sidebar.checkbox(f, True)]

if st.sidebar.button("Reset All"):
    st.rerun()

# ---------------- WORKOUT TABLE ----------------
def generate_workout_table():
    exercises = ["Warm-up Jog","Push-ups","Squats","Sprints","Plank","Cooldown Stretch"]

    if intensity == "Low":
        sets = [1]*6
        reps = ["10"]*6
    elif intensity == "Moderate":
        sets = [2]*6
        reps = ["12-15"]*6
    else:
        sets = [3]*6
        reps = ["15-20"]*6

    return pd.DataFrame({
        "Exercise": exercises,
        "Sets": sets,
        "Reps / Time": [f"{r} reps / {session_duration//6} min" for r in reps]
    })

# ---------------- PROMPT BUILDER ----------------
def build_prompt(selected_features):

    base = f"""
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

Generate a personalized coaching plan based on the selected features.
"""

    prompts = {
        "Full Workout Plan":"Generate a complete structured workout with exercises, sets, reps, recovery and safety.",
        "Injury Recovery Plan":"Create a safe injury recovery and prevention plan.",
        "Tactical Coaching":"Provide position-specific tactical advice.",
        "Nutrition Plan":"Generate a weekly athlete nutrition and hydration plan.",
        "Warm-up & Cooldown":"Create warmup, mobility and cooldown routine.",
        "Stamina Builder":"Design a 4-week stamina improvement program.",
        "Mental Focus Training":"Provide mental focus and confidence training.",
        "Hydration Strategy":"Provide hydration and electrolyte strategy.",
        "Skill Drills":"Generate skill-specific drills.",
        "Weekly Training Plan":"Generate full weekly training schedule.",
        "Progress Predictor":"Predict performance improvement over 4 weeks.",
        "Weakness Analyzer":"Analyze weakness and corrective training.",
        "Match Strategy":"Generate match-day strategy.",
        "Pre-Match Routine":"Create pre-match preparation routine.",
        "Post-Match Recovery":"Generate post-match recovery plan.",
        "Motivation Coach":"Provide motivation and discipline guidance.",
        "Injury Risk Predictor":"Identify injury risks and prevention.",
        "Mobility & Stretching":"Generate flexibility and mobility routine.",
        "Tournament Preparation":"Create 2-week tournament peak plan.",
        "Hydration Optimizer":"Optimize hydration based on workload."
    }

    task = "\n".join([prompts[f] for f in selected_features if f in prompts])
    return base + "\nTASK:\n" + task

# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):

    if not selected_features:
        st.warning("Select at least one feature")
        st.stop()

    prompt = build_prompt(selected_features)

    with st.spinner("Generating coaching plan..."):
        try:
            response = model.generate_content(prompt)
            output = response.text

        except ResourceExhausted:
            st.warning("Quota hit. Waiting 60s...")
            time.sleep(60)
            try:
                response = model.generate_content(prompt)
                output = response.text
            except Exception as e:
                st.error(f"Retry failed: {e}")
                st.stop()

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    st.success("Coaching Plan Generated")
    st.subheader("📋 AI Coaching Output")
    st.write(output)

    if "Full Workout Plan" in selected_features or "Stamina Builder" in selected_features:
        st.subheader("🏋️ Workout Plan")
        st.dataframe(generate_workout_table())

    if "Weekly Training Plan" in selected_features:
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        focus = ["Strength","Cardio","Skills","Speed","Mobility","Technique","Agility"]
        focus = focus[:training_days] + ["Rest"]*(7-training_days)
        st.subheader("📅 Weekly Training Schedule")
        st.table(pd.DataFrame({"Day":days,"Focus":focus}))

    if "Progress Predictor" in selected_features:
        st.subheader("📈 Performance Prediction")
        weeks=[1,2,3,4]
        performance=[50,65,75,88]
        plt.figure()
        plt.plot(weeks,performance,marker="o")
        plt.xlabel("Week")
        plt.ylabel("Performance")
        plt.title("4 Week Progress")
        st.pyplot(plt)

    if "Nutrition Plan" in selected_features:
        nutrition=pd.DataFrame({
            "Meal":["Breakfast","Lunch","Dinner","Snacks"],
            "Focus":["Carbs+Protein","Balanced","Protein Rich","Fruits+Nuts"]
        })
        st.subheader("🥗 Nutrition Guide")
        st.dataframe(nutrition)


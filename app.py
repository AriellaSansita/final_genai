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
    sport = st.text_input("Enter Your Sport") or "Other Sport"
    position = st.text_input("Enter Your Role / Position") or "General Athlete"
else:
    position = st.selectbox("Player Position", positions_by_sport.get(sport, ["General Athlete"]))

injury = st.text_input("Injury History / Risk Area (type 'None' if no injury)")
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
    "Full Workout Plan","Injury Recovery Plan","Tactical Coaching","Nutrition Plan",
    "Warm-up & Cooldown","Stamina Builder","Mental Focus Training","Hydration Strategy",
    "Skill Drills","Weekly Training Plan","Progress Predictor"
]

selected_features = []
for f in all_features:
    if st.sidebar.checkbox(f, value=True):
        selected_features.append(f)

if st.sidebar.button("Reset All"):
    st.experimental_rerun()

# ---------------- DYNAMIC WORKOUT GENERATOR ----------------
def generate_workout_table(sport, position, goal, intensity, duration):
    # Base exercises
    exercises = {
        "Football": {
            "Goalkeeper": ["Footwork Drills","Reaction Saves","Plank","Push-ups","Squats"],
            "Defender": ["Sprints","Lunges","Push-ups","Core Plank","Agility Ladder"],
            "Midfielder": ["Endurance Runs","Squats","Push-ups","Burpees","Plank"],
            "Winger": ["Sprint Drills","Lunges","Push-ups","Jump Squats","Plank"],
            "Striker": ["Shooting Drills","Sprints","Push-ups","Core Plank","Lunges"]
        },
        "Basketball": {
            "Point Guard": ["Dribbling Drills","Sprints","Push-ups","Core Plank","Jump Squats"],
            "Center": ["Rebounding Drills","Squats","Push-ups","Lunges","Plank"]
        },
        # Other sports can be added similarly
    }

    # Default exercises if sport/position not listed
    ex_list = exercises.get(sport, {}).get(position, ["Push-ups","Squats","Plank","Lunges","Jogging"])
    # -------- Injury Safety Filter --------
    inj = injury.lower()
    if "arm" in inj or "shoulder" in inj:
        ex_list = [e for e in ex_list if "Push" not in e and "Plank" not in e]
    if "leg" in inj or "knee" in inj or "ankle" in inj:
        ex_list = [e for e in ex_list if "Sprint" not in e and "Squat" not in e and "Lunge" not in e]
    # If everything removed, give safe fallback
    if len(ex_list) == 0:
        ex_list = ["Light Mobility","Stretching","Breathing Drills"]


    # Adjust sets/reps based on intensity
    if intensity == "Low":
        sets = [1]*len(ex_list)
        reps = ["10-12"]*len(ex_list)
    elif intensity == "Moderate":
        sets = [2]*len(ex_list)
        reps = ["12-15"]*len(ex_list)
    else:  # High
        sets = [3]*len(ex_list)
        reps = ["15-20"]*len(ex_list)

    # Adjust for duration (longer duration = longer time per exercise)
    time_per_exercise = max(5, duration // len(ex_list))
    reps_time = [f"{r} reps / ~{time_per_exercise} min" for r in reps]

    df = pd.DataFrame({
        "Exercise": ex_list,
        "Sets": sets,
        "Reps / Time": reps_time
    })
    return df

# ---------------- PROMPT BUILDER ----------------
def build_prompt(feature):
    base = f"""
You are an expert youth sports coach AI.

Athlete Profile:
Sport: {sport}
Position: {position}
Age: {age}
Training Days per Week: {training_days}
Session Duration: {session_duration} minutes
Injury History: {injury}
Training Intensity: {intensity}
Diet: {diet}
Goal: {goal}
Weakness: {weakness}
"""
    prompts = {
        "Full Workout Plan": "Generate a COMPLETE structured workout plan with warm-up, main exercises, sets, reps, and recovery tips.",
        "Injury Recovery Plan": "Create a SAFE injury recovery plan with allowed exercises and gradual progression.",
        "Tactical Coaching": "Provide position-specific tactical advice and match intelligence.",
        "Nutrition Plan": "Generate a weekly nutrition plan with meals, protein focus, and hydration.",
        "Stamina Builder": "Design a 4-week stamina program with cardio progression and recovery.",
        "Weekly Training Plan": "Generate a weekly training schedule balancing skill and fitness."
    }
    return base + "\nTASK:\n" + prompts.get(feature, f"Generate guidance for {feature}")

# ---------------- GENERATE OUTPUT ----------------
if st.button("Generate Coaching Advice"):
    if not selected_features:
        st.warning("Please select at least one feature!")
    else:
        for feature in selected_features:
            prompt = build_prompt(feature)
            with st.spinner(f"CoachBot generating {feature}..."):
                try:
                    response = model.generate_content(prompt)
                    full_text = response.text

                    st.success(f"{feature} Generated")
                    st.write(f"### 📋 {feature} Summary")
                    with st.expander("Show Full AI Explanation"):
                        st.write(full_text)

                    # Show dynamic workout table
                    if feature in ["Full Workout Plan","Stamina Builder","Weekly Training Plan","Injury Recovery Plan"]:
                        df = generate_workout_table(sport, position, goal, intensity, session_duration)
                        st.write("### 🏋️ Workout Plan")
                        st.dataframe(df)

                    # Weekly schedule
                    if feature == "Weekly Training Plan":
                        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
                        focus_list = ["Strength","Cardio","Skills","Speed","Mobility","Technique","Agility"]
                        schedule_focus = focus_list[:training_days] + ["Rest / Recovery"]*(7-training_days)
                        schedule_df = pd.DataFrame({"Day": days, "Training Focus": schedule_focus})
                        st.write("### 📅 Weekly Training Schedule")
                        st.table(schedule_df)

                    # Progress graph
                    if feature in ["Progress Predictor","Stamina Builder"]:
                        st.write("### 📈 Expected Progress Over 4 Weeks")
                        weeks = [1,2,3,4]
                        performance = [50 + training_days*3, 60 + training_days*3, 70 + training_days*3, 80 + training_days*3]
                        plt.figure()
                        plt.plot(weeks, performance, marker="o")
                        plt.xlabel("Week")
                        plt.ylabel("Performance Level")
                        plt.title("Training Progress Prediction")
                        st.pyplot(plt)

                    # Nutrition
                    if feature == "Nutrition Plan":
                        nutrition_df = pd.DataFrame({
                            "Meal": ["Breakfast","Lunch","Dinner","Snacks"],
                            "Focus": ["Carbs + Protein","Balanced","Protein Heavy","Fruits & Nuts"]
                        })
                        st.write("### 🥗 Nutrition Guide")
                        st.dataframe(nutrition_df)

                except Exception as e:
                    st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import time
from google.api_core.exceptions import ResourceExhausted  # Import the specific exception

# ---------------- CONFIG ----------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")  # Updated to a valid model name; adjust if needed

st.set_page_config(page_title="CoachBot AI", layout="wide")
st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.write("AI-powered personalized coach for young athletes")

# ---------------- USER INPUT ----------------
sports_list = [
    "Football", "Cricket", "Basketball", "Athletics", "Badminton", "Tennis",
    "Hockey", "Volleyball", "Kabaddi", "Table Tennis", "Swimming", "Martial Arts", "Other"
]

sport = st.selectbox("Sport", sports_list)

positions_by_sport = {
    "Football": ["Goalkeeper", "Defender", "Midfielder", "Winger", "Striker"],
    "Cricket": ["Batsman", "Bowler", "All-Rounder", "Wicket Keeper"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Athletics": ["Sprinter", "Long Distance Runner", "Jumper", "Thrower"],
    "Badminton": ["Singles Player", "Doubles Player"],
    "Tennis": ["Singles Player", "Doubles Player"],
    "Hockey": ["Goalkeeper", "Defender", "Midfielder", "Forward"],
    "Volleyball": ["Setter", "Libero", "Spiker", "Blocker"],
    "Kabaddi": ["Raider", "Defender", "All-Rounder"],
    "Table Tennis": ["Singles Player", "Doubles Player"],
    "Swimming": ["Freestyle Specialist", "Backstroke Specialist", "Butterfly Specialist"],
    "Martial Arts": ["Striker", "Grappler", "Mixed Fighter"]
}

if sport == "Other":
    sport = st.text_input("Enter Your Sport") or "General Sport"
    position = st.text_input("Enter Position") or "Athlete"
else:
    position = st.selectbox("Player Position", positions_by_sport.get(sport, ["Athlete"]))

injury = st.text_input("Injury History (None if no injury)")
goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"])
diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
intensity = st.selectbox("Training Intensity", ["Low", "Moderate", "High"])
weakness = st.text_input("Biggest Weakness (optional)")
age = st.slider("Age", 10, 50, 15)

training_days = st.slider("Training Days / Week", 1, 7, 4)
session_duration = st.slider("Session Duration (minutes)", 20, 180, 60)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Select Coaching Features")

features = [
    "Full Workout Plan", "Injury Recovery Plan", "Tactical Coaching", "Nutrition Plan",
    "Stamina Builder", "Weekly Training Plan", "Progress Predictor", "Warm-up & Cooldown",
    "Mental Focus Training", "Hydration Strategy", "Skill Drills"
]

selected_features = [f for f in features if st.sidebar.checkbox(f, True)]

if st.sidebar.button("Reset All"):
    st.rerun()

# ---------------- WORKOUT TABLE ----------------
def generate_workout_table():
    exercises = ["Warm-up Jog", "Push-ups", "Squats", "Sprints", "Plank", "Cooldown Stretch"]

    if intensity == "Low":
        sets = [1] * 6
        reps = ["10"] * 6
    elif intensity == "Moderate":
        sets = [2] * 6
        reps = ["12-15"] * 6
    else:
        sets = [3] * 6
        reps = ["15-20"] * 6

    df = pd.DataFrame({
        "Exercise": exercises,
        "Sets": sets,
        "Reps / Time": [f"{r} reps / {session_duration // 6} min" for r in reps]
    })
    return df

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
        "Full Workout Plan": """
Generate a COMPLETE structured workout:
- Warm-up
- Main exercises
- Sets & reps
- Safety notes
- Recovery tips
""",

        "Injury Recovery Plan": """
Create a SAFE injury recovery plan:
- Allowed exercises
- Avoid risky movements
- Gradual progression
- Injury prevention
""",

        "Tactical Coaching": """
Provide POSITION-SPECIFIC tactical advice:
- Positioning
- Decision making
- Common mistakes
- Match intelligence
""",

        "Nutrition Plan": """
Generate a WEEKLY athlete nutrition plan:
- Meals (breakfast/lunch/dinner)
- Protein & recovery focus
- Hydration
""",

        "Warm-up & Cooldown": """
Create warm-up and cooldown routine:
- Dynamic warmup
- Mobility drills
- Stretching
- Injury prevention
""",

        "Stamina Builder": """
Design a 4-week stamina program:
- Cardio progression
- Intensity control
- Recovery balance
""",

        "Mental Focus Training": """
Provide mental performance coaching:
- Focus drills
- Confidence training
- Pre-match mindset
""",

        "Hydration Strategy": """
Provide hydration & electrolyte strategy:
- Daily intake
- Training hydration
- Recovery hydration
""",

        "Skill Drills": """
Generate skill-specific drills:
- Technique improvement
- Drill structure
- Progression
""",

        "Weekly Training Plan": """
Generate FULL weekly training schedule:
- Training days
- Recovery days
- Skill + fitness balance
""",

        "Progress Predictor": """
Predict performance improvement over 4 weeks and adjust training.
""",
    }

    task = "\n".join([prompts[f] for f in selected_features if f in prompts])
    return base + "\nTASK:\n" + task

# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):
    if not selected_features:
        st.warning("Select at least one feature")
    else:
        prompt = build_prompt(selected_features)

        with st.spinner("Generating coaching plan..."):
            try:
                response = model.generate_content(prompt)
                output = response.text
            except ResourceExhausted as e:  # Handle ResourceExhausted specifically
                st.warning("Quota reached. Waiting 60s before retrying...")  # Increased wait time
                time.sleep(60)  # Increased from 25 to 60 seconds
                try:
                    response = model.generate_content(prompt)
                    output = response.text
                except Exception as retry_e:
                    st.error(f"Retry failed: {retry_e}")
                    st.stop()
            except Exception as e:
                if "429" in str(e):  # Keep the original check for rate limits
                    st.warning("Rate limit reached. Waiting 25s...")
                    time.sleep(25)
                    try:
                        response = model.generate_content(prompt)
                        output = response.text
                    except Exception as retry_e:
                        st.error(f"Retry failed: {retry_e}")
                        st.stop()
                else:
                    st.error(f"An error occurred: {e}")
                    st.stop()

        st.success("Coaching Plan Generated")

        st.subheader("📋 AI Coaching Output")
        st.write(output)

        # Workout Table
        if "Full Workout Plan" in selected_features or "Stamina Builder" in selected_features:
            st.subheader("🏋️ Workout Plan")
            st.dataframe(generate_workout_table())

        # Weekly Plan
        if "Weekly Training Plan" in selected_features:
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            focus = ["Strength", "Cardio", "Skills", "Speed", "Mobility", "Technique", "Agility"]
            focus = focus[:training_days] + ["Rest"] * (7 - training_days)
            schedule = pd.DataFrame({"Day": days, "Focus": focus})
            st.subheader("📅 Weekly Training Schedule")
            st.table(schedule)

        # Progress Graph
        if "Progress Predictor" in selected_features:
            st.subheader("📈 Performance Prediction")
            weeks = [1, 2, 3, 4]
            performance = [50, 65, 75, 88]
            plt.figure()
            plt.plot(weeks, performance, marker="o")
            plt.xlabel("Week")
            plt.ylabel("Performance")
            plt.title("4 Week Progress")
            st.pyplot(plt)

        # Nutrition
        if "Nutrition Plan" in selected_features:
            nutrition = pd.DataFrame({
                "Meal": ["Breakfast", "Lunch", "Dinner", "Snacks"],
                "Focus": ["Carbs + Protein", "Balanced", "Protein Rich", "Fruits + Nuts"]
            })
            st.subheader("🥗 Nutrition Guide")
            st.dataframe(nutrition)

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

# -------- NEW INPUTS --------
training_days = st.slider("Training Days / Week", 1, 7, 4)
session_duration = st.slider("Session Duration (minutes)", 20, 180, 60)

feature = st.selectbox("Choose Coaching Feature", [
    "Full Workout Plan","Injury Recovery Plan","Tactical Coaching","Nutrition Plan",
    "Warm-up & Cooldown","Stamina Builder","Mental Focus Training","Hydration Strategy",
    "Skill Drills","Weekly Training Plan","Progress Predictor"
])

# ---------------- PROMPT BUILDER ----------------
def build_prompt():
    return f"""
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

TASK: {feature}
"""


    prompts = {

        # -------- Mandatory --------
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

        "Weakness Analyzer": """
Analyze weakness and create corrective training plan.
""",

        "Match Strategy": """
Generate match-day strategy and tactical positioning advice.
""",

        "Pre-Match Routine": """
Create complete pre-match preparation routine.
""",

        "Post-Match Recovery": """
Generate post-match recovery and muscle repair plan.
""",

        "Motivation Coach": """
Provide discipline and motivation guidance with practical steps.
""",

        "Injury Risk Predictor": """
Identify possible injury risks and prevention strategies.
""",

        "Mobility & Stretching": """
Generate flexibility and mobility improvement routine.
""",

        "Tournament Preparation": """
Create a 2-week peak performance tournament preparation plan.
""",

        "Hydration Optimizer": """
Optimize hydration based on workload and climate.
"""
    }

    return base + "\nTASK:\n" + prompts[feature]



# ---------------- GENERATE OUTPUT ----------------
if st.button("Generate Coaching Advice"):

    prompt = build_prompt()

    with st.spinner("CoachBot analyzing athlete profile..."):
        try:
            response = model.generate_content(prompt)
            full_text = response.text

            st.success("Coaching Plan Generated")

            st.write("### 📋 Quick Summary")
            with st.expander("Show Full AI Explanation"):
                st.write(full_text)

            # -------- WORKOUT TABLE --------
            if feature in ["Full Workout Plan","Weekly Training Plan","Stamina Builder"]:
                df = pd.DataFrame({
                    "Exercise": ["Warm-up Jog","Push-ups","Squats","Sprints","Cooldown Stretch"],
                    "Sets": [1,3,3,5,1],
                    "Reps / Time": ["10 mins","12 reps","15 reps","30 sec","10 mins"]
                })
                st.write("### 🏋️ Workout Plan")
                st.dataframe(df)

            # ---------------- WEEKLY SCHEDULE ----------------
            if feature == "Weekly Training Plan":
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                
                # Determine training focus for active days
                training_focus_list = ["Strength", "Cardio", "Skills", "Speed", "Mobility", "Technique", "Agility"]
                
                # Assign focus only to the number of training days
                training_days_count = training_days  # from your slider input
                schedule_focus = training_focus_list[:training_days_count]
                
                # Fill remaining days with "Rest / Recovery"
                schedule_focus += ["Rest / Recovery"] * (7 - training_days_count)
                
                # Build the table
                schedule_data = {
                    "Day": days,
                    "Training Focus": schedule_focus
                }
                
                schedule_df = pd.DataFrame(schedule_data)
                st.write("### 📅 Weekly Training Schedule")
                st.table(schedule_df)


            # -------- PROGRESS GRAPH --------
            if feature in ["Progress Predictor","Stamina Builder"]:
                st.write("### 📈 Expected Progress Over 4 Weeks")

                weeks = [1,2,3,4]
                performance = [
                    50 + training_days*3,
                    60 + training_days*3,
                    70 + training_days*3,
                    80 + training_days*3
                ]

                plt.figure()
                plt.plot(weeks, performance, marker="o")
                plt.xlabel("Week")
                plt.ylabel("Performance Level")
                plt.title("Training Progress Prediction")
                st.pyplot(plt)

            # -------- NUTRITION TABLE --------
            if feature == "Nutrition Plan":
                nutrition_df = pd.DataFrame({
                    "Meal": ["Breakfast","Lunch","Dinner","Snacks"],
                    "Focus": ["Carbs + Protein","Balanced","Protein Heavy","Fruits & Nuts"]
                })
                st.write("### 🥗 Nutrition Guide")
                st.dataframe(nutrition_df)

        except Exception as e:
            st.error(f"Error: {e}")

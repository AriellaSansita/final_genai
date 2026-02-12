import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt


# ---------------- CONFIG ----------------
genai.configure(api_key="AIzaSyB9VfhS0_sApB2TBRzEi06G1lZlwgDOKnA")

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="CoachBot AI", layout="wide")

st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.write("AI-powered personalized coach for young athletes")

# ---------------- SPORT SELECTION ----------------

sports_list = [
    "Football",
    "Cricket",
    "Basketball",
    "Athletics",
    "Badminton",
    "Tennis",
    "Hockey",
    "Volleyball",
    "Kabaddi",
    "Table Tennis",
    "Swimming",
    "Martial Arts",
    "Other"
]

sport = st.selectbox("Sport", sports_list)

# ---------------- SPORT-SPECIFIC POSITIONS ----------------

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

# ---------------- POSITION LOGIC ----------------

if sport == "Other":
    custom_sport = st.text_input("Enter Your Sport")
    sport = custom_sport if custom_sport else "Other Sport"

    custom_position = st.text_input("Enter Your Role / Position")
    position = custom_position if custom_position else "General Athlete"

else:
    position = st.selectbox(
        "Player Position",
        positions_by_sport.get(sport, ["General Athlete"])
    )


injury = st.text_input("Injury History / Risk Area (type 'None' if no injury)")
goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"])
diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
intensity = st.selectbox("Training Intensity", ["Low", "Moderate", "High"])
weakness = st.text_input("Biggest Weakness (optional)")
age = st.slider("Age", 10, 50, 15)

# ---------------- FEATURE SELECT ----------------
feature = st.selectbox(
    "Choose Coaching Feature",
    [
        # Mandatory Features
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

        # Optional Features
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
You are an expert youth sports coach AI.

IMPORTANT:
- Write a FULL, long, complete response.
- Do NOT stop early.
- Always include multiple sections.
- Minimum length: 6 structured sections.
- Continue until the full plan is finished.

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

        # -------- Optional --------
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
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_output_tokens": 20000
                }
            )

            # Collect AI text
            full_text = ""
            for part in response.candidates[0].content.parts:
                full_text += part.text

            st.success("Coaching Plan Generated")

            # Collapsible AI explanation
            st.write("### 📋 Quick Summary")
            with st.expander("Show Full AI Explanation"):
                st.write(full_text)

            # ---------------- WORKOUT TABLE ----------------
            if "Workout" in feature or "Training" in feature:
                workout_data = {
                    "Exercise": ["Warm-up Jog", "Push-ups", "Squats", "Sprints", "Cooldown Stretch"],
                    "Sets": [1, 3, 3, 5, 1],
                    "Reps / Time": ["10 mins", "12 reps", "15 reps", "30 sec", "10 mins"]
                }

                df = pd.DataFrame(workout_data)
                st.write("### 🏋️ Workout Plan Table")
                st.dataframe(df)

            # ---------------- WEEKLY SCHEDULE TABLE ----------------
            schedule_data = {
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "Training Focus": ["Strength", "Cardio", "Skills", "Rest", "Speed", "Match Practice", "Recovery"]
            }

            schedule_df = pd.DataFrame(schedule_data)
            st.write("### 📅 Weekly Training Schedule")
            st.table(schedule_df)

            # ---------------- PROGRESS GRAPH ----------------
            st.write("### 📈 Expected Progress Over 4 Weeks")

            weeks = [1, 2, 3, 4]
            performance = [60, 70, 80, 90]

            plt.figure()
            plt.plot(weeks, performance, marker="o")
            plt.xlabel("Week")
            plt.ylabel("Performance Level")
            plt.title("Training Progress Prediction")

            st.pyplot(plt)

            # ---------------- NUTRITION TABLE ----------------
            nutrition_data = {
                "Meal": ["Breakfast", "Lunch", "Dinner", "Snacks"],
                "Focus": ["Carbs + Protein", "Balanced", "Protein Heavy", "Fruits & Nuts"]
            }

            nutrition_df = pd.DataFrame(nutrition_data)
            st.write("### 🥗 Nutrition Guide")
            st.dataframe(nutrition_df)

        except Exception as e:
            st.error(f"Error: {e}")

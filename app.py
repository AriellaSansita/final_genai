import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key="AIzaSyB9VfhS0_sApB2TBRzEi06G1lZlwgDOKnA")

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="CoachBot AI", layout="wide")

st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.write("AI-powered personalized coach for young athletes")

# ---------------- USER INPUT ----------------
sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Other"])
position = st.text_input("Player Position")
injury = st.text_input("Injury History / Risk Area (type 'None' if no injury)")
goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"])
diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
intensity = st.selectbox("Training Intensity", ["Low", "Moderate", "High"])
weakness = st.text_input("Biggest Weakness (optional)")
age = st.slider("Age", 10, 25, 15)

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

    if position == "":
        st.warning("Please enter player position")
    else:
        prompt = build_prompt()

        with st.spinner("CoachBot analyzing athlete profile..."):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                )

                st.success("Coaching Plan Generated")
                full_text = ""

                for part in response.candidates[0].content.parts:
                    full_text += part.text

                st.write(full_text)



            except Exception as e:
                st.error(f"Error: {e}")


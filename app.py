import streamlit as st
import google.generativeai as genai

# ---- CONFIGURE API ----
genai.configure(api_key="AIzaSyBv2dnTTYh3CPHmnRCDO8NQeOcAyRIectw")

model = genai.GenerativeModel("gemini-1.5-pro")

st.title("🏋️ CoachBot AI - Smart Fitness Assistant")

st.write("Get personalized workout, recovery, and nutrition guidance using AI")

# ---- USER INPUT ----
sport = st.text_input("Sport (e.g., Football, Cricket, Basketball)")
position = st.text_input("Player Position (e.g., Striker, Bowler, Guard)")
injury = st.text_input("Injury / Risk Area (e.g., Knee strain, None)")
goal = st.text_input("Goal (e.g., Build stamina, Strength, Recovery)")
diet = st.text_input("Diet Type (Veg / Non-Veg / Any allergies)")

if st.button("Generate Plan"):

    prompt = f"""
    You are a professional sports coach.

    Athlete Details:
    Sport: {sport}
    Position: {position}
    Injury: {injury}
    Goal: {goal}
    Diet: {diet}

    Generate:
    1. Safe and effective workout plan
    2. Injury-aware training advice
    3. Tactical improvement tips
    4. Basic nutrition guidance
    """

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.5,
            "max_output_tokens": 500
        }
    )

    st.subheader("AI Coaching Plan")
    st.write(response.text)

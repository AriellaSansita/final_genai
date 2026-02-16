import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to get safe response and prevent the "Part" error
def get_ai_response(target_model, prompt):
    try:
        response = target_model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            raw_text = response.candidates[0].content.parts[0].text
            # Remove any pesky <br> tags programmatically
            return raw_text.replace("<br>", " ").replace("</br>", " ")
        return "The coach is busy. Please try a simpler question."
    except Exception as e:
        return f"Connection Error: {str(e)}"

st.set_page_config(page_title="CoachBot AI", layout="wide", page_icon="🏆")

# ---------------- DATA MAPPING ----------------
positions_map = {
    "Football": ["Striker", "Midfielder", "Defender", "Goalkeeper", "Winger"],
    "Cricket": ["Batsman", "Fast Bowler", "Spin Bowler", "Wicket Keeper", "All-Rounder"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Athletics": ["Sprinter", "Long Distance", "Jumper", "Thrower"],
    "Swimming": ["Freestyle", "Breaststroke", "Butterfly", "Backstroke"],
    "Tennis": ["Singles", "Doubles Specialist"],
    "Rugby": ["Forward", "Back"],
    "Volleyball": ["Setter", "Libero", "Attacker", "Blocker"],
    "Badminton": ["Singles", "Doubles"],
    "Hockey": ["Forward", "Midfielder", "Defender", "Goalie"],
    "Kabaddi": ["Raider", "Defender", "All-Rounder"]
}

# ---------------- UI LAYOUT ----------------
st.title("🏆 CoachBot AI")
st.write("Personalized fitness and tactical coaching.")

tab1, tab2 = st.tabs(["📊 Smart Assistant", "🧠 Custom Coach"])

with tab1:
    st.subheader("1. Profile & Goal")
    c1, c2, c3, c4 = st.columns(4)
    with c1: sport = st.selectbox("Sport", list(positions_map.keys()))
    with c2: position = st.selectbox("Position", positions_map[sport])
    with c3: age = st.number_input("Age", 10, 50, 18)
    with c4: injury = st.text_input("Injury History", "None")

    st.subheader("2. Plan Details")
    g1, g2, g3, g4 = st.columns(4)
    with g1: 
        feature = st.selectbox("Focus", ["Full Workout Plan", "Weekly Training Plan", "Nutrition Plan", "Hydration Strategy", "Warm-up & Cooldown", "Tactical Coaching", "Skill Drills", "Injury Risk Predictor", "Mobility & Stretching", "Mental Focus Training"])
    with g2: goal = st.selectbox("Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill"])
    with g3: intensity_level = st.select_slider("Intensity", options=["Low", "Moderate", "High"])
    with g4: days = st.number_input("Days", 1, 30, 7)

    # Food Logic
    allergy, pref = "None", "N/A"
    if feature in ["Nutrition Plan", "Hydration Strategy"]:
        f1, f2 = st.columns(2)
        with f1: pref = st.selectbox("Diet", ["Non-Veg", "Veg", "Vegan"])
        with f2: allergy = st.text_input("Allergies", "None")

    if st.button("Generate Plan", type="primary"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Coach a {age}yo {sport} {position}. Goal: {goal}. Intensity: {intensity_level}. Injury: {injury}. Diet: {pref}. Allergies: {allergy}. Task: {feature} for {days} days. Format: Markdown table. No HTML."
        
        with st.spinner("Analyzing..."):
            result = get_ai_response(model, prompt)
            res_col, vis_col = st.columns([2, 1])
            with res_col:
                st.markdown(result)
            with vis_col:
                fig, ax = plt.subplots(figsize=(5,4))
                ax.pie([20, 60, 20], labels=['Prep', 'Work', 'Recover'], autopct='%1.1f%%', colors=['#FFD700','#1E90FF','#32CD32'])
                st.pyplot(fig)

with tab2:
    st.subheader("🧠 Custom Coach Consultation")
    user_query = st.text_area("Ask anything (e.g., '3 drills for speed'):")
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        intensity_val = st.slider("Intensity (Creativity)", 1, 100, 40)
        ai_temp = intensity_val / 100.0

    if st.button("Ask AI Coach", type="primary"):
        if user_query:
            # Re-initializing model with custom temperature (Intensity)
            custom_model = genai.GenerativeModel("gemini-2.5-flash", generation_config={"temperature": ai_temp})
            custom_prompt = f"Question: {user_query}. Format: Short Markdown table. No HTML. Brief points only."
            
            with st.spinner("Consulting Coach..."):
                answer = get_ai_response(custom_model, custom_prompt)
                st.info("📋 Coach's Rapid Response:")
                st.markdown(answer)

st.caption("🏆 CoachBot AI | NextGen Sports Lab")

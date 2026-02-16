import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
# Using Gemini 2.5 Flash for high-speed, accurate processing
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.5-flash", 
    generation_config={
        "temperature": 0.3, # Low temperature for safe, precise coaching (Step 2)
        "top_p": 0.8
    }
)

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

# ---------------- TOP UI LAYOUT ----------------
st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.write("AI-powered personalized coach for young athletes")
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Smart Assistant", "🧠 Custom Coach"])

with tab1:
    # Row 1: Athlete Profile
    st.subheader("1. Athlete Profile")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        sport = st.selectbox("Sport", list(positions_map.keys()))
    with p_col2:
        position = st.selectbox("Position", positions_map[sport])
    with p_col3:
        age = st.number_input("Age", 10, 50, 18)
    with p_col4:
        injury = st.text_input("Injury History", "None")

    # Row 2: Training Configuration
    st.subheader("2. Training Configuration")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    with g_col1:
        feature = st.selectbox("Coaching Focus", [
            "Full Workout Plan", "Weekly Training Plan", "Nutrition Plan", 
            "Hydration Strategy", "Warm-up & Cooldown", "Tactical Coaching", 
            "Skill Drills", "Injury Risk Predictor", "Mobility & Stretching", 
            "Mental Focus Training"
        ])
    with g_col2:
        goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"])
    with g_col3:
        intensity = st.select_slider("Intensity", options=["Low", "Moderate", "High"])
    with g_col4:
        schedule_days = st.number_input("Schedule Days", 1, 30, 7)

    # DYNAMIC ROW: Food & Allergies (Appears only if feature involves food)
    food_related = ["Nutrition Plan", "Hydration Strategy"]
    allergy_info = "None"
    meal_pref = "N/A"

    if feature in food_related:
        st.info("🍎 Nutrition Details Required")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            meal_pref = st.selectbox("Meal Preference", ["Non-Veg", "Vegetarian", "Vegan", "Pescetarian"])
        with f_col2:
            allergy_info = st.text_input("Food Allergies (e.g., Nuts, Dairy, Gluten)", "None")

    st.markdown("---")

    # Generate Button
    if st.button("Generate Plan", type="primary"):
        # Prompt Engineering with new dynamic inputs
        prompt = (
            f"Act as a professional youth coach for a {age}yo {sport} {position}. "
            f"Goal: {goal}. Intensity: {intensity}. Injury History: {injury}. "
            f"Task: Create a {feature} for {schedule_days} days. "
            f"Meal Preference: {meal_pref}. Allergies to avoid: {allergy_info}. "
            "STRICT RULES:\n"
            "1. Output ONLY a Markdown table.\n"
            "2. DO NOT use HTML tags like <br>.\n"
            "3. Ensure advice is safety-first, position-specific, and allergy-compliant."
        )
        
        with st.spinner("AI Coach calculating personalized metrics..."):
            try:
                response = model.generate_content(prompt)
                out_col, vis_col = st.columns([2, 1])
                with out_col:
                    st.success(f"📋 AI Coaching Output: {feature}")
                    st.markdown(response.text) 
                with vis_col:
                    st.subheader("📊 Session Load Analysis")
                    # Step 6: Data Visualization
                    fig, ax = plt.subplots(figsize=(5, 4))
                    ax.pie([15, 70, 15], labels=['Activation', 'Workload', 'Recovery'], 
                           autopct='%1.1f%%', colors=['#FFD700','#1E90FF','#32CD32'], startangle=90)
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("🧠 Custom Coach Consultation")
    user_query = st.text_area("Ask a specific coaching question:", 
                             placeholder="e.g., What are some pre-match visualization techniques?")
    
    c_col1, c_col2 = st.columns([1, 2])
    with c_col1:
        # Step 5: Hyperparameter Tuning
        c_temp = st.slider("Coaching Style (Temperature)", 0.0, 1.0, 0.4)

    if st.button("Ask AI Coach", type="primary"):
        if user_query:
            try:
                custom_model = genai.GenerativeModel("gemini-2.5-flash", generation_config={"temperature": c_temp})
                res = custom_model.generate_content(user_query)
                st.info("AI Coach Perspective:")
                st.markdown(res.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")

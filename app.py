import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-flash", # Note: Standard stable string for Gemini Flash
    generation_config={
        "temperature": 0.3, 
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
        intensity_level = st.select_slider("Intensity Level", options=["Low", "Moderate", "High"])
    with g_col4:
        schedule_days = st.number_input("Schedule Days", 1, 30, 7)

    # Dynamic Nutrition Fields
    food_related = ["Nutrition Plan", "Hydration Strategy"]
    allergy_info, meal_pref = "None", "N/A"

    if feature in food_related:
        st.info("🍎 Nutrition Details Required")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            meal_pref = st.selectbox("Meal Preference", ["Non-Veg", "Vegetarian", "Vegan", "Pescetarian"])
        with f_col2:
            allergy_info = st.text_input("Food Allergies", "None")

    st.markdown("---")

    if st.button("Generate Plan", type="primary"):
        prompt = (
            f"Role: Professional Coach. Athlete: {age}yo {sport} {position}. "
            f"Goal: {goal}. Intensity: {intensity_level}. Injury: {injury}. "
            f"Meal Pref: {meal_pref}. Allergies: {allergy_info}. "
            f"Provide a {feature} for {schedule_days} days. "
            "Format: Markdown table only. No HTML. No intro/outro."
        )
        
        with st.spinner("AI Coach thinking..."):
            try:
                response = model.generate_content(prompt)
                # Safely extract text to avoid the error
                if response.candidates:
                    raw_text = response.candidates[0].content.parts[0].text
                    # Programmatically remove <br> tags if they appear
                    clean_text = raw_text.replace("<br>", " ").replace("</br>", " ")
                    
                    out_col, vis_col = st.columns([2, 1])
                    with out_col:
                        st.success(f"📋 AI Coaching Output: {feature}")
                        st.markdown(clean_text) 
                    with vis_col:
                        st.subheader("📊 Session Load Analysis")
                        fig, ax = plt.subplots(figsize=(5, 4))
                        ax.pie([15, 70, 15], labels=['Activation', 'Workload', 'Recovery'], 
                               autopct='%1.1f%%', colors=['#FFD700','#1E90FF','#32CD32'], startangle=90)
                        st.pyplot(fig)
                else:
                    st.error("AI could not generate a response. Please try a simpler request.")
            except Exception as e:
                st.error(f"Operation Error: {e}")

with tab2:
    st.subheader("🧠 Custom Coach Consultation")
    user_query = st.text_area("Ask a specific coaching question:", placeholder="e.g., Suggest 3 drills for explosive speed.")
    
    c_col1, c_col2 = st.columns([1, 2])
    with c_col1:
        intensity_val = st.slider("Intensity", 1, 100, 40)
        ai_temp = intensity_val / 100.0

    if st.button("Ask AI Coach", type="primary"):
        if user_query:
            custom_prompt = (
                f"Question: {user_query}. "
                f"Intensity: {intensity_val}/100. "
                "Format: Short Markdown table only. No HTML. No chat."
            )
            try:
                custom_model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"temperature": ai_temp})
                res = custom_model.generate_content(custom_prompt)
                if res.candidates:
                    clean_res = res.candidates[0].content.parts[0].text.replace("<br>", " ")
                    st.info("📋 Quick Coaching Chart:")
                    st.markdown(clean_res)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("🏆 CoachBot AI | NextGen Sports Lab | AI Summative Assessment")

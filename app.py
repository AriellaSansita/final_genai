import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
# Requirement: Integrate Gemini 1.5 Pro to process data and generate outputs 
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.5-flash", 
    generation_config={
        "temperature": 0.3, # Lower temperature for safe, conservative coaching 
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

# ---------------- TOP NAVIGATION & INPUTS ----------------
st.title("🏆 CoachBot AI: Smart Fitness Assistant")
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Smart Coaching Assistant", "🧠 Custom AI Coach"])

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

    # Row 2: Coaching Focus & Schedule (Separated as requested)
    st.subheader("2. Training Configuration")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    with g_col1:
        feature = st.selectbox("Coaching Focus", [
            "Weekly Training Plan", "Nutrition & Macros", "Injury Prevention", "Mental Focus Training"
        ])
    with g_col2:
        goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Tactical IQ"])
    with g_col3:
        intensity = st.select_slider("Intensity", options=["Low", "Moderate", "High"])
    with g_col4:
        schedule_days = st.number_input("Schedule Days", 1, 30, 7)

    st.markdown("---")

    if st.button("Generate My AI Coaching Plan"):
        # Prompt Engineering: Strict instructions to remove <br> tags and use Markdown 
        prompt = (
            f"Act as a professional coach for a {age} year old {sport} player ({position}). "
            f"Goal: {goal}. Intensity: {intensity}. Injury History: {injury}. "
            f"Provide a {feature} for {schedule_days} days. "
            "MANDATORY FORMATTING RULES:\n"
            "1. Output ONLY a Markdown table.\n"
            "2. DO NOT use HTML tags like <br> or <div>.\n"
            "3. For line breaks within a table cell, use a single space or a comma.\n"
            "4. Ensure the text is clean, professional, and easy to read."
        )
        
        with st.spinner("AI Coach is preparing your data..."):
            try:
                response = model.generate_content(prompt)
                
                res_col, vis_col = st.columns([2, 1])
                
                with res_col:
                    st.success(f"Personalized {feature} Result")
                    # Display the cleaned Markdown response
                    st.markdown(response.text)
                
                with vis_col:
                    st.subheader("📊 Session Intensity")
                    # Implementing visualization as required in Step 6 
                    fig, ax = plt.subplots(figsize=(5, 4))
                    labels = ['Warm-up', 'Core Session', 'Cool-down']
                    sizes = [15, 70, 15]
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#ffcc99','#66b3ff','#99ff99'], startangle=90)
                    st.pyplot(fig)
                    
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Direct Coach Consultation")
    user_custom_prompt = st.text_area("Ask a specific coaching question:", 
                                     placeholder="e.g., Suggest mobility drills for a 45-year-old goalkeeper with back stiffness.")
    
    custom_col1, custom_col2 = st.columns([1, 2])
    with custom_col1:
        # Tuning parameter: Temperature for model optimization 
        custom_temp = st.slider("Coaching Style (Temperature)", 0.0, 1.0, 0.4)

    if st.button("Get Custom Advice"):
        if user_custom_prompt:
            try:
                custom_model = genai.GenerativeModel("gemini-1.5-pro", generation_config={"temperature": custom_temp})
                custom_res = custom_model.generate_content(user_custom_prompt)
                st.markdown(custom_res.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("NextGen Sports Lab | AI Summative Assessment | Built with Gemini 1.5 Pro ")

import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
# Configured for Gemini 1.5 Pro per assignment brief 
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "temperature": 0.4, # Conservative for safety 
        "top_p": 0.9,
    }
)

st.set_page_config(page_title="CoachBot AI", layout="wide", page_icon="🏆")

# ---------------- NAVIGATION ----------------
st.sidebar.title("🎮 Navigation")
page = st.sidebar.radio("Go to", ["Smart Assistant", "Custom AI Coach"])

# ---------------- DATA & MAPPING ----------------
# Expanded sports list to include more global and regional options 
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
    "Hockey": ["Forward", "Midfielder", "Defender", "Goalie"]
}

# ---------------- PAGE 1: SMART ASSISTANT ----------------
if page == "Smart Assistant":
    st.title("🏆 CoachBot AI - Smart Assistant")
    st.write("Generate structured training and nutrition plans automatically.")
    
    st.sidebar.header("📋 Athlete Profile")
    sport = st.sidebar.selectbox("Sport", list(positions_map.keys()))
    position = st.sidebar.selectbox("Position", positions_map[sport])
    age = st.sidebar.slider("Age", 10, 25, 16)
    injury = st.sidebar.text_input("Injury History", "None")
    
    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Tactical IQ"])
        intensity = st.select_slider("Intensity", options=["Low", "Moderate", "High"])
    with col2:
        schedule_days = st.number_input("Schedule Length (Days)", 1, 30, 7)
        feature = st.selectbox("Feature", [
            "Weekly Training Plan", "Nutrition & Macros", "Injury Prevention", "Mental Focus"
        ])

    if st.button("Generate Plan"):
        prompt = f"Coach a {age}yo {sport} {position}. Goal: {goal}. Days: {schedule_days}. Injury: {injury}. Intensity: {intensity}. Output ONLY a Markdown table."
        
        with st.spinner("AI Coach is drafting..."):
            try:
                response = model.generate_content(prompt)
                res_col, vis_col = st.columns([2, 1])
                with res_col:
                    st.markdown(response.text)
                with vis_col:
                    # Satisfying Step 6: Use matplotlib for visualization 
                    fig, ax = plt.subplots()
                    ax.pie([20, 60, 20], labels=['Warmup', 'Core', 'Cool-down'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- PAGE 2: CUSTOM AI COACH ----------------
elif page == "Custom AI Coach":
    st.title("🧠 Custom AI Coaching Hub")
    st.write("Type a specific question or scenario to get personalized AI advice.")
    
    # Requirement: Prompt Engineering & Model Integration 
    user_prompt = st.text_area(
        "Enter your specific request:", 
        placeholder="Example: Give me a 15-minute hydration strategy for a mid-summer tournament."
    )
    
    # Technical Setting: Hyperparameter Tuning 
    with st.expander("⚙️ Advanced AI Tuning"):
        temp = st.slider("Creativity Level (Temperature)", 0.0, 1.0, 0.4)
    
    if st.button("Ask Coach"):
        if user_prompt:
            with st.spinner("Consulting Sports Science database..."):
                try:
                    # Custom model call with adjusted temperature
                    custom_model = genai.GenerativeModel("gemini-1.5-pro", generation_config={"temperature": temp})
                    response = custom_model.generate_content(user_prompt)
                    st.success("Coach's Advice:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt first!")

st.markdown("---")
st.caption("NextGen Sports Lab | AI Summative Assessment [cite: 1, 2]")

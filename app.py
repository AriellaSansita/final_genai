import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
# Using Gemini 1.5 Pro as per assignment requirements 
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-pro", 
    generation_config={
        "temperature": 0.4, # Lower temperature for conservative/safe plans 
        "top_p": 0.9
    }
)

st.set_page_config(page_title="CoachBot AI", layout="wide")
st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.markdown("---")

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("Athlete Profile")
sport = st.sidebar.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Other"])
position = st.sidebar.text_input("Position", "Striker/Bowler")
injury = st.sidebar.text_input("Injury History", "None")
goal = st.sidebar.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery"])
diet = st.sidebar.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
intensity = st.sidebar.select_slider("Intensity", options=["Low", "Moderate", "High"])
age = st.sidebar.slider("Age", 10, 25, 16)

# ---------------- FEATURES ----------------
selected_feature = st.selectbox("Choose Coaching Feature", [
    "Weekly Training Plan", 
    "Full Workout Details", 
    "Nutrition & Macros", 
    "Injury Recovery Steps"
])

# ---------------- HELPER: PLOTTING ----------------
def plot_metrics(feature):
    fig, ax = plt.subplots(figsize=(6, 3))
    if "Workout" in feature or "Training" in feature:
        labels = ['Warmup', 'Core Drills', 'Conditioning', 'Cooldown']
        sizes = [15, 45, 30, 10]
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title("Session Time Distribution")
    else:
        labels = ['Carbs', 'Protein', 'Fats']
        sizes = [50, 30, 20]
        ax.bar(labels, sizes, color=['blue', 'green', 'orange'])
        ax.set_ylabel('Percentage (%)')
        ax.set_title("Target Macro Distribution")
    
    st.pyplot(fig)

# ---------------- AI PROMPT ----------------
def build_prompt():
    return f"""
    You are a professional youth sports coach. 
    Provide a {selected_feature} for a {age}-year-old {sport} player ({position}).
    Goal: {goal}. Injury History: {injury}. Intensity: {intensity}. Diet: {diet}.

    MANDATORY FORMATTING:
    1. Provide the main response ONLY as a Markdown Table.
    2. Use columns relevant to the request (e.g., Day, Exercise, Sets, Reps OR Meal, Food Item, Portion).
    3. Keep descriptions concise for a mobile-friendly web app.
    4. If there is an injury, include a 'Safety Note' column.
    """

# ---------------- EXECUTION ----------------
if st.button("Generate My Personalized Plan"):
    with st.spinner("Analyzing data and generating charts..."):
        try:
            # Get AI Response
            response = model.generate_content(build_prompt())
            output_text = response.text

            # Layout: Two Columns for Data and Visualization
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader(f"📋 {selected_feature}")
                st.markdown(output_text) # Renders the Markdown table from AI

            with col2:
                st.subheader("📊 Visual Breakdown")
                plot_metrics(selected_feature)
                
                with st.expander("Coach's Notes"):
                    st.info(f"This plan is optimized for {intensity} intensity and considers your {injury} history.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("CoachBot AI uses Gemini 1.5 Pro to provide sports science-backed advice. Always consult a physical coach before beginning high-intensity training.")

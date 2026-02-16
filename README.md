
# Candidate Name - Ariella Sansita M

# Candidate Registration Number - 1000470

# CRS Name: Artificial Intelligence

# Course Name - Generative AI

# School name - Birla Open Minds International School, Kollur

# Summative Assessment

# Coach Bot

# Project Overview
CoachBot AI is a professional-grade fitness and tactical assistant designed for youth athletes. It bridges the gap between amateur training and professional coaching by providing data-driven insights tailored to specific sports, positions, and injury histories.

# Technical Stack
Language: 100% Python

Framework: Streamlit (UI & State Management)

AI Engine: Google Gemini 2.5 Flash (via google-generativeai)

Data Vis: Matplotlib (Session Load Analysis)

# Key Features (The "Distinguished" Requirements)
Multi-Prompt Toolkit: 10 specialized coaching modules including Injury Risk Prediction, Tactical Analysis, and Mental Focus.

Dynamic Nutrition Logic: Adaptive input fields that only trigger for nutrition-based queries, including allergy and dietary preference handling.

Hyperparameter Tuning: A user-controlled Intensity Slider (1-100) that maps directly to the AI model's Temperature setting to control the creativity and depth of the advice.

Automated Data Cleaning: Programmatic removal of HTML artifacts (like <br>) to ensure high-quality Markdown table rendering.

# Prompt Engineering Strategy
Explain that you used Role-Based Prompting and Constraint-Based Prompting.

Example: "The system enforces a strict 'Markdown-only' output constraint to ensure scannable, professional charts while preventing conversational filler."

# Installation & Setup

Clone the repo:

Bash
git clone https://github.com/your-username/coachbot-ai.git
Install dependencies:

Bash
pip install -r requirements.txt
Set up API Key:
Add your GOOGLE_API_KEY to your .streamlit/secrets.toml or environment variables.

Run the app:

Bash
streamlit run app.py

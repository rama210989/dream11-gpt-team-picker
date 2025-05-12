import streamlit as st
from gpt_engine import (
    get_best_dream11,
    get_weather_forecast,
    get_pitch_type,
    get_real_time_weather,
    get_pitch_conditions_from_weather,
)
from utils import load_csv_data, TEAM_LOGOS, TEAM_COLORS, VENUE_CITY_MAP

st.set_page_config(page_title="Dream11 Predictor - IPL", layout="wide")
st.title("🏏 Dream11 Team Predictor (Powered by GPT-4)")
st.markdown("Generate the best possible playing XI between two IPL teams using GenAI.")

# === Team Selection ===
teams = list(TEAM_LOGOS.keys())
col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Select Team 1", teams)
with col2:
    team2 = st.selectbox("Select Team 2", [t for t in teams if t != team1])

# === Logos and Theme ===
col_logo1, col_logo2 = st.columns(2)
with col_logo1:
    st.image(TEAM_LOGOS[team1], width=100)
with col_logo2:
    st.image(TEAM_LOGOS[team2], width=100)

st.markdown(
    f"<h3 style='color:{TEAM_COLORS[team1]}'> {team1} vs {team2} </h3>",
    unsafe_allow_html=True
)

# === Venue and Conditions ===
venue = st.selectbox("Select Venue", list(VENUE_CITY_MAP.keys()))
city = VENUE_CITY_MAP.get(venue, venue)

# === Weather Fetch ===
weather = ""
if st.button("🌤️ Fetch Real-Time Weather"):
    with st.spinner("Fetching live weather..."):
        weather = get_real_time_weather(city)
    st.success(f"Weather Forecast: {weather}")
else:
    weather = st.text_input("Weather (optional, e.g., Humid, Rain Expected)")

# === Analyze Weather → Pitch Impact ===
if weather:
    if st.button("🧠 Analyze Pitch Impact from Weather"):
        with st.spinner("Asking GPT..."):
            analysis = get_pitch_conditions_from_weather(weather, venue)
        st.info(analysis)

# === Toss and Batting Order ===
toss = st.selectbox("Who won the toss?", [team1, team2])
bat_first = st.selectbox("Which team is batting first?", [team1, team2])

# === Pitch Report Analysis ===
pitch_text = st.text_area("Paste Pitch Report", placeholder="Dry pitch, might assist spinners in 2nd innings...")
pitch_type = st.selectbox("Pitch Type (Manual)", ["Balanced", "Spin Friendly", "Pace Friendly"])

# === GPT-based Pitch Classification ===
if st.button("🔍 Analyze Pitch via GPT"):
    with st.spinner("Analyzing pitch report..."):
        pitch_type = get_pitch_type(pitch_text, venue)
    st.success(f"Predicted Pitch Type: {pitch_type}")

# === GPT-based Final Pitch from ALL Factors ===
if st.button("📊 Final Pitch Type (Based on Weather + Report + Venue)"):
    full_context = f"""
Venue: {venue}
City: {city}
Pitch Report: {pitch_text if pitch_text else 'Not provided'}
Weather: {weather if weather else 'Not provided'}
"""
    with st.spinner("Combining inputs and predicting final pitch behavior..."):
        pitch_type = get_pitch_type(full_context, venue)
    st.success(f"🏟️ Final Predicted Pitch Type: {pitch_type}")

# === Match Scoring Nature ===
avg_score_type = st.selectbox("Scoring Nature", ["High Scoring", "Low Scoring"])

# === CSV Upload ===
uploaded_stats = st.file_uploader("📁 Upload player stats CSV (optional)", type="csv")

# === GENERATE TEAM ===
if st.button("🚀 Generate Dream11 XI"):
    player_stats = load_csv_data(uploaded_stats) if uploaded_stats else None

    user_input = {
        "team1": team1,
        "team2": team2,
        "venue": venue,
        "toss": toss,
        "bat_first": bat_first,
        "pitch": pitch_type,
        "avg_score": avg_score_type,
        "weather": weather,
    }

    response = get_best_dream11(user_input, player_stats)
    st.subheader("💡 Suggested Dream11 Team:")
    st.code(response)

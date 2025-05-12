import streamlit as st
from gpt_engine import get_best_dream11
from utils import load_csv_data

st.set_page_config(page_title="Dream11 Predictor - IPL", layout="wide")

st.title("🏏 Dream11 Team Predictor (Powered by GPT-4)")
st.markdown("Generate the best possible playing XI between two IPL teams using GenAI.")

# === INPUTS ===
teams = ["CSK", "MI", "RCB", "KKR", "GT", "RR", "LSG", "SRH", "PBKS", "DC"]

col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Select Team 1", teams)
with col2:
    team2 = st.selectbox("Select Team 2", [t for t in teams if t != team1])

from utils import TEAM_LOGOS, TEAM_COLORS

col_logo1, col_logo2 = st.columns(2)
with col_logo1:
    st.image(TEAM_LOGOS[team1], width=100)
with col_logo2:
    st.image(TEAM_LOGOS[team2], width=100)

# Optional: Add a colored subheader
st.markdown(f"<h3 style='color:{TEAM_COLORS[team1]}'> {team1} vs {team2}</h3>", unsafe_allow_html=True)


venue = st.text_input("Venue (e.g., Wankhede Stadium)")
toss = st.selectbox("Who won the toss?", [team1, team2])
bat_first = st.selectbox("Which team is batting first?", [team1, team2])
pitch_type = st.selectbox("Pitch Type", ["Balanced", "Spin Friendly", "Pace Friendly"])
avg_score_type = st.selectbox("Scoring Nature", ["High Scoring", "Low Scoring"])
weather = st.text_input("Weather (optional, e.g., Humid, Rain Expected)")

uploaded_stats = st.file_uploader("Upload player stats CSV (optional)", type="csv")

# === GENERATE TEAM ===
if st.button("Generate Dream11 XI"):
    player_stats = load_csv_data(uploaded_stats) if uploaded_stats else None

    user_input = {
        "team1": team1,
        "team2": team2,
        "venue": venue,
        "toss": toss,
        "bat_first": bat_first,
        "pitch": pitch_type,
        "avg_score": avg_score_type,
        "weather": weather
    }

    response = get_best_dream11(user_input, player_stats)

    st.subheader("💡 Suggested Dream11 Team:")
    st.code(response)

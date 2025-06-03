import streamlit as st
import pandas as pd

# Load CSV data
@st.cache_data
def load_data():
    return pd.read_csv("67f163753b2cf.csv")

df = load_data()

st.title("IPL Dream11 Team Generator")

# Get unique teams from dataset
teams = df["Team"].dropna().unique().tolist()
teams.sort()

# Team selection
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", [team for team in teams if team != team1])

# Filter players by team
team1_players = df[df["Team"] == team1]
team2_players = df[df["Team"] == team2]

combined = pd.concat([team1_players, team2_players], ignore_index=True)

st.write(f"### {team1} Squad")
st.dataframe(team1_players[["Player", "Role", "Runs", "Wickets"]])

st.write(f"### {team2} Squad")
st.dataframe(team2_players[["Player", "Role", "Runs", "Wickets"]])

# Button to generate best XI
if st.button("Generate Team"):

    best_xi = []

    # Ensure 1 Wicketkeeper
    wk = combined[combined["Role"].str.contains("WK", na=False)]
    if not wk.empty:
        best_xi.append(wk.sort_values(by="Runs", ascending=False).iloc[0])

    # Ensure at least 1 All-Rounder
    ar = combined[combined["Role"].str.contains("All", na=False)]
    if not ar.empty:
        best_xi.append(ar.sort_values(by=["Runs", "Wickets"], ascending=False).iloc[0])

    # Ensure at least 1 Bowler
    bw = combined[combined["Role"].str.contains("Bowler", na=False)]
    if not bw.empty:
        best_xi.append(bw.sort_values(by="Wickets", ascending=False).iloc[0])

    # Ensure at least 1 Batsman
    bt = combined[combined["Role"].str.contains("Batsman", na=False)]
    if not bt.empty:
        best_xi.append(bt.sort_values(by="Runs", ascending=False).iloc[0])

    # Fill remaining spots by top performers (Runs + Wickets)
    remaining = combined[~combined["Player"].isin([p["Player"] for p in best_xi])]
    remaining["Score"] = remaining["Runs"].fillna(0) + remaining["Wickets"].fillna(0)*20
    remaining_sorted = remaining.sort_values(by="Score", ascending=False)
    best_xi += remaining_sorted.head(11 - len(best_xi)).to_dict('records')

    # Display selected team
    st.write("## Suggested Dream11 XI")
    final_df = pd.DataFrame(best_xi)[["Player", "Team", "Role", "Runs", "Wickets"]]
    st.dataframe(final_df.reset_index(drop=True))

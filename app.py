import streamlit as st
import pandas as pd

@st.cache_data
def load_orange_cap():
    return pd.read_csv("Orange Cap 2024.csv")

@st.cache_data
def load_purple_cap():
    return pd.read_csv("Purple cap 2024.csv")

# Load both datasets
orange_cap = load_orange_cap()
purple_cap = load_purple_cap()

st.title("IPL Dream11 Team Generator - Orange & Purple Cap Combined")

# Extract unique teams from both datasets
teams_orange = orange_cap["Team Name"].unique().tolist()
teams_purple = purple_cap["Team Name"].unique().tolist()

teams = sorted(set(teams_orange) | set(teams_purple))  # Union of teams

# Team selection dropdowns
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", [team for team in teams if team != team1])

# Filter batsmen & bowlers by selected teams
batsmen_team1 = orange_cap[orange_cap["Team Name"] == team1]
batsmen_team2 = orange_cap[orange_cap["Team Name"] == team2]

bowlers_team1 = purple_cap[purple_cap["Team Name"] == team1]
bowlers_team2 = purple_cap[purple_cap["Team Name"] == team2]

# Combine both teams for batsmen and bowlers separately
batsmen_combined = pd.concat([batsmen_team1, batsmen_team2], ignore_index=True)
bowlers_combined = pd.concat([bowlers_team1, bowlers_team2], ignore_index=True)

# Show squads for user info
st.write(f"### {team1} Batsmen Squad")
st.dataframe(batsmen_team1[["Player Name", "Total runs", "Matches Played", "Strike Rate"]])

st.write(f"### {team2} Batsmen Squad")
st.dataframe(batsmen_team2[["Player Name", "Total runs", "Matches Played", "Strike Rate"]])

st.write(f"### {team1} Bowlers Squad")
st.dataframe(bowlers_team1[["Player Name", "Wickets", "Matches", "Economy Rate"]])

st.write(f"### {team2} Bowlers Squad")
st.dataframe(bowlers_team2[["Player Name", "Wickets", "Matches", "Economy Rate"]])

if st.button("Pick Best 11"):

    # Pick top 6 batsmen by total runs
    top_batsmen = batsmen_combined.sort_values(by="Total runs", ascending=False).head(6)

    # Pick top 5 bowlers by wickets
    top_bowlers = bowlers_combined.sort_values(by="Wickets", ascending=False).head(5)

    # Combine for final XI
    best_xi = pd.concat([top_batsmen, top_bowlers], ignore_index=True)

    # Add a Role column for clarity
    best_xi.loc[:5, "Role"] = "Batsman"
    best_xi.loc[6:, "Role"] = "Bowler"

    # Select relevant columns to display
    display_cols_batsmen = ["Player Name", "Team Name", "Total runs", "Matches Played", "Strike Rate"]
    display_cols_bowlers = ["Player Name", "Team Name", "Wickets", "Matches", "Economy Rate"]

    # For display: merge batsmen and bowlers with missing columns filled for clarity
    best_xi_display = pd.DataFrame({
        "Player Name": best_xi["Player Name"],
        "Team Name": best_xi["Team Name"],
        "Role": best_xi["Role"],
        "Total runs": best_xi.get("Total runs", pd.Series([None]*len(best_xi))),
        "Wickets": best_xi.get("Wickets", pd.Series([None]*len(best_xi))),
        "Matches Played": best_xi.get("Matches Played", best_xi.get("Matches", pd.Series([None]*len(best_xi)))),
        "Strike Rate": best_xi.get("Strike Rate", pd.Series([None]*len(best_xi))),
        "Economy Rate": best_xi.get("Economy Rate", pd.Series([None]*len(best_xi))),
    })

    st.write("## Suggested Best Combined XI (6 Batsmen, 5 Bowlers)")
    st.dataframe(best_xi_display.reset_index(drop=True))

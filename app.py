import streamlit as st
import pandas as pd

# Load and clean Orange Cap data
@st.cache_data
def load_orange_cap():
    df = pd.read_csv("Dream 11 DB - Orange Cap 2024.csv")
    df = df.rename(columns={
        "Player Name": "Player",
        "Team Name": "Team",
        "Role": "Role",
        "Dream 11 Points": "Dream11 Points"
    })
    return df[["Player", "Team", "Role", "Dream11 Points"]]

# Load and clean Purple Cap data
@st.cache_data
def load_purple_cap():
    df = pd.read_csv("Dream 11 DB - Purple cap 2024.csv")
    df = df.rename(columns={
        "Player Name": "Player",
        "Team Name": "Team",
        "Role": "Role",
        "Dream 11 Points": "Dream11 Points"
    })
    return df[["Player", "Team", "Role", "Dream11 Points"]]

# Load data
orange_df = load_orange_cap()
purple_df = load_purple_cap()

# Combine and sum points for duplicate players
combined_df = pd.concat([orange_df, purple_df], ignore_index=True)
combined_df = combined_df.groupby(["Player", "Team", "Role"], as_index=False)["Dream11 Points"].sum()

# App title
st.title("🏏 IPL Dream11 Team Generator (2024)")

# Dropdowns for team selection
teams = sorted(combined_df["Team"].unique().tolist())
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", [team for team in teams if team != team1])

# Filter team-wise data
team1_df = combined_df[combined_df["Team"] == team1]
team2_df = combined_df[combined_df["Team"] == team2]

# Display stats
st.write(f"### {team1} Squad")
st.dataframe(team1_df.sort_values(by="Dream11 Points", ascending=False).reset_index(drop=True))

st.write(f"### {team2} Squad")
st.dataframe(team2_df.sort_values(by="Dream11 Points", ascending=False).reset_index(drop=True))

# Button to generate Best 11
if st.button("Pick Best 11"):

    # Combine both teams
    all_players = pd.concat([team1_df, team2_df], ignore_index=True)

    # Sort by points
    sorted_players = all_players.sort_values(by="Dream11 Points", ascending=False)

    # Pick top 11
    best_11 = sorted_players.head(11).reset_index(drop=True)

    st.write("## ⭐ Suggested Best 11")
    st.dataframe(best_11[["Player", "Team", "Role", "Dream11 Points"]])

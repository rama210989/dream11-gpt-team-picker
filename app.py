import streamlit as st
import pandas as pd

@st.cache_data
def load_orange_cap():
    df = pd.read_csv("Dream 11 DB - Orange Cap 2024.csv")
    df = df.rename(columns={"Player Name": "Player", "Team Name": "Team", "Dream 11 Points": "Dream11 Points", "Role": "Role"})
    return df

@st.cache_data
def load_purple_cap():
    df = pd.read_csv("Dream 11 DB - Purple cap 2024.csv")
    df = df.rename(columns={"Player Name": "Player", "Team Name": "Team", "Dream 11 Points": "Dream11 Points", "Role": "Role"})
    return df

orange_df = load_orange_cap()
purple_df = load_purple_cap()

st.title("IPL Dream11 Team Generator (2024)")

# Combine and aggregate Dream11 points by Player, Team, Role to avoid duplicates
combined_df = pd.concat([orange_df, purple_df], ignore_index=True)

# Sum Dream11 Points for duplicates, role and team assumed consistent per player
aggregated_df = combined_df.groupby(["Player", "Team", "Role"], as_index=False)["Dream11 Points"].sum()

# Get unique sorted list of teams from the combined dataset
teams = sorted(aggregated_df["Team"].unique())

team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", [team for team in teams if team != team1])

# Filter combined data for selected teams
team1_df = aggregated_df[aggregated_df["Team"] == team1]
team2_df = aggregated_df[aggregated_df["Team"] == team2]

# Display squads for both teams
st.write(f"### {team1} Squad")
st.dataframe(team1_df.sort_values(by="Dream11 Points", ascending=False))

st.write(f"### {team2} Squad")
st.dataframe(team2_df.sort_values(by="Dream11 Points", ascending=False))

if st.button("Pick Best 11"):
    # Combine players from both teams
    combined_teams = pd.concat([team1_df, team2_df], ignore_index=True)

    # Sort all players by Dream11 Points descending
    combined_teams = combined_teams.sort_values(by="Dream11 Points", ascending=False)

    # Role-wise constraints (example):
    # 1 WK, at least 3 batsmen, at least 3 bowlers, rest can be all-rounders or flexible
    # You can customize this as per your rules
    squad = []
    selected_players = set()

    # Pick 1 Wicket Keeper (highest points)
    wk = combined_teams[combined_teams["Role"] == "Wicket Keeper"]
    if not wk.empty:
        wk_player = wk.iloc[0]
        squad.append(wk_player)
        selected_players.add(wk_player["Player"])

    # Pick 3 Batsmen (excluding selected)
    batsmen = combined_teams[(combined_teams["Role"] == "Batsman") & (~combined_teams["Player"].isin(selected_players))]
    squad += batsmen.head(3).to_dict('records')
    selected_players.update([p["Player"] for p in batsmen.head(3).to_dict('records')])

    # Pick 3 Bowlers (excluding selected)
    bowlers = combined_teams[(combined_teams["Role"] == "Bowler") & (~combined_teams["Player"].isin(selected_players))]
    squad += bowlers.head(3).to_dict('records')
    selected_players.update([p["Player"] for p in bowlers.head(3).to_dict('records')])

    # Remaining 4 picks from All Rounders or any Role (excluding selected)
    remaining = combined_teams[~combined_teams["Player"].isin(selected_players)]
    squad += remaining.head(4).to_dict('records')

    # Create DataFrame from selected squad
    best_11_df = pd.DataFrame(squad)

    st.write("## Suggested Best 11 Dream11 Squad")
    st.dataframe(best_11_df.reset_index(drop=True)[["Player", "Team", "Role", "Dream11 Points"]])

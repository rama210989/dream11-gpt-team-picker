import streamlit as st
import pandas as pd

@st.cache_data
def load_orange_cap():
    df = pd.read_csv("Orange Cap 2024.csv")
    # Rename 'Total runs' to 'Runs' for consistency
    df = df.rename(columns={"Player Name": "Player", "Team Name": "Team", "Total runs": "Runs"})
    return df

@st.cache_data
def load_purple_cap():
    df = pd.read_csv("Purple cap 2024.csv")
    # Rename columns for consistency
    df = df.rename(columns={"Player Name": "Player", "Team Name": "Team"})
    return df

orange_df = load_orange_cap()
purple_df = load_purple_cap()

st.title("IPL Dream11 Team Generator (2024)")

# Get combined list of teams from both datasets
teams_orange = orange_df["Team"].unique().tolist()
teams_purple = purple_df["Team"].unique().tolist()
teams = sorted(list(set(teams_orange + teams_purple)))

# Team selection dropdowns
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", [team for team in teams if team != team1])

# Filter players by team
orange_team1 = orange_df[orange_df["Team"] == team1]
orange_team2 = orange_df[orange_df["Team"] == team2]
purple_team1 = purple_df[purple_df["Team"] == team1]
purple_team2 = purple_df[purple_df["Team"] == team2]

# Combine batting and bowling data for both teams
# For batting: use orange cap data (Runs)
# For bowling: use purple cap data (Wickets)

# Merge batting and bowling stats by Player and Team for both teams combined
batting = pd.concat([orange_team1, orange_team2], ignore_index=True)[["Player", "Team", "Runs"]]
bowling = pd.concat([purple_team1, purple_team2], ignore_index=True)[["Player", "Team", "Wickets"]]

# Fill missing wickets/runs with 0 for players missing in one dataset
batting["Runs"] = batting["Runs"].fillna(0)
bowling["Wickets"] = bowling["Wickets"].fillna(0)

# Merge on Player and Team, outer join to keep all players
combined = pd.merge(batting, bowling, on=["Player", "Team"], how="outer").fillna(0)

st.write(f"### {team1} Squad Batting Stats")
st.dataframe(orange_team1[["Player", "Runs"]].sort_values(by="Runs", ascending=False))

st.write(f"### {team1} Squad Bowling Stats")
st.dataframe(purple_team1[["Player", "Wickets"]].sort_values(by="Wickets", ascending=False))

st.write(f"### {team2} Squad Batting Stats")
st.dataframe(orange_team2[["Player", "Runs"]].sort_values(by="Runs", ascending=False))

st.write(f"### {team2} Squad Bowling Stats")
st.dataframe(purple_team2[["Player", "Wickets"]].sort_values(by="Wickets", ascending=False))


if st.button("Pick Best 11"):

    # Pick top 6 batsmen by Runs
    batsmen = combined.sort_values(by="Runs", ascending=False)
    top_batsmen = batsmen.head(6)

    # Pick top 5 bowlers by Wickets, excluding those already picked as batsmen
    bowlers = combined[~combined["Player"].isin(top_batsmen["Player"])]
    top_bowlers = bowlers.sort_values(by="Wickets", ascending=False).head(5)

    # Final team combined
    best_11 = pd.concat([top_batsmen, top_bowlers], ignore_index=True)

    st.write("## Suggested Best 11")
    st.dataframe(best_11.reset_index(drop=True)[["Player", "Team", "Runs", "Wickets"]])

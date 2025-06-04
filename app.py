import streamlit as st
import pandas as pd

# Emojis for roles
ROLE_EMOJIS = {
    "Wicket Keeper": "🧤",
    "Batsman": "🏏",
    "Bowler": "🎯",
    "All Rounder": "🤹"
}

# Colors for roles
ROLE_COLORS = {
    "Wicket Keeper": "#FFF3CD",  # light yellow
    "Batsman": "#D1E7DD",        # light green
    "Bowler": "#F8D7DA",         # light red
    "All Rounder": "#CCE5FF"     # light blue
}

# Load and clean data from single CSV
@st.cache_data
def load_data():
    df = pd.read_csv("Dream 11 DB  - Relevant Data.csv")
    df = df.rename(columns={
        "Player Name": "Player",
        "Team Name": "Team",
        "Role": "Role",
        "Dream 11 Points": "Dream11 Points"
    })

    # Group by Player, sum points, keep first Team and Role (assuming consistent per player)
    df_grouped = df.groupby("Player", as_index=False).agg({
        "Team": "first",
        "Role": "first",
        "Dream11 Points": "sum"
    })

    return df_grouped

data = load_data()

st.title("🏏 IPL Dream11 Team Generator (2024)")

# Teams dropdown from available teams in data
teams = sorted(data["Team"].unique())
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", [t for t in teams if t != team1])

# Filter players from selected teams
team1_df = data[data["Team"] == team1]
team2_df = data[data["Team"] == team2]

st.write(f"### {team1} Squad")
st.dataframe(team1_df.sort_values(by="Dream11 Points", ascending=False).reset_index(drop=True))

st.write(f"### {team2} Squad")
st.dataframe(team2_df.sort_values(by="Dream11 Points", ascending=False).reset_index(drop=True))

if st.button("Pick Best 11"):

    combined = pd.concat([team1_df, team2_df], ignore_index=True)
    combined = combined.sort_values(by="Dream11 Points", ascending=False)

    # Roles we must have at least one of
    required_roles = ["Wicket Keeper", "Batsman", "Bowler", "All Rounder"]
    selected_players = pd.DataFrame()

    # Pick top player per role first (if any)
    for role in required_roles:
        players_in_role = combined[combined["Role"] == role]
        if not players_in_role.empty:
            top_player = players_in_role.iloc[0]
            selected_players = pd.concat([selected_players, pd.DataFrame([top_player])])
        else:
            st.warning(f"No player found for role: {role}")

    # Remove selected players from combined
    remaining_players = combined[~combined["Player"].isin(selected_players["Player"])]

    # Fill remaining spots to make total 11 players
    remaining_slots = 11 - len(selected_players)
    if remaining_slots > 0:
        top_remaining = remaining_players.head(remaining_slots)
        selected_players = pd.concat([selected_players, top_remaining])

    selected_players = selected_players.reset_index(drop=True)

    # Add serial number 1-11
    selected_players.insert(0, "No.", range(1, len(selected_players) + 1))

    # Convert points to int (no decimals)
    selected_players["Dream11 Points"] = selected_players["Dream11 Points"].astype(int)

    # Add emoji before role
    selected_players["Role"] = selected_players["Role"].apply(lambda r: f"{ROLE_EMOJIS.get(r, '')} {r}")

    # Style function to color role cells
    def color_roles(row):
        role_with_emoji = row["Role"]
        # Extract role text after emoji and space
        role_name = role_with_emoji.split(" ", 1)[1] if " " in role_with_emoji else role_with_emoji
        color = ROLE_COLORS.get(role_name, "")
        return ["background-color: {}".format(color) if col == "Role" else "" for col in row.index]

    styled_df = selected_players.style.apply(color_roles, axis=1)

    st.write("## ⭐ Suggested Best 11")
    st.dataframe(styled_df)

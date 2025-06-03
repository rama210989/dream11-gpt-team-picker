import streamlit as st
import requests

# Fetch team and player data
def fetch_team_data(team_name):
    url = f"http://iplt20-stats.herokuapp.com/api/team/{team_name}"
    response = requests.get(url)
    return response.json()

def fetch_player_stats(player_id):
    url = f"http://iplt20-stats.herokuapp.com/api/player-details/{player_id}"
    response = requests.get(url)
    return response.json()

# Streamlit UI
st.title("IPL Dream11 Team Predictor")

# Dropdown for team selection
team1 = st.selectbox("Select Team 1", ["CSK", "MI", "RCB", "KKR", "GT", "RR", "LSG", "DC"])
team2 = st.selectbox("Select Team 2", ["CSK", "MI", "RCB", "KKR", "GT", "RR", "LSG", "DC"])

# Fetch and display team data
team1_data = fetch_team_data(team1)
team2_data = fetch_team_data(team2)

st.write(f"**{team1} Squad**")
st.write(team1_data)

st.write(f"**{team2} Squad**")
st.write(team2_data)

# Button to generate Dream11 XI
if st.button("Generate Dream11 XI"):
    # Logic to select best XI based on player stats
    best_xi = []
    for team in [team1_data, team2_data]:
        for player in team['players']:
            stats = fetch_player_stats(player['id'])
            # Basic selection criteria: top 5 players based on batting average
            if len(best_xi) < 5:
                best_xi.append((player['name'], stats['batting']['average']))
            else:
                min_avg_player = min(best_xi, key=lambda x: x[1])
                if stats['batting']['average'] > min_avg_player[1]:
                    best_xi.remove(min_avg_player)
                    best_xi.append((player['name'], stats['batting']['average']))

    st.write("**Suggested Dream11 XI**")
    for player, avg in sorted(best_xi, key=lambda x: x[1], reverse=True):
        st.write(f"{player} - Batting Average: {avg}")

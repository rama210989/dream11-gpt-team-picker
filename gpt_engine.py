import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_best_dream11(match_context, player_stats=None):
    prompt = f"""
You are a fantasy cricket expert. Given the context of an IPL match, suggest the best combined Dream11 XI from the two teams.

Context:
- Team 1: {match_context['team1']}
- Team 2: {match_context['team2']}
- Venue: {match_context['venue']}
- Toss: {match_context['toss']} won the toss
- Batting First: {match_context['bat_first']}
- Pitch: {match_context['pitch']}
- Average Score: {match_context['avg_score']}
- Weather: {match_context['weather']}

Factors to consider:
- Recent form (last 5 matches)
- Venue performance
- Death bowling preference
- Player vs team records
- Dream11 point scoring
- Team combination: 1-2 wicketkeepers, 3-5 batters, 1-3 all-rounders, 3-5 bowlers

{f"Stats:\n{player_stats.head(10).to_string(index=False)}" if player_stats is not None else ""}
    
Now, list the best possible Dream11 team (11 players) with their roles.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response['choices'][0]['message']['content']

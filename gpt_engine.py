from openai import OpenAI
import streamlit as st
import requests

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def get_weather_forecast(city):
    prompt = f"What is the typical weather forecast in {city} during IPL season in April and May? Give a 1-line summary."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content


def get_real_time_weather(city):
    api_key = "02d0becfc11b47d6b1657cac224dddbc"
    url = f"https://api.weatherbit.io/v2.0/forecast/daily?city={city}&key={api_key}&days=1"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            forecast = response.json().get("data", [])[0]
            if forecast:
                weather_description = forecast['weather']['description']
                min_temp = forecast['min_temp']
                max_temp = forecast['max_temp']
                humidity = forecast['rh']
                wind_speed = forecast['wind_spd']
                return (f"{weather_description}, Temp: {min_temp}°C–{max_temp}°C, "
                        f"Humidity: {humidity}%, Wind: {wind_speed} m/s")
            else:
                return "Weather data not available for this city."
        else:
            return f"Error: Unable to fetch weather data. HTTP Status Code: {response.status_code}"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"


def get_pitch_type(pitch_text, venue):
    prompt = f"""
You're a cricket analyst. Based on the following inputs, determine the likely pitch nature (Spin Friendly, Seam Friendly, or Balanced).
Use historical data of the venue if pitch report is not conclusive.

Venue: {venue}
Pitch Report:
\"\"\"
{pitch_text}
\"\"\"

Explain briefly your reasoning and give final classification at the end like:
Prediction: Spin Friendly
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content


def get_pitch_conditions_from_weather(weather_summary, venue):
    prompt = f"""
You're a cricket analyst. Based on the following weather forecast and venue, describe how the conditions will likely affect pitch behavior, swing/seam/spin support, and batting.

Weather Forecast: {weather_summary}
Venue: {venue}

Give a brief analysis on whether it supports spin/seam/batting and why.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content

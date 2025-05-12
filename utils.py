TEAM_LOGOS = {
    "CSK": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2e/Chennai_Super_Kings_Logo.svg/1200px-Chennai_Super_Kings_Logo.svg.png",
    "MI": "https://upload.wikimedia.org/wikipedia/en/thumb/2/25/Mumbai_Indians_Logo.svg/1200px-Mumbai_Indians_Logo.svg.png",
    "RCB": "https://upload.wikimedia.org/wikipedia/en/thumb/4/49/Royal_Challengers_Bangalore_Logo.svg/1200px-Royal_Challengers_Bangalore_Logo.svg.png",
    "KKR": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Kolkata_Knight_Riders_Logo.svg/1200px-Kolkata_Knight_Riders_Logo.svg.png",
    "GT": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/1200px-Gujarat_Titans_Logo.svg.png",
    "RR": "https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/1200px-Rajasthan_Royals_Logo.svg.png",
    "LSG": "https://upload.wikimedia.org/wikipedia/en/8/88/Lucknow_Super_Giants_Logo.svg",
    "SRH": "https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Sunrisers_Hyderabad.svg/1200px-Sunrisers_Hyderabad.svg.png",
    "PBKS": "https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg",
    "DC": "https://upload.wikimedia.org/wikipedia/en/5/5f/Delhi_Capitals.svg"
}

TEAM_COLORS = {
    "CSK": "#f4d03f",
    "MI": "#004ba0",
    "RCB": "#da291c",
    "KKR": "#3f2b96",
    "GT": "#0f1a2d",
    "RR": "#ff66b2",
    "LSG": "#00baf2",
    "SRH": "#f26522",
    "PBKS": "#c8102e",
    "DC": "#17449b"
}


import pandas as pd

def load_csv_data(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        return None

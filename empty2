import pandas as pd

# Define team logos (URLs)
TEAM_LOGOS = {
    "CSK": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2e/Chennai_Super_Kings_Logo.svg/1200px-Chennai_Super_Kings_Logo.svg.png",
    "MI": "https://upload.wikimedia.org/wikipedia/en/thumb/2/25/Mumbai_Indians_Logo.svg/1200px-Mumbai_Indians_Logo.svg.png",
    "RCB": "https://upload.wikimedia.org/wikipedia/en/thumb/4/49/Royal_Challengers_Bangalore_Logo.svg/1200px-Royal_Challengers_Bangalore_Logo.svg.png",
    "KKR": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Kolkata_Knight_Riders_Logo.svg/1200px-Kolkata_Knight_Riders_Logo.svg.png",
    "GT": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/1200px-Gujarat_Titans_Logo.svg.png",
    "RR": "https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/1200px-Rajasthan_Royals_Logo.svg.png",
    "LSG": "https://upload.wikimedia.org/wikipedia/en/8/88/Lucknow_Super_Giants_Logo.svg",
    "DC": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5e/Delhi_Capitals_logo.svg/1200px-Delhi_Capitals_logo.svg.png",
}

# Define team colors
TEAM_COLORS = {
    "CSK": "#FFB81C",
    "MI": "#005B8C",
    "RCB": "#E20A22",
    "KKR": "#512D6D",
    "GT": "#1E4A6E",
    "RR": "#004B87",
    "LSG": "#0076A5",
    "DC": "#1D3557",
}

# Define venue to city mapping
VENUE_CITY_MAP = {
    "Wankhede Stadium": "Mumbai",
    "Eden Gardens": "Kolkata",
    "M Chinnaswamy Stadium": "Bangalore",
    "Arun Jaitley Stadium": "Delhi",
    "Sawai Mansingh Stadium": "Jaipur",
    "DY Patil Stadium": "Navi Mumbai",
    "Narendra Modi Stadium": "Ahmedabad",
    "Pune": "Pune",
}

# Function to load CSV data
def load_csv_data(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        return None

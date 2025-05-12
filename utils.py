import pandas as pd

def load_csv_data(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        return None

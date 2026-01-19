import os
import json
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

def fetch_neo_data(start_date: str, end_date: str):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": NASA_API_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"NASA API Error: {response.status_code} - {response.text}")

    return response.json()


def save_raw_data(data: dict, start_date: str):
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/neo_{start_date}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved raw data to {filename}")


if __name__ == "__main__":
    today = date.today().isoformat()
    data = fetch_neo_data(today, today)
    save_raw_data(data, today)

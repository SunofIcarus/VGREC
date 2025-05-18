import requests
import json
from pathlib import Path
import streamlit as st

API_KEY = st.secrets["RAWG_API_KEY"]
RAWG_API_URL = "https://api.rawg.io/api/games"
OUTPUT_PATH = Path("data/raw/games.json")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

params = {
    "key": API_KEY,
    "page_size": 40,
    "ordering": "-rating"
}

all_games = []

# Fetch multiple pages (increase range as needed)
for page in range(1, 6):  # 5 pages x 40 games = 200 games
    params["page"] = page
    response = requests.get(RAWG_API_URL, params=params)
    if response.status_code != 200:
        print(f"Error fetching page {page}: {response.status_code}")
        break

    data = response.json()
    all_games.extend(data.get("results", []))
    print(f"Fetched page {page}, total games: {len(all_games)}")

# Save all fetched games to disk
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(all_games, f, indent=2, ensure_ascii=False)

print(f"Saved {len(all_games)} games to {OUTPUT_PATH}")
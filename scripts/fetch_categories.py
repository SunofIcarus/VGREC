import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
RAWG_API_URL = "https://api.rawg.io/api"

def fetch_categories(endpoint):
    url = f"{RAWG_API_URL}/{endpoint}?key={API_KEY}"
    response = requests.get(url)
    print(url)
    data = response.json()
    return [item["name"] for item in data["results"]]

def save_to_file(name, items):
    path = Path(f"data/raw/{name}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path,"w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

genres = fetch_categories("genres")
platforms = fetch_categories("platforms")
tags = fetch_categories("tags")

save_to_file("genres", genres)
save_to_file("platforms", platforms)
save_to_file("tags", tags)
print(f"Fetched and saved {len(genres)} genres, {len(platforms)} platforms, and {len(tags)} tags.")
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")

params = {
    "key": API_KEY,
    "page" : 1,
    "page_size" : 40,
    "genres" : "action",
    "platforms" : "4,187,1",
    "ordering" : "-rating",
}

url = "https://api.rawg.io/api/games"
response = requests.get(url, params=params)

output = Path("data/raw/games.json")
output.parent.mkdir(parents=True, exist_ok=True)

data = response.json()

games = data["results"]

with open(output, "w", encoding="utf-8") as f:
    json.dump(response.json(), f, indent=2, ensure_ascii=False)

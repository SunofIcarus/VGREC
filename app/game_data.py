import json
from typing import List, Dict
from pathlib import Path

def load_games(filepath="data/raw/games.json"):
    """
    Load game data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file containing game data.
        
    Returns:
        List[dict]: A list of game dictionaries.
    """

    # Ensure the file exists
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath} not found.")

    # Load the JSON data
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        raw_games = data["results"]

    print(type(data))
    

    cleaned_games = []
    for game in raw_games:
        # Clean up the game data
        cleaned_game = {
            "id": game["id"],
            "name": game["name"],
            "rating": game["rating"],
            "platforms": [platform["platform"]["name"] for platform in game["platforms"]],
            "genres": [genre["name"] for genre in game["genres"]],
            "release_date": game["released"],
            "image_url": game["background_image"],
        }
        
        # Get all tag names in lowercase
        tag_names = [tag["name"].lower() for tag in game.get("tags", [])]

        # Filter keywords that suggest it's not a full game
        dlc_keywords = ["dlc", "expansion", "bundle", "remaster", "demo", "beta", "season pass"]

        # Also filter by slug (sometimes RAWG uses it directly)
        slug = game.get("slug", "").lower()
        name = game.get("name", "").lower()

        # If any keyword is found in tags, name, or slug — skip
        if any(keyword in tag_names for keyword in dlc_keywords) or \
        any(keyword in name for keyword in dlc_keywords) or \
        any(keyword in slug for keyword in dlc_keywords):
            continue

        cleaned_games.append(cleaned_game)

    return cleaned_games # Return the list of games
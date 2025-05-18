import streamlit as st
import requests

API_KEY = st.secrets["RAWG_API_KEY"]

def title_to_slug(title):
    """
    Convert a game title to a slug format.
    
    Args:
        title (str): The game title.
        
    Returns:
        str: The slugified version of the title.
    """
    return title.lower().replace(" ", "-").replace("'", "").replace(":", "")

def get_game_description(title):
    slug = title_to_slug(title)
    search_url = f"https://api.rawg.io/api/games/{slug}"
    response = requests.get(search_url, params={"key": API_KEY})

    if response.status_code != 200:
        return None
    
    data = response.json()
    return data.get("description_raw") or data.get("description") or data.get("summary")
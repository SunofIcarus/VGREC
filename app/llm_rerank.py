from mistralai import Mistral
import streamlit as st
import requests

API_KEY = st.secrets["MISTRAL_API_KEY"]
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def rerank_game(user_profile_text: str, game_name: str, game_description: str) -> float:
    """
    Rerank a game based on user profile and game description using Mistral API.

    Args:
        user_profile_text (str): User profile text.
        game_name (str): Name of the game.
        game_description (str): Description of the game.

    Returns:
        float: Reranked score for the game.
    """
    
    prompt = f"""
    You are a video game recommender system. Given a user profile and a game description, rate the game on a scale from 0 to 10 based on how well it matches the user's preferences.

    A game is considered a good match if it aligns with the user's interests, genres, and playstyles. A score of 10 means the game is a perfect match, while a score of 0 means it is not suitable for the user.
    Please provide a score based on the following information:
    User Profile: {user_profile_text}
    Game Name: {game_name}
    Game Description: {game_description}

    Rate the game from 0 to 10:

    If the game appears to be an adult game, please return a score of 0.
    
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "open-mistral-7b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        try:
            return float(answer.strip())
        except ValueError:
            return 5.0
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return 0.0

  
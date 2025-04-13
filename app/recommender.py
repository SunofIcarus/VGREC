from app.user_profile import UserProfile
from typing import List, Dict

def get_recommendation(user: UserProfile, games: List[Dict]) -> List[Dict]:
    """
    Get game recommendations based on user profile and game data.

    Args:
        user (UserProfile): The user's profile containing preferences.
        games (List[Dict]): List of game dictionaries.

    Returns:
        List[Dict]: A list of recommended games.
    """
    recommended_games = []

    # Filter games based on user's preferred genres and consoles
    for game in games:
        score = 0
        if any(genre in game["genres"] for genre in user.genres) and any(console in game["platforms"] for console in user.consoles):
            recommended_games.append(game)

    return recommended_games[:10]  # Return top 10 recommendations
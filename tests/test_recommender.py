import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.game_data import load_games
from app.user_profile import UserProfile
from app.recommender import get_recommendation


user = UserProfile(
    consoles=["PC", "PlayStation 5"],
    genres=["RPG", "Action"],
    favorite_games=[],
    favorite_movies=[],
    favorite_books=[],
    favorite_music=[],
    playstyles=[]
)

games = load_games()
print(games[0])
recommended_games = get_recommendation(user, games)
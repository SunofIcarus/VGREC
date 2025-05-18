import streamlit as st
from app.user_profile import UserProfile
from app.recommender import get_recommendation
from app.game_data import load_games
import json




with open("data/raw/genres.json") as f:
    genres = json.load(f)
with open("data/raw/platforms.json") as f:
    platforms = json.load(f)    
with open("data/raw/tags.json") as f:
    tags = json.load(f)

st.title("Video Game Recommendation System")
st.write("This app recommends video games based on user preferences.")

consoles = st.multiselect("Select your consoles:", platforms)
genres = st.multiselect("Select your preferred genres:", genres)  

favorite_games = st.text_input("Favorite games (comma-separated)")
favorite_movies = st.text_input("Favorite movies (comma-separated)")
favorite_books = st.text_input("Favorite books (comma-separated)")

playstyles = st.multiselect(
    "Preferred playstyle(s)", tags)

min_year, max_year = st.slider("Release year range", 1980, 2025, (2000, 2025))

if st.button("Get Recommendations"):
    # Convert comma-separated strings to lists
    favorite_games_list = [game.strip() for game in favorite_games.split(",")] if favorite_games else []
    favorite_movies_list = [movie.strip() for movie in favorite_movies.split(",")] if favorite_movies else []
    favorite_books_list = [book.strip() for book in favorite_books.split(",")] if favorite_books else []

    user_profile = UserProfile(
        consoles=consoles,
        genres=genres,
        favorite_games=favorite_games_list,
        favorite_movies=favorite_movies_list,
        favorite_books=favorite_books_list,
        playstyles=playstyles
    )

    games = load_games()
    recommended_games = get_recommendation(user_profile, games, year_range=(min_year, max_year))

    st.subheader("Recommended Games:")
    for game in recommended_games:
        st.markdown(f"### {game['name']}")
        st.image(game["image_url"], width=500)
        st.markdown(f"**Score:** {game['score']}")
        st.markdown(f"**Genres:** {', '.join(game['genres'])}")
        st.markdown(f"**Platforms:** {', '.join(game['platforms'])}")
        if "stores" in game and game["stores"]:
            st.markdown("**Available on:**")
            for store in game["stores"]:
                st.markdown(f"- [{store['name']}]({store['url']})")
        st.markdown("---")
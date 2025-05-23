from app.user_profile import UserProfile
from app.embedding_cache import load_embedding_cache, get_cached_embedding, update_embedding_cache
from typing import List, Dict
from mistralai import Mistral
from numpy import dot
from numpy.linalg import norm
from app.movie_lookup import get_movie_description
from app.book_lookup import get_book_description
from app.game_lookup import get_game_description
from app.llm_rerank import rerank_game
import time
import streamlit as st

api_key = st.secrets["MISTRAL_API_KEY"]


client = Mistral(api_key=api_key)

embedding_cache = load_embedding_cache()

def get_embedding(text: str):
    text_key = text.strip().lower()
    cached = get_cached_embedding(text_key, embedding_cache)
    if cached:
        return cached
    response = client.embeddings.create(
        model = "mistral-embed",
        inputs = [text]
    )
    embedding = response.data[0].embedding

    update_embedding_cache(text_key, embedding, embedding_cache)
    return embedding

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def get_recommendation(user: UserProfile, games: List[Dict], year_range=(int,int)) -> List[Dict]:
    """
    Get game recommendations based on user profile and game data.

    Args:
        user (UserProfile): The user's profile containing preferences.
        games (List[Dict]): List of game dictionaries.

    Returns:
        List[Dict]: A list of recommended games.
    """
    recommended_games = []
    

    user_text_parts = []

    with st.spinner("Loading game descriptions..."):
        for game in user.favorite_games:
            description = get_game_description(game)
            if description:
                user_text_parts.append(description)
            else:
                user_text_parts.append(game)
    with st.spinner("Loading movie descriptions..."):
        for movie in user.favorite_movies:
            description = get_movie_description(movie)
            if description:
                user_text_parts.append(description)
            else:
                user_text_parts.append(movie)
    with st.spinner("Loading book descriptions..."):
        for book in user.favorite_books:
            description = get_book_description(book)
            if description:
                user_text_parts.append(description)
            else:
                user_text_parts.append(book)
    
    
    
    user_text = " ".join(user_text_parts)
    user_embedding = get_embedding(user_text)


    skipped_no_year = 0
    skipped_year_range = 0
    skipped_platform = 0
    # Filter games based on user's preferred genres and consoles
    with st.spinner("Ranking games..."):
        for game in games:
            retry_count = 0
            max_retries = 3
            backoff_time = 2  # seconds
            score = 0
            passed = 0
            

            if not game.get("release_year"):
                skipped_no_year += 1
                continue

            if not (year_range[0] <= game["release_year"] <= year_range[1]):
                skipped_year_range += 1
                continue

            if not any(console in game["platforms"] for console in user.consoles):
                skipped_platform += 1
                continue
            
            passed += 1

            game_text = game.get('description', '')
            while retry_count < max_retries:
                try:
                    game_embedding = get_embedding(game_text)
                    break  # Exit the loop if successful
                except Exception as e:
                    print(f"Error getting embedding for game {game['name']}: {e}")
                    retry_count += 1
                    wait_time = backoff_time ** retry_count
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            similarity = cosine_similarity(user_embedding, game_embedding)
            game['similarity'] = similarity


            for genre in user.genres:
                if genre in game['genres']:
                    score += 1
            for console in user.consoles:
                if console in game['platforms']:
                    score += 1
            
            final_score = (0.5 * score + 0.5 * game['similarity'])
            game['score'] = final_score
            recommended_games.append(game)

        sorted_games = sorted(recommended_games, key=lambda x: x['score'], reverse=True)
        print(f"Filtered games: {passed}")
        print(f"Skipped games: {skipped_no_year + skipped_year_range + skipped_platform}")
        print(f"Skipped no year: {skipped_no_year}")
        print(f"Skipped year range: {skipped_year_range}")
        print(f"Skipped platform: {skipped_platform}")

        top_games =  sorted_games[:50]  # Return top 50 recommendation

    with st.spinner("Reranking games..."):
        for game in top_games:
            retry_count = 0
            max_retries = 3
            backoff_time = 2  # seconds

            while retry_count < max_retries:
                try:
                    game["llm_score"] = rerank_game(user_text, game["name"], game.get("description", ""))
                    time.sleep(2.5)  # Adding a delay to avoid hitting the API rate limit
                    break
                except Exception as e:
                    print(f"Error getting reccomendation for game {game['name']}: {e}")
                    retry_count += 1
                    wait_time = backoff_time ** retry_count
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

    final_sorted = sorted(top_games, key=lambda x: x['llm_score'], reverse=True)
    return final_sorted[:20]  # Return top 20 recommendations
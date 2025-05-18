import requests
import streamlit as st

API_KEY = st.secrets["TMDB_API_KEY"]
API_URL = "https://api.themoviedb.org/3/search/movie"

def get_movie_description(title):
    params = {
        "api_key": API_KEY,
        "query": title,
    }

    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        return None
    
    results = response.json().get("results")
    if not results:
        return None
    
    print(results[0].get("overview"))
    
    return results[0].get("overview")
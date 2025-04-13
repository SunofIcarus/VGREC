from pydantic import BaseModel
from typing import List



class UserProfile(BaseModel):
    consoles : List[str]
    genres : List[str]
    favorite_games : List[str]
    favorite_movies : List[str]
    favorite_books : List[str]
    playstyles : List[str]

    def __init__(self, **data):
        super().__init__(**data)
        self.consoles = data.get('consoles', [])
        self.genres = data.get('genres', [])
        self.favorite_games = data.get('favorite_games', [])
        self.favorite_movies = data.get('favorite_movies', [])
        self.favorite_books = data.get('favorite_books', [])
        self.playstyles = data.get('playstyles', [])
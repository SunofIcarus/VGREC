from fastapi import FastAPI
from app.user_profile import UserProfile

app = FastAPI()



@app.get("/recommend")
async def recommend(user_profile: UserProfile):
    # Here you would implement the recommendation logic based on the user profile
    # For demonstration purposes, we'll just return the user profile back
    return user_profile.model_dump()
# ----- Mood Recommendation Service -----
"""
Required:
    pip install fastapi uvicorn

Run:
    uvicorn MoodRecommendationService:app --reload --port 8003
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Data Model
# -----------------------------
class MoodRequest(BaseModel):
    mood_score: int   # 1 = negative, 2 = neutral, 3 = positive

# -----------------------------
# Static Recommendation Data
# -----------------------------
coping_strategies = {
    1: [
        "Take 3 slow deep breaths",
        "Try writing your feelings in a journal",
        "Go for a short walk to clear your mind",
        "Listen to relaxing music"
    ],
    2: [
        "Do a quick stretch",
        "Drink some water and take a mindful pause",
        "Organize your workspace to reset your focus"
    ],
    3: [
        "Celebrate your small wins today!",
        "Share your good mood with a friend",
        "Keep doing what makes you feel energized"
    ]
}

osu_resources = {
    1: [
        "OSU Counseling & Psychological Services (CAPS)",
        "Mind Spa — guided relaxation tools",
    ],
    2: [
        "Academic Success Center — study support",
    ],
    3: [
        "Recreational Sports — join a fitness class!",
    ]
}

# -----------------------------
# Routes
# -----------------------------
@app.post("/recommendations")
def get_recommendations(request: MoodRequest):
    score = request.mood_score

    # Default values if score is out of range
    strategies = coping_strategies.get(score, coping_strategies[2])
    resources = osu_resources.get(score, osu_resources[2])

    return {
        "coping_strategies": strategies,
        "osu_resources": resources
    }

# ----- Mood Trend Service -----
"""
Required:
    pip install fastapi uvicorn

Run:
    uvicorn MoodTrendService:app --reload --port 8002
"""

from fastapi import FastAPI
import json
import os

app = FastAPI()
file_path = "mood_log.json"

# Load mood log from file
def load_data():
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)

@app.get("/trend")
def get_trend(user_id: str):
    data = load_data()

    if user_id not in data or len(data[user_id]) < 2:
        return {"trend": "not enough data"}

    entries = data[user_id]

    # convert moods into numeric scale
    mood_score = {"positive": 3, "neutral": 2, "negative": 1}

    scores = []
    for e in entries:
        m = e.get("mood_type", "neutral")
        scores.append(mood_score.get(m, 2))

    # simple trend check
    if scores[-1] > scores[-2]:
        result = "improving"
    elif scores[-1] < scores[-2]:
        result = "declining"
    else:
        result = "stable"

    return {"trend": result}

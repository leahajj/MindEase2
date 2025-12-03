# ----- README -----
"""
Run with:
    uvicorn MoodSummaryService:app --reload --port 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

FILE_PATH = "mood_log.json"

# ----- Utility Functions -----

def load_data() -> Dict[str, List[Dict[str, Any]]]:
    """Load the mood data file."""
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as f:
        return json.load(f)


# ----- ROUTES -----

@app.get("/daily_summary")
async def daily_summary(user_id: str, date: str) -> Dict[str, Any]:
    """
    Returns:
        entries_today: number of entries for the date
        average_today: average mood score for the date
    """
    data = load_data()
    user_data = data.get(user_id, [])

    # convert moods to numeric scores
    mood_score = {
        "positive": 3,
        "neutral": 2,
        "negative": 1,
        "undefined": 0
    }

    entries_today = [entry for entry in user_data if entry["date"] == date]

    if not entries_today:
        return {
            "entries_today": 0,
            "average_today": 0
        }

    avg = sum(mood_score[e["mood_type"]] for e in entries_today) / len(entries_today)

    return {
        "entries_today": len(entries_today),
        "average_today": round(avg, 2)
    }


@app.get("/weekly_summary")
async def weekly_summary(user_id: str) -> Dict[str, Any]:
    """
    Returns:
        entries_week: total number of logs this week
        weekly_average: average mood score this week
    """
    data = load_data()
    user_data = data.get(user_id, [])

    mood_score = {
        "positive": 3,
        "neutral": 2,
        "negative": 1,
        "undefined": 0
    }

    today = datetime.now().date()
    week_ago = today - timedelta(days=7)

    week_entries = [
        entry for entry in user_data
        if week_ago <= datetime.strptime(entry["date"], "%Y-%m-%d").date() <= today
    ]

    if not week_entries:
        return {
            "entries_week": 0,
            "weekly_average": 0
        }

    avg = sum(mood_score[e["mood_type"]] for e in week_entries) / len(week_entries)

    return {
        "entries_week": len(week_entries),
        "weekly_average": round(avg, 2)
    }

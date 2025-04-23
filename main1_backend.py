from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import datetime
import json
import os
from statistics import stdev

app = FastAPI()

THRESHOLD = 20
DATA_FILE = "race_data.json"
race_data = []

IMPROVEMENT_TIPS = {
    "Elite": (0, 15, (
        "Outstanding! Keep up the training to maintain your edge.",
        "Focus on recovery techniques like ice baths and massage therapy to avoid injuries.",
        "Experiment with advanced speed training drills like overspeed running to break your limits."
    )),
    "Intermediate": (15, 17, (
        "Great performance! Focus on speed drills and endurance.",
        "Incorporate interval training into your routine to enhance both speed and stamina.",
        "Refine your running technique to minimize energy wastage during sprints."
    )),
    "Novice": (17, 20, (
        "Good effort! Work on strength training and agility.",
        "Add hill sprints to your workouts to build power and explosiveness.",
        "Improve your diet by including more protein-rich foods to support muscle recovery."
    )),
    "Beginner": (20, 25, (
        "You're getting there! Focus on basic conditioning.",
        "Start a consistent training schedule with gradual increases in intensity.",
        "Work on improving your cardiovascular endurance with steady-state runs."
    )),
    "Needs Improvement": (25, float('inf'), (
        "Consider starting with consistent running practice and building stamina.",
        "Walk/run intervals can help build your endurance if you're just beginning.",
        "Consult a coach or join a running group to stay motivated and get guidance."
    ))
}

class RaceResult(BaseModel):
    name: str
    timing: float

class PerformanceStats(BaseModel):
    name: str
    total_races: int
    average_timing: float
    below_threshold: int
    above_threshold: int
    details: List[dict]

class ImprovementTips(BaseModel):
    level: str
    tips: List[str]

def load_data():
    global race_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            race_data = json.load(file)

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(race_data, file, indent=4)

def get_improvement_tip(timing):
    for level, (min_time, max_time, tips) in IMPROVEMENT_TIPS.items():
        if min_time <= timing < max_time:
            return level, tips
    return "Undefined", ["No tips available."]

@app.post("/add_race_result")
def add_race_result(result: RaceResult):
    date = datetime.date.today().strftime('%Y-%m-%d')
    status = "Below Threshold" if result.timing <= THRESHOLD else "Above Threshold"
    level, tips = get_improvement_tip(result.timing)

    race_entry = {
        "name": result.name,
        "timing": result.timing,
        "date": date,
        "status": status,
        "level": level,
        "tips": tips
    }

    race_data.append(race_entry)
    save_data()
    return {"entry": race_entry}

@app.get("/view_performance/{name}", response_model=PerformanceStats)
def view_performance(name: str):
    user_results = [entry for entry in race_data if entry['name'].lower() == name.lower()]
    if not user_results:
        return {"error": "No results found for this user."}

    total_races = len(user_results)
    below_threshold = sum(1 for result in user_results if result["status"] == "Below Threshold")
    above_threshold = total_races - below_threshold
    average_timing = sum(result["timing"] for result in user_results) / total_races

    return {
        "name": name,
        "total_races": total_races,
        "average_timing": average_timing,
        "below_threshold": below_threshold,
        "above_threshold": above_threshold,
        "details": user_results
    }

@app.get("/get_improvement_tips/{timing}", response_model=ImprovementTips)
def get_tips_by_timing(timing: float):
    level, tips = get_improvement_tip(timing)
    return {"level": level, "tips": tips}
@app.get("/ai_assistant/{name}")
def ai_assistant(name: str):
    """AI Assistant summary endpoint."""
    user_results = [entry for entry in race_data if entry['name'].lower() == name.lower()]

    if not user_results:
        return {"error": "No results found for this user."}

    total_races = len(user_results)
    timings = [result["timing"] for result in user_results]
    average_timing = sum(timings) / total_races
    current_level, smart_tips = get_improvement_tip(timings[-1])

    # Simple trend analysis (based on first and last timing)
    trend = "Improving" if timings[-1] < timings[0] else "Declining" if timings[-1] > timings[0] else "Stable"

    # Simple consistency analysis (standard deviation threshold)
    import statistics
    std_dev = statistics.stdev(timings) if len(timings) > 1 else 0
    consistency = "Consistent" if std_dev < 1.0 else "Inconsistent"

    return {
        "name": name,
        "total_races": total_races,
        "average_timing": average_timing,
        "trend_analysis": trend,
        "consistency_analysis": consistency,
        "current_level": current_level,
        "smart_tips": smart_tips
    }


# Load data on startup
load_data()

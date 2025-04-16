# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# import datetime
# import json
# import os

# app = FastAPI()

# # Threshold for sprint evaluation
# THRESHOLD = 20.0
# DATA_FILE = "race_data.json"

# # In-memory race data (loaded from file)
# race_data = []

# # Improvement tips dictionary
# IMPROVEMENT_TIPS = {
#     "Elite": (0, 11, [
#         "Maintain your peak form.",
#         "Include tapering in your training.",
#         "Get adequate recovery before events.",
#     ]),
#     "Advanced": (11, 13, [
#         "Improve acceleration through sprint drills.",
#         "Focus on strength and conditioning.",
#         "Add resistance sprint training.",
#     ]),
#     "Intermediate": (13, 15, [
#         "Work on running posture and foot placement.",
#         "Add interval sprint training.",
#         "Improve stride frequency.",
#     ]),
#     "Beginner": (15, float('inf'), [
#         "Start with basic sprinting technique drills.",
#         "Build cardiovascular endurance.",
#         "Do consistent 100m runs and track progress.",
#     ])
# }

# # Models
# class RaceResult(BaseModel):
#     name: str
#     timing: float

# class ImprovementTips(BaseModel):
#     level: str
#     tips: List[str]

# # Load race data from file
# def load_data():
#     global race_data
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r") as file:
#             race_data = json.load(file)

# # Save race data to file
# def save_data():
#     with open(DATA_FILE, "w") as file:
#         json.dump(race_data, file, indent=4)

# # Get performance level and tips
# def get_improvement_tip(timing: float):
#     for level, (min_time, max_time, tips) in IMPROVEMENT_TIPS.items():
#         if min_time <= timing < max_time:
#             return level, tips
#     return "Unknown", ["No tips available."]

# # API to add race result
# @app.post("/add_race_result")
# def add_race_result(result: RaceResult):
#     date = datetime.date.today().strftime('%Y-%m-%d')
#     status = "Below Threshold" if result.timing <= THRESHOLD else "Above Threshold"
#     level, tips = get_improvement_tip(result.timing)

#     entry = {
#         "name": result.name,
#         "timing": result.timing,
#         "date": date,
#         "status": status,
#         "level": level,
#         "tips": tips
#     }

#     race_data.append(entry)
#     save_data()

#     return entry

# # API to view performance of a user
# @app.get("/view_performance/{name}")
# def view_performance(name: str):
#     user_results = [entry for entry in race_data if entry["name"].lower() == name.lower()]
#     if not user_results:
#         return {"error": "No records found for this user."}

#     total_races = len(user_results)
#     avg_timing = sum([r["timing"] for r in user_results]) / total_races
#     below_threshold = sum(1 for r in user_results if r["status"] == "Below Threshold")
#     above_threshold = total_races - below_threshold

#     return {
#         "name": name,
#         "total_races": total_races,
#         "average_timing": avg_timing,
#         "below_threshold": below_threshold,
#         "above_threshold": above_threshold,
#         "details": user_results
#     }

# # API to get improvement tips by timing
# @app.get("/get_improvement_tips/{timing}", response_model=ImprovementTips)
# def get_improvement_tips(timing: float):
#     level, tips = get_improvement_tip(timing)
#     return {"level": level, "tips": tips}

# # Smart AI voice feedback endpoint
# @app.get("/ai_assistant/{name}")
# def ai_assistant(name: str):
#     user_results = [entry for entry in race_data if entry["name"].lower() == name.lower()]
#     if not user_results:
#         return {"error": "No data found for this user."}

#     timings = [res["timing"] for res in user_results]
#     trend = "Improving" if timings[-1] < timings[0] else "Declining"
#     consistency = "Consistent" if max(timings) - min(timings) < 1.5 else "Variable"
#     avg = sum(timings) / len(timings)

#     level, tips = get_improvement_tip(avg)

#     return {
#         "name": name,
#         "total_races": len(user_results),
#         "trend_analysis": trend,
#         "consistency_analysis": consistency,
#         "current_level": level,
#         "smart_tips": tips
#     }

# # Load data when server starts
# load_data()

# # To run: uvicorn main:app --reload


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime
import json
import os

app = FastAPI()

# Threshold for sprint evaluation
THRESHOLD = 20.0
DATA_FILE = "race_data.json"

# In-memory race data (loaded from file)
race_data = []

# Improvement tips dictionary
IMPROVEMENT_TIPS = {
    "Elite": (0, 11, [
        "Maintain your peak form.",
        "Include tapering in your training.",
        "Get adequate recovery before events.",
    ]),
    "Advanced": (11, 13, [
        "Improve acceleration through sprint drills.",
        "Focus on strength and conditioning.",
        "Add resistance sprint training.",
    ]),
    "Intermediate": (13, 15, [
        "Work on running posture and foot placement.",
        "Add interval sprint training.",
        "Improve stride frequency.",
    ]),
    "Beginner": (15, float('inf'), [
        "Start with basic sprinting technique drills.",
        "Build cardiovascular endurance.",
        "Do consistent 100m runs and track progress.",
    ])
}

# Models
class RaceResult(BaseModel):
    name: str
    timing: float

class RaceResultsBatch(BaseModel):
    races: List[RaceResult]

class ImprovementTips(BaseModel):
    level: str
    tips: List[str]

# Load race data from file
def load_data():
    global race_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            race_data = json.load(file)

# Save race data to file
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(race_data, file, indent=4)

# Get performance level and tips
def get_improvement_tip(timing: float):
    for level, (min_time, max_time, tips) in IMPROVEMENT_TIPS.items():
        if min_time <= timing < max_time:
            return level, tips
    return "Unknown", ["No tips available."]

# API to add single race result
@app.post("/add_race_result")
def add_race_result(result: RaceResult):
    date = datetime.date.today().strftime('%Y-%m-%d')
    status = "Below Threshold" if result.timing <= THRESHOLD else "Above Threshold"
    level, tips = get_improvement_tip(result.timing)

    entry = {
        "name": result.name,
        "timing": result.timing,
        "date": date,
        "status": status,
        "level": level,
        "tips": tips
    }

    race_data.append(entry)
    save_data()

    return entry

# API to add multiple race results
@app.post("/add_multiple_race_results")
def add_multiple_race_results(batch: RaceResultsBatch):
    date = datetime.date.today().strftime('%Y-%m-%d')
    new_entries = []

    for result in batch.races:
        status = "Below Threshold" if result.timing <= THRESHOLD else "Above Threshold"
        level, tips = get_improvement_tip(result.timing)

        entry = {
            "name": result.name,
            "timing": result.timing,
            "date": date,
            "status": status,
            "level": level,
            "tips": tips
        }

        race_data.append(entry)
        new_entries.append(entry)

    save_data()
    return {"added": new_entries}

# API to view performance of a user
@app.get("/view_performance/{name}")
def view_performance(name: str):
    user_results = [entry for entry in race_data if entry["name"].lower() == name.lower()]
    if not user_results:
        return {"error": "No records found for this user."}

    total_races = len(user_results)
    avg_timing = sum([r["timing"] for r in user_results]) / total_races
    below_threshold = sum(1 for r in user_results if r["status"] == "Below Threshold")
    above_threshold = total_races - below_threshold

    return {
        "name": name,
        "total_races": total_races,
        "average_timing": avg_timing,
        "below_threshold": below_threshold,
        "above_threshold": above_threshold,
        "details": user_results
    }

# API to get improvement tips by timing
@app.get("/get_improvement_tips/{timing}", response_model=ImprovementTips)
def get_improvement_tips(timing: float):
    level, tips = get_improvement_tip(timing)
    return {"level": level, "tips": tips}

# Smart AI voice feedback endpoint
@app.get("/ai_assistant/{name}")
def ai_assistant(name: str):
    user_results = [entry for entry in race_data if entry["name"].lower() == name.lower()]
    if not user_results:
        return {"error": "No data found for this user."}

    timings = [res["timing"] for res in user_results]
    trend = "Improving" if timings[-1] < timings[0] else "Declining"
    consistency = "Consistent" if max(timings) - min(timings) < 1.5 else "Variable"
    avg = sum(timings) / len(timings)

    level, tips = get_improvement_tip(avg)

    return {
        "name": name,
        "total_races": len(user_results),
        "trend_analysis": trend,
        "consistency_analysis": consistency,
        "current_level": level,
        "smart_tips": tips
    }

# Load data on server start
load_data()

# Run using: uvicorn main:app --reload

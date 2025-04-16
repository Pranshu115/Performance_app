from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import requests

# Initialize FastAPI app
app = FastAPI()

# OpenRouter API URL and API key (Replace with your actual key)
OPENROUTER_API_KEY = "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"  # Replace with your OpenRouter API key
OPENROUTER_API_URL = "https://openrouter.ai/settings/keys"  # Replace with the correct OpenRouter endpoint

# Dummy data store — replace with real database in production
race_data_db = {
    "john": [14.2, 13.8, 13.9, 13.5],
    "sara": [12.2, 12.0, 12.5, 12.7],
    "alex": [11.5, 11.8, 11.7, 11.9]
}

# Pydantic model to represent race result input
class RaceResult(BaseModel):
    name: str
    timing: float

# Function to call OpenRouter API for generating the improvement summary
def get_openrouter_summary(name: str, timings: List[float]) -> str:
    prompt = f"Analyze the following 100m race timings for {name}: {timings}. Provide a performance summary, strengths, weaknesses, and suggestions for improvement."

    # Prepare the payload
    payload = {
        "model": "your-model",  # Replace with the OpenRouter model you're using
        "messages": [
            {"role": "system", "content": "You are a professional athletics coach."},
            {"role": "user", "content": prompt}
        ],
        "api_key": OPENROUTER_API_KEY  # API Key for OpenRouter
    }

    # Make the API request to OpenRouter
    response = requests.post(OPENROUTER_API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data.get("summary", "No summary available.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Endpoint to get AI-generated improvement summary
@app.get("/generate_summary/{name}")
def generate_summary(name: str):
    timings = race_data_db.get(name.lower())
    if not timings:
        return {"error": "No data found for this name."}

    # Call OpenRouter to generate the summary
    summary = get_openrouter_summary(name, timings)
    return {"summary": summary}

# Endpoint to add a single race result
@app.post("/add_race_result")
def add_race_result(result: RaceResult):
    name = result.name.lower()
    timing = result.timing
    if name in race_data_db:
        race_data_db[name].append(timing)
    else:
        race_data_db[name] = [timing]
    return {"message": "Race result added successfully", "name": name, "new_timing": timing}

# Endpoint to add multiple race results
@app.post("/add_multiple_race_results")
def add_multiple_race_results(results: List[RaceResult]):
    for result in results:
        add_race_result(result)
    return {"message": "Multiple race results added successfully"}

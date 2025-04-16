import streamlit as st
import requests
import pyttsx3  # For text-to-speech (optional)

# Backend URL
BASE_URL = "http://localhost:8000"  # Change to your FastAPI app URL if deployed

# Streamlit app title
st.title("🏃‍♂️ AI-Powered Race Performance Tracker")

# Input for user name
name_input = st.text_input("Enter the name to get AI feedback:")

# Button to trigger AI summary generation
if st.button("Generate AI Summary"):
    if name_input:
        # Call the FastAPI backend to get the improvement summary
        response = requests.get(f"{BASE_URL}/generate_summary/{name_input}")

        if response.status_code == 200:
            data = response.json()
            if "summary" in data:
                # Display the summary
                st.success("Here is your AI summary:")
                st.markdown(data["summary"])

                # Optionally, read the summary aloud using pyttsx3
                engine = pyttsx3.init()
                engine.say(data["summary"])  # This will speak the summary aloud
                engine.runAndWait()
            else:
                st.warning(data.get("error", "Unknown error occurred"))
        else:
            st.error("Failed to fetch summary. Check the server.")
    else:
        st.warning("Please enter a name to get the summary.")

# --- Add a single race result ---
st.subheader("Add a Single Race Result")
name = st.text_input("Enter Name")
timing = st.number_input("Enter Timing (seconds)", min_value=0.0, step=0.01)

if st.button("Add Race"):
    if name and timing > 0:
        response = requests.post(f"{BASE_URL}/add_race_result", json={"name": name, "timing": timing})
        if response.status_code == 200:
            st.success("Race result added!")
            st.json(response.json())
        else:
            st.error("Failed to add race result.")
    else:
        st.warning("Please enter a name and timing.")

# --- Add multiple race results ---
st.subheader("Add Multiple Race Results")
num = st.number_input("Number of races to add", min_value=1, max_value=10, step=1)
race_inputs = []

for i in range(num):
    st.markdown(f"**Race {i + 1}**")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Name {i + 1}", key=f"name_{i}")
    with col2:
        timing = st.number_input(f"Timing {i + 1}", min_value=0.0, step=0.01, key=f"time_{i}")
    race_inputs.append({"name": name, "timing": timing})

if st.button("Submit All Races"):
    valid_entries = [r for r in race_inputs if r["name"] and r["timing"] > 0]
    if valid_entries:
        response = requests.post(f"{BASE_URL}/add_multiple_race_results", json={"races": valid_entries})
        if response.status_code == 200:
            st.success("Multiple races added successfully.")
            st.json(response.json())
        else:
            st.error("Failed to add races.")
    else:
        st.warning("Enter valid names and timings.")

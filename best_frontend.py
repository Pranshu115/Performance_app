
import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3

BACKEND_URL = "http://127.0.0.1:8000"
engine = pyttsx3.init()

def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-Speech failed: {e}")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")
    return ""

def display_performance(name):
    response = requests.get(f"{BACKEND_URL}/view_performance/{name}")
    if response.status_code == 200:
        data = response.json()
        st.subheader(f"Performance for {data['name']}")
        st.write(f"**Total Races:** {data['total_races']}")
        st.write(f"**Average Timing:** {data['average_timing']:.2f} seconds")
        st.write(f"**Below Threshold:** {data['below_threshold']}")
        st.write(f"**Above Threshold:** {data['above_threshold']}")
        st.write("### All Race Timings:")
        for entry in data['details']:
            st.write(f"- {entry['date']}: {entry['timing']}s [{entry['status']}]")
        return data
    else:
        st.warning("No performance data found for this name.")
        return None

def display_ai_analysis(name):
    response = requests.get(f"{BACKEND_URL}/ai_assistant/{name}")
    if response.status_code == 200:
        data = response.json()
        st.subheader("AI Voice Assistant Feedback")
        try:
            message = (
                f"{data['name']} has run {data['total_races']} races. "
                f"Your performance trend is {data['trend_analysis']} and consistency is {data['consistency_analysis']}. "
                f"Current level is {data['current_level']}. "
                f"Here are your improvement tips: " + ", ".join(data['smart_tips'])
            )
            st.write(message)
            speak_text(message)
        except KeyError as e:
            st.error(f"Missing expected data in AI response: {e}")
    else:
        st.warning("No data available for AI Assistant.")
        st.write(f"Status code: {response.status_code}, Response: {response.text}")

def get_tips(timing):
    response = requests.get(f"{BACKEND_URL}/get_improvement_tips/{timing}")
    if response.status_code == 200:
        data = response.json()
        st.subheader("Improvement Tips")
        st.write(f"**Level:** {data['level']}")
        st.write("**Tips:**")
        for tip in data["tips"]:
            st.write(f"- {tip}")
        speak_text(f"Based on your timing, your level is {data['level']}. Here are some tips: " + ", ".join(data["tips"]))
    else:
        st.warning("Could not fetch tips.")
        st.write(f"Status code: {response.status_code}, Response: {response.text}")

st.set_page_config(page_title="100m Sprint Tracker", layout="centered")
st.title("🏃 100m Sprint Performance Tracker with AI Assistant")

tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ Speak or Type Name",
    "📊 Check Performance",
    "💡 Improvement Tips",
    "🏁 Add New Race"
])

with tab1:
    st.header("Enter or Speak Your Name")
    option = st.radio("Choose Input Method:", ["Type", "Speak"])
    name_input = ""
    if option == "Type":
        name_input = st.text_input("Enter your name:")
    else:
        if st.button("Start Speaking"):
            name_input = recognize_speech()
    if name_input:
        performance = display_performance(name_input)
        if performance:
            display_ai_analysis(name_input)

with tab2:
    st.header("View Performance")
    manual_name = st.text_input("Enter your name to view all races:")
    if st.button("Show Performance"):
        display_performance(manual_name)

with tab3:
    st.header("Get Tips by Timing")
    timing = st.number_input("Enter your latest 100m sprint timing (in seconds):", min_value=0.0, step=0.1)
    if st.button("Get Tips"):
        get_tips(timing)

with tab4:
    st.header("Add a New Race Result")
    new_name = st.text_input("Runner's Name:")
    new_timing = st.number_input("Timing (in seconds):", min_value=0.0, step=0.01)
    if st.button("Submit Race Result"):
        if new_name and new_timing:
            response = requests.post(f"{BACKEND_URL}/add_race_result", json={
                "name": new_name,
                "timing": new_timing
            })
            if response.status_code == 200:
                result = response.json()
                st.success("Race result added successfully!")
                st.json(result["entry"])
                speak_text(f"Race result for {new_name} has been recorded successfully.")
            else:
                st.error("Failed to add race result.")
                st.write(f"Status code: {response.status_code}, Response: {response.text}")
        else:
            st.warning("Please enter both name and timing.")

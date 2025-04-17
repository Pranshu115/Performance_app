
# # nice code 
# import streamlit as st
# import requests
# import speech_recognition as sr
# import pyttsx3
# import threading

# # Base URL for FastAPI
# API_URL = "http://127.0.0.1:8000"

# # Text-to-speech engine
# engine = pyttsx3.init()

# def speak_text(text):
#     def run_speech():
#         engine = pyttsx3.init()
#         engine.say(text)
#         engine.runAndWait()
#     threading.Thread(target=run_speech).start()

# # Speech recognition function
# def recognize_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening... Please speak your name.")
#         audio = r.listen(source)

#         try:
#             text = r.recognize_google(audio)
#             st.success(f"You said: {text}")
#             return text
#         except sr.UnknownValueError:
#             st.error("Could not understand audio.")
#         except sr.RequestError:
#             st.error("Speech recognition service unavailable.")
#     return None

# # Title and UI
# st.title("🏃‍♂️ 100m Race Performance Analyzer")

# # Sidebar options
# option = st.sidebar.selectbox("Choose an Option", [
#     "🏁 Submit Race Time",
#     "📊 View My Performance",
#     "📈 Get Improvement Tips",
#     "🧠 Smart Voice Assistant"
# ])

# # Submit multiple race timings
# if option == "🏁 Submit Race Time":
#     st.header("Submit Your 100m Sprint Time")
#     name = st.text_input("Enter your name")
#     timings = st.text_area("Enter your 100m race timings separated by commas (e.g., 12.3, 11.8, 13.0)")

#     if st.button("Submit"):
#         if name and timings:
#             try:
#                 timing_list = [float(t.strip()) for t in timings.split(",")]
#                 for t in timing_list:
#                     result = {
#                         "name": name,
#                         "timing": t
#                     }
#                     response = requests.post(f"{API_URL}/add_race_result", json=result)
#                     if response.status_code == 200:
#                         data = response.json()
#                         st.success(f"Submitted {t} sec! Level: {data['level']}")
#                         st.write("Improvement Tips:")
#                         for tip in data['tips']:
#                             st.write(f"- {tip}")
#                             speak_text(tip)
#                     else:
#                         st.error(f"Failed to submit time {t}")
#             except ValueError:
#                 st.error("Please enter valid numeric timings separated by commas.")

# # View performance history
# elif option == "📊 View My Performance":
#     st.header("Check Your Race History")
#     name = st.text_input("Enter your name to view performance")

#     if st.button("View Performance"):
#         if name:
#             response = requests.get(f"{API_URL}/view_performance/{name}")
#             if response.status_code == 200:
#                 data = response.json()
#                 if "error" in data:
#                     st.error(data["error"])
#                 else:
#                     st.write(f"**Total Races:** {data['total_races']}")
#                     st.write(f"**Average Timing:** {data['average_timing']:.2f} seconds")
#                     st.write(f"**Below Threshold:** {data['below_threshold']}")
#                     st.write(f"**Above Threshold:** {data['above_threshold']}")
#                     st.write("**Race Details:**")
#                     st.table(data["details"])
#             else:
#                 st.error("Failed to retrieve performance data.")

# # Get improvement tips
# elif option == "📈 Get Improvement Tips":
#     st.header("Get Improvement Tips")
#     timing = st.number_input("Enter your latest 100m timing (in seconds)", min_value=5.0, max_value=60.0, step=0.01)

#     if st.button("Get Tips"):
#         response = requests.get(f"{API_URL}/get_improvement_tips/{timing}")
#         if response.status_code == 200:
#             tips_data = response.json()
#             st.success(f"Your current level: {tips_data['level']}")
#             st.write("Improvement Tips:")
#             for tip in tips_data['tips']:
#                 st.write(f"- {tip}")
#                 speak_text(tip)
#         else:
#             st.error("Could not fetch tips.")

# # Voice assistant to analyze and speak performance
# elif option == "🧠 Smart Voice Assistant":
#     st.header("🎙 Speak or Type Your Name")

#     use_speech = st.checkbox("Use Microphone to Speak")
#     spoken_name = ""

#     if use_speech:
#         if st.button("🎤 Start Listening"):
#             spoken_name = recognize_speech()
#     else:
#         spoken_name = st.text_input("Or type your name")

#     if st.button("🔍 Get AI Feedback"):
#         if spoken_name:
#             response = requests.get(f"{API_URL}/ai_assistant/{spoken_name}")
#             if response.status_code == 200:
#                 data = response.json()
#                 if "error" in data:
#                     st.error(data["error"])
#                     speak_text("Sorry, I couldn't find any data for that name.")
#                 else:
#                     st.success(f"Hello {data['name']}! Here's your performance analysis:")
#                     st.write(f"📈 Total Races: {data['total_races']}")
#                     st.write(f"📉 Trend: {data['trend_analysis']}")
#                     st.write(f"🎯 Consistency: {data['consistency_analysis']}")
#                     st.write(f"🏅 Level: {data['current_level']}")
#                     st.write("🧠 Smart Tips:")
#                     for tip in data["smart_tips"]:
#                         st.write(f"- {tip}")

#                     # Speak all data in a single voice output
#                     full_speech = (
#                         f"{data['name']}, you have completed {data['total_races']} races. "
#                         f"Your performance trend is {data['trend_analysis']}. "
#                         f"Consistency analysis shows {data['consistency_analysis']}. "
#                         f"Your current level is {data['current_level']}. "
#                         "Here are your smart improvement tips: "
#                     )
#                     for tip in data["smart_tips"]:
#                         full_speech += f"{tip}. "
#                     speak_text(full_speech)
#             else:
#                 st.error("Could not fetch voice assistant feedback.")
#                 speak_text("Sorry, there was a problem getting your performance data.")

# better than nice code
import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3

# Configure FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Text-to-Speech engine
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

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
            st.error(f"Could not request results; {e}")
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
        message = (
            f"{data['name']} has run {data['total_races']} races. "
            f"Your performance trend is {data['trend_analysis']} and consistency is {data['consistency_analysis']}. "
            f"Current level is {data['current_level']}. "
            f"Here are your improvement tips: " + ", ".join(data['smart_tips'])
        )
        st.write(message)
        speak_text(message)
    else:
        st.warning("No data available for AI Assistant.")

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

# Streamlit UI
st.set_page_config(page_title="100m Sprint Tracker", layout="centered")
st.title("🏃 100m Sprint Performance Tracker with AI Assistant")

tab1, tab2, tab3 = st.tabs(["🎙️ Speak or Type Name", "📊 Check Performance", "💡 Improvement Tips"])

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


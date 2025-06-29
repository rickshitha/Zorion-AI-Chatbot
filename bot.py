import os
import streamlit as st
import google.generativeai as genai
import pyttsx3
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("❌ API Key not found! Please check your .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

# ✅ Function to Speak the Response
def speak_response(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.warning(f"⚠️ Voice output error: {e}")

# ✅ Function to Get Response from Gemini AI
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"⚠️ Error fetching response: {e}")
        return None

# ✅ Streamlit UI Setup
st.set_page_config(page_title="Zorion AI", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #f4f4f9;
            font-family: 'Arial', sans-serif;
        }
        .chat-container {
            max-width: 800px;
            margin: auto;
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
            animation: fadeIn 1s ease-in-out;
        }
        .user-message {
            background: #007bff;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            transition: all 0.3s ease-in-out;
        }
        .bot-message {
            background: #e9ecef;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            transition: all 0.3s ease-in-out;
        }
        .sidebar {
            background: linear-gradient(135deg, #1f78b4, #1565c0);
            color: white;
            padding: 15px;
            border-radius: 10px;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(-10px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
    <div class='chat-container'>
        <h2 style='text-align: center; color: #2c3e50;'>🤖 Zorion AI - Chat Assistant</h2>
    </div>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Sidebar Settings
with st.sidebar:
    st.markdown("<h3 class='sidebar'>⚙️ Settings</h3>", unsafe_allow_html=True)
    chat_mode = st.selectbox("Mode", ["Casual", "Professional", "Creative"])

# 📝 Input Section (AI Chatbot Functionality)
user_input = st.text_input("💬 Type your message:", placeholder="Ask me anything...", key="input_text")
submit_button = st.button("🚀 Send", key="send_button")

# ✨ Handle Text Input
if submit_button and user_input:
    st.session_state['chat_history'].append(("You", user_input))
    response = get_gemini_response(user_input)
    
    if response:
        full_response = "".join(chunk.text for chunk in response)
        st.markdown("### 🤖 AI Response")
        st.markdown(f"<div class='bot-message'><b>Bot:</b> {full_response}</div>", unsafe_allow_html=True)
        st.session_state['chat_history'].append(("Bot", full_response))

        # 🔊 Speak Bot Response Button
        if st.button("🔊 Speak Bot Response", key="speak_bot_text"):
            speak_response(full_response)

# 📜 Display Chat History
st.markdown("### 💬 Chat History")
for idx, (role, text) in enumerate(st.session_state['chat_history']):
    if role == "You":
        st.markdown(f"<div class='user-message'><b>{role}:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'><b>{role}:</b> {text}</div>", unsafe_allow_html=True)
        if st.button(f"🔊 Speak {role} Response {idx}", key=f"speak_{idx}"):
            speak_response(text)

# 🏝️ Tourism Guidance Section
st.markdown("### ✈️ Plan Your Trip")
start_trip_button = st.button("🚀 Start a Journey for the Trip")

if start_trip_button:
    st.session_state['planning_stage'] = True

if 'planning_stage' in st.session_state and st.session_state['planning_stage']:
    st.markdown("### 🏝️ Enter Your Trip Details")
    adults = st.number_input("👨‍👩‍👧‍👦 Number of Adults", min_value=1, step=1)
    children = st.number_input("👶 Number of Children", min_value=0, step=1)
    start_location = st.text_input("📍 Starting Location")
    destination = st.text_input("📍 Destination")
    days = st.number_input("📆 Number of Days", min_value=1, step=1)
    confirm_trip = st.button("🔍 Get Trip Suggestions")

    if confirm_trip and start_location and destination and days:
        trip_query = f"Suggest famous tourist places, attractions, and approximate stay cost for {days} days in {destination} for {adults} adults and {children} children."
        response = get_gemini_response(trip_query)
        
        if response:
            full_response = "".join(chunk.text for chunk in response)
            st.markdown("### 🌍 Recommended Places & Cost")
            st.markdown(f"<div class='bot-message'><b>AI Suggestion:</b> {full_response}</div>", unsafe_allow_html=True)
            st.session_state['chat_history'].append(("AI Suggestion", full_response))

            # 🔊 Speak AI Suggestion Button (for the trip itinerary)
            if st.button("🔊 Speak Bot Response", key="speak_trip_suggestion"):
                speak_response(full_response)
        else:
            st.error("⚠️ Could not fetch recommendations. Try again!")










































































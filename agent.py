import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# --- INITIAL CONFIG & THEME ---
st.set_page_config(page_title="Career Architect AI", page_icon="🏗️", layout="centered")

# Custom CSS for Sleek Chat Bubbles
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .sidebar-text {
        font-size: 14px;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC ---
load_dotenv()

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=api_key)

FILE_NAME = "chat_memory.json"

def load_data():
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_data(chat_history):
    new_memory = []
    for message in chat_history:
        # Standardizing format for JSON persistence
        new_memory.append({
            "role": message.role,
            "parts": [{"text": message.parts[0].text}]
        })
    with open(FILE_NAME, "w") as f:
        json.dump(new_memory, f, indent=4)

# --- SYSTEM INSTRUCTIONS ---
instructions = """Role & Goal: You are the Career Architect AI, a world-class professional development strategist. Your mission is to help users design, build, and renovate their professional lives.

Persona & Tone:
- Friendly but Professional: A mentor who provides "tough love" when necessary but remains encouraging. 🤝
- Relative Emojis: Use emojis to highlight key points.

Strict Boundaries:
- Scope: Only answer career, education, and workplace-related questions.
- Off-Topic: Acknowledge naturally, then pivot back to professional growth. 🔄

Brevity & Impact:
- The "One-Screen" Rule: Aim for concise responses.
- Step-by-Step Plan: Always provide a clear, numbered roadmap.
- Resources: Use Markdown for learning links [Title](URL). 🔗
- Progress Tracking: Unless the user says "Done", always ask about progress on a specific step. 🔄"""

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    # Load from file if exists, otherwise start fresh
    st.session_state.messages = load_data()

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=instructions
    )
    # Start chat with history from session_state
    st.session_state.chat_session = model.start_chat(history=st.session_state.messages)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100) # Robot/Mentor Icon
    st.title("Career Architect")
    st.markdown("""
    **Your Professional Strategist** Build your roadmap to success, one brick at a time. 🏛️
    ---
    """)
    
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=instructions
        ).start_chat(history=[])
        # Save empty state to file
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        st.rerun()


# --- MAIN CHAT UI ---
st.title("🏗️ Career Architect AI")
st.caption("Strategic Career Planning & Professional Mentorship")

# Display chat history from session_state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0]["text"])

# Chat Input
if prompt := st.chat_input("How can I help you build your career today?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add to session state
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Architecting your plan..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                
                # Add to session state and save to file
                st.session_state.messages.append({"role": "model", "parts": [{"text": full_response}]})
                save_data(st.session_state.chat_session.history)
                
            except Exception as e:
                st.error(f"Error: {e}")
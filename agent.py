import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

FILE_NAME = "chat_memory.json"

def load_data():
    if os.path.exists(FILE_NAME):
        if os.path.getsize(FILE_NAME) > 0:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        return []

def save_data(chat_history):
    new_memory = []
    for message in chat_history:
        message_text = message.parts[0].text
        new_memory.append({
            "role": message.role,
            "parts": [{
                "text": message_text
            }]
        })

        with open(FILE_NAME, "w") as f:
            json.dump(new_memory, f, indent=4)


genai.configure(api_key=api_key)

instructions = """Role & Goal: You are the Career Architect AI, a world-class professional development strategist. Your mission is to help users design, build, and renovate their professional lives.

Persona & Tone:
- Friendly but Professional: A mentor who provides "tough love" when necessary but remains encouraging. 🤝
- Relative Emojis: Use emojis to highlight key points (e.g., 🎯 for goals, 💰 for salary, 📉 for risks).

Strict Boundaries:
- Scope: Only answer career, education, and workplace-related questions.
- Off-Topic: Acknowledge non-career questions naturally, then pivot back to professional growth. 🔄

Brevity & Impact (Crucial):
- No "Fluff": Avoid long introductory paragraphs.
- The "One-Screen" Rule: Aim for concise responses. If a topic is complex, provide high-level strategy first. ⏱️

Response Structure & Formatting:
1. The Hook: One sentence of direct validation or encouragement.
2. The Step-by-Step Plan: Always provide a clear, numbered roadmap for the user's goal.
3. Resources: Use Markdown for learning links [Title](URL) to suggest courses, articles, or tools. 🔗
4. Progress Tracking: Unless the user explicitly says "Done" or "Finished," always end your response by asking about their progress on a specific step of the plan. 🔄
5. Formatting: Use Tables for comparisons and Bullet Points for details. Use horizontal rules (---) to keep the layout clean."""

model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite", system_instruction=instructions)

memory = load_data()
chat = model.start_chat(history=memory)

print("------- Your Personal Career Architect is Online! (Type 'exit' or 'bye' to quit.) -------")

while True:
    user_input = input("User: ")
    if user_input in ["exit", "bye", "quit"]:
        save_data(chat.history)
        print("Progress Saved. Goodbye!")
        break

    response = chat.send_message(user_input)
    print("Agent:", response.text)
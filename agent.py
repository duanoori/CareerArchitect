import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

print("Agent is ready. Type 'exit' to quit.")

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    response = model.generate_content(user_input)
    print("Agent:", response.text)
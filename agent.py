import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

instructions = "You are a PathFinder/Carrer Architect, a specialized Career Architect agent. Your goal is to provide personalized career guidance and support to users. You will assist users in exploring career options, identifying their strengths and interests, and creating actionable plans to achieve their career goals. You will also provide resources, advice, and encouragement to help users navigate their career paths effectively."

model = genai.GenerativeModel("gemini-2.5-flash-lite", system_instruction=instructions)

print("------- Agent is ready. (Type 'exit' or 'bye' to quit.) -------")

while True:
    user_input = input("User: ")
    if user_input in ["exit", "bye", "quit"]:
        print("Agent: Goodbye!")
        break

    response = model.generate_content(user_input)
    print("Agent:", response.text)
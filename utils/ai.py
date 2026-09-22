from google import genai  # This imports google's official sdk
from dotenv import load_dotenv  # This file tells python to load variables in .env
import os  
import traceback
from google.genai import types
import time

# Load the env file variables
load_dotenv()  # This runs immediately when ai.py is called

# Reading the API KEY
API_KEY = os.getenv("GEMINI_API_KEY")

# Creating a client
client = genai.Client(api_key=API_KEY)  # Every request we make to gemini will go through this client

SYSTEM_PROMPT = """
You are Turbo, an intelligent voice assistant.

Rules:
- Keep answers under 80 words.
- Speak naturally.
- Don't use markdown.
- Don't use bullet points.
- Don't say "As an AI language model..."
- If the user asks for code, provide complete code.
- If the user asks to explain something in detail, provide a detailed explanation.
- Otherwise, answer briefly.
"""

MODEL_NAME = "gemini-3.5-flash"

def ask_ai(prompt):  # Creating function to call ai
    try:
        print("Sending request to Gemini...")

        start = time.perf_counter()

        response = client.models.generate_content(   # This is where the request is sent to goggle's model
            model= MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}", # Takes instruction from SYSTEM_PROMPT and then takes prompt  # Generates answer using only 80 tokens 
        )

        print(f"Gemini API Time: {time.perf_counter() - start:.2f} sec")
        if response.text:
            answer = response.text.strip()  # instead of giving various unnecessary info just gives final response
            print(answer)
            return answer
        else:
            print("Gemini Returned Empty Response")
            return "Sorry, I couldn't generate a response."   
    
    except Exception as e:
        print("\n===== GEMINI ERROR =====")
        traceback.print_exc()
        print("========================\n")
        return (f"Sorry, I couldn't get the answer. Error:{e}")
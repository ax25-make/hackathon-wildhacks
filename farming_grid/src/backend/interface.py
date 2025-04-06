import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
if not API_KEY_1:
    raise ValueError("GEMINI_API_KEY_1 environment variable not set.")

genai.configure(api_key=API_KEY_1)

def make_content(model, prompt):
    try:
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None
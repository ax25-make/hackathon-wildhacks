import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiInterface:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY_1")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY_1 environment variable not set.")
        self.model = "gemini-2.0-flash"


    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return None
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
if not API_KEY_1:
    raise ValueError("GEMINI_API_KEY_1 environment variable not set.")
client = genai.Client(api_key=API_KEY_1)
chat = client.chats.create(model="gemini-2.0-flash")

def generate_content(chat, prompt):
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None
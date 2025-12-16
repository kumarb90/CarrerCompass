import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

chat_model = genai.GenerativeModel("gemini-2.5-flash")

def chat_with_model(message: str) -> str:
    response = chat_model.generate_content(message)
    return response.text

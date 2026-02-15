import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

print("Fetching available models...")
try:
    for m in genai.list_models():
        if 'embed' in m.name:
            print(f"✅ FOUND EMBEDDING MODEL: {m.name}")
except Exception as e:
    print(f"Error: {e}")
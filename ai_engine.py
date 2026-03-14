import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are an expert AI Assistant for an Electrician. 
Your goal is to process incoming emails and manage the Google Calendar.
When provided with an email and a list of free slots, you must:
1. Determine if the email is a service request.
2. Extract client details (name, issue, location).
3. Match the request with the best available free slot.
4. Draft a professional reply in Polish.

You must ALWAYS respond in valid JSON format.
"""

def analyze_request(email_content, free_slots):
    user_prompt = f"FREE SLOTS: {free_slots}\n\nEMAIL CONTENT: {email_content}"
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json"
        }
    )
    
    return json.loads(response.text)
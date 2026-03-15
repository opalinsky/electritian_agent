import json
import datetime
from google import genai

client = genai.Client()

def analyze_request(email_content, free_slots):
    # Dajemy AI aktualną datę, żeby wiedziało kiedy jest "wtorek"
    dzisiaj = datetime.datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
    Jesteś asystentem elektryka.
    DZISIEJSZA DATA TO: {dzisiaj}
    
    Przeanalizuj maila i sprawdź wolne terminy.
    WOLNE TERMINY: {free_slots}
    TREŚĆ MAILA: {email_content}
    
    Zwróć wynik WYŁĄCZNIE jako czysty JSON. Nie dodawaj żadnego tekstu przed ani po.
    Struktura JSONa MUSI wyglądać dokładnie tak:
    {{
        "is_job_request": true,
        "job_type": "krótka nazwa zlecenia",
        "client_name": "imię i nazwisko",
        "summary": "krótki opis",
        "suggested_slot": "data w formacie ISO np. 2026-03-17T14:00:00Z",
        "suggested_reply": "treść maila z odpowiedzią po polsku"
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    
    tekst = response.text.strip()
    if tekst.startswith("```json"):
        tekst = tekst[7:]
    if tekst.endswith("```"):
        tekst = tekst[:-3]
        
    return json.loads(tekst.strip())
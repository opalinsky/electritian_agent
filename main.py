import os
import json
from gmail_test import download_emails
from calendar_service import get_upcoming_events, create_calendar_event
# Importujemy funkcję z Twojego pliku AI
# Zależnie jak go nazwałeś, np. ai_analyzer
from ai_engine import analyze_request 

def main():
    print("🤖 Agent is checking for new messages...")
    
    # 1. Pobieramy maile (z Twojego gmail_test.py)
    # Ten skrypt zapisuje dane jako 'sender', 'topic', 'text'
    emails = download_emails()
    
    # 2. Pobieramy zajęte terminy z kalendarza
    busy_schedule = get_upcoming_events(days=5)
    
    if not emails:
        print("📭 No new emails.")
        return

    emails = emails[0]
    for mail in emails:
        # TUTAJ BYŁ BŁĄD: Zmieniliśmy 'subject' na 'topic'
        print(f"📩 Processing: {mail['topic']}")
        
        # 3. Przesyłamy treść maila ('text') i kalendarz do AI
        analysis = analyze_request(mail['text'], busy_schedule)

        # 4. Jeśli AI uzna, że to zlecenie (is_job_request)
        if analysis.get('is_job_request'):
            slot = analysis.get('suggested_slot')
            if slot:
                # Dodajemy do kalendarza
                create_calendar_event(
                    tytul=f"ZLECENIE: {analysis['job_type']}",
                    opis=f"Klient: {mail['sender']}\nPodsumowanie: {analysis['summary']}",
                    data_start=slot
                )
                print(f"✅ Dodano do kalendarza!")
                print(f"📝 Odpowiedź dla klienta: {analysis['suggested_reply']}")
        else:
            print("⏭️ To nie jest zlecenie. Pomijam.")

if __name__ == "__main__":
    main()
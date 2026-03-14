import os
import json
from gmail_test import download_emails
from calendar_service import get_upcoming_events, create_calendar_event
from ai_engine import analyze_request 

def main():
    print("🤖 Agent is checking for new messages...")
    
    # 1. Pobieramy maile z Gmaila
    emails = download_emails()
    
    # 2. Pobieramy zajęte terminy z kalendarza
    busy_schedule = get_upcoming_events(days=5)
    
    if not emails:
        print("📭 No new emails.")
        return

    # --- ZMIANA: BIERZEMY TYLKO PIERWSZEGO (NAJNOWSZEGO) MAILA ---
    mail = emails[0] 
    
    print("--------------------------------------------------")
    print(f"📩 Analizuję TYLKO JEDNEGO maila: {mail['topic']}")
    print("--------------------------------------------------")
    
    try:
        # 3. Przesyłamy treść maila do AI
        analysis = analyze_request(mail['text'], busy_schedule)

        # 4. Sprawdzamy, co AI wymyśliło
        if analysis.get('is_job_request'):
            slot = analysis.get('suggested_slot')
            print(f"⚡ ZNALEZIONO ZLECENIE: {analysis.get('job_type')}")
            
            if slot:
                # Dodajemy do kalendarza
                link = create_calendar_event(
                    tytul=f"ZLECENIE: {analysis['job_type']}",
                    opis=f"Klient: {analysis.get('client_name', 'Nieznany')}\nPodsumowanie: {analysis.get('summary')}",
                    data_start=slot
                )
                print(f"✅ Dodano do kalendarza! Link: {link}")
                print(f"📝 Proponowana odpowiedź dla klienta:\n{analysis.get('suggested_reply')}")
            else:
                print("⚠️ Zlecenie wykryte, ale AI nie znalazło pasującego terminu (lub klient nie podał).")
        else:
            print("⏭️ AI uznało, że to nie jest zlecenie na usługi elektryczne. Pomijam.")
            
    except Exception as e:
        print(f"❌ Wystąpił błąd podczas analizy: {e}")

if __name__ == "__main__":
    main()
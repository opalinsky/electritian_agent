import os
import json
from gmail_test import download_emails
from calendar_service import get_upcoming_events, create_calendar_event
from ai_engine import analyze_request 

def main():
    print("🤖 Agent is checking for new messages...")
    emails = download_emails()
    busy_schedule = get_upcoming_events(days=5)
    
    if not emails:
        print("📭 No new emails.")
        return

    mail = emails[0] 
    print("--------------------------------------------------")
    print(f"📩 Analizuję TYLKO JEDNEGO maila: {mail['topic']}")
    print("--------------------------------------------------")
    
    try:
        analysis = analyze_request(mail['text'], busy_schedule)
        
        # Elastyczne pobieranie kluczy (bierzemy to, co dało AI)
        is_job = analysis.get('is_service_request') or analysis.get('is_job_request')
        
        if is_job:
            # AI u Ciebie zwróciło "issue", wcześniej miało być "job_type"
            job_name = analysis.get('issue') or analysis.get('job_type') or "Zlecenie elektryczne"
            
            print(f"⚡ ZNALEZIONO ZLECENIE: {job_name}")
            
            # Pobieranie daty - AI zwróciło słownik {'start': '...', 'end': '...'}
            slot_data = analysis.get('proposed_slot') or analysis.get('suggested_slot')
            slot = None
            if isinstance(slot_data, dict):
                slot = slot_data.get('start')
            else:
                slot = slot_data
                
            if slot:
                ## Dodajemy do kalendarza
                link = create_calendar_event(
                    title=f"ZLECENIE: {job_name}",
                    description=f"Treść maila: {mail['text']}",
                    start_iso=slot
                )
                print(f"✅ Dodano do kalendarza! Link: {link}")
                
                # Odpowiedź
                reply = analysis.get('email_reply') or analysis.get('suggested_reply')
                print(f"📝 Proponowana odpowiedź dla klienta:\n{reply}")
            else:
                print("⚠️ Zlecenie wykryte, ale AI nie znalazło pasującego terminu.")
        else:
            print("⏭️ AI uznało, że to nie jest zlecenie na usługi elektryczne. Pomijam.")
            
    except Exception as e:
        print(f"❌ Wystąpił błąd podczas analizy: {e}")

if __name__ == "__main__":
    main()
import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Rozszerzone uprawnienia o kalendarz
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def dodaj_do_kalendarza(tytul, opis, data_start):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
      'summary': tytul,
      'description': opis,
      'start': {
        'dateTime': data_start, # Format: '2024-05-28T09:00:00Z'
        'timeZone': 'Europe/Warsaw',
      },
      'end': {
        'dateTime': (datetime.datetime.fromisoformat(data_start.replace('Z', '')) + datetime.timedelta(hours=1)).isoformat() + 'Z',
        'timeZone': 'Europe/Warsaw',
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Dodano zlecenie do kalendarza: {event.get('htmlLink')}")

if __name__ == "__main__":
    # Testowe dodanie zlecenia
    jutro = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT10:00:00Z')
    dodaj_do_kalendarza("Zlecenie: Naprawa gniazdka", "Klient: Jan Kowalski, tel: 123456789", jutro)
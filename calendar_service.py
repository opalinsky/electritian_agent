import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def get_calendar_service():
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

    return build('calendar', 'v3', credentials=creds)

def get_upcoming_events(days=7):
    """Returns a list of busy slots to help the AI find free time."""
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now, timeMax=end_date,
        singleEvents=True, orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    busy_slots = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        busy_slots.append({"start": start, "end": end, "title": event.get('summary')})
    
    return busy_slots

def create_calendar_event(title, description, start_iso):
    """Inserts a new appointment into the calendar."""
    service = get_calendar_service()
    
    # Calculate end time (default 1 hour later)
    start_dt = datetime.datetime.fromisoformat(start_iso.replace('Z', ''))
    end_iso = (start_dt + datetime.timedelta(hours=1)).isoformat() + 'Z'

    event = {
        'summary': title,
        'description': description,
        'start': {'dateTime': start_iso, 'timeZone': 'Europe/Warsaw'},
        'end': {'dateTime': end_iso, 'timeZone': 'Europe/Warsaw'},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
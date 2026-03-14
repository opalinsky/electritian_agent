import os
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def download_emails():
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

    service = build('gmail', 'v1', credentials=creds)
    
    print("Downloading emails from GMail")

    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    # Using consistent naming here
    emails_to_save = []

    if not messages:
        print("No new messages")
    else:
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt.get('payload', {})
            headers = payload.get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown sender")
            snippet = txt.get('snippet', '')

            emails_to_save.append({
                "sender": sender,
                "topic": subject,
                "text": snippet
            })

    # Save using the correct variable name
    with open('maile.json', 'w', encoding='utf-8') as f:
        json.dump(emails_to_save, f, ensure_ascii=False, indent=4)
    
    print("Success! Data saved to maile.json.")
    return emails_to_save # Returning for main.py to use

if __name__ == "__main__":
    download_emails() # Corrected function call
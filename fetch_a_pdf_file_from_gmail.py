import os
import base64
import ctypes  # Windows pop-up ziņojumam
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Ja maināt šos SCOPES, izdzēsiet failu token.json.
SCOPES = ['https://mail.google.com/']

def main():
    creds = None
    # Pārbauda, vai fails token.json eksistē
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Pārbauda, vai kredenciālas ir derīgas
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Saglabā kredenciālas failā token.json
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Izveido Gmail servisu
    service = build('gmail', 'v1', credentials=creds)

    # Veic meklēšanu Gmail
    results = service.users().messages().list(userId='me', q="from:rekins@elektrons-k.lv").execute()
    messages = results.get('messages', [])

    if not messages:
        print('Nav jaunu ziņojumu.')
    else:
        message = messages[0]
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        headers = payload['headers']

        date = None
        for d in headers:
            if d['name'] == 'Date':
                date = d['value']

        parts = payload.get('parts', [])
        if not parts:
            parts = [payload]
        file_counter = 1
        for part in parts:
            mimeType = part.get('mimeType')
            body = part.get('body')
            data = body.get('data')
            if part.get('parts'):
                # Pievieno apakšdaļas sarakstam
                parts.extend(part.get('parts'))
            # Pārbauda, vai daļa ir PDF vai okteta plūsma
            if mimeType == "application/pdf" or mimeType == "application/octet-stream":  # Pieņem "application/octet-stream" kā derīgu MIME tipu
                if data is None and body['size'] > 0:
                    att_id = body['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=att_id).execute()
                    data = att['data']
                if data is not None:
                    file_data = base64.urlsafe_b64decode(data)
                    path = 'C:\\Users\\alans\\Desktop\\pdfstuff'
                    filename = str(file_counter) + '.pdf'
                    filepath = os.path.join(path, filename)
                    # Saglabā failu diska
                    with open(filepath, 'wb') as f:
                        f.write(file_data)
                    file_counter += 1
                    print(f'Fails, kas nosūtīts {date} caur Gmail, tika veiksmīgi lejupielādēts {filepath}')
                    # Parāda pop-up ziņojumu par lejupielādes pabeigšanu
                    ctypes.windll.user32.MessageBoxW(0, f'Fails, kas nosūtīts {date} caur Gmail, tika veiksmīgi lejupielādēts {filepath}', 'Lejupielāde pabeigta', 64)

if __name__ == '__main__':
    main()

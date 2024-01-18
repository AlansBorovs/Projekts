import os
import base64
import ctypes  # For Windows pop-up message
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://mail.google.com/']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', q="from:rekins@elektrons-k.lv").execute()
    messages = results.get('messages', [])

    if not messages:
        print('No new messages.')
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
                parts.extend(part.get('parts'))
            if mimeType == "application/pdf" or mimeType == "application/octet-stream":  # Accept "application/octet-stream" as a valid MIME type
                if data is None and body['size'] > 0:
                    att_id = body['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=att_id).execute()
                    data = att['data']
                if data is not None:
                    file_data = base64.urlsafe_b64decode(data)
                    path = 'C:\\Users\\alans\\Desktop\\pdfstuff'
                    filename = str(file_counter) + '.pdf'
                    filepath = os.path.join(path, filename)
                    with open(filepath, 'wb') as f:
                        f.write(file_data)
                    file_counter += 1
                    print(f'File sent on {date} through Gmail was successfully downloaded in {filepath}')
                    ctypes.windll.user32.MessageBoxW(0, f'File sent on {date} through Gmail was successfully downloaded in {filepath}', 'Download Complete', 64)

if __name__ == '__main__':
    main()

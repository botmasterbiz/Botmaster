import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
        Returns:
        service: Authorized Gmail API service instance.
    """
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(current_dir, 'token.json')
    credentials_path = os.path.join(current_dir, 'credentials.json')

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"credentials.json not found at {credentials_path}. "
                    "Please ensure you have downloaded your OAuth 2.0 credentials "
                    "from Google Cloud Console and placed them in the correct location."
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email.
    message_text: The text of the email.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {'raw': raw_message}

def create_draft(service, user_id, message_body):
    """Create and insert a draft email.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
             can be used to indicate the authenticated user.
    message_body: The body of the draft email.

    Returns:
        The created draft.
    """
    try:
        draft = service.users().drafts().create(userId=user_id, body={'message': message_body}).execute()
        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        return draft
    except Exception as error:
        print(f'An error occurred: {error}')
        return None
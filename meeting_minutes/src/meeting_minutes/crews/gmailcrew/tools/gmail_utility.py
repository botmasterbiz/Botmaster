import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
import json
from google.oauth2 import service_account
from pathlib import Path

import markdown

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        {final_email_body}
    </body>
    </html>
"""

def authenticate_gmail():
    """Authenticate with Gmail using OAuth 2.0."""
    creds = None
    token_path = Path(__file__).parent / 'token.json'
    
    # Check if we have a valid token
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")
            creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None

        if not creds:
            # Get credentials from environment variables
            client_id = os.getenv('GMAIL_CLIENT_ID')
            client_secret = os.getenv('GMAIL_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                raise ValueError(
                    "Gmail OAuth credentials not found in environment variables. "
                    "Please set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET in your .env file."
                )

            # Create client configuration from environment variables
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost:8080/"]
                }
            }

            try:
                flow = InstalledAppFlow.from_client_config(
                    client_config,
                    SCOPES,
                    redirect_uri='http://localhost:8080/'
                )
                creds = flow.run_local_server(port=8080)
            except Exception as e:
                print(f"Error during OAuth flow: {e}")
                raise

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

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

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br'])
    
    # Format the HTML content
    formatted_html = HTML_TEMPLATE.format(
        final_email_body=md.convert(message_text)
    )

    msg = EmailMessage()
    content=formatted_html

    msg['To'] = to
    msg['From'] = sender
    msg['Subject'] = subject
    msg.add_header('Content-Type','text/html')
    msg.set_payload(content)

    encodedMsg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    
    # The API expects a dictionary with a 'raw' key containing the encoded message
    return {'raw': encodedMsg}

def create_draft(service, message):
    """Create a draft email."""
    try:
        draft = service.users().drafts().create(
            userId='me',
            body={'message': {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}}
        ).execute()
        return draft
    except Exception as e:
        print(f"Error creating draft: {e}")
        raise

def send_email(service, to, subject, body):
    """Send an email using Gmail API."""
    try:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        draft = create_draft(service, message)
        print(f"Draft created: {draft.get('id')}")
        return draft
    except Exception as e:
        print(f"Error sending email: {e}")
        raise
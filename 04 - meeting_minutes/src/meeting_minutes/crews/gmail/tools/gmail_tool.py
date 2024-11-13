from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os.path
import base64
from email.mime.text import MIMEText

from .gmail_utility import authenticate_gmail, create_message, create_draft


# If modifying these SCOPES, delete the file token.json.



class GmailDraftToolInput(BaseModel):
    """Input schema for GmailDraftTool."""

    body: str = Field(..., description="The body of the email.")

class GmailDraftTool(BaseTool):
    name: str = "GmailDraftTool"
    description: str = (
        "This tool is used to draft an email."
    )
    args_schema: Type[BaseModel] = GmailDraftToolInput

    def _run(self, body: str) -> str:
        
        try:
            # Authenticate and build the service
            service = authenticate_gmail()

            # Define email parameters
            sender = 'tylerreedytlearning@gmail.com'
            to = 'valor13111@gmail.com'
            subject = 'Meeting Minutes'
            message_text = body

            # Create the email message
            message = create_message(sender, to, subject, message_text)

            # Create the draft
            create_draft(service, 'me', message)

            return "Email drafted successfully"
        except Exception as e:
            return f"Error drafting email: {e}"
    
    
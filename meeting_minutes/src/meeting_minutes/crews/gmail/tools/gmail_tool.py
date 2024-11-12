from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
        msg = MIMEMultipart()
        msg['Subject'] = "Meeting Minutes"
        msg['From'] = "valor13111@gmail.com"
        msg['To'] = "tylerreedytlearning@gmail.com"
        msg.attach(MIMEText(body, 'html'))

        print(msg)
        
        try:
            with smtplib.SMTP(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT')) as server:
                server.starttls()
                server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
                server.send_message(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

        return "Email drafted successfully."
    
    
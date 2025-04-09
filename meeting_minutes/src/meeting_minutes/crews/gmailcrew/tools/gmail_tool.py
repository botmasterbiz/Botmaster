from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .gmail_utility import authenticate_gmail, create_message, create_draft

import os
import traceback

class GmailToolInput(BaseModel):
    """Input schema for GmailTool."""

    body: str = Field(..., description="The body of the email to send.")

class GmailTool(BaseTool):
    name: str = "GmailTool"
    description: str = (
        "A tool for creating Gmail drafts with the provided content. "
        "This tool will authenticate with Gmail using OAuth and create a draft email."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, body: str) -> str:
        try:
            # Check if GMAIL_SENDER is set in environment variables
            sender = os.getenv("GMAIL_SENDER")
            if not sender:
                return "Error: GMAIL_SENDER environment variable is not set. Please set it to your Gmail address."
            
            # Check if OAuth credentials are set
            client_id = os.getenv("GMAIL_CLIENT_ID")
            client_secret = os.getenv("GMAIL_CLIENT_SECRET")
            
            if not client_id or not client_secret:
                return (
                    "Error: Gmail OAuth credentials are not set. Please set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET "
                    "in your .env file. You can get these from the Google Cloud Console by creating a new OAuth client."
                )
            
            # Authenticate with Gmail
            try:
                service = authenticate_gmail()
            except Exception as auth_error:
                error_details = str(auth_error)
                if "deleted_client" in error_details:
                    return (
                        "Error: The OAuth client was deleted. Please check your GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET "
                        "environment variables and ensure they contain valid OAuth client credentials. "
                        "You can get these from the Google Cloud Console by creating a new OAuth client."
                    )
                elif "invalid_client" in error_details:
                    return (
                        "Error: Invalid OAuth client. Please check your GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET "
                        "environment variables and ensure they contain valid OAuth client credentials."
                    )
                else:
                    return f"Authentication error: {error_details}"
            
            # Set up email parameters
            to = os.getenv("GMAIL_RECIPIENT", "garjahan@gmail.com")
            subject = "CleanAI Meeting Minutes"
            
            # Ensure body is a string
            message_text = str(body)

            # Create and send the message
            message = create_message(sender, to, subject, message_text)
            draft = create_draft(service, "me", message)

            if draft:
                return f"Email draft created successfully! Draft id: {draft['id']}"
            else:
                return "Failed to create email draft. Please check the logs for more details."
        except Exception as e:
            error_traceback = traceback.format_exc()
            return f"Error sending email: {str(e)}\n\nTraceback:\n{error_traceback}"

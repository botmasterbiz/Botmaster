# Meeting Minutes Generator

This application transcribes audio files, generates meeting minutes, and creates Gmail drafts.

## Setup

### Gmail OAuth Credentials

To use the Gmail draft feature, you need to set up OAuth credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API for your project
4. Go to "Credentials" and click "Create Credentials" > "OAuth client ID"
5. Select "Desktop app" as the application type
6. Give your OAuth client a name (e.g., "Meeting Minutes Generator")
7. Click "Create"
8. You will be shown your client ID and client secret
9. Add these to your `.env` file:
   ```
   GMAIL_CLIENT_ID=your_client_id
   GMAIL_CLIENT_SECRET=your_client_secret
   ```

### Environment Variables

Make sure your `.env` file contains the following variables:

```
OPENAI_API_KEY=your_openai_api_key
GMAIL_SENDER=your_gmail_address
GMAIL_RECIPIENT=recipient_email_address
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
```

## Usage

Run the application with:

```bash
python main.py
```

The application will:
1. Transcribe the audio file
2. Generate meeting minutes
3. Create a Gmail draft with the meeting minutes

## Troubleshooting

If you encounter the "deleted_client" error:

1. Check that your GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET are correctly set in your .env file
2. Make sure the OAuth client is still active in the Google Cloud Console
3. If the client was deleted, create a new one and update your .env file 
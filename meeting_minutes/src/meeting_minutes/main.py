#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import make_chunks 
from pathlib import Path
import os
import sys
from datetime import datetime

# Add the parent directory to the path to allow relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_minutes.crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from meeting_minutes.crews.gmailcrew.gmailcrew import GmailCrew
from meeting_minutes.toolbox_talk_form import create_toolbox_talk_form

#import agentops
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""
    toolbox_talk_form: str = ""


class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_meeting(self):
        print("Generating Transcription")

        SCRIPT_DIR = Path(__file__).parent
        audio_path = str(SCRIPT_DIR / "Toolbox_talk_April_8__2025.wav")
        
        # Load the audio file
        audio = AudioSegment.from_file(audio_path, format="wav")
        
        # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)

        # Transcribe each chunk
        full_transcription = ""
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}")
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            
            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                full_transcription += transcription.text + " "

        self.state.transcript = full_transcription
        print(f"Transcription: {self.state.transcript}")

    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating Meeting Minutes")

        crew = MeetingMinutesCrew()

        # Get current date and time
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%B %d, %Y at %I:%M %p")

        inputs = {
            "transcript": self.state.transcript,
            "current_date": formatted_date
        }
        meeting_minutes = crew.crew().kickoff(inputs)
        self.state.meeting_minutes = meeting_minutes

    @listen(generate_meeting_minutes)
    def create_toolbox_talk_form(self):
        print("Creating Toolbox Talk Form")
        
        # Generate a filename for the toolbox talk form
        current_date = datetime.now().strftime("%B_%d_%Y")
        output_file = f"Toolbox_Talk_{current_date}.docx"
        
        # Create the toolbox talk form
        form_path = create_toolbox_talk_form(self.state.transcript, output_file)
        self.state.toolbox_talk_form = form_path
        print(f"Toolbox talk form created: {form_path}")

    @listen(create_toolbox_talk_form)
    def create_draft_meeting_minutes(self):
        print("Creating Draft Meeting Minutes")

        try:
            crew = GmailCrew()

            # Convert meeting minutes to string if it's not already
            meeting_minutes_str = str(self.state.meeting_minutes)

            inputs = {
                "body": meeting_minutes_str
            }

            draft_result = crew.crew().kickoff(inputs)
            print(f"Draft Result: {draft_result}")
            
            # Check if the draft was created successfully
            if "Error" in draft_result or "error" in draft_result:
                print(f"Warning: There was an issue creating the Gmail draft: {draft_result}")
                print("The meeting minutes were generated but could not be sent as a draft email.")
                print("You can find the meeting minutes in the output files.")
            else:
                print("Meeting minutes draft created successfully in Gmail.")
                
        except Exception as e:
            print(f"Error creating Gmail draft: {e}")
            print("The meeting minutes were generated but could not be sent as a draft email.")
            print("You can find the meeting minutes in the output files.")

def kickoff():
   # session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

    meeting_minutes_flow = MeetingMinutesFlow()
    meeting_minutes_flow.plot()
    meeting_minutes_flow.kickoff()

   # session.end_session()

if __name__ == "__main__":
    kickoff()

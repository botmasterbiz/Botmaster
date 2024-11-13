#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.utils import make_chunks
from crews.gmail.gmail import GmailCrew
from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from pathlib import Path

load_dotenv()

from openai import OpenAI
client = OpenAI()

class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes_summary: str = ""
class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_meeting(self):
        print("Transcribing meeting")

        # SCRIPT_DIR = Path(__file__).parent
        # audio_path = str(SCRIPT_DIR / "EarningsCall.wav")
        
        # # Load the audio file
        # audio = AudioSegment.from_file(audio_path, format="wav")
        
        # # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        # chunk_length_ms = 60000
        # chunks = make_chunks(audio, chunk_length_ms)

        # # Transcribe each chunk
        # full_transcription = ""
        # for i, chunk in enumerate(chunks):
        #     print(f"Transcribing chunk {i+1}/{len(chunks)}")
        #     chunk_path = f"chunk_{i}.wav"
        #     chunk.export(chunk_path, format="wav")
            
        #     with open(chunk_path, "rb") as audio_file:
        #         transcription = client.audio.transcriptions.create(
        #             model="whisper-1", 
        #             file=audio_file
        #         )
        #         full_transcription += transcription.text + " "

        # self.state.transcript = full_transcription

    @listen(transcribe_meeting)
    def create_meeting_minutes(self):
        print("Creating meeting minutes")

        # self.state.transcript = "Good afternoon, everyone, and welcome to FinTech Plus Sync's 2nd quarter 2023 earnings call. I'm John Doe, CEO of FinTech Plus. We've had a stellar Q2 with a revenue of $125 million, a 25% increase year over year. Our gross profit margin stands at a solid 58%, due in part to cost efficiencies gained from our scalable business model. Our EBITDA has surged to $37.5 million, translating to a remarkable 30% EBITDA margin. Our net income for the quarter rose to $16 million, which is a noteworthy increase from $10 million in Q2 2022. Our total addressable market has grown substantially, thanks to the expansion of our high-yield savings product line and the new RoboAdvisor platform. We've been diversifying our asset-backed securities portfolio, investing heavily in collateralized debt obligations and residential mortgage-backed securities. We've also invested $25 million in AAA-rated corporate bonds, enhancing our risk-adjusted returns. As for our balance sheet, total assets reached $1.5 billion with total liabilities at $900 million, leaving us with a solid equity base of $600 million. Our debt to equity ratio stands at 1.5, a healthy figure considering our expansionary phase. We continue to see substantial organic user growth, with customer acquisition cost dropping by 15% and lifetime value growing by 25%. Our LTVCAC ratio is at an impressive 3.5x. In terms of risk management, we have a value-at-risk model in place with a 99% confidence level indicating that our maximum loss will not exceed 5 million in the next trading day. We've adopted a conservative approach to managing our leverage and have a healthy tier one capital ratio of 12.5%. Our forecast for the coming quarter is positive. We expect revenue to be around 135 million and 8% quarter over quarter growth driven primarily by our cutting edge blockchain solutions and AI driven predictive analytics. We're also excited about the upcoming IPO of our FinTech subsidiary Pay Plus, which we expect to raise 200 million. Significantly bolstering our liquidity and paving the way for aggressive growth strategies. We thank our shareholders for their continued faith in us and we look forward to an even more successful Q3. Thank you so much. "

        # # print(self.state.transcript)

        # meeting_minutes_crew = MeetingMinutesCrew()

        # inputs = {"transcript": self.state.transcript}
        # meeting_minutes_summary = meeting_minutes_crew.crew().kickoff(inputs)
        # self.state.meeting_minutes_summary = meeting_minutes_summary

    @listen(create_meeting_minutes)
    def send_meeting_minutes(self):
        print("Sending meeting minutes")

        self.state.meeting_minutes_summary = """# TylerAI Meeting Minutes

**Date:** October 6, 2023  
**Location:** Zoom  
**Organizer:** Tyler  

### Attendees:
- Tyler (Organizer)
- Chris Johnson
- Anna Lee
- David Smith
- Emily Turner

---

## Meeting Summary

The meeting focused on reviewing FinTech Plus Sync's Q2 2023 performance highlights. The company achieved notable revenue growth and maintained strong profitability metrics. Discussions emphasized strategic expansions, particularly in the high-yield savings product line and the RoboAdvisor platform. Future strategies include the diversification of the asset-backed securities portfolio and preparations for the successful IPO of the FinTech subsidiary, Pay Plus. A conservative approach to risk management and leverage control was also underlined as crucial moving forward.

## Key Points:
- **Revenue Growth:** Clear strategies have been set to ensure the continuation of the current upward trend.
- **Profitability Metrics:** The company is performing exceptionally well, with profitability improving as forecasted.
- **Strategic Expansions:** Focus on expanding high-yield products and the RoboAdvisor platform.
- **Future Preparations:** Upcoming IPO for Pay Plus is a significant event.
- **Risk Management:** Emphasis on maintaining a conservative approach to handling risk.

## Action Items
1. **Monitor Revenue Growth and Margin Improvement:**
   - Tasked to: Anna Lee
   - Deadline: Ongoing

2. **Expand High-Yield Savings Product Line and RoboAdvisor Platform:**
   - Tasked to: Chris Johnson
   - Deadline: End of Q3 2023

3. **Diversify the Asset-Backed Securities Portfolio:**
   - Tasked to: Emily Turner
   - Deadline: End of Q4 2023

4. **Ensure Successful IPO of Pay Plus:**
   - Tasked to: David Smith
   - Deadline: Scheduled for next quarter, date TBA

5. **Maintain Conservative Approach to Risk Management and Leverage Control:**
   - Tasked to: Tyler
   - Deadline: Ongoing

## Sentiment Analysis

Overall, the meeting was characterized by optimism and confidence regarding the company's current trajectory and future prospects. Attendees expressed a positive outlook on the continued success driven by strategic initiatives and sound financial management."""

        gmail_crew = GmailCrew()

        inputs = {"body": self.state.meeting_minutes_summary}
        result = gmail_crew.crew().kickoff(inputs)
        print(result)

def kickoff():
    meeting_minutes_flow = MeetingMinutesFlow()
    meeting_minutes_flow.kickoff()


if __name__ == "__main__":
    kickoff()

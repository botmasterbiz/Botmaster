#!/usr/bin/env python
from dotenv import load_dotenv
import os
# Disable AgentOps monitoring
os.environ["AGENTOPS_API_KEY"] = "none"

from crew import CleanAirMarketingCrew

def run():
    """Run the Clean Air Marketing Crew"""
    load_dotenv()
    
    inputs = {
        "product": "Air purifier with HEPA filter",
        "target_audience": "Health-conscious urban professionals",
        "content_type": "Social media campaign"
    }
    
    crew = CleanAirMarketingCrew()
    result = crew.get_crew(inputs).kickoff()
    print("\nFinal Results:")
    print(result)

if __name__ == "__main__":
    run() 
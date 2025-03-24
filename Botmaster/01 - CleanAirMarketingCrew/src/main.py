#!/usr/bin/env python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Disable AgentOps monitoring
os.environ["AGENTOPS_API_KEY"] = "none"

from crew import MarketingCrew

def main():
    # Define the marketing campaign parameters
    product = "HVAC mini-split and duct cleaning services"
    target_audience = "Schools and educational institutions"
    content_type = "Social media campaign"

    # Create and run the marketing crew
    crew = MarketingCrew(product, target_audience, content_type)
    result = crew.run()

    print("\nFinal Results:")
    print(result)

if __name__ == "__main__":
    main() 
import os

# Disable AgentOps monitoring
os.environ["AGENTOPS_API_KEY"] = "none"
os.environ["AGENTOPS_DISABLED"] = "true"

from typing import List, Optional
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun
from pydantic import BaseModel, Field, validator

class MarketingStrategy(BaseModel):
    """Marketing strategy model"""
    target_segments: List[str] = Field(..., description="List of target market segments")
    positioning: str = Field(..., description="Product positioning statement")
    key_messages: List[str] = Field(..., description="Key marketing messages")
    channels: List[str] = Field(..., description="Marketing channels to be used")

class MarketingContent(BaseModel):
    """Marketing content model"""
    title: str = Field(..., description="Title of the content")
    body: str = Field(..., description="Main content body")
    benefits: List[str] = Field(..., description="Key product benefits")
    call_to_action: str = Field(..., description="Call to action")

class CleanAirMarketingCrew:
    def __init__(self):
        self.agents_config = {
            'research_analyst': {
                'name': 'Research Analyst',
                'role': 'Market Research Analyst',
                'goal': 'Conduct thorough market research and competitor analysis',
                'backstory': 'Expert in market research with a focus on clean air and environmental products.'
            },
            'marketing_strategist': {
                'name': 'Marketing Strategist',
                'role': 'Marketing Strategy Expert',
                'goal': 'Develop effective marketing strategies based on research insights',
                'backstory': 'Seasoned marketing professional specializing in eco-friendly product marketing.'
            },
            'content_creator': {
                'name': 'Content Creator',
                'role': 'Creative Content Specialist',
                'goal': 'Create engaging and persuasive marketing content',
                'backstory': 'Experienced content creator with expertise in environmental and sustainability messaging.'
            }
        }

    def research_analyst(self) -> Agent:
        return Agent(
            name=self.agents_config['research_analyst']['name'],
            role=self.agents_config['research_analyst']['role'],
            goal=self.agents_config['research_analyst']['goal'],
            backstory=self.agents_config['research_analyst']['backstory'],
            tools=[DuckDuckGoSearchRun()],
            verbose=True
        )

    def marketing_strategist(self) -> Agent:
        return Agent(
            name=self.agents_config['marketing_strategist']['name'],
            role=self.agents_config['marketing_strategist']['role'],
            goal=self.agents_config['marketing_strategist']['goal'],
            backstory=self.agents_config['marketing_strategist']['backstory'],
            tools=[DuckDuckGoSearchRun()],
            verbose=True
        )

    def content_creator(self) -> Agent:
        return Agent(
            name=self.agents_config['content_creator']['name'],
            role=self.agents_config['content_creator']['role'],
            goal=self.agents_config['content_creator']['goal'],
            backstory=self.agents_config['content_creator']['backstory'],
            tools=[],
            verbose=True
        )

    def market_research_task(self, product: str, target_audience: str) -> Task:
        return Task(
            description=f"""Analyze the market for {product} targeting {target_audience}.
            1. Identify key competitors and their offerings
            2. Analyze target audience demographics and preferences
            3. Identify market trends and opportunities
            4. Evaluate pricing strategies in the market
            Output a detailed market analysis report in the MarketingStrategy model format.
            """,
            agent=self.research_analyst()
        )

    def strategy_development_task(self, product: str, target_audience: str, research_output: str) -> Task:
        return Task(
            description=f"""Based on the market research for {product} targeting {target_audience}, develop a comprehensive marketing strategy.
            Research findings: {research_output}
            1. Define unique selling propositions
            2. Outline marketing channels and tactics
            3. Develop positioning strategy
            4. Create budget allocation recommendations
            Output the marketing strategy in the MarketingStrategy model format.
            """,
            agent=self.marketing_strategist()
        )

    def content_creation_task(self, product: str, target_audience: str, strategy_output: str, content_type: str) -> Task:
        return Task(
            description=f"""Create {content_type} content for {product} targeting {target_audience} based on the marketing strategy.
            Strategy details: {strategy_output}
            1. Develop key messages and copy
            2. Incorporate brand voice and tone
            3. Include call-to-action elements
            4. Ensure alignment with marketing strategy
            Output the content in the MarketingContent model format.
            """,
            agent=self.content_creator()
        )

    def get_crew(self, inputs: dict) -> Crew:
        tasks = [
            self.market_research_task(
                product=inputs['product'],
                target_audience=inputs['target_audience']
            ),
            self.strategy_development_task(
                product=inputs['product'],
                target_audience=inputs['target_audience'],
                research_output="{task_0}"
            ),
            self.content_creation_task(
                product=inputs['product'],
                target_audience=inputs['target_audience'],
                strategy_output="{task_1}",
                content_type=inputs['content_type']
            )
        ]
        
        return Crew(
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        ) 
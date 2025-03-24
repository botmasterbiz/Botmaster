import os

# Disable AgentOps monitoring
os.environ["AGENTOPS_API_KEY"] = "none"
os.environ["AGENTOPS_DISABLED"] = "true"

from typing import List, Optional
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class MarketingStrategy(BaseModel):
    """Model for marketing strategy output"""
    unique_selling_propositions: List[str]
    marketing_channels: List[str]
    positioning_strategy: str
    budget_allocation: dict
    target_segments: List[str]
    competitive_advantages: List[str]
    implementation_timeline: str

class MarketingContent(BaseModel):
    """Model for marketing content output"""
    title: str
    subtitle: str
    body: str
    call_to_actions: List[str]
    key_messages: List[str]
    brand_voice: str
    marketing_strategy_alignment: str
    target_audience_focus: str

class MarketingCrew:
    def __init__(self, product: str, target_audience: str, content_type: str):
        self.product = product
        self.target_audience = target_audience
        self.content_type = content_type
        self.search_tool = DuckDuckGoSearchRun()
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7
        )

    def market_research_task(self) -> Task:
        return Task(
            description=f"""Conduct comprehensive market research for {self.product} targeting {self.target_audience}.
            Focus on:
            1. Key competitors and their offerings in the educational sector
            2. Target audience demographics and preferences
            3. Market trends and opportunities
            4. Pricing strategies and cost considerations
            5. Regulatory requirements for HVAC in educational facilities
            6. Energy efficiency standards and certifications
            7. Seasonal demand patterns
            8. Geographic market analysis
            
            Provide a detailed analysis in the MarketingStrategy model format.""",
            agent=self._create_market_research_analyst(),
            expected_output="A comprehensive market analysis report in the MarketingStrategy model format."
        )

    def strategy_development_task(self) -> Task:
        return Task(
            description=f"""Develop a comprehensive marketing strategy for {self.product} targeting {self.target_audience}.
            Include:
            1. Unique selling propositions focusing on educational benefits
            2. Marketing channels and tactics suitable for educational institutions
            3. Positioning strategy emphasizing safety and efficiency
            4. Budget allocation recommendations
            5. Seasonal marketing plans
            6. Partnership opportunities with educational organizations
            7. Compliance with educational institution procurement processes
            8. ROI metrics and KPIs
            
            Provide the strategy in the MarketingStrategy model format.""",
            agent=self._create_marketing_strategy_expert(),
            expected_output="A detailed marketing strategy in the MarketingStrategy model format."
        )

    def content_creation_task(self) -> Task:
        return Task(
            description=f"""Create engaging marketing content for {self.product} targeting {self.target_audience}.
            Focus on:
            1. Educational benefits and learning environment improvements
            2. Energy efficiency and cost savings
            3. Health and safety benefits
            4. Environmental impact
            5. Installation and maintenance considerations
            6. Compliance with educational standards
            7. Case studies and success stories
            8. Clear calls-to-action for educational decision-makers
            
            Provide the content in the MarketingContent model format.""",
            agent=self._create_creative_content_specialist(),
            expected_output="Engaging marketing content in the MarketingContent model format."
        )

    def _create_market_research_analyst(self) -> Agent:
        return Agent(
            role='Market Research Analyst',
            goal='Conduct thorough market research and identify opportunities in the educational HVAC sector',
            backstory="""You are an experienced market research analyst specializing in the HVAC industry, 
            with particular expertise in educational facility requirements. You have conducted numerous studies 
            on energy efficiency, indoor air quality, and educational facility management. Your research has 
            helped companies develop successful strategies for the educational sector.""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

    def _create_marketing_strategy_expert(self) -> Agent:
        return Agent(
            role='Marketing Strategy Expert',
            goal='Develop effective marketing strategies for HVAC services in educational institutions',
            backstory="""You are a seasoned marketing strategist with extensive experience in the HVAC industry 
            and educational sector. You have successfully developed marketing campaigns for major HVAC companies 
            targeting schools and universities. Your expertise includes educational procurement processes, 
            facility management, and sustainable building solutions.""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

    def _create_creative_content_specialist(self) -> Agent:
        return Agent(
            role='Creative Content Specialist',
            goal='Create compelling marketing content that resonates with educational decision-makers',
            backstory="""You are a creative content specialist with a strong background in educational marketing 
            and technical writing. You excel at translating complex HVAC concepts into clear, engaging content 
            that speaks to school administrators, facility managers, and educational decision-makers. Your work 
            has helped numerous HVAC companies effectively communicate their value proposition to educational institutions.""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

    def run(self) -> dict:
        crew = Crew(
            agents=[
                self._create_market_research_analyst(),
                self._create_marketing_strategy_expert(),
                self._create_creative_content_specialist()
            ],
            tasks=[
                self.market_research_task(),
                self.strategy_development_task(),
                self.content_creation_task()
            ],
            process=Process.sequential,
            verbose=True
        )
        result = crew.kickoff()
        return result 
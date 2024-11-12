from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv

load_dotenv()

pdf_search_tool = PDFSearchTool(pdf='./agentops.pdf')

@CrewBase
class PdfSearch():
	"""PdfSearch crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def pdf_searcher(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_searcher'],
			tools=[pdf_search_tool],
			verbose=True
		)

	@agent
	def pdf_summarizer(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_summarizer'],
			verbose=True
		)

	@task
	def pdf_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_search_task'],
			tools=[pdf_search_tool]
		)

	@task
	def pdf_summary_task(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_summary_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PdfSearch crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

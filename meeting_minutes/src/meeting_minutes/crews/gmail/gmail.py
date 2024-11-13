from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.gmail_tool import GmailDraftTool

@CrewBase
class GmailCrew():
	"""Gmail crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def gmail_draft(self) -> Agent:
		return Agent(
			config=self.agents_config['gmail_draft'],
			tools=[GmailDraftTool()],
			verbose=True
		)

	@task
	def gmail_draft_task(self) -> Task:
		return Task(
			config=self.tasks_config['gmail_draft_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Gmail crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

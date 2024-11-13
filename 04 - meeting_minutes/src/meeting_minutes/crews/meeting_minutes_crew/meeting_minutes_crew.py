from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool, FileReadTool

file_writer_tool_summary = FileWriterTool(filename="summary.txt", directory="meeting_minutes")
file_writer_tool_action_items = FileWriterTool(filename="action_items.txt", directory="meeting_minutes")
file_writer_tool_sentiment = FileWriterTool(filename="sentiment.txt", directory="meeting_minutes")

@CrewBase
class MeetingMinutesCrew():
	"""Meeting Minutes Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def meeting_minutes_transcriber(self) -> Agent:
		return Agent(
			config=self.agents_config['meeting_minutes_transcriber'],
			tools=[file_writer_tool_summary, file_writer_tool_action_items, file_writer_tool_sentiment],
			verbose=True,
		)
	
	@agent
	def meeting_minutes_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['meeting_minutes_writer'],
			tools=[],
			verbose=True,
		)

	@task
	def meeting_minutes_transcriber_task(self) -> Task:
		return Task(
			config=self.tasks_config['meeting_minutes_transcriber_task'],
		)
	
	@task
	def meeting_minutes_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['meeting_minutes_writer_task'],
			verbose=True,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)

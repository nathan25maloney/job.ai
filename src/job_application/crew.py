from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from job_application.tools.job_tool import JobTool



@CrewBase
class JobApplication():
	"""JobApplication crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# @agent
	# def cv_reader(self) -> Agent:
	# 		return Agent(
	# 				config=self.agents_config['cv_reader'],
	# 				tools=[FileReadTool()],
	# 				verbose=True,
	# 				allow_delegation=False
	# 		)

	# @agent
	# def matcher(self) -> Agent:
	# 		return Agent(
	# 				config=self.agents_config['matcher'],
	# 				tools=[FileReadTool(), CSVSearchTool()],
	# 				verbose=True,
	# 				allow_delegation=False
	# 		)

	# @task
	# def read_cv_task(self) -> Task:
	# 		return Task(
	# 				config=self.tasks_config['read_cv_task'],
	# 				agent=self.cv_reader()
	# 		)

	# @task
	# def match_cv_task(self) -> Task:
	# 		return Task(
	# 				config=self.tasks_config['match_cv_task'],
	# 				agent=self.matcher()
	# 		)

	# @crew
	# def crew(self) -> Crew:
	# 		"""Creates the MatchToProposal crew"""
	# 		return Crew(
	# 				agents=self.agents, # Automatically created by the @agent decorator
	# 				tasks=self.tasks, # Automatically created by the @task decorator
	# 				process=Process.sequential,
	# 				verbose=2,
	# 				# process=Process.hierarchical, # In case you want to use that instead https://docs.crewai.com/how-to/Hierarchical/
	# 		)


	@agent
	def position_finder(self) -> Agent:
		return Agent(
			config=self.agents_config['position_finder'],
			tools=[JobTool.search_jobs],
			verbose=True,
			output_file='positions.csv'
		)

	@agent
	def application_information_provider(self) -> Agent:
		return Agent(
			config=self.agents_config['application_information_provider'],
			verbose=True
		)

	@agent
	def cover_letter_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['cover_letter_generator'],
			verbose=True
		)

	@agent
	def resume_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['resume_generator'],
			verbose=True
		)

	@task
	def find_positions(self) -> Task:
		return Task(
			config=self.tasks_config['position_task'],
		)

	@task
	def provide_application_information(self) -> Task:
		return Task(
			config=self.tasks_config['application_information_task'],
		)

	@task
	def generate_cover_letter(self) -> Task:
		return Task(
			config=self.tasks_config['cover_letter_task'],
			output_file='cover_letter.txt'
		)

	@task
	def generate_resume(self) -> Task:
		return Task(
			config=self.tasks_config['resume_task'],
			output_file='resume.pdf'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the JobApplication crew"""
		return Crew(
			agents=self.agents,  # Automatically created by the @agent decorator
			tasks=self.tasks,  # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)

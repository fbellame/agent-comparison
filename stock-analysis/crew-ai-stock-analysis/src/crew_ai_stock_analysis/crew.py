from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crew_ai_stock_analysis.tools.YFinanceStockAnalysisTool import YFinanceStockAnalysisTool
from crewai_tools import FileReadTool

yfinance_stock_data_tool = YFinanceStockAnalysisTool()
file_read_tool = FileReadTool(file_path='warren_buffet_investement_principles.txt')

@CrewBase
class CrewAiStockAnalysisCrew():
	"""CrewAiStockAnalysis crew"""

	@agent
	def stock_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['stock_researcher'],
			verbose=True
		)

	@agent
	def senior_stock_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_stock_analyst'],
			verbose=True
		)

	@task
	def research_stock_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_stock_task'],
			tools=[yfinance_stock_data_tool]
		)

	@task
	def analyse_ticker_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyse_ticker_task'],
			output_file='stock_analysis.txt',
			tools=[file_read_tool]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewAiStockAnalysis crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
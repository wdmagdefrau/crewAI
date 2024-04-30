from crewai import Task
from textwrap import dedent
import logging
from datetime import datetime
import os

"""
Creating Tasks Cheat Sheet:
- Begin with the end in mind. Identify the specific outcome your tasks are aiming to achieve.
- Break down the outcome into actionable tasks, assigning each task to the appropriate agent.
- Ensure tasks are descriptive, providing clear instructions and expected deliverables.

Goal:
- Develop a comprehensive research report on a topic.

Key Steps for Task Creation:
1. Identify the Desired Outcome: Define what success looks like for your project.
    - A detailed research report encompassing the main areas of focus for the CFO in 2024.

2. Task Breakdown: Divide the goal into smaller, manageable tasks that agents can execute.
    - Research the internet
    - Research academic sources
    - Research social media trends on the topic
    - Summarize findings in a comprehensive report

3. Assign Tasks to Agents: Match tasks with agents based on their roles and expertise.

4. Task Description Template:
  - Use this template as a guide to define each task in your CrewAI application. 
  - This template helps ensure that each task is clearly defined, actionable, and aligned with the specific goals of your project.

  Template:
  ---------
  def [task_name](self, agent, [parameters]):
      return Task(description=dedent(f'''
      **Task**: [Provide a concise name or summary of the task.]
      **Description**: [Detailed description of what the agent is expected to do, including actionable steps and expected outcomes. This should be clear and direct, outlining the specific actions required to complete the task.]

      **Parameters**: 
      - [Parameter 1]: [Description]
      - [Parameter 2]: [Description]
      ... [Add more parameters as needed.]

      **Note**: [Optional section for incentives or encouragement for high-quality work. This can include tips, additional context, or motivations to encourage agents to deliver their best work.]

      '''), agent=agent)

"""
'''
class Task:
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent

        # Create a logger
        self.logger = logging.getLogger('task')
        self.logger.setLevel(logging.INFO)

        # Create a directory for the log files if it doesn't exist
        os.makedirs('crews/research_basic/logs', exist_ok=True)

        # Create a file handler that writes to a new file for each task
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        handler = logging.FileHandler(f'crews/research_basic/logs/task_{timestamp}.txt')
        handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def perform_task(self):
        # Perform the task...
        output = 'Task output'
        self.logger.info(f'Task output: {output}')
'''


class ResearchTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
                                                                 

    def topic_research(self, agent, topic):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Create a comprehensive research report on {topic}. 
                    **Description**: Conduct comprehensive research to find information from articles and academic papers related to {topic}.
                            Pay special attention to the historical progress, trends, recent developments, and potential future impacts.
                            Aggregate your findings into a comprehensive research report.
                            Make sure to include the most recent and relevant information possible.
                            You MUST include AT LEAST 4 references to RECENT articles or publications utilizing the Chicago style format for citations.
                            
                    **Parameters**: 
                    - Topic: {topic}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"Comprehensive research report on {topic}, highlighting information that would be relevant for Chief Financial Officers.",
            #output_file='research_report.txt'
        )



    def industry_analysis(self, agent, industry):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Analyze the current trends, challenges and opportunities in the {industry} industry. 
                    **Description**: Aggregate information from market reports, recent developments, and expert opinions to provide a comprensive overview of the {industry} industry.
                            Compile your findings into a comprehensive report that includes the most recent and relevant information possible.
                            Your report should include historical progress, trends, recent developments, and potential future impacts.
                            You MUST include AT LEAST 4 references to RECENT articles or publications utilizing the Chicago style format for citations.

                    **Parameters**: 
                    - Topic: {industry}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"An insightful analysis that identifies major trends, potential challenges, and strategic opportunities in {industry}."
        )

    def strategy(self, agent):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Develop strategic business recommendations and actionable advice for Chief Financial Officers. 
                    **Description**: Use the research and industry analysis conducted to develop strategic business recommendations and actionable advice for Chief Financial Officers.
                            Recommendations and advice should be for the next 12 months.
                            Each recommendation should be supported by data, evidence, and clear reasoning.
                            Explain the rationale behind each recommendation and provide a clear path for implementation.

                    **Parameters**: 

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"Comprehensive report with a list of key strategic business recommendations supported by evidence."
        ) 

    def compile_report(self, agent):
        return Task(
            description=dedent(
                f"""
                    **Task**: Compile all the research findings, industry analysis, and strategic business recommendations into a comprehensive report.
                    **Description**: Compile the research findings, industry analysis, and strategic business recommendations into a comprehensive report for the Chief Financial Officer. 
                            Ensure the report is well-structured and easy to digest for the CFO.
                            You MUST include citations to ALL referenced documents and supporting information in Chicago format at the bottom of the report.

                    **Parameters**: 

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="A comprehensive and well-structured research report for the Chief Financial Officer that includes all research findings, industry analysis, and strategic business recommendations."
        )

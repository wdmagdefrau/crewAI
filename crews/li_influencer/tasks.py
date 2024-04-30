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

# Create a directory for the log files if it doesn't exist
os.makedirs('crews/ai_influencer/logs', exist_ok=True)

# Create a file handler that writes to a new file for each run of the program
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

# create a directory for the log files based on the timestamp
os.makedirs(f'crews/li_influencer/logs/{timestamp}', exist_ok=True)

class ResearchTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
                                                                 

    def scrape_linkedin_task(self, agent):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Scrape LinkedIn profile. 
                    **Description**: Scrape LinkedIn to extract relevant posts from the given profile.
                            
                    **Parameters**: 

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"A list of LinkedIn posts obtained from a LinkedIn profile.",
            output_file=f'crews/li_influencer/logs/{timestamp}/extracted_posts_{timestamp}.txt'
        )



    def web_research_task(self, agent, topic):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Conduct web research. 
                    **Description**: Conduct web research on {topic} to gather valuable and high quality web information.

                    **Parameters**: 
                    - Topic: {topic}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"High quality research report on {topic}.",
            output_file=f'crews/li_influencer/logs/{timestamp}/research_report_{timestamp}.txt'
        )

    def create_linkedin_post_task(self, agent):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Draft a LinkedIn post. 
                    **Description**: Create a LinkedIn post following the writing style observed in the LinkedIn posts scraped by the LinkedIn Post Scraper.

                    **Parameters**: 

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"A high-quality and engaging LinkedIn post that is in line with the style of the scraped LinkedIn posts.",
            output_file=f'crews/li_influencer/logs/{timestamp}/linkedin_post_{timestamp}.txt'
        ) 

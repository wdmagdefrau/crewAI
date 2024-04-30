from crewai import Task
from textwrap import dedent
from logging_util import get_logger

import os
import json
from datetime import datetime
import uuid

'''
class Task:
    def __init__(self, description, expected_output, agent):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent

    def execute(self):
        # Execute the task and get the actual output
        actual_output = self.agent.perform_task(self.description)

        # Log the task and its output
        self.log_task_output(actual_output)

        return actual_output

    def log_task_output(self, actual_output, folder_path="crews/ai_influencer/logs/"):
        # Generate a unique identifier for each task
        unique_id = uuid.uuid4()

        # Create file paths for both JSON and TXT files
        json_file_path = os.path.join(folder_path, f"task_{unique_id}.json")
        txt_file_path = os.path.join(folder_path, f"task_{unique_id}.txt")

        task_entry = {
            "timestamp": datetime.now().isoformat(),
            "description": self.description,
            "expected_output": self.expected_output,
            "actual_output": actual_output
        }

        # Write to JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(task_entry, json_file, indent=4)

        # Write to TXT file
        with open(txt_file_path, "w") as txt_file:
            txt_file.write(f"Timestamp: {task_entry['timestamp']}\n")
            txt_file.write(f"Description: {task_entry['description']}\n")
            txt_file.write(f"Expected Output: {task_entry['expected_output']}\n")
            txt_file.write(f"Actual Output: {task_entry['actual_output']}\n")
            txt_file.write("\n")
'''

# Create a directory for the log files if it doesn't exist
os.makedirs('crews/ai_influencer/logs', exist_ok=True)

# Create a file handler that writes to a new file for each run of the program
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

class ResearchTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
    
    def research(self, agent, topic):
        return Task(
            description=dedent(
                f"""
                **Task**: Conduct a comprehensive analysis of the latest advancements in Artificial Intelligence in 2024.
                **Description**: Search the internet and academic journals for RECENT news on {topic}.
                    Validate that all sources are from the last 30 days.
                    Identify key trends, breakthrough technologies, and potential industry impacts.
                    Compile your findings in a detailed report.
                **Parameters**: 
                    - Topic: {topic}
                **Note**: {self.__tip_section()}

                """), 
            expected_output="Full analysis report in bullet points with links to reference articles that support each bullet point.", 
            agent=agent,
            #human_input=True,
            output_file=f'crews/ai_influencer/logs/research_report_{timestamp}.txt'
            )
    
    def draft(self, agent):
        return Task(
            description=dedent(
                f"""
                **Task**: Develop a theme based on the research. Write 3 engaging LinkedIn posts.
                **Description**: Use the insights provided from the research to develop 3 engaging blog posts.
                    Highlights the most significant AI advancements.
                    Your post should be informative yet accessible, catering to a tech-savvy audience.
                    Humanize your writing. Avoid complex words so it doesn't sound like AI.
                    You MUST include a a reference link to the research article that support the claim of each post.

                **Note**: {self.__tip_section()}

                """), 
            expected_output="An informative yet accessible LinkedIn post.", 
            agent=agent,
            output_file=f'crews/ai_influencer/logs/linkedin_posts_{timestamp}.txt'
            )

    def critique(self, agent):
        return Task(
            description=dedent(
                f"""
                **Task**: Provide feedback on LinkedIn posts to help them go viral.
                **Description**: Humanize the LinkedIn post to make it more accessible.
                    Suggest post hooks that immediately engage readers.
                    Structure the post so that readers will be enticed to continue reading beyond the hook of the first sentence.

                **Note**: {self.__tip_section()}

                """), 
            expected_output="Constructive feedback on LinkedIn post.", 
            agent=agent)
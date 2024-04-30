from datetime import datetime
from crewai import Crew, Process
from textwrap import dedent
from agents import ResearchAgents
from tasks import ResearchTasks
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import json
import os
import uuid
import logging

load_dotenv()

class ResearchCrew:
    def __init__(self, topic): 
        self.topic = topic

        # Create a logger
        self.logger = logging.getLogger('research_crew')
        self.logger.setLevel(logging.INFO)

        # Create a directory for the log files if it doesn't exist
        os.makedirs('crews/research_basic/logs', exist_ok=True)

        # Create a file handler that writes to a new file for each run of the program
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        handler = logging.FileHandler(f'crews/research_basic/logs/run_{timestamp}.txt')
        handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def run(self):
        self.logger.info('Starting research run')
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = ResearchAgents()
        tasks = ResearchTasks()

        # Define your custom agents and tasks here
        research_manager = agents.research_manager()
        researcher = agents.researcher()
        academic_researcher = agents.academic_researcher()

        self.logger.info('Agents created')

        research = tasks.research(
            researcher,
            self.topic
        )

        academic_research = tasks.academic_research(
            academic_researcher,
            self.topic,
        )

        compile_report = tasks.compile_report(
            research_manager,
            #web_research.expected_output,
            #academic_research.expected_output
        )

        self.logger.info('Tasks established')

        # Define crew
        crew = Crew(
            agents=[research_manager,
                    researcher,
                    #academic_researcher
                    ],
            tasks=[
                research,
                #academic_research,
                compile_report
            ],
            verbose=True,
            #manager_llm=ChatOpenAI(temperature=0, model="gpt-4-0125-preview"),
            manager_llm=AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"), 
                                         openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
                                         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                         deployment_name='GPT4',
                                         model_version='gpt-4-0125-preview',
                                         temperature=0),
            process=Process.hierarchical
            #process = Process.sequential
        )

        result = crew.kickoff()
        return result


def save_progress(data, filename="research_progress.json"):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_progress(filename="research_progress.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    progress = load_progress()
    if progress:
        resume = input("Resume previous research? (yes/no): ").strip().lower()
        if resume == 'yes':
            topic = progress['topic']
        else:
            progress = None
    
    if not progress:
        topic = input("What would you like to research? ").strip()
        #platform = input("Where will this research be published? (LinkedIn, Medium, etc.): ").strip()
        #length = input("How long should the research article/blog post be? ").strip()

        # Confirm details
        confirm = input(f"Confirm details - Topic: {topic} (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Research cancelled.")
            exit()

        save_progress({"topic": topic})

    research_crew = ResearchCrew(topic)
    result = research_crew.run()
    print("\n\n########################")
    print("## Here is your Research ##")
    print("########################\n")
    print(result)
    # Log the result
    research_crew.logger.info("Research Result: %s", result)
    


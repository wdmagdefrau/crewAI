from datetime import datetime
from crewai import Crew, Process
from textwrap import dedent
from agents import ResearchAgents
from tasks import ResearchTasks
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import os
import uuid

# New logging function for conversations
def log_conversation(user_input, ai_response, file_path="crews/researcher/logs/"):
    conversation_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "ai_response": ai_response
    }
    # Generate a unique filename for each run
    file_path += str(uuid.uuid4()) + ".json"
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            if not file_content:
                log_data = []
            else:
                log_data = json.loads(file_content)
    except FileNotFoundError:
        log_data = []

    log_data.append(conversation_entry)

    with open(file_path, "w") as file:
        json.dump(log_data, file, indent=4)

# Modify the run method of ResearchCrew to log conversations
class ResearchCrew:
    def __init__(self, topic, platform, length): 
        self.topic = topic
        self.length = length
        self.platform = platform

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = ResearchAgents()
        tasks = ResearchTasks()
        # Define your custom agents and tasks here
        journalist = agents.journalist()
        research_manager = agents.research_manager()
        research_agent = agents.research_agent()

        # Log conversations
        log_conversation("journalist", journalist)
        log_conversation("research_manager", research_manager)
        log_conversation("research_agent", research_agent)

        # Continue with the rest of your code...



load_dotenv()

class ResearchCrew:
    def __init__(self, topic, platform, length): 
        self.topic = topic,
        self.length = length,
        self.platform = platform


    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = ResearchAgents()
        tasks = ResearchTasks()

        # Define your custom agents and tasks here
        journalist = agents.journalist()
        research_manager = agents.research_manager()
        research_agent = agents.research_agent()

        # Custom tasks include agent name and variables as input
        #narrow_topic = tasks.narrow_topic(
        #    journalist,
        #    self.topic
        #)

        background_research = tasks.dynamic_background_research(
            research_agent,
            self.topic
        )

        establish_questions = tasks.establish_questions(
            research_agent,
            self.topic,
        )

        refine_questions = tasks.refine_questions(
            research_manager,
            self.topic,
            questions=establish_questions
        )


        thesis_statement = tasks.thesis_statement(
            research_manager,
            self.topic,
        )

        critique_thesis = tasks.critique_thesis(
            journalist,
            self.topic,
            self.platform,
            self.length,
            thesis=thesis_statement
        )

        write_post = tasks.write_post(
            journalist,
            self.topic,
            self.platform,
            self.length,
            thesis=thesis_statement,
            critique=critique_thesis
        )

        # Define crew
        crew = Crew(
            agents=[journalist,
                    research_manager,
                    research_agent
                    ],
            tasks=[
                #narrow_topic,
                background_research,
                establish_questions,
                refine_questions,
                thesis_statement,
                critique_thesis,
                write_post
                ],
            verbose=True,
            manager_llm=ChatOpenAI(temperature=0, model="gpt-4-0125-preview"),
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
            topic, platform, length = progress['topic'], progress['platform'], progress['length']
        else:
            progress = None
    
    if not progress:
        topic = input("What would you like to research? ").strip()
        platform = input("Where will this research be published? (LinkedIn, Medium, etc.): ").strip()
        length = input("How long should the research article/blog post be? ").strip()

        # Confirm details
        confirm = input(f"Confirm details - Topic: {topic}, Platform: {platform}, Length: {length} (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Research cancelled.")
            exit()

        save_progress({"topic": topic, "platform": platform, "length": length})

    research_crew = ResearchCrew(topic, platform, length)
    result = research_crew.run()
    print("\n\n########################")
    print("## Here is your Research ##")
    print("########################\n")
    print(result)


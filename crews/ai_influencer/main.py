import json
from datetime import datetime
import os
from crewai import Crew, Process
from textwrap import dedent
from agents import ResearchAgents
from tasks import ResearchTasks
from langchain_openai import ChatOpenAI
from logging_util import setup_logging
from dotenv import load_dotenv
import uuid

#def main():
#    setup_logging()

# New logging function for conversations
def log_conversation(user_input, ai_response, folder_path="crews/ai_influencer/logs/"):
    # Generate a unique identifier for each conversation
    unique_id = uuid.uuid4()

    # Create file paths for both JSON and TXT files
    json_file_path = os.path.join(folder_path, f"conversation_{unique_id}.json")
    txt_file_path = os.path.join(folder_path, f"conversation_{unique_id}.txt")

    conversation_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "ai_response": ai_response
    }

    # As we are creating a new file for each conversation, no need to read existing content
    log_data = [conversation_entry]

    # Write to JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(log_data, json_file, indent=4)

    # Write to TXT file
    with open(txt_file_path, "w") as txt_file:
        for entry in log_data:
            txt_file.write(f"Timestamp: {entry['timestamp']}\n")
            txt_file.write(f"User Input: {entry['user_input']}\n")
            txt_file.write(f"AI Response: {entry['ai_response']}\n")
            txt_file.write("\n")

load_dotenv()

class ResearchCrew:
    def __init__(self, topic):
        self.topic = topic
        #log_message("ResearchCrew", f"Initialized ResearchCrew with topic: {topic}")


    def run(self):
        user_input = self.topic

        agents = ResearchAgents()
        tasks = ResearchTasks()

        researcher = agents.researcher()
        influencer = agents.influencer()
        critic = agents.critic()

        research = tasks.research(
            researcher, 
            self.topic
        )

        draft = tasks.draft(
            influencer
        )

        critique = tasks.critique(
            critic
        )

        crew = Crew(
            agents = [researcher,
                      influencer,
                      #critic
                      ],
            tasks = [research,
                     draft,
                     #critique
                     ],
            verbose=True,
            manager_llm=ChatOpenAI(temperature=0, model="gpt-4-0125-preview"),
            process=Process.hierarchical
            #process=Process.sequential
        )
        #log_message("ResearchCrew", "Starting crew kickoff")
        result = crew.kickoff()
        #log_message("ResearchCrew", "Crew kickoff completed")
        ai_response = result
        log_conversation(user_input, ai_response)
        return result

def save_progress(data, filename="research_progress.json"):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_progress(filename="research_progress.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    #main()
    progress = load_progress()
    if progress:
        resume = input("Reload previous research topic? (yes/no): ").strip().lower()
        if resume == 'yes':
            topic = progress['topic']
        else:
            progress = None

    if not progress:
        print("### WELCOME TO YOUR DIGITAL INFLUENCER ###")
        print('------------------------------------------')

        topic = input(
            dedent("""
                What would you like to write about?
                """)
        )

        confirm = input(f"Confirm details - Topic: {topic} (yes/no)").strip().lower()
        if confirm != 'yes':
            print("Research cancelled.")
            exit()

        save_progress({"topic": topic})

    research_crew = ResearchCrew(topic)
    #log_message("System", "Starting research crew run")
    result = research_crew.run()
    #log_message("System", "Research crew run completed")

    print("\n\n#######################################")
    print("###### HERE IS YOUR LINKEDIN POST ######")
    print("########################################")
    print(result)



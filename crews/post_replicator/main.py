import json
from datetime import datetime
import os
from crewai import Crew, Process
from textwrap import dedent
from agents import PostAgents
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
    def __init__(self, post_content):
        self.post_content = post_content

    def run(self):
        user_input = self.post_content

        agents = PostAgents()
        tasks = ResearchTasks()

        content_analyst = agents.content_analyst()
        research_agent = agents.research_agent()
        writer_agent = agents.writer_agent()

        syle_guide = tasks.analyze_post(
            content_analyst, 
            self.post_content
        )

        research_data = tasks.research_content(
            research_agent,
            syle_guide
        )

        new_post = tasks.write_post(
            writer_agent,
            syle_guide,
            research_data
        )

        crew = Crew(
            agents = [content_analyst,
                      research_agent,
                      writer_agent
                      ],
            tasks = [syle_guide,
                     research_data,
                     new_post
                     ],
            verbose=True,
            #manager_llm=ChatOpenAI(temperature=0, model="gpt-4-0125-preview"),
                        #manager_llm=AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"), 
            #                             openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
            #                             azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            #                             deployment_name='GPT4',
            #                             model_version='gpt-4-0125-preview',
            #                             temperature=0),
            #process=Process.hierarchical
            process=Process.sequential
        )

        result = crew.kickoff()
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
        resume = input("Reload previous post content? (yes/no): ").strip().lower()
        if resume == 'yes':
            post_content = progress['post_content']
        else:
            progress = None

    if not progress:
        print("### WELCOME TO YOUR DIGITAL INFLUENCER ###")
        print('------------------------------------------')

        post_content = input(
            dedent("""
                What post would you like to replicate?
                """)
        )

        confirm = input(f"Confirm details - Original Post: {post_content} (yes/no)").strip().lower()
        if confirm != 'yes':
            print("Research cancelled.")
            exit()

        save_progress({"post_content": post_content})

    research_crew = ResearchCrew(post_content)
    #log_message("System", "Starting research crew run")
    result = research_crew.run()
    #log_message("System", "Research crew run completed")

    print("\n\n#######################################")
    print("###### HERE IS YOUR LINKEDIN POST ######")
    print("########################################")
    print(result)



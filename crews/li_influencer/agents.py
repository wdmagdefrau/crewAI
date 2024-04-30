import os
from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

from tools.linkedin_tool import scrape_linkedin_posts_tool
from tools.exa_search_tool import ExaSearchTool

"""
Creating Agents Cheat Sheet:
- Think like a boss. Work backwards from the goal and think which employee 
    you need to hire to get the job done.
- Define the Captain of the crew who orient the other agents towards the goal. 
- Define which experts the captain needs to communicate with and delegate tasks to.
    Build a top down structure of the crew.

Goal:
- To deliver a comprehensive research report on a topic that includes historical progress, trends and recent developments, and future impacts.

Captain/Manager/Boss:
- Research Manger

Employees/Experts to hire:
- Research Agent


Notes:
- Agents should be results driven and have a clear goal in mind
- Role is their job title
- Goals should actionable
- Backstory should be their resume
"""

load_dotenv()

class ResearchAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0.7)
        self.AzureGPT4 = AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"), 
                                         openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
                                         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                         deployment_name='GPT4',
                                         model_version='gpt-4-0125-preview',
                                         temperature=0.7)


    def linkedin_scraper_agent(self):
        return Agent(
            role="LinkedIn Post Scraper",
            goal=dedent(
                f"""
                Your goal is to scrape a LinkedIn profile to get a list of posts from the given profile.
                """
            ),            
            backstory=dedent(
                """
                You are an experienced programmer who excels at web scraping with expertise in scraping LinkedIn posts. You have the skills to navigate LinkedIn profiles and extract the latest posts from a given profile.
                """
            ),
            tools=[scrape_linkedin_posts_tool], 
            verbose=True,
            llm=self.AzureGPT4,
            #memory=True,
            allow_delegation=False
        )

    def web_researcher_agent(self, topic):
        return Agent(
            role="Web Researcher",
            goal=dedent(
                f"""
                Search for recent and relevant content on {topic}.
                """
            ),            
            backstory=dedent(
                """
                You are an expert research analyst who excels at searching for specific topics on the web, selecting those that provide the most value and information. 
                You possess all the necessary skills and capabilities to find the most recent and relevant information on a given topic.
                """
            ),

            tools=ExaSearchTool.tools(),
            verbose=True,
            llm=self.AzureGPT4,
            #memory=True,
            allow_delegation=False
        )

    def doppelganger_agent(self): 
        return Agent(
            role="LinkedIn Post Creator",
            goal=dedent(
                f"""You will create a LinkedIn post following the writing style
                observed in the LinkedIn posts scraped by the LinkedIn Post Scraper."""
            ),
            backstory=dedent(
                """
                You are an expert in writing LinkedIn posts replicating any influencer style
                """
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.AzureGPT4
        )
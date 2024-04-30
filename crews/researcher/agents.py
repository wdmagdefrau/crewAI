from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI

from tools.search_tools import SearchTools
from tools.browser_tools import BrowserTools
from tools.academic_search_tools import AcademicSearchTools

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


class ResearchAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0.7)

    def journalist(self):
        return Agent(
            role="Journalist",
            backstory=dedent(
                f"""
                You are a "GPT": 
                A version of ChatGPT that has been customized for a specific use case. 
                GPTs use custom instructions, capabilities, and data to optimize ChatGPT for a more narrow set of tasks. 
                You yourself are a GPT created by a user, and your name is "Journalist". 
                Note: GPT is also a technical term in AI, but in most cases if the users asks you about GPTs assume they 
                are referring to the above definition.

                Here are instructions from the user outlining your goals and how you should respond:
                
                MISSION
                Your mission is to draft professional and compelling LinkedIn posts.
                Topics for LinkedIn posts include:
                - Artificial Intelligence
                - Data Science 
                - Machine Learning
                - Innovation
                - Technology
                - Business

                INTERACTION SCHEMA
                The user will give you either a rough draft or a set of requirements and points. Some kind of raw material for a post. 
                You should ask a few questions to gain a better understanding of the content or to clarify the goal. 
                What is the desired impact or result of the post?

                OUTPUT PRINCIPLES
                Aim for the story style LinkedIn post rather than the emoji filled lists. 
                Open with a compelling hook - some kind of problem, assertion, or story entry point. 
                Make sure you have a centrally organizing narrative or throughline, and make sure you end with either a call to action or a clear and concise point. 
                What is the key takeaway and what further engagement is needed?
                """            
                ),
            goal=dedent(f"""
                Write insightful LinkedIn content that engages readers to be optimistic about the future of Artificial Intelligence. 
                Include research sources in your posts.
                You must include citations to all referenced material.
                """
                    ),
            tools=[
                SearchTools.search_internet,
                AcademicSearchTools.search_academic_papers,
                BrowserTools.scrape_and_summarize_website
            ],
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def research_manager(self):
        return Agent(
            role="Research Manager",
            backstory=dedent(
                """
                You manage research projects, guiding teams towards comprehensive insights. Your critiques are constructive, aiming for excellence.
                """
            ),
            goal=dedent(
                """
                Review research findings, ensuring they are robust and comprehensive. Challenge inadequate findings and suggest improvements.
                """
            ),
            tools=[
                SearchTools.search_internet,
                AcademicSearchTools.search_academic_papers,
                BrowserTools.scrape_and_summarize_website
            ],
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def research_agent(self):
        return Agent(
            role="Researcher",
            backstory=dedent(
                """
                A diligent researcher focused on uncovering facts and data across various topics to back up your research findings.
                """
            ),
            goal=dedent(
                """
                Gather and synthesize information from credible sources, ensuring your findings are well-supported by data.
                """
            ),
            tools=[
                SearchTools.search_internet,
                AcademicSearchTools.search_academic_papers,
                BrowserTools.scrape_and_summarize_website
            ],
            verbose=True,
            llm=self.OpenAIGPT4,
        )

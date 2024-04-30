import os
from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

from tools.search_tools import SearchTools
from tools.browser_tools import BrowserTools
from tools.academic_search_tools import AcademicSearchTools

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

    def research_manager(self):
        return Agent(
            role="Research Manager",
            goal=dedent(
                """
                Manage research projects, guiding teams towards comprehensive research reports.  
                """
            ),
            backstory=dedent(
                """
                You review and compile research findings for Chief Financial Officers.
                You challenge inadequate findings and suggest improvements.
                You provide constructive critiques on research efforts to ensure research reports are thorough and comprehensive.
                You MUST include citations and references to all sources in your reports using the Chicago formatting style.
                """
            ),
            #tools=[
            #    ExaSearchTool.tools(),
            #    AcademicSearchTools.search_academic_papers
            #],
            verbose=True,
            #llm=self.OpenAIGPT4,
            llm=self.AzureGPT4,
            #memory=True,
            #allow_delegation=True
        )

    def researcher(self):
        return Agent(
            role="Researcher",
            goal=dedent(
                """
                Gather and synthesize information on a given topic from credible sources, ensuring your findings are well-supported by data.
                """
            ),            
            backstory=dedent(
                """
                You are an expert research analyst specializing in internet based research. 
                You search the internet to uncover RECENT information and data on a provided topic. 
                You only search credible sources to ensure the information you provide is accurate and reliable.
                When a promising source is found, you scrape the website and summarize the information.
                You are meticulous in your research, ensuring that all relevant information is included in your findings.
                You produce a comprehensive report that is well-organized and easy to understand.
                You MUST include citations and references to the sources you find using the Chicago formatting style.
                """
            ),
            tools=ExaSearchTool.tools(), 
                #ExaSearchTool.tools(),
                #AcademicSearchTools.search_academic_papers
            
            verbose=True,
            #llm=self.OpenAIGPT4,
            llm=self.AzureGPT4,
            #memory=True,
            #allow_delegation=False
        )

    def academic_researcher(self):
        return Agent(
            role="Academic Researcher",
            goal=dedent(
                """
                Gather and synthesize information from academic research publications, ensuring all findings are well-supported by data.
                """
            ),            
            backstory=dedent(
                """
                You are an expert research analyst specializing in identifying and summarizing RECENT academic research papers on a given topic.  
                You search the arXiv repository of academic research papers to uncover facts and data on a provided topic. 
                You ensure the information you provide is accurate and reliable.
                You are meticulous in your research, ensuring that all relevant information is included in your findings.
                You produce a comprehensive report that is well-organized and easy to understand.
                You MUST include citations and references to the academic papers you find using the Chicago formatting style.
                """
            ),

            tools=[
                AcademicSearchTools.search_academic_papers
            ],
            verbose=True,
            #llm=self.OpenAIGPT4,
            llm=self.AzureGPT4,
            #memory=True,
            #allow_delegation=False
        )

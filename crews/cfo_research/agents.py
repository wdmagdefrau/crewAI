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

    def research_agent(self):
        return Agent(
            role="Research Specialist",
            goal=dedent(
                """
                Conduct thorough research on a topic to uncover recent news, trends, and developments.  
                """
            ),
            backstory=dedent(
                """
                As a Research Specialist, your mission is to uncover detailed information about a provided topic.
                Your research will provides the foundation for a comprehensive research report for the Chief Financial Officer.
                Your research should provide thought leadership and future foresight on the topic.
                You will consolidate your research into a comprehensive research report that is clear and concise.
                You MUST include citations and references to all sources in your reports using the Chicago formatting style.
                """
            ),
            tools=ExaSearchTool.tools(),
            verbose=True,
            llm=self.AzureGPT4,
            memory=True,
            #allow_delegation=True
        )

    def industry_agent(self):
        return Agent(
            role="Industry Analyst",
            goal=dedent(
                """
                Analyze the current industry trends, challenges, and opportunities.
                """
            ),            
            backstory=dedent(
                """
                As an Industry Analyst, your analysis will identify key trends, challenges facing the industry, and potential opportunities that could be leveraged. 
                Your analysis will be used by the Chief Financial Officer to inform future decisions and establish strategic advantage.
                You ensure the information you provide is accurate and reliable.
                You are meticulous in your analysis, ensuring that all relevant information is included in your findings.
                You produce a comprehensive report that is well-organized and easy to understand.
                You MUST include citations using the Chicago formatting style.
                """
            ),

            tools=ExaSearchTool.tools(),
            verbose=True,
            #llm=self.OpenAIGPT4,
            llm=self.AzureGPT4,
            #memory=True,
            #allow_delegation=False
        )

    def strategy_agent(self):
        return Agent(
            role="Strategy Advisor",
            goal=dedent(
                """
                Develop business recommendations and advice for Chief Financial Officers over the next 12 months. 
                """
            ),            
            backstory=dedent(
                """
                As a Strategy Advisor, your expertise will guide the development of an actionable business plan for Chief Financial Officers over the next 12 months.
                You make business recommendations based on the research and analysis conducted by other team members.
                Each recommendations MUST be clearly reasoned and supported by data and evidence.
                """
            ),

            tools=ExaSearchTool.tools(),
            verbose=True,
            llm=self.AzureGPT4,
            #memory=True,
            #allow_delegation=False
        )


    def reporting_agent(self):
        return Agent(
            role="Briefing Coordinator",
            goal=dedent(
                """
                Compile all gathered information into a comprehensive report.
                """
            ),            
            backstory=dedent(
                """
                As the Briefing Coordinator, your role is to consolidate the research, analysis, and strategic insights for the Chief Financial Officer. 
                You produce a comprehensive report that is well-organized and easy to understand.
                Your report will be used by the Chief Financial Officer to inform future decisions and establish strategic business advantage.
                You MUST include ALL citations using the Chicago formatting style.
                """
            ),

            tools=ExaSearchTool.tools(),
            verbose=True,
            llm=self.AzureGPT4,
            #memory=True,
            #allow_delegation=False
        )
    
'''    
    def research_critic(self):
        return Agent(
            role="Research Critic",
            goal=dedent(
                """
                Critique research findings to ensure they are thorough, accurate, and relevant.
                """
            ),            
            backstory=dedent(
                """
                An experienced researcher with a keen eye for detail and a critical mind. 
                Skilled in various research methodologies and statistical analysis, always looking for the truth behind the data.
                You challenge inadequate reserach findings and suggest improvements.
                You ensure that research reports are thorough and comprehensive and include references to all sources in Chicago formatting style.
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
'''

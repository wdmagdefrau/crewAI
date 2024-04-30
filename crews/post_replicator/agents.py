from tools.exa_search_tool import ExaSearchTool
from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI    
from logging_util import get_logger
from langchain.agents import load_tools
from dotenv import load_dotenv
import os

from tools.search_tools import SearchTools
from tools.browser_tools import BrowserTools
from tools.academic_search_tools import AcademicSearchTools


'''
class Agent:
    def __init__(self, role, goal, backstory, verbose, allow_delegation, tools, llm):
        self.logger = get_logger(self.__class__.__name__)
        #self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        self.tools = tools
        self.llm = llm
        self.logger.info(f'Agent {self.role} initialized with goal: {self.goal}')

    def assign_task(self, task):
        self.logger.info(f'Task "{task.description}" assigned to agent {self.name}')
'''

human_tools = load_tools(['human'])

load_dotenv()

class PostAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0.7
        )
        self.OpenAIGPT4 = ChatOpenAI(
            model_name="gpt-4-0125-preview", 
            temperature=0.7
        )
        self.AzureGPT4 = AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"), 
                                    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
                                    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                    deployment_name='GPT4',
                                    model_version='gpt-4-0125-preview',
                                    temperature=0.7)
        #log_message("ResearchAgents", "Agents initialized")

    def content_analyst(self):
        return Agent(
            role='Senior Content Analyst',
            goal='Extract key characteristics, structure, style, and formatting from the original LinkedIn post.',
            backstory="""Once a renowned data scientist with a passion for digital marketing, 
                you have evolved into a meticulous analyst of digital content. 
                Your career has been marked by a series of pioneering research projects on digital content effectiveness, 
                making you a leading expert in identifying the key elements that make digital content successful. 
                With a keen eye for detail and a rich understanding of content dynamics, 
                you are now dedicated to dissecting complex information and deriving actionable insights that can be replicated in new contexts.
                """,
            verbose=True,
            allow_delegation=False,
            tools=ExaSearchTool.tools(),
            llm=self.AzureGPT4
        )
    
    def research_agent(self):
        return Agent(
            role='Researcher',
            goal="Find alternative sources of content that are similar to the topic of the original post.",
            backstory="""Curiosity has always been your driving force. 
                From your early days as a journalist to your transition into a research specialist, 
                your quest has always been to uncover hidden truths and alternative perspectives. 
                Your extensive experience in investigative journalism has equipped you with the skills to 
                navigate vast oceans of information and bring to light the most relevant and impactful data. 
                With a network of sources across multiple industries and a knack for predictive trends, 
                you excel at providing fresh and valuable content inputs for creative endeavors.
                """,
            verbose=True,
            allow_delegation=True,
            tools=ExaSearchTool.tools(),
            llm=self.AzureGPT4
        )
    
    
    def writer_agent(self):
        return Agent(
            role='Writer',
            goal="Develop a LinkedIn post that mirrors the original using the new information.",
            backstory="""Armed with a background in creative writing and digital communication, 
                you have a talent for crafting compelling narratives that resonate with a diverse audience. 
                Your journey through various editorial roles has honed your ability to adapt your voice to 
                match the tone and style of different platforms and purposes. 
                Known for your ability to transform dry information into engaging stories, 
                you approach each writing task with a blend of creativity and strategic thinking, 
                ensuring that each piece not only informs but also inspires and engages.""",
            verbose=True,
            allow_delegation=True,
            tools=ExaSearchTool.tools(),
            llm=self.AzureGPT4
        )



    
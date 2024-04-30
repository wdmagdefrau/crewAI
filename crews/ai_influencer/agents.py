from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from logging_util import get_logger
from langchain.agents import load_tools

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

class ResearchAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0.7
        )
        self.OpenAIGPT4 = ChatOpenAI(
            model_name="gpt-4-0125-preview", 
            temperature=0.7
        )
        #log_message("ResearchAgents", "Agents initialized")

    def researcher(self):
        #log_message("Researcher", "Researcher agent created")
        return Agent(
            role='Senior Research Analyst',
            goal='Uncover cutting-edge developments in Artificial Intelligence and data science.',
            backstory="""You work at a leading tech think tank.
                Your expertise lies in identifying emerging trends.
                You have a knack for dissecting complex data and presenting actionable insights.
                Make sure to check with a human if the draft is good before finalizing your answer.
                """,
            verbose=True,
            allow_delegation=False,
            tools=[
                SearchTools.search_internet,
                AcademicSearchTools.search_academic_papers,
                BrowserTools.scrape_and_summarize_website
            ] + human_tools,
            llm=self.OpenAIGPT4
        )
    
    def influencer(self):
        #log_message("Influencer", "Influencer agent created")
        return Agent(
            role='LinkedIn Influencer',
            goal="Craft compelling content on tech advancements and Artificial Intelligence.",
            backstory="""You're a renowned LinkedIn influencer and content strategist. 
                You are known for your insightful and engaging LinkedIn posts that resonate with the posts target audience. 
                You transform complex concepts into compelling narratives. 
                You focus on creating content that showcases the positive impact Artificial Intelligence is having on the world.
                You MUST ALWAYS include a full reference to the research article supporting your claim.
                Make sure to check with a human if the draft is good BEFORE finalizing your answer.
                """,
            verbose=True,
            allow_delegation=True,
            tools=[
                SearchTools.search_internet,
                SearchTools.search_linkedin,
                #AcademicSearchTools.search_academic_papers,
                #BrowserTools.scrape_and_summarize_website
            ] + human_tools,
            llm=self.OpenAIGPT35
        )
    
    
    def critic(self):
        #log_message("Critic", "Critic agent created")
        return Agent(
            role='Expert LinkedIn Writing Critic',
            goal="Give constructive feedback on LinkedIn posts",
            backstory="""You're an expert LinkedIn copywriter that's skilled in offering straightforward, effective advice. 
                You specialize in .  
                Your feedback improves reader engagement to help posts go viral.""",
            verbose=True,
            allow_delegation=True,
            tools=[
                SearchTools.search_internet,
                AcademicSearchTools.search_academic_papers,
                BrowserTools.scrape_and_summarize_website
            ],
            llm=self.OpenAIGPT35
        )

    def chief_creative_director(self):
        return Agent(
                role="Chief Creative Director",
                goal=dedent("""\
                    Oversee the work done by your team to make sure it's the best
                    possible. and aligned with the product's goals, review, approve,
                    ask clarifying question or delegate follow up work if necessary to make
                    decisions"""),
                backstory=dedent("""\
                    You're the Chief Content Officer of leading digital
                    marketing specialized in product branding. You're working on a new
                    customer, trying to make sure your team is crafting the best possible
                    content for the customer."""),
                tools=[
                    BrowserTools.scrape_and_summarize_website,
                    SearchTools.search_internet,
                    SearchTools.search_instagram
                ],
                llm=self.OpenAIGPT35,
                verbose=True
        )

    
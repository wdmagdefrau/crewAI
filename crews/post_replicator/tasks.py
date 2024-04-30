from crewai import Task
from textwrap import dedent
from logging_util import get_logger

import os
import json
from datetime import datetime
import uuid

"""
Creating Tasks Cheat Sheet:
- Begin with the end in mind. Identify the specific outcome your tasks are aiming to achieve.
- Break down the outcome into actionable tasks, assigning each task to the appropriate agent.
- Ensure tasks are descriptive, providing clear instructions and expected deliverables.

Goal:
- Develop a detailed itinerary, including city selection, attractions, and practical travel advice.

Key Steps for Task Creation:
1. Identify the Desired Outcome: Define what success looks like for your project.
    - A detailed 7 day travel itenerary.

2. Task Breakdown: Divide the goal into smaller, manageable tasks that agents can execute.
    - Itenerary Planning: develop a detailed plan for each day of the trip.
    - City Selection: Analayze and pick the best cities to visit.
    - Local Tour Guide: Find a local expert to provide insights and recommendations.

3. Assign Tasks to Agents: Match tasks with agents based on their roles and expertise.

4. Task Description Template:
  - Use this template as a guide to define each task in your CrewAI application. 
  - This template helps ensure that each task is clearly defined, actionable, and aligned with the specific goals of your project.

  Template:
  ---------
  def [task_name](self, agent, [parameters]):
      return Task(description=dedent(f'''
      **Task**: [Provide a concise name or summary of the task.]
      **Description**: [Detailed description of what the agent is expected to do, including actionable steps and expected outcomes. This should be clear and direct, outlining the specific actions required to complete the task.]

      **Parameters**: 
      - [Parameter 1]: [Description]
      - [Parameter 2]: [Description]
      ... [Add more parameters as needed.]

      **Note**: [Optional section for incentives or encouragement for high-quality work. This can include tips, additional context, or motivations to encourage agents to deliver their best work.]

      '''), agent=agent)

"""

# Create a directory for the log files if it doesn't exist
os.makedirs('crews/ai_influencer/logs', exist_ok=True)

# Create a file handler that writes to a new file for each run of the program
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

class ResearchTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
    
    def analyze_post(self, agent, post_content):
        return Task(description=dedent(f'''
            **Task**: Analyze LinkedIn Post
            **Description**: Access the LinkedIn post at the provided URL.
                    Analyze the given LinkedIn post to extract key characteristics such as 
                    structure, style, key phrases, and thematic elements. 
                    Document these elements to provide a clear guideline for recreating similar content.

            **Parameters**: 
                - Post Content: {post_content}

            **Note**: 
                - Pay attention to subtleties in language and formatting that could influence engagement. Your insights will directly shape the creation of new posts, aiming to replicate the success of the original.
                - {self.__tip_section()}
            '''),
        expected_output="A detailed report containing the format, style, key phrases, and thematic analysis of the post.", 
        agent=agent,
        output_file=f'crews/post_replicator/logs/post_analysis_{timestamp}.txt')

    
    def research_content(self, agent, report_details):
        return Task(
            description=dedent(
                f"""
                **Task**: Conduct Content Research
                **Description**: Based on the analysis report provided, conduct thorough research to find alternative but similar content sources. 
                        Identify trends, related articles, and data that align with the themes and style of the original post.

                **Parameters**: 
                    - Report Details: {report_details}
                **Note**: 
                    - Utilize a diverse range of sources to enrich the content pool. The quality of your research will enhance the authenticity and appeal of the new post.
                    - {self.__tip_section()}

                """), 
            expected_output="A comprehensive list of alternative content sources, including articles, data points, and trends related to the original post's topic.", 
            agent=agent,
            output_file=f'crews/ai_influencer/logs/research_report_{timestamp}.txt'
            )
    
    def write_post(self, agent, style_guide, research_data):
        return Task(
            description=dedent(
                f"""
                **Task**: Write New LinkedIn Post.
                **Description**: Using the style guide from the Content Analyst and data from the Research Agent, 
                    compose a new LinkedIn post. Ensure that the new post mirrors the original in formatting, 
                    style, context, and content, using freshly researched information.
                **Parameters**: 
                    - Style Guide: {style_guide}
                    - Research Data: {research_data}

                **Note**: 
                    - Strive for clarity and engagement in your writing. Your post should not only reflect the style of the original but also stand out on its own with fresh insights and information.
                    - {self.__tip_section()}

                """), 
            expected_output="A draft of a new LinkedIn post formatted in markdown, reflecting the style and content directives provided.", 
            agent=agent,
            output_file=f'crews/ai_influencer/logs/linkedin_posts_{timestamp}.txt'
            )


from crewai import Task
from textwrap import dedent

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


class ResearchTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def dynamic_background_research(self, agent, topic, depth='basic'):
        depth_description = {
            'basic': 'Get a general understanding of the topic',
            'detailed': 'Conduct a thorough investigation, including different viewpoints and recent developments.'
        }
        description = depth_description.get(depth, 'Get a general understanding of the topic.')
                                            
        return Task(
            description = dedent(
                f"""
                **Task**: Conduct background research on {topic}
                **Description**:  {description}
                
                **Parameters**: 
                - Topic: {topic}
                
                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"{depth.capitalize()} background research on the topic."
        )
                                          
                                            
    '''                                   
    def narrow_topic(self, agent, topic):
        return Task(
            description=dedent(
                f"""
            **Task**: Narrow the topic to improve search parameters
            **Description**: Narrow the focus from a general subject, to a more limited topic, to a specific focus or issue. 
                The reader does not want a cursory look at the topic; 
                they want to walk away with some newfound knowledge and deeper understanding of the issue. 
                For that, details are essential. 
                For example, suppose you want to explore the topic of autism. 
                You might move from:
                    General topic: special needs in a classroom
                    Limited topic: autistic students in a classroom setting
                    Specific focus: how technology can enhance learning for autistic students

            **Parameters**: 
            - Topic: {topic}

            **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="A narrow research topic that improves search parameters."
        )


    def background_research(self, agent, topic):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Research and understand the basics of the {topic}. 
                    **Description**: Use the internet search tool and academic search tool to find articles and papers related to {topic}, summarize findings.

                    **Parameters**: 
                    - Topic: {topic}

                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="Background research on a topic."
        )
    '''
        

    def establish_questions(self, agent, topic): 
        return Task(
            description=dedent(
                f"""
                    **Task**:  Estgablish research questions based on background research on the given topic.
                    **Description**: Generate research questions about the topic. 
                        Create thought-provoking, open-ended questions that encourage debate. 
                        Decide which question addresses the issue that concerns you — that will be your main research question. 
                        Secondary questions will address the who, what, when, where, why, and how of the issue. 
                        As an example:
                            Main question: Do media depictions of women show their strengths or weaknesses as political leaders?
                            Supporting questions: How can more women get involved in leadership roles? Why aren’t more women involved in politics? What role do media play in discouraging women from being involved? How many women are involved in politics at a state or national level? How long do they typically stay in politics, and for what reasons do they leave?

                    **Parameters**: 
                    - Topic: {topic}                                       

                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="A main research question and secondary supporting questions."
        )
        
    
    # Parameter usage example
    def refine_questions(self, agent, topic, questions, question_count=5):
        return Task(
            description=dedent(
                f"""
                **Task**: Refine research questions based on initial findings.
                **Description**: Based on the background research, develop {question_count} refined questions that delve deeper into specific aspects of the topic.
                **Parameters**: 
                - Topic: {topic}
                - Question Count: {question_count}
                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"{question_count} refined research questions.",
            context = [questions]
        )
    
    def thesis_statement(self, agent, topic): 
        return Task(
            description=dedent(
                f"""
                    **Task**:  Develop a working thesis statement that answers the main research question. 
                    **Description**: A working thesis statement answers the main research question in a single sentence. 
                        It identifies the topic and shows the direction of the paper while 
                        simultaneously allowing the reader to glean the writer’s stance on that topic. 
                        A working thesis performs four main functions:
                            Narrows the subject to the single point that readers should understand
                            Names the topic and makes a significant assertion about that topic
                            Conveys the purpose
                            Provides a preview of how the essay will be arranged (usually).

                    **Parameters**: 
                    - Topic: {topic}
                    
                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="A working research thesis."
        )


    def write_post(self, agent, topic, platform, length, thesis, critique): 
        return Task(
            description=dedent(
                f"""
                    **Task**:  Write an engaging {length} research article on the thesis to be published on {platform}.
                    **Description**: Write an engaging research article to be published on {platform}. 
                        The research article should be approximately {length} when finished.
                        Support your claim with evidence from your research and humanize all writing. 
                        Incorporate the research questions into an optimized research article that will engage and interest readers. 
                        You MUST include proper citations for any research referenced througout the article. 
                        Include a bibliography at the end.
                        

                    **Parameters**: 
                    - Topic: {topic}
                    - Platform: {platform} 
                    - Length: {length}            

                   
                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
            context=[thesis, critique],
            expected_output= f"A {length} research article that's optimized for user interaction and engagement on {platform}. Include proper citations and bibliography."
        )



    def critique_thesis(self, agent, topic, platform, length, thesis): 
        return Task(
            description=dedent(
                f"""
                    **Task**:  Question the thesis and provide feedback for improvement. 
                    **Description**: Why does this topic matter? 
                        Why should readers care?
                        Will the thesis resonate with other readers on {platform}?
                        Is a {length} article consistent with other {platform} articles?
                        How many sources will you need? 
                        Will you need primary or secondary sources? 
                        Where will you find the best information?

                    **Parameters**: 
                    - Topic: {topic}  
                    - Platform: {platform}  
                    - Length: {length}
                                    
                    **Note**: 
                    - Only critique a thesis one time.
                    - {self.__tip_section()}
        """
            ),
            agent=agent,
            context=[thesis],
            expected_output="A refined thesis that has been optimized for content creation."
        )


'''
    def determine_sources(self, agent, thesis):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Determine what kind of sources are best for your thesis
                    **Description**: How many sources will you need? 
                        How long should your paper be? 
                        Will you need primary or secondary sources? 
                        Where will you find the best information?

                    **Parameters**: 
                    - Topic: {thesis}

                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
        )
'''

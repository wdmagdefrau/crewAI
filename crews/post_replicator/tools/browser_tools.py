import os
import json
from playwright.sync_api import sync_playwright
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
from langchain_openai import ChatOpenAI
import requests

class CustomWebScraper():
    def scrape_website_content(self, website):
        """Scrapes the content of a website using Playwright synchronously."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(website)
            content = page.content()
            browser.close()
            return content

class BrowserTools():

    @staticmethod
    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """
        Scrapes and summarizes a website's content. This method takes a single argument,
        'website', which should be a string containing the full URL of the website to scrape.
        No trailing slash is required. For example: 'https://example.com'.

        The function scrapes the website's content, partitions it, and then summarizes it
        using an AI model. The summarized content is then returned as a string.

        Parameters:
        - website (str): The URL of the website to scrape and summarize.

        Returns:
        - str: The summarized content of the website.
        """
        scraper = CustomWebScraper()
        content = scraper.scrape_website_content(website)
        elements = partition_html(text=content)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                llm=ChatOpenAI(temperature=0.7, model="gpt-4-0125-preview"),
                allow_delegation=False)
            task = Task(
                agent=agent,
                description=f'Analyze and make a LONG summary of the content below, make sure to include ALL relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}',
                expected_output=f'A summary of the information scraped from {website}'
            )
            summary = task.execute()
            summaries.append(summary)
        summarized_content = "\n\n".join(summaries)
        return f'\nScrapped Content: {summarized_content}\n'


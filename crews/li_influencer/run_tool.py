from tools.linkedin_tool import scrape_linkedin_posts_fn
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()

print(scrape_linkedin_posts_fn())

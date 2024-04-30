import os
import datetime
from exa_py import Exa
from langchain.agents import tool

class ExaSearchTool:
	@tool
	def search(query: str):
		"""Search for a webpage based on the query."""
		# calculate the date 30 days ago from today
		thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
		formatted_date = thirty_days_ago.strftime("%Y-%m-%d")

		# Append the date filter to the query
		query_with_date_filter = f"{query} after:{formatted_date}"
		return ExaSearchTool._exa().search(query_with_date_filter, use_autoprompt=True, num_results=6)

	@tool
	def find_similar(url: str):
		"""Search for webpages similar to a given URL.
		The url passed in should be a URL returned from `search`.
		"""
		return ExaSearchTool._exa().find_similar(url, num_results=6)

	@tool
	def get_contents(ids): #str):
		"""Get the contents of a webpage.
		The ids must be passed in as a list, a list of ids returned from `search`.
		"""
		#ids = eval(ids)
		contents = str(ExaSearchTool._exa().get_contents(ids))
		print(contents)
		contents = contents.split("URL:")
		contents = [content[:1000] for content in contents]
		return "\n\n".join(contents)

	def tools():
		return [ExaSearchTool.search, ExaSearchTool.find_similar, ExaSearchTool.get_contents]

	def _exa():
		return Exa(api_key=os.environ["EXA_API_KEY"])
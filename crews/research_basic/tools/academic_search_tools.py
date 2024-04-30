import requests
import xml.etree.ElementTree as ET
from langchain.tools import tool

class AcademicSearchTools:
    """
    A class to search academic papers on arXiv.
    """
    
    @tool("Search Academic Papers")
    def search_academic_papers(query, max_results=10):
        """
        Search for academic papers on arXiv related to the given query.
        
        :param query: The search query.
        :param max_results: Maximum number of results to fetch.
        :return: A list of dictionaries containing papers' information.
        """
        base_url = "http://export.arxiv.org/api/query?"
        query_params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results
        }
        response = requests.get(base_url, params=query_params)
        papers = AcademicSearchTools.parse_response(response.text)
        formatted_papers = AcademicSearchTools.format_search_results(papers)
        return formatted_papers

    @staticmethod
    def parse_response(response_xml):
        """
        Parse the XML response from the arXiv API.
        
        :param response_xml: XML response as a string.
        :return: A list of dictionaries containing papers' information.
        """
        namespace = {'arxiv': 'http://www.w3.org/2005/Atom'}
        root = ET.fromstring(response_xml)
        papers = []
        
        for entry in root.findall('arxiv:entry', namespace):
            paper_info = {
                "title": entry.find('arxiv:title', namespace).text.strip(),
                "summary": entry.find('arxiv:summary', namespace).text.strip(),
                "authors": [author.find('arxiv:name', namespace).text for author in entry.findall('arxiv:author', namespace)],
                "link": entry.find('arxiv:link[@type="application/pdf"]', namespace).attrib['href']
            }
            papers.append(paper_info)
            
        return papers

    @staticmethod
    def format_search_results(papers):
        """
        Format the search results into a readable string.
        
        :param papers: The list of papers as dictionaries.
        :return: A formatted string of the search results.
        """
        formatted_results = ""
        for idx, paper in enumerate(papers, start=1):
            formatted_results += f"Paper {idx}: {paper['title']}\n"
            formatted_results += f"Authors: {', '.join(paper['authors'])}\n"
            formatted_results += f"Summary: {paper['summary']}\n"
            formatted_results += f"Link: {paper['link']}\n\n"
        
        return formatted_results.strip()


'''
# Example usage
if __name__ == "__main__":
    query = "quantum computing"
    papers = AcademicSearchTools.search_academic_papers(query)
    formatted_results = AcademicSearchTools.format_search_results(papers)
    print(formatted_results)
'''
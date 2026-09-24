import os
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

def search_web(query: str, max_results: int = 5):
    response = tavily_client.search(query=query, search_depth="basic", max_results=max_results)
    sources = []
    for index, result in enumerate(response.get("results", []),start=1):
        source={
            "id": index,
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content")
        }
        sources.append(source)
    return sources
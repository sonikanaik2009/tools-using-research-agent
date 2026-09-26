import os
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError(
        "TAVILY_API_KEY was not found. "
        "Please add it to your .env file."
    )
tavily_client = TavilyClient(api_key=tavily_api_key)

def search_web(query: str, max_results: int = 5):
    """
    Search the web using Tavilt and returnn structured source information.
    """
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

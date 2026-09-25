import os
from dotenv import load_dotenv
from google import genai
from search_tool import search_web
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)
def research (question: str):
    """
    Research a question using Tavily and generate a grounded answer using Gemini. 
    """
    sources = search_web(question)
    research_context = ""
    for source in sources:
        research_context+=f"""
Source[{source["id"]}]
Title: {source["title"]}
URL: {source["url"]}
Content:
{source["content"]}
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
You are a research assistant.
Answer the user's research question using only the web research provided below.
Research question:
{question}

Web research:
{research_context}

Instructions:
- Give a clear and well-structured answer.
- Use only information supported by the provided sources. 
- Cite sources using [1], [2], [3], etc. 
- Do not invent sources or URLs. 
- If the sources do not contain enough information, clearly say so. 
"""
    )
    answer= response.text
    return answer, sources


if __name__ == "__main__":

    question = input("Enter your research question: ")

    answer, sources = research(question)

    print("\nANSWER")
    print("=" * 60)
    print(answer)

    print("\nSOURCES")
    print("=" * 60)

    for source in sources:
        print(f"[{source['id']}] {source['title']}")
        print(source["url"])
        print()
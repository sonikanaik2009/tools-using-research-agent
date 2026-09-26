import os
import time
from dotenv import load_dotenv
from google import genai
from search_tool import search_web
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please add it to your .env file."
    )
client = genai.Client(api_key=gemini_api_key)
def research (question: str):
    """
    Search a question using Tavily and generate a grounded answer using Gemini. 
    """
    try: 
        sources = search_web(question)
    except Exception as error:
        raise RuntimeError("Web search failed. Please try again.") from error
    if not sources:
        raise RuntimeError("No relevant web sources were found for this question.")
    research_context = ""
    for source in sources:
        research_context+=f"""
Source[{source["id"]}]
Title: {source["title"]}
URL: {source["url"]}
Content:
{source["content"]}
"""
    prompt = f"""
You are a research assistant.
Answer the user's research question using only the web research provided below.

Research question:
{question}

Web research:
{research_context}

Instructions:
- Give a clear and well-structured answer.
- Use only information supported by the provided sources.
- Cite factual claims using the source numbers provided.
- Use citation format [1], [2], [3], etc.
- When multiple sources support a claim, use [1][2].
- Only cite source numbers that actually exist in the provided research.
- Do not create or invent source numbers.
- Do not write or invent URLs in the answer.
- If the provided sources do not contain enough information, clearly say so.
"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(model="gemini-3.5-flash-lite", contents=prompt)
            answer = response.text
            return answer, sources
        except Exception as error:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise RuntimeError(
                    "The AI service is temporarily unavailable. "
                    "Please try again later."
                ) from error


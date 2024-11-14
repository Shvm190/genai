from azure.search.documents import SearchClient
from openai import AzureOpenAI
from azure.search.documents.models import VectorizableTextQuery

from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from crewai import LLM, Agent, Task, Crew

import os, sys, json

os.environ["AZURE_API_KEY"] = "KEY"
os.environ["AZURE_API_BASE"] = "https://genai-openai-tmquant.openai.azure.com/"
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

SEARCH_ENDPOINT = "https://policy-search-genaihackathon.search.windows.net"
SEARCH_INDEX_NAME = "adverse-media-index",
SEARCH_KEY = "KEY"

llm = LLM(model=f'azure/gpt-4o')

class AISearchTool(BaseTool):
    name: str = "Query AI Search"
    description: str = "Searches AI Index."

    def _run(self, name: str) -> str:
        
        endpoint = os.getenv("ENDPOINT_URL", "https://genai-openai-tmquant.openai.azure.com/")  
        deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
        search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://policy-search-genaihackathon.search.windows.net")  
        search_key = os.getenv("SEARCH_KEY", SEARCH_KEY)  
        search_index = os.getenv("SEARCH_INDEX_NAME", "adverse-media-index")  
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY", os.environ["AZURE_API_KEY"])  

        # Initialize Azure OpenAI client with key-based authentication
        client = AzureOpenAI(  
            azure_endpoint=endpoint,  
            api_key=subscription_key,  
            api_version="2024-05-01-preview",  
        )

        SYSTEM_PROMPT = """
        You are an AI assistant that screens news articles and headlines searching for adverse media relating to customers. Given the provide name,
        return any articles relating to that customer that involve any kind of financial crime for example money laundering, terrorist financing, human trafficking etc.,

        If you can find an article, return the date of that article alongside a short 1 line summary of the article. If no such article can be found, state `Not Found`.
        """

        # Prepare the chat prompt  
        chat_prompt = [
            {
            "role": "system",
            "content": SYSTEM_PROMPT,
            },
            {
            "role": "user",
            "content": name
            },
        ]  

        # Include speech result if speech is enabled  
        speech_result = chat_prompt  

        # Generate the completion  
        completion = client.chat.completions.create(  
            model=deployment,  
            messages=speech_result,  
            # past_messages=10,  
            max_tokens=800,  
            temperature=0.7,  
            top_p=0.95,  
            frequency_penalty=0,  
            presence_penalty=0,  
            stop=None,  
            stream=False,


            extra_body={
            "data_sources": [{
            "type": "azure_search",
            "parameters": {
            "endpoint": f"{search_endpoint}",
            "index_name": "adverse-media-index",
            "semantic_configuration": "semantic-search",
            "query_type": "semantic",
            "fields_mapping": {},
            "in_scope": True,
            "role_information": SYSTEM_PROMPT,
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
            "type": "api_key",
            "key": f"{search_key}"
            }
            }
            }]
            }
        )

        return completion.to_dict()["choices"][0]["message"]["content"]
    
tool = AISearchTool()

researcher = Agent(
    role='Adverse Media Scraper',
    goal="""
    Query through news articles to search for adverse media relating to customers for any instances of potential financial crime.
    If articles can be found, we should consider the recency of the article, the nature of the activities and the reliability of the source.

    Given a customer name in the input `name`, use the AISearchTool to find articles.
    """,
    backstory='An expert analyst specialised in recognisgin potential financial crime activities in the media.',
    tools=[tool],
    verbose=True,
    llm=llm
)

class MediaOutput(BaseModel):
    Risk: int = Field(..., description="Risk of article between 1 and 5.")
    Reason: str = Field(..., description="A short reasoning considering the content of the article.")

research = Task(
    description="""Search for adverse media for the given customer <NAME>{name}</NAME>. Given the returned articles, grade the risk of the
    media according to the following scale:
    - 5: High Risk - the article is recent, the source is reliable and the nature of the activities are highly suspicious.
    - 3-4: Medium Risk - the article is recent and the nature of the activities are suspicious, but the source is not as reliable.
    - 2: Low Risk - the article is old, from an unreliable source or not relating to financial crime.
    - 1: No Risk - no articles found.
    """,
    expected_output="""Return the decison in the following format:
    <Risk>: 1-5
    <Reason>: A short reasoning for the decision</Reason>
    """,
    output_json=MediaOutput,
    agent=researcher
)

crew = Crew(
    agents=[researcher],
    tasks=[research],
    verbose=True,
    # planning=True,  # Enable planning feature
)



if __name__ == "__main__":

    query_name = sys.argv[1]

    output = crew.kickoff(inputs={'name': query_name})

    print(json.dumps(output.to_dict(), indent=True))

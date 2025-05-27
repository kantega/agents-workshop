import asyncio
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from autogen_agentchat.agents import AssistantAgent
from duckduckgo_search import DDGS


from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-4.1-nano",
    model="gpt-4.1-nano",
    api_version="2024-10-21",
    azure_endpoint="https://kjzopenai.openai.azure.com/",
    api_key=api_key,
)


# # Define a tool that searches the web for information.
# # For simplicity, we will use a mock function here that returns a static string.
# async def web_search(query: str) -> str:
#     """Find information on the web"""
#     return "Kantega is an IT consultancy, with offices in Trondheim, Oslo and Bergen"


# Ducky go go
async def web_search_dgg(query: str) -> str:
    """Find information on the web Using Ducky Go Go.
    This grabs the top result snippet for the user's query"""
    with DDGS(verify=False) as ddgs:
        results = ddgs.text(query, max_results=3, safesearch="off")
        for result in results:
            # return the snippet (you can also add result['title'] or result['href'] if needed)
            return result["body"]


agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[web_search_dgg],
    system_message="Use tools to solve tasks.",
)

result = asyncio.run(agent.run(task="Find information about Kantega"))
print(result.messages[-1])

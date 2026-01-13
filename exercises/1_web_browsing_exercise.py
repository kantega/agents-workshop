import asyncio
import os

from ddgs import DDGS
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()
api_key = os.getenv("API_KEY")

model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-5-nano",
    model="gpt-5-nano",
    api_version="2025-01-01-preview",
    azure_endpoint="https://agentsbcd.openai.azure.com/",
    api_key=api_key, # type: ignore
)

# Define a tool that searches the web for information.
# For simplicity, we will use a mock function here that returns a static string.
async def web_search(query: str) -> str:
    """Find information on the web"""
    return "Kantega is an IT consultancy, with offices in Trondheim, Oslo and Bergen"

async def web_search_dgg(query: str) -> str:
    with DDGS(verify=False) as ddgs:
        results = ddgs.text(query, max_results=3, safesearch="off")
        all_results = []
        for result in results:
            all_results.append(result["body"])
        return "\n\n".join(all_results)  # Combine all results

agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[web_search_dgg],
    system_message="Use tools to solve tasks.",
)

result = asyncio.run(agent.run(task="Find information about Kantega"))
print(result.messages[-1])

# EXERCISE: write a real browsing tool to search for your name, company, or something else interesting.
# Hint: you may use DuckDuckGo API that is free to use.

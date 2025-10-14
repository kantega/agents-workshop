import asyncio
import os

from dotenv import load_dotenv
from duckduckgo_search import DDGS

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()
api_key = os.getenv("API_KEY")

model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-4.1-nano",
    model="gpt-4.1-nano",
    api_version="2024-10-21",
    azure_endpoint="https://kjzopenai.openai.azure.com/",
    api_key=api_key,
)


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
    system_message="Make a clear an easy to read answer to the user query. Use tools to solve tasks.",
)

result = asyncio.run(
    agent.run(
        task="Make a summary about Kantega AS, a company located in Trondheim, Norway"
    )
)
print("\nAGENT'S ANSWER:\n", result.messages[-1].content)

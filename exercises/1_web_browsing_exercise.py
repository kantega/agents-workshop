import asyncio

from agent_framework import tool
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

# Define a tool that searches the web for information.
# For simplicity, we will use a mock function here that returns a static string.
@tool(approval_mode="never_require")
async def web_search(query: str) -> str:
    """Find information on the web"""
    print(f"Tool called with query: {query}")
    return "Kantega is an IT consultancy, with offices in Trondheim, Oslo and Bergen"

async def search(query: str) -> None:
    async with AzureOpenAIChatClient(credential=AzureCliCredential()).as_agent(
        instructions="Make a clear an easy to read answer to the user query. Use tools to solve tasks. Only ask the tools 5 times and with strict str queries!",
        tools=[web_search],
    ) as agent:
        print(f"User: {query}")
        # NOTE: This agent API expects the user prompt as a positional argument.
        # Passing it as a keyword (e.g. query=...) can be ignored/misrouted.
        result = await agent.run(query)
        print(f"Agent: {result}\n")

async def main() -> None:
    await search("Make a summary about Kantega AS, a company located in Trondheim, Norway")

if __name__ == "__main__":
    asyncio.run(main())

# EXERCISE: write a real browsing tool to search for your name, company, or something else interesting.
# Hint: you may use DuckDuckGo API that is free to use.

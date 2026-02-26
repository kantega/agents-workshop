import asyncio

from agent_framework import tool
from agent_framework.azure import AzureOpenAIChatClient
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()

# Define a tool that searches the web for information.
# For simplicity, we will use a mock function here that returns a static string.
@tool(approval_mode="never_require")
async def web_search(query: str) -> str:
    with DDGS(verify=False) as ddgs:
        results = ddgs.text(query, max_results=3, safesearch="off")
        all_results = []
        for result in results:
            all_results.append(result["body"])
        return "\n\n".join(all_results)  # Combine all results

async def search(query: str) -> None:
    async with AzureOpenAIChatClient().as_agent(
        instructions="Make a clear and easy to read answer to the user query. Use tools to solve tasks. Only perform a web search once, using a single well-formed query. Do not search multiple times.",
        tools=[web_search],
    ) as agent:
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result}\n")

async def main() -> None:
    await search("Make a summary about Kantega AS, a company located in Trondheim, Norway. Keep it in english. ")

if __name__ == "__main__":
    asyncio.run(main())


# EXERCISE: write a real browsing tool to search for your name, company, or something else interesting.
# Hint: you may use DuckDuckGo API that is free to use.


import asyncio

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from ddgs import DDGS


# Define a tool that searches the web for information.
async def web_search_dgg(query: str) -> str:
    with DDGS(verify=False) as ddgs:
        print(f"{query}")
        results = ddgs.text(query, max_results=3, safesearch="off", )
        all_results = []
        for result in results:
            print(f"{result["body"]}")
            all_results.append(result["body"])
        return "\n\n".join(all_results)  # Combine all results

async def search(query: str) -> None:
    async with AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
        instructions="Make a clear an easy to read answer to the user query. Use tools to solve tasks.",
        tools=[web_search_dgg],
    ) as agent:
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result}\n")

async def main() -> None:
    await search("Make a summary about Kantega AS, a company located in Trondheim, Norway")

if __name__ == "__main__":
    asyncio.run(main())

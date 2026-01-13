import asyncio
import os

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()
api_key = os.getenv("API_KEY")

model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-5-nano",
    model="gpt-5-nano",
    api_version="2025-01-01-preview",
    azure_endpoint="https://agentsbcd.openai.azure.com/",
    api_key=api_key,
)

# Create the primary agent.
primary_agent = AssistantAgent(
    "primary",
    model_client=model_client,
    system_message="You are a helpful AI assistant.",
)

# Create the critic agent.
critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedback is addressed. Do not be too strict.",  # Adjusted prompt
)

termination = TextMentionTermination("APPROVE") | MaxMessageTermination(max_messages=10)

# Create a team with the primary and critic agents.
team = RoundRobinGroupChat(
    [primary_agent, critic_agent],
    termination_condition=termination,
)

asyncio.run(team.reset())

result = asyncio.run(
    Console(team.run_stream(task="Write simple code that calculates pi number"))
)
print(result.stop_reason)

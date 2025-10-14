import asyncio
import os

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
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
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
)

# Define a termination condition that stops the task if the critic approves.
text_termination = TextMentionTermination("APPROVE")

# Create a team with the primary and critic agents.
team = RoundRobinGroupChat(
    [primary_agent, critic_agent],
    termination_condition=text_termination,
)

asyncio.run(team.reset())  # Reset the team for a new task.
result = asyncio.run(
    Console(team.run_stream(task="Write a short poem about the fall season."))
)  # Stream the messages to the console.

# EXERCISE: ask the agent to create a code suggestion for something, e.g. find the pi-number.
# Hint: you may need to limit the number of rounds so the discussion doesn't take forever: termination = TextMentionTermination("APPROVE") | MaxMessageTermination(max_messages=10).
# See also: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html

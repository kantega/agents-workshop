import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os

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
# text_termination = TextMentionTermination("APPROVE")
termination = TextMentionTermination("APPROVE") | MaxMessageTermination(max_messages=10)

# Create a team with the primary and critic agents.
team = RoundRobinGroupChat(
    [primary_agent, critic_agent],
    termination_condition=termination,
)

asyncio.run(team.reset())  # Reset the team for a new task.
# result = asyncio.run(Console(team.run_stream(task="Write a short poem about the fall season.")) ) # Stream the messages to the console.

# TASK 1: SPØR OM Å LAGE KODEFORSLAG PÅ NOE, SOM F.EKS. FINN PI-NUMBER. Tips: muligens må du begrense antall rounds slik at diskusjon tar ikke evighet: termination = TextMentionTermination("APPROVE") | MaxMessageTermination(max_messages=10). See also: https://microsoft.github.io/autogen/dev//user-guide/agentchat-user-guide/tutorial/termination.html

result = asyncio.run(
    Console(team.run_stream(task="Write simple code that calculates pi number"))
)
print(
    result.stop_reason
)  # Get to know if stopped due to APPROVE or because of max rounds

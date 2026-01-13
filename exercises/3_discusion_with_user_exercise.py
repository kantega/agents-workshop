import asyncio
import os

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents import UserProxyAgent
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

assistant = AssistantAgent("assistant", model_client=model_client)
user_proxy = UserProxyAgent(
    "user_proxy", input_func=input
)  # Use input() to get user input from console.

# Create the termination condition which will end the conversation when the user says "APPROVE".
termination = TextMentionTermination("APPROVE")

# Create the team.
team = RoundRobinGroupChat([assistant, user_proxy], termination_condition=termination)

# Run the conversation and stream to the console.
stream = team.run_stream(task="Write a 4-line poem about the ocean.")
asyncio.run(Console(stream))

# EXERCISE: No exercise, just play around with the conversation. Try to get the assistant to write a poem you like and then approve it.

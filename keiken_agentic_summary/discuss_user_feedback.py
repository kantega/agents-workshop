import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import MaxMessageTermination

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
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


with open("feedback.txt", "r") as file:
    doc = file.read()

# Create the primary agent.
positive_agent = AssistantAgent(
    "positiv_agent",
    model_client=model_client,
    system_message="Fokus på alt som gikk bra.",
)

# Create the critic agent.
critic_agent = AssistantAgent(
    "kritisk_agent",
    model_client=model_client,
    system_message="Fokus på ting som kan forbedres",
)

cynic_agent = AssistantAgent(
    "kynisk_agent",
    model_client=model_client,
    system_message="Kommenter alt på en kynisk måte",
)

funny_agent = AssistantAgent(
    "morsom_agent",
    model_client=model_client,
    system_message="Lag en spøk ut av diskusjon",
)

user_proxy = UserProxyAgent(
    "user_proxy", input_func=input
)  # Use input() to get user input from console.

# Create the termination condition which will end the conversation when the user says "APPROVE".
termination = TextMentionTermination("APPROVE") | MaxMessageTermination(
    max_messages=100
)
# Create the team.
team = RoundRobinGroupChat(
    [positive_agent, critic_agent, cynic_agent, funny_agent, user_proxy],
    termination_condition=termination,
)

# Run the conversation and stream to the console.
stream = team.run_stream(
    task=f"Diskuter kort (max 1 setning) feedback fra brukere fra ditt perspektiv. Feedback:\n {doc}"
)
asyncio.run(Console(stream))
# asyncio.run(model_client.close()) # Runs into error

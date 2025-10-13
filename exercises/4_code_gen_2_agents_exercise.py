import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()
api_key = os.getenv("API_KEY")

model_client = AzureOpenAIChatCompletionClient(
    # azure_deployment="gpt-4.1-nano", # Nano is quite bad for this task
    # model="gpt-4.1-nano",
    azure_deployment="gpt-4o",
    model="gpt-4o",
    api_version="2024-10-21",
    azure_endpoint="https://kjzopenai.openai.azure.com/",
    api_key=api_key,
)

termination_condition = TextMentionTermination("TASK_COMPLETED") | MaxMessageTermination(6)
work_dir = Path("coding")


async def main() -> None:
    # define the Docker CLI Code Executor
    code_executor = DockerCommandLineCodeExecutor(work_dir=work_dir)

    # start the execution container
    await code_executor.start()

    code_executor_agent = CodeExecutorAgent(
        "code_executor_agent", code_executor=code_executor
    )
    coder_agent = AssistantAgent("coder_agent", model_client=model_client, system_message="Respond with 'TASK_COMPLETED' to when you see the code has been executed and the task is complete.")

    groupchat = RoundRobinGroupChat(
        participants=[coder_agent, code_executor_agent],
        termination_condition=termination_condition,
    )

    task = "Write Python code to calculate pi-number"
    await Console(groupchat.run_stream(task=task))

    # stop the execution container
    await code_executor.stop()


asyncio.run(main())

# EXERCISE: ask agents to solve a more complex coding task that involves several rounds of code generation and execution and some external libraries. You may want to scrape websites for data. Example tasks:
# - analyse some local data, e.g. csv files in the working directory.
# - create a plot of NVIDA vs TSLA stock returns ytd from 2025-01-01.
# - create a small web app using e.g. Flask or FastAPI.


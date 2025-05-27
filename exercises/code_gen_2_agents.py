import asyncio
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from pathlib import Path
from dotenv import load_dotenv

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

termination_condition = MaxMessageTermination(3)
work_dir = Path("coding")


async def main() -> None:
    # define the Docker CLI Code Executor
    code_executor = DockerCommandLineCodeExecutor(work_dir=work_dir)

    # start the execution container
    await code_executor.start()

    code_executor_agent = CodeExecutorAgent(
        "code_executor_agent", code_executor=code_executor
    )
    coder_agent = AssistantAgent("coder_agent", model_client=model_client)

    groupchat = RoundRobinGroupChat(
        participants=[coder_agent, code_executor_agent],
        termination_condition=termination_condition,
    )

    task = "Write python code to calculate pi number"
    await Console(groupchat.run_stream(task=task))

    # stop the execution container
    await code_executor.stop()


asyncio.run(main())

# TASK: Analyse some local data, e.g. csv files in the working directory.
# TASK: Create a plot of NVIDA vs TSLA stock returns YTD from 2025-01-01.
# TASK (Optional): Include web browsing capabilities.

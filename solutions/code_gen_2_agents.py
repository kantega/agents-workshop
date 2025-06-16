import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
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

# Improved termination condition - stops when task is completed
termination_condition = (
    TextMentionTermination("TASK_COMPLETED")
    | MaxMessageTermination(30)  # Reasonable fallback
)

work_dir = Path("coding")


async def main() -> None:
    # define the Docker CLI Code Executor
    code_executor = DockerCommandLineCodeExecutor(work_dir=work_dir)

    # start the execution container
    await code_executor.start()

    code_executor_agent = CodeExecutorAgent(
        "code_executor_agent",
        code_executor=code_executor,
    )
    coder_agent = AssistantAgent(
        "coder_agent",
        model_client=model_client,
        system_message="You are a helpful AI assistant. When you think the task has been successfully executed by a coder, write 'TASK_COMPLETED' in your answer. Do not write it before the task is completed. If you are not sure, ask the coder to check the results.",
    )

    groupchat = RoundRobinGroupChat(
        participants=[coder_agent, code_executor_agent],
        termination_condition=termination_condition,
    )

    task = "Visualize survival rates of Titanic passengers by class. Write visualization a file. Data is in titanic.csv."
    result = await Console(groupchat.run_stream(task=task))

    print(f"Execution stopped due to: {result.stop_reason}")

    await code_executor.stop()

# Start Docker: sudo systemctl start docker
# TIPS Put a local file to root/coding dir

asyncio.run(main())

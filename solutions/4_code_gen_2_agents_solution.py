# import asyncio
# import os
# from pathlib import Path

# from dotenv import load_dotenv

# from autogen_agentchat.agents import AssistantAgent
# from autogen_agentchat.agents import CodeExecutorAgent
# from autogen_agentchat.conditions import MaxMessageTermination
# from autogen_agentchat.conditions import TextMentionTermination
# from autogen_agentchat.teams import RoundRobinGroupChat
# from autogen_agentchat.ui import Console
# from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
# from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

# load_dotenv()
# api_key = os.getenv("API_KEY")

# model_client = AzureOpenAIChatCompletionClient(
#     azure_deployment="gpt-5-nano",
#     model="gpt-5-nano",
#     api_version="2025-01-01-preview",
#     azure_endpoint="https://agentsbcd.openai.azure.com/",
#     api_key=api_key,
# )

# # Improved termination condition - stops when task is completed or max 30 messages
# termination_condition = TextMentionTermination(
#     "TASK_COMPLETED"
# ) | MaxMessageTermination(30)

# work_dir = Path("coding")


# async def main() -> None:
#     # define the Docker CLI Code Executor
#     code_executor = DockerCommandLineCodeExecutor(work_dir=work_dir)

#     # start the execution container
#     await code_executor.start()

#     code_executor_agent = CodeExecutorAgent(
#         "code_executor_agent",
#         code_executor=code_executor,
#     )
#     coder_agent = AssistantAgent(
#         "coder_agent",
#         model_client=model_client,
#         system_message="""You are a helpful AI assistant that writes Python and shell code that are necessary to complete a task. You may need to install additional libraries or tools to execute your code. You are not able to execute code yourselves. The code will be executed by a code-executor agent after you send it. This is why you ALWAYS MUST provide code in markdown-encoded code blocks as a part of your answer, for example:

#         ```python
#         print("Hello world")
#         ```
#         or

#         ```sh
#         pip install numpy
#         ```

#         When you are certain the task has been successfully executed, write only 'TASK_COMPLETED' in your answer. Do not write it before the code has been run and task is completed.""",
#     )

#     groupchat = RoundRobinGroupChat(
#         participants=[coder_agent, code_executor_agent],
#         termination_condition=termination_condition,
#     )

#     task = "Visualize survival rates of Titanic passengers by class. Write visualization a file. Data is in titanic.csv."
#     result = await Console(groupchat.run_stream(task=task))

#     print(f"Execution stopped due to: {result.stop_reason}")

#     await code_executor.stop()


# asyncio.run(main())

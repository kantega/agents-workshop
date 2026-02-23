import asyncio
import sys
from pathlib import Path

from agent_framework import Workflow
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.orchestrations import GroupChatBuilder
from azure.identity import AzureCliCredential

sys.path.insert(0, str(Path(__file__).parent.parent))
from process_event_stream import process_event_stream

rounds_of_discussion = 2
chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())

# Create the coding agent.
primary = chat_client.as_agent(
    name="Coder",
    instructions="You are a helpful AI assistant that keeps it short.",
    chat_client=chat_client,
)

# Create the orchestrator coordinating the discussion
orchestrator = chat_client.as_agent(
    name="orchestrator",
    instructions=(
        "You are a discussion manager coordinating a team conversation between participants. "
        "Your job is to select who speaks next.\n\n"
        "RULES:\n"
        "1. Rotate through ALL participants - do not favor any single participant\n"
        "2. Each participant should speak at least once before any participant speaks twice\n"
        "3. Continue for at least {rounds_of_discussion} rounds before ending the discussion\n"
        "4. Do NOT select the same participant twice in a row"
    ),
)

team = (
    GroupChatBuilder(
        participants=[primary],
        max_rounds=rounds_of_discussion,
        orchestrator_agent=orchestrator,
    )
    # .with_request_info()  # Only pause before primary speaks
    .build()
)

async def main_stream(task: str, workflow: Workflow) -> None:
     stream = workflow.run(task, stream=True)
     pending_responses = await process_event_stream(stream, setHumanInTheLoop=False)
     while pending_responses is not None:
        # Run the workflow until there is no more human feedback to provide,
        # in which case this workflow completes.
        stream = workflow.run(stream=True, responses=pending_responses)
        pending_responses = await process_event_stream(stream, setHumanInTheLoop=False)

task = "What is the answer to everything?"

if __name__ == "__main__":
    print("Starting team discussion...")
    asyncio.run(main_stream(task, team))

# EXERCISES:
# a) Ask the team to solve the task: "Write code that calculates the pi number."
# b) Give the Coder space: remove the limitation of keeping it short. Observe the quality of the output.
# c) Create a "critic" agent and add it to the discussion. The critic should:
#    "Provide constructive feedback. Do not be too strict."

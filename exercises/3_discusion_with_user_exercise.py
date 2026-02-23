import asyncio
import sys
from pathlib import Path

from agent_framework import Workflow
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.orchestrations import GroupChatBuilder
from azure.identity import AzureCliCredential

sys.path.insert(0, str(Path(__file__).parent.parent))
from process_event_stream import process_event_stream

discussion_rounds = 2
chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())

# Create the author agent.
author = chat_client.as_agent(
    name="Author",
    instructions="You are a helpful AI assistant. Keep your answers somewhat short.",
    chat_client=chat_client,
)

# Create the critic agent.
critic = chat_client.as_agent(
    name="Critic",
    instructions=
        "Provide constructive feedback. "
        "Do not be too strict. Keep your answers somewhat short.",
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
        f"3. Continue for at least {discussion_rounds} rounds before ending the discussion\n"
        "4. Do NOT select the same participant twice in a row"
    )
)

# Create a team with the author and critic agents.
team = (
    GroupChatBuilder(
    participants=[author, critic],
    orchestrator_agent=orchestrator)
    .with_max_rounds(discussion_rounds)  # Limit the number of rounds the discussion can go on for
    .build()
)

async def main_stream(task: str, workflow: Workflow) -> None:
     stream = workflow.run(task, stream=True)
     pending_responses = await process_event_stream(stream, setHumanInTheLoop=False)
     while pending_responses is not None:
        stream = workflow.run(stream=True, responses=pending_responses)
        pending_responses = await process_event_stream(stream, setHumanInTheLoop=False)

task = "Write a 4-line poem about the ocean."

if __name__ == "__main__":
    print("Starting team discussion...")
    asyncio.run(main_stream(task, team))

# EXERCISE: 
# a) Try to get the author to write a poem you like by improving the task text.
# b) If you like you can increase the discussion_rounds to give the agents more space to improve the poem.
# c) Put yourself in the team and give feedback to the author to steer the poem in a direction you like:
#   - Change setHumanInTheLoop to True in the process_event_stream function call.
#     This will allow the human to provide feedback to the agents when the workflow requests it.
#   - Provide feedback to the discussion and observe how the discussion changes.
# Just play around with the conversation. You can change the task to be anything you like.

import asyncio
import sys
from pathlib import Path

from agent_framework import ChatAgent
from agent_framework import GroupChatBuilder
from agent_framework import GroupChatState
from agent_framework import Workflow
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

sys.path.insert(0, str(Path(__file__).parent.parent))
from streaming_output import stream

chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())

# Create the coding agent.
primary = ChatAgent(
    name="Coder",
    instructions="You are a helpful AI assistant.",
    chat_client=chat_client,
)

# Create the critic agent.
critic = ChatAgent(
    name="Critic",
    instructions="Provide constructive feedback. Respond with 'APPROVE' to when your feedback is addressed. Do not be too strict.",
    chat_client=chat_client,
)

# Create the discussion selection algorithm.
def round_robin_selector(state: GroupChatState) -> str:
    """A round-robin selector function that picks the next speaker based on the current round index."""
    participant_names = list(state.participants.keys())
    selected = participant_names[state.current_round % len(participant_names)]
    print(f"\n\nRound {state.current_round}: Selected speaker: {selected}\n")
    return selected

# Create a team with the primary and critic agents.
team = (
    GroupChatBuilder()
    .with_select_speaker_func(round_robin_selector)
    .participants([primary, critic])
    .with_termination_condition(lambda conversation: len(conversation) >= 4)
    .build()
)

async def main_stream(task: str, workflow: Workflow) -> None:
    await stream(task, workflow)

task = "Write code that calculates the pi number"

if __name__ == "__main__":
    print("Starting team discussion...")
    asyncio.run(main_stream(task, team))

# EXERCISES:
# a) Ask the team to solve the task: "Write code that calculates the pi number."
# b) Give the Coder space: remove the limitation of keeping it short.
# c) Create a "critic" agent and add it to the discussion. The critic should:
#   "Provide constructive feedback. Respond with 'APPROVE' to when your feedback is addressed. Do not be too strict.""

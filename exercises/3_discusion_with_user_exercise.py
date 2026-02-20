import asyncio
import sys
from pathlib import Path

from agent_framework import ChatAgent
from agent_framework.orchestrations import GroupChatBuilder
from agent_framework import GroupChatState
from agent_framework import Workflow
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

sys.path.insert(0, str(Path(__file__).parent.parent))
from streaming_output import stream

chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())

# Create the author
author = ChatAgent(
    name="Author",
    instructions="You are a helpful AI assistant with quite good author skills.",
    chat_client=chat_client,
)

# Create the critic agent.
critic = ChatAgent(
    name="Critic",
    instructions="Provide constructive feedback to the author. Respond with 'APPROVE' to when your feedback is addressed. Do not be too strict.",
    chat_client=chat_client,
)

user = UserProxyAgent(
    "user_proxy", input_func=input
)  # Use input() to get user input from console.

# Create the team.

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
    .participants([author, critic])
    .with_termination_condition(lambda conversation: len(conversation) >= 4)
    .with_request_info(agents=[author])  # Only pause before pragmatist speaks
    .build()
)


# Initiate the first run of the workflow.
# Runs are not isolated; state is preserved across multiple calls to run.
stream = team.run(
    "Discuss how our team should approach adopting AI tools for productivity. "
    "Consider benefits, risks, and implementation strategies.",
    stream=True,
)

pending_responses = await process_event_stream(stream)
while pending_responses is not None:
    # Run the workflow until there is no more human feedback to provide,
    # in which case this workflow completes.
    stream = team.run(stream=True, responses=pending_responses)
    pending_responses = await process_event_stream(stream)


# Run the conversation and stream to the console.
stream = team.run_stream(task="Write a 4-line poem about the ocean.")

if __name__ == "__main__":
    asyncio.run(main())
# EXERCISE: No exercise, just play around with the conversation. Try to get the author to write a poem you like and then approve it.

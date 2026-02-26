import asyncio
import sys
from pathlib import Path

from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework.orchestrations import GroupChatBuilder
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
from process_event_stream import process_event_stream

discussion_rounds = 1
load_dotenv()

async def main_stream(task: str) -> None:

    client = AzureOpenAIResponsesClient()

    # Create the author agent.
    author = client.as_agent(
        name="Author",
        instructions="You are a helpful AI assistant. Keep your answers somewhat short.",
    )

    # Create the critic agent.
    critic = client.as_agent(
        name="Critic",
        instructions=
            "Provide constructive feedback. "
            "Do not be too strict. Keep your answers somewhat short.",
    )

    # Create the orchestrator coordinating the discussion
    orchestrator = client.as_agent(
        name="orchestrator",
        instructions=(
            "You are a discussion manager coordinating a team conversation between participants. "
            "Your job is to select who speaks next.\n\n"
            "RULES:\n"
            "1. Rotate through ALL participants - do not favor any single participant\n"
            "2. Each participant should speak at least once before any participant speaks twice\n"
            f"3. Continue for at least {discussion_rounds-1} rounds before ending the discussion\n"
            "4. Do NOT select the same participant twice in a row"
        )
    )

    # Create a team with the author and critic agents.
    team = (
        GroupChatBuilder(
            participants=[author, critic],
            orchestrator_agent=orchestrator,
            intermediate_outputs=True
         )
        .with_max_rounds(discussion_rounds)  # Limit the number of rounds the discussion can go on for
        .build()
    )

    stream = team.run(task, stream=True)

    pending_responses = await process_event_stream(stream)
    while pending_responses is not None:
        # Run the team until there is no more human feedback to provide,
        # in which case this team completes.
        stream = team.run(stream=True, responses=pending_responses)
        pending_responses = await process_event_stream(stream)


if __name__ == "__main__":
    print("Starting team discussion...")
    task = "Write a 3-line poem about the ocean."
    asyncio.run(main_stream(task))

# EXERCISE: 
# a) Try to get the author to write a poem you like by improving the task text.
# b) If you like you can increase the discussion_rounds to give the agents more space to improve the poem.
# c) Put yourself in the team and give feedback to the author to steer the poem in a direction you like:
#   - add .with_request_info(agents=[critic])  # Only pause before critic speaks
#     This will allow the human to provide feedback to the agents when the workflow requests it.
#   - Provide feedback to the discussion and observe how the discussion changes.
#
# Just play around with the conversation. You can change the task to be anything you like.

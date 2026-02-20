from collections.abc import AsyncIterable
from typing import cast

from agent_framework import AgentExecutorResponse
from agent_framework import Message
from agent_framework import WorkflowEvent
from agent_framework.orchestrations import AgentRequestInfoResponse


async def process_event_stream(stream: AsyncIterable[WorkflowEvent]) -> dict[str, AgentRequestInfoResponse] | None:
    """Process events from the workflow stream to capture human feedback requests."""
    requests: dict[str, AgentExecutorResponse] = {}
    async for event in stream:
        if event.type == "request_info" and isinstance(event.data, AgentExecutorResponse):
            requests[event.request_id] = event.data

        if event.type == "output":
            # The output of the workflow comes from the orchestrator and it's a list of messages
            print("\n" + "=" * 60)
            print("DISCUSSION COMPLETE")
            print("=" * 60)
            print("Final discussion summary:")
            # To make the type checker happy, we cast event.data to the expected type
            outputs = cast(list[Message], event.data)
            for msg in outputs:
                speaker = msg.author_name or msg.role
                print(f"[{speaker}]: {msg.text}")

    responses: dict[str, AgentRequestInfoResponse] = {}
    if requests:
        for request_id, request in requests.items():
            # Display pre-agent context for human input
            print("\n" + "-" * 40)
            print("INPUT REQUESTED")
            print(
                f"Agent {request.executor_id} just responded with: '{request.agent_response.text}'. "
                "Please provide your feedback."
            )
            print("-" * 40)
            if request.full_conversation:
                print("Conversation context:")
                recent = (
                    request.full_conversation[-2:] if len(request.full_conversation) > 2 else request.full_conversation
                )
                for msg in recent:
                    name = msg.author_name or msg.role
                    text = (msg.text or "")[:150]
                    print(f"  [{name}]: {text}...")
                print("-" * 40)

            # Get human input to steer the agent
            user_input = input(f"Feedback for {request.executor_id} (or 'skip' to approve): ")  # noqa: ASYNC250
            if user_input.lower() == "skip":
                user_input = AgentRequestInfoResponse.approve()
            else:
                user_input = AgentRequestInfoResponse.from_strings([user_input])

            responses[request_id] = user_input

    return responses if responses else None

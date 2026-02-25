from collections.abc import AsyncIterable

from agent_framework import AgentExecutorResponse
from agent_framework import AgentResponseUpdate
from agent_framework import WorkflowEvent
from agent_framework.orchestrations import AgentRequestInfoResponse


async def process_event_stream(stream: AsyncIterable[WorkflowEvent]) -> dict[str, AgentRequestInfoResponse] | None:
    """Process events from the workflow stream to capture human feedback requests."""
    requests: dict[str, AgentExecutorResponse] = {}
    # Spor siste agent for streaming output
    last_author: str | None = None
    async for event in stream:
        # Oppdateringene kan brukes til å vise en stream av agentenes svar mens de genereres.
        if event.type == "output" and isinstance(event.data, AgentResponseUpdate):
            update = event.data
            author = update.author_name
            if author != last_author:
                if last_author is not None:
                    print()  # Newline between different authors
                if author is not None:
                    print(f"[{author.upper()}]: {update.text}\n", end="", flush=True)
                else:
                    print(f"[?]: {update.text}\n", end="", flush=True)
                last_author = author
            else:
                print(update.text, end="", flush=True)

        if event.type == "request_info" and isinstance(event.data, AgentExecutorResponse):
            requests[event.request_id] = event.data

    responses: dict[str, AgentRequestInfoResponse] = {}
    if requests:
        for request_id, request in requests.items():

            # Vis pre-agent kontekst for bruker-input
            print("\n" + "-" * 40)
            print("INPUT REQUESTED")
            print(
                f"[{request.executor_id}] just responded with: '{request.agent_response.text}'. "
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
                    text = (msg.text or "")[:350]
                    print(f"[{name.upper()}]: {text}\n...")
                print("-" * 40)

            # Bruker-input blokkerer event loop og venter til brukeren har skrevet og trykket enter 
            user_input = input(f"Feedback for {request.executor_id} (or 'skip' to approve): ")  # noqa: ASYNC250
            if user_input.lower() == "skip":
                user_input = AgentRequestInfoResponse.approve()
            else:
                user_input = AgentRequestInfoResponse.from_strings([user_input])

            responses[request_id] = user_input

    return responses if responses else None

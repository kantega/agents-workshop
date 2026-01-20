from agent_framework import AgentRunUpdateEvent
from agent_framework import ChatMessage
from agent_framework import Workflow
from agent_framework import WorkflowOutputEvent


# Streaming specifics to understand the discussion
async def stream(task: str, workflow: Workflow) -> None:
    """Streaming output handler for agent framework workflows."""

    last_executor_id: str | None = None
    output_event: WorkflowOutputEvent | None = None
    async for event in workflow.run_stream(task):
        if isinstance(event, AgentRunUpdateEvent):
            eid = event.executor_id
            if eid != last_executor_id:
                if last_executor_id is not None:
                    print("\n")
                print(f"{eid}:", end=" ", flush=True)
                last_executor_id = eid
            print(event.data, end="", flush=True)
        elif isinstance(event, WorkflowOutputEvent):
            output_event = event
            
    # The output of the workflow is the full list of messages exchanged
    if output_event:
        if not isinstance(output_event.data, list) or not all(
            isinstance(msg, ChatMessage)
            for msg in output_event.data  # type: ignore
        ):
            raise RuntimeError("Unexpected output event data format.")
        print("\n" + "=" * 80)
        print("\nFINAL OUTPUT (The conversation history)\n")
        for msg in output_event.data:  # type: ignore
            assert isinstance(msg, ChatMessage)
            print(f"{msg.author_name or msg.role}: {msg.text}\n")
    else:
        raise RuntimeError("Workflow did not produce a final output event.")

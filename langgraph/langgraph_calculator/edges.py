from typing import Literal
from langgraph.graph import END


def should_continue(state) -> Literal["tool_node", END]:
    """Decide to continue the loop or stop based on tool call"""
    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END

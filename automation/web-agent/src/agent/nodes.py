from langchain.messages import SystemMessage
from langchain.messages import ToolMessage
from agent.model import model_with_tools
from agent.tools import tools_by_name


def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""
    messages = [
        model_with_tools.invoke(
            [
                SystemMessage(
                    content="""You are a web automation agent. Your job is to help the user achieve their goals on the web using the available tools.
Always prioritize using the built-in tools to interact with the web page.
If you encounter an error or get stuck, use extract_sanitized_html to analyze the page content and try an alternative approach to achieve the goal.
Always break down complex tasks into simple steps using available tools.
Think step by step and use tools one at a time."""
                )
            ]
            + state["messages"]
        )
    ]
    
    return {
        "messages": messages,
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


def tool_node(state: dict):
    """Performs the tool call"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}
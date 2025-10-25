from langgraph.graph import StateGraph, START, END
from state import MessagesState
from nodes import llm_call, tool_node
from edges import should_continue
from langchain.messages import HumanMessage

# Build agent workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
agent = agent_builder.compile()

# Save agent graph image
img_bytes = agent.get_graph(xray=True).draw_mermaid_png()
with open("agent_graph.png", "wb") as f:
    f.write(img_bytes)


# Agent invocation
messages = [HumanMessage(content="Add 3 and 4.")]
state = {"messages": messages}
messages = agent.invoke(state)
for m in messages["messages"]:
    m.pretty_print()

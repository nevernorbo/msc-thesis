from langchain.messages import HumanMessage
from langgraph.graph import END, START, StateGraph
from agent.edges import should_continue
from agent.nodes import llm_call, tool_node
from agent.state import MessagesState

# Build agent workflow
graph = StateGraph(MessagesState)

# Add nodes
graph.add_node("llm_call", llm_call)
graph.add_node("tool_node", tool_node)

# Add edges to connect nodes
graph.add_edge(START, "llm_call")
graph.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
graph.add_edge("tool_node", "llm_call")

# Compile the agent
agent = graph.compile()

# # Save agent graph image
# img_bytes = agent.get_graph(xray=True).draw_mermaid_png()
# with open("agent_graph.png", "wb") as f:
#     f.write(img_bytes)


# # Agent invocation
# messages = [HumanMessage(content="Add 3 and 4.")]
# state = {"messages": messages}
# messages = agent.invoke(state)
# for m in messages["messages"]:
#     m.pretty_print()

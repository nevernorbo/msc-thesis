import os
from langchain_openai import ChatOpenAI
from agent.tools import tools

# model = ChatOllama(model="qwen3:4b")
model = ChatOpenAI(
    model="gemini-2.5-flash",
    temperature=0,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)
model_with_tools = model.bind_tools(tools)

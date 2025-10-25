from langchain_ollama import ChatOllama
from tools import tools

model = ChatOllama(model="qwen3:4b")
model_with_tools = model.bind_tools(tools)

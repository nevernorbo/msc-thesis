from typing import Optional
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL_OLLAMA_QWEN3 = "ollama_chat/qwen3:4b"
# MODEL_OLLAMA_GEMMA3 = "ollama_chat/gemma3:12b"
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash"


def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
        print(f"--- Tool: say_hello called with name: {name} ---")
    else:
        greeting = "Hello there!"
        print(
            f"--- Tool: say_hello called without a specific name (name_arg_value: {name}) ---"
        )
    return greeting


greeting_agent = Agent(
    # model=LiteLlm(model=MODEL_OLLAMA_QWEN3, api_base="http://localhost:11434"),
    model=MODEL_GEMINI_2_5_FLASH,
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
    "Use the 'say_hello' tool to generate the greeting. "
    "If the user provides their name, make sure to pass it to the tool. "
    "Do not engage in any other conversation or tasks.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",  # Crucial for delegation
    tools=[say_hello],
)

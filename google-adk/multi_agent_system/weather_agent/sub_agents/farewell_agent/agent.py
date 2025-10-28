from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


MODEL_OLLAMA_QWEN3 = "ollama_chat/qwen3:4b"
# MODEL_OLLAMA_GEMMA3 = "ollama_chat/gemma3:12b"
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash"


def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print("--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."


farewell_agent = Agent(
    # model=LiteLlm(model=MODEL_OLLAMA_QWEN3, api_base="http://localhost:11434"),
    model=MODEL_GEMINI_2_5_FLASH,
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
    "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
    "Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)

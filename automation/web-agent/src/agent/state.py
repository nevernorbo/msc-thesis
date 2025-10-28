from typing_extensions import TypedDict, Annotated
from langchain.messages import AnyMessage
import operator


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

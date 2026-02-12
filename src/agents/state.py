"""Agent state definitions for LangGraph."""

from __future__ import annotations

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """Shared state that flows through the agent graph.

    Extend this class to add domain-specific fields as the project evolves.
    """

    messages: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)
    context: str = ""
    query: str = ""
    confidence: float = 0.0

"""New LangGraph Agent.

This module defines a custom graph.
"""
from agent.tools import create_chrome_driver
from agent.graph import graph

__all__ = ["graph"]
create_chrome_driver()

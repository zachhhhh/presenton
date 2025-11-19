"""Simplified state context data used in MCP tests."""

from __future__ import annotations


class StateContext:
    """Simple state context with metadata."""

    def __init__(self) -> None:
        self.metadata: dict[str, object] = {}

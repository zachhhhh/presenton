"""Shared helpers for the MCP tool stubs."""

from __future__ import annotations

from typing import Any, Iterable


def success_response(**payload: Any) -> dict[str, Any]:
    """Build a success payload for a tool response."""
    return {"status": "success", **payload}


def error_response(message: str, **payload: Any) -> dict[str, Any]:
    """Build an error payload for a tool response."""
    return {"status": "error", "error": message, **payload}


def ensure_layouts(layouts: Iterable[str] | None = None) -> list[str]:
    """Ensure layouts list is always populated."""
    return list(layouts or ["default"])

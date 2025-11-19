"""Simple show_layouts tool for MCP tests."""

from __future__ import annotations

from fastmcp import FastMCP

from app_mcp.services.workflow_orchestrator import WorkflowOrchestrator
from app_mcp.tools._helpers import ensure_layouts, error_response, success_response


def register_show_layouts(
    mcp: FastMCP, orchestrator: WorkflowOrchestrator
) -> None:
    """Register a tool that lists layouts for a session."""

    @mcp.tool(name="show_layouts")
    async def show_layouts(
        session_id: str | None = None,
    ) -> dict[str, object]:
        if not session_id:
            return error_response("Session ID is required", session_id="")

        orchestrator.get_session(session_id)
        return success_response(
            session_id=session_id,
            layouts=ensure_layouts(),
            message="Available layouts returned.",
            suggestion="Choose a layout to continue.",
        )

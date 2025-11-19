"""Stub start_presentation tool used in MCP tests."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from app_mcp.services.workflow_orchestrator import WorkflowOrchestrator
from app_mcp.tools._helpers import error_response, success_response


def register_start_presentation(
    mcp: FastMCP, orchestrator: WorkflowOrchestrator
) -> None:
    """Register a simplified start presentation tool."""

    @mcp.tool(name="start_presentation")
    async def start_presentation(
        session_id: str | None = None,
        prompt: str | None = None,
        files: Any | None = None,
        n_slides: int | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        if not session_id:
            return error_response("Session ID is required", session_id="")
        if not prompt:
            return error_response("Prompt is required", session_id=session_id)

        orchestrator.get_session(session_id)
        return success_response(
            session_id=session_id,
            message="Presentation started!",
            suggestion="Use continue_workflow to move forward.",
            next_step="continue_workflow",
            parameters={
                "n_slides": n_slides or 0,
                "language": language or "English",
            },
        )

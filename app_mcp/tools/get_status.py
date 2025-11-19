"""Simple get_status tool used in MCP tests."""

from __future__ import annotations

from fastmcp import FastMCP

from app_mcp.services.workflow_orchestrator import WorkflowOrchestrator
from app_mcp.tools._helpers import error_response, success_response


def register_get_status(
    mcp: FastMCP, orchestrator: WorkflowOrchestrator
) -> None:
    """Register a status tool that reports progress for a session."""

    @mcp.tool(name="get_status")
    async def get_status(session_id: str | None = None) -> dict[str, object]:
        if not session_id:
            return error_response("Valid session_id is required", session_id="")

        orchestrator.get_session(session_id)
        return success_response(
            session_id=session_id,
            current_step="start_presentation",
            progress=0.5,
            message="Workflow in progress",
            next_action="continue_workflow",
            context={"metadata": {}},
        )

"""Simplified continue workflow tool used in MCP tests."""

from __future__ import annotations

from fastmcp import FastMCP

from app_mcp.services.workflow_orchestrator import WorkflowOrchestrator
from app_mcp.tools._helpers import error_response, success_response


def register_continue_workflow(
    mcp: FastMCP, orchestrator: WorkflowOrchestrator
) -> None:
    """Register a continuation tool that inspects the session_id."""

    @mcp.tool(name="continue_workflow")
    async def continue_workflow(
        session_id: str | None = None,
    ) -> dict[str, object]:
        if not session_id:
            return error_response("Valid session_id is required", session_id="")

        orchestrator.get_session(session_id)
        return success_response(
            session_id=session_id,
            next_step="show_layouts",
        )

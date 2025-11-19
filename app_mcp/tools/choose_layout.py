"""Choose layout MCP tool stub."""

from __future__ import annotations

from fastmcp import FastMCP

from app_mcp.services.workflow_orchestrator import WorkflowOrchestrator
from app_mcp.tools._helpers import error_response, success_response


def register_choose_layout(
    mcp: FastMCP, orchestrator: WorkflowOrchestrator
) -> None:
    """Register a layout selection tool for tests."""

    @mcp.tool(name="choose_layout")
    async def choose_layout(
        session_id: str | None = None, layout_name: str | None = None
    ) -> dict[str, object]:
        if not session_id:
            return error_response("Valid session_id is required", session_id="")
        if not layout_name:
            return error_response(
                "Layout name is required", session_id=session_id
            )

        orchestrator.get_session(session_id)
        return success_response(
            session_id=session_id,
            message=f"Layout {layout_name} selected.",
            suggestion="You can export the presentation next.",
            available_actions=["export_presentation"],
        )

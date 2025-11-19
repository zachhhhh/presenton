"""Stub export presentation tool for MCP tests."""

from __future__ import annotations

from fastmcp import FastMCP

from app_mcp.services.workflow_orchestrator import WorkflowOrchestrator
from app_mcp.tools._helpers import error_response, success_response


def register_export_presentation(
    mcp: FastMCP, orchestrator: WorkflowOrchestrator
) -> None:
    """Register an export presentation tool that validates the format."""

    VALID_FORMATS = {"pptx", "pdf"}

    @mcp.tool(name="export_presentation")
    async def export_presentation(
        session_id: str | None = None, format: str | None = None
    ) -> dict[str, object]:
        if not session_id:
            return error_response("Session ID is required", session_id="")

        if not format or format.lower() not in VALID_FORMATS:
            return error_response(
                "Please choose either 'pdf' or 'pptx' format", session_id=session_id
            )

        orchestrator.get_session(session_id)
        normalized = format.lower()
        suffix = "PPTX!" if normalized == "pptx" else "PDF!"
        return success_response(
            session_id=session_id,
            message=f"Exported presentation {suffix}",
            path=f"/tmp/{session_id}.{normalized}",
            suggestion="Download the file via the path",
            available_actions=["show_layouts"],
        )

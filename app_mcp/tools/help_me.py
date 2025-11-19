"""Minimal help tool used in MCP tests."""

from fastmcp import FastMCP


def register_help_me(mcp: FastMCP, orchestrator) -> None:  # orchestrator used for compatibility
    """Register a simple help tool."""

    @mcp.tool(name="help")
    async def help_tool() -> dict[str, object]:
        return {
            "status": "info",
            "message": "Use the start_presentation tool to begin.",
            "workflow": {"step_1": "start_presentation"},
            "helpful_commands": ["get_status", "continue_workflow"],
            "quick_start": "Start with a topic and number of slides.",
            "tips": ["Keep prompts short", "Provide context when possible"],
        }

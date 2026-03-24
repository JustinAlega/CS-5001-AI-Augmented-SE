"""
AutoGen AssistantAgent definitions for the Repository Agent v2 (MCP + A2A).
"""
from pathlib import Path
from typing import List
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

import config

def _model_client() -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
        model=config.MODEL,
        base_url=f"{config.OLLAMA_HOST}/v1",
        api_key="ollama",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "structured_output": False,
            "family": "unknown",
        },
    )

# ── MCP TOOLKIT SETUP ──────────────────────────────────────────

async def get_mcp_tools():
    # Define the MCP server connection
    server_path = str(Path(__file__).parent / "mcp_server.py")
    server_params = StdioServerParams(command="python", args=[server_path])
    return await mcp_server_tools(server_params)

# ── AGENT DEFINITIONS ──────────────────────────────────────────

_ANALYZER_PROMPT = """\
You are the Repository Analyzer. Your goal is to review code changes and decide on actions.
Use the provided MCP tools to:
1. Call get_git_status and get_git_diff to see what changed.
2. Call read_file on affected files to understand context.

OUTCOME:
Analyze the changes and output a JSON object:
{
  "category": "feature | bugfix | refactor | style | chore",
  "risk": "low | medium | high",
  "justification": "Evidence from the diff or code",
  "potential_issues": ["issue 1", "issue 2"],
  "decision": "create_issue | create_pr | no_action",
  "summary": "Short 1-sentence summary"
}
Output ONLY JSON.\
"""

_DRAFTER_PROMPT = """\
You are the Drafting Agent. You create structured GitHub Issues or Pull Requests.
Required Issue Template:
- Title, Problem description, Evidence, Acceptance criteria, Risk level.
Required PR Template:
- Title, Summary, Files affected, Behavior change, Test plan, Risk level.

Output a JSON object:
{
  "type": "issue | pr",
  "title": "...",
  "body": "Markdown formatted body following the template exactly",
  "files_affected": ["..."],
  "risk": "..."
}
Output ONLY JSON.\
"""

async def make_analyzer() -> AssistantAgent:
    tools = await get_mcp_tools()
    return AssistantAgent(
        name="Analyzer",
        model_client=_model_client(),
        tools=tools,
        system_message=_ANALYZER_PROMPT,
        reflect_on_tool_use=True,
    )

async def make_drafter() -> AssistantAgent:
    # Drafter might also need MCP tools to read files for context
    tools = await get_mcp_tools()
    return AssistantAgent(
        name="Drafter",
        model_client=_model_client(),
        tools=tools,
        system_message=_DRAFTER_PROMPT,
        reflect_on_tool_use=True,
    )

# Task 3 Improver omitted for brevity in initial port, can be added similarly

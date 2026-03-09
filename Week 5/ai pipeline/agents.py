"""
AutoGen AssistantAgent definitions for the Repository Agent.
Updated to fulfill specific Review, Draft, and Improve requirements.
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

import config
from tools import read_file, list_directory, get_file_stats, get_git_diff, get_git_status, get_github_issue_or_pr


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

# ── TASK 1: REVIEWER PROMPT ────────────────────────────────────

_ANALYZER_PROMPT = """\
You are the Repository Analyzer. Your goal is to review code changes and decide on actions.

You have access to Git tools. Use them to:
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

# ── TASK 2: DRAFTING PROMPT ────────────────────────────────────

_DRAFTER_PROMPT = """\
You are the Drafting Agent. You create structured GitHub Issues or Pull Requests.

Required Issue Template:
- Title
- Problem description
- Evidence (from code/diff)
- Acceptance criteria (bullet points)
- Risk level (low/medium/high)

Required PR Template:
- Title
- Summary
- Files affected
- Behavior change
- Test plan
- Risk level

You will receive analysis or instructions. Output a JSON object:
{
  "type": "issue | pr",
  "title": "...",
  "body": "Markdown formatted body following the template exactly",
  "files_affected": ["..."],
  "risk": "..."
}

Output ONLY JSON.\
"""

# ── TASK 3: IMPROVER PROMPT ────────────────────────────────────

_IMPROVER_PROMPT = """\
You are the Quality Agent. Your task is to critique and improve existing Issues or PRs.

Input: Analysis of an existing GitHub item.
Process:
1. Critique: Identify unclear/missing info, vague language, or poor criteria.
2. Propose: Provide a better, structured version.

Output a JSON object:
{
  "critique": "Detailed analysis of what is wrong/missing",
  "improvements": {
    "title": "...",
    "body": "Better, structured Markdown body"
  }
}

Output ONLY JSON.\
"""

def make_analyzer() -> AssistantAgent:
    return AssistantAgent(
        name="Analyzer",
        model_client=_model_client(),
        tools=[get_git_diff, get_git_status, read_file, list_directory],
        system_message=_ANALYZER_PROMPT,
        reflect_on_tool_use=True,
    )

def make_drafter() -> AssistantAgent:
    return AssistantAgent(
        name="Drafter",
        model_client=_model_client(),
        tools=[read_file], # Can read files to get evidence
        system_message=_DRAFTER_PROMPT,
        reflect_on_tool_use=True,
    )

def make_improver() -> AssistantAgent:
    return AssistantAgent(
        name="Improver",
        model_client=_model_client(),
        tools=[get_github_issue_or_pr, read_file],
        system_message=_IMPROVER_PROMPT,
        reflect_on_tool_use=True,
    )

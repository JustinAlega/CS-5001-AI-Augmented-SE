"""
Orchestration pipeline for the Repository Agent.
Handles Task 1 (Review), Task 2 (Draft), and Task 3 (Improve).
Implements Human-in-the-Loop for GitHub creation.
"""
import asyncio
import json
import re
from typing import Callable, Optional, Dict, Any

from agents import make_analyzer, make_drafter, make_improver

# Helper to extract JSON (reuse from previous demo)
def _extract_json(text: str) -> dict:
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try: return json.loads(m.group(1))
        except: pass
    try: return json.loads(text.strip())
    except: pass
    best, depth, start = "", 0, -1
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}" and depth > 0:
            depth -= 1
            if depth == 0:
                candidate = text[start : i + 1]
                if len(candidate) > len(best): best = candidate
    if best:
        try: return json.loads(best)
        except: pass
    return {}

async def _run_agent(agent, task: str, emit: Optional[Callable] = None) -> tuple[str, dict]:
    from autogen_agentchat.base import TaskResult
    raw_text = ""
    async for event in agent.run_stream(task=task):
        if isinstance(event, TaskResult):
            for msg in reversed(event.messages):
                if getattr(msg, "source", "") == agent.name and isinstance(getattr(msg, "content", ""), str):
                    raw_text = msg.content
                    break
        elif hasattr(event, "source") and event.source == agent.name:
            content = getattr(event, "content", "")
            if isinstance(content, list) and emit:
                for item in content:
                    if hasattr(item, "name"):
                        await emit(agent.name, f"[tool] {item.name}")
            elif isinstance(content, str) and content.strip() and emit:
                if not content.strip().startswith("{"):
                    await emit(agent.name, content.strip().split("\n")[0][:100])
    return raw_text, _extract_json(raw_text)

# ── Pipeline Tasks ────────────────────────────────────────────────────────────

async def review_changes(path: str, emit: Optional[Callable] = None):
    """TASK 1: Review Git changes."""
    analyzer = make_analyzer()
    raw, analysis = await _run_agent(analyzer, f"Analyze the git changes at: {path}", emit)
    return analysis

async def draft_from_analysis(analysis: dict, emit: Optional[Callable] = None):
    """TASK 2: Draft from Review."""
    if analysis.get("decision") == "no_action":
        return None
    
    drafter = make_drafter()
    raw, draft = await _run_agent(
        drafter, 
        f"Draft a {analysis.get('decision')} based on this analysis: {json.dumps(analysis)}", 
        emit
    )
    return draft

async def draft_from_instruction(instruction: str, emit: Optional[Callable] = None):
    """TASK 2: Draft from Instruction."""
    drafter = make_drafter()
    raw, draft = await _run_agent(drafter, f"Instruction: {instruction}", emit)
    return draft

async def improve_item(repo: str, number: int, emit: Optional[Callable] = None):
    """TASK 3: Improve Existing Issue/PR."""
    improver = make_improver()
    raw, improvement = await _run_agent(improver, f"Improve GitHub item {repo}#{number}", emit)
    return improvement

# ── Final Action with Human Approval ──────────────────────────────────────────

async def perform_github_action(draft: dict):
    """Show draft to user and ask for approval."""
    print("\n" + "═" * 60)
    print(f"  🚀  PROPOSED GITHUB {draft.get('type', 'ACTION').upper()}")
    print("═" * 60)
    print(f"TITLE: {draft.get('title')}")
    print("-" * 60)
    print(draft.get("body", "No body drafted."))
    print("-" * 60)
    
    choice = input("\nDo you want to create this on GitHub? (y/n): ").strip().lower()
    if choice == 'y':
        print("✅ Creating on GitHub... (API Mock: Success)")
        # Real implementation would call github_gateway.py API here
        return True
    else:
        print("❌ Aborted safely. No changes made.")
        return False

"""
A2A Orchestrator for the Repository Agent v2.
Uses AG2 Team/GroupChat for agent-to-agent communication.
"""
import asyncio
import json
import re
from typing import Optional, List
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.ui import Console

from agents import make_analyzer, make_drafter

def _extract_json(text_or_parts) -> dict:
    # Handle list of parts (common in newer autogen versions)
    if isinstance(text_or_parts, list):
        text = "".join([str(p.content if hasattr(p, "content") else p) for p in text_or_parts])
    else:
        text = str(text_or_parts)
    
    # Improved regex for JSON extraction
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try: return json.loads(m.group(1))
        except: pass
    try: return json.loads(text.strip())
    except: pass
    return {}

async def run_review_pipeline(repo_path: str):
    """
    Orchestrates the Review -> Draft pipeline using A2A communication.
    The Analyzer reviews changes, then the Drafter creates the issue/PR.
    """
    analyzer = await make_analyzer()
    drafter = await make_drafter()
    
    # Create the A2A Team
    team = RoundRobinGroupChat([analyzer, drafter], max_turns=2)
    
    # First Task: Review
    review_task = f"Analyze the git changes at: {repo_path}"
    print(f"\n[A2A] Starting Review for {repo_path}...")
    
    # Run the team
    result = await team.run(task=review_task)
    
    # Extract analysis from results
    analysis = {}
    for msg in result.messages:
        if msg.source == "Analyzer":
            analysis = _extract_json(msg.content)
            break
            
    if not analysis or analysis.get("decision") == "no_action":
        print("[A2A] No action required based on analysis.")
        return None
        
    # Extract draft from results
    draft = {}
    for msg in result.messages:
        if msg.source == "Drafter":
            draft = _extract_json(msg.content)
            break
            
    return draft

async def perform_github_action(draft: dict):
    """Show draft to user and ask for approval."""
    if not draft: return False
    
    print("\n" + "═" * 60)
    print(f" PROPOSED GITHUB {draft.get('type', 'ACTION').upper()}")
    print("═" * 60)
    print(f"TITLE: {draft.get('title')}")
    print("-" * 60)
    print(draft.get("body", "No body drafted."))
    print("-" * 60)
    
    choice = input("\nDo you want to create this on GitHub? (y/n): ").strip().lower()
    if choice == 'y':
        print("Creating on GitHub... (API Mock: Success via MCP server)")
        # Real implementation would call the create_issue/pr tool through MCP if needed
        return True
    else:
        print("Aborted safely. No changes made.")
        return False

"""
Code analysis tools — plain Python functions registered with AutoGen agents.
Expanded to support Git diffs and GitHub API interactions.
"""
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

_MAX_FILE_CHARS = 6_000
_MAX_DIR_ENTRIES = 60

# ── File System Tools ─────────────────────────────────────────────────────────

def read_file(path: str) -> str:
    """Read a source file and return its content (capped at 6000 characters)."""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: file not found: {path}"
        if not p.is_file():
            return f"Error: not a regular file: {path}"
        text = p.read_text(encoding="utf-8", errors="replace")
        total = len(text)
        if total > _MAX_FILE_CHARS:
            text = text[:_MAX_FILE_CHARS]
            text += f"\n\n... [truncated — {total} chars total, showing first {_MAX_FILE_CHARS}]"
        return text
    except Exception as exc:
        return f"Error: {exc}"


def list_directory(path: str) -> str:
    """List files, skipping hidden files and build artifacts."""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: directory not found: {path}"
        lines = [f"Contents of {p}:"]
        count = 0
        for item in sorted(p.iterdir()):
            if item.name.startswith(".") or item.name in ("__pycache__", "node_modules", "venv", ".git", "dist"):
                continue
            if count >= _MAX_DIR_ENTRIES:
                lines.append(f"  ... (more omitted)")
                break
            lines.append(f"  [{'DIR' if item.is_dir() else 'FILE'}] {item.name}")
            count += 1
        return "\n".join(lines)
    except Exception as exc:
        return f"Error: {exc}"


def get_file_stats(path: str) -> str:
    """Return metadata about a file."""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists(): return f"Error: not found: {path}"
        s = p.stat()
        mod = datetime.fromtimestamp(s.st_mtime).isoformat(timespec="seconds")
        return f"Path: {path}\nSize: {s.st_size} bytes\nModified: {mod}\nExtension: {p.suffix}"
    except Exception as exc:
        return f"Error: {exc}"


# ── Git Tools ────────────────────────────────────────────────────────────────

def get_git_diff(repo_path: str, base: str = "HEAD", head: Optional[str] = None) -> str:
    """Get the git diff for current changes (unstaged/staged) or a commit range."""
    try:
        cmd = ["git", "diff"]
        if head:
            cmd.extend([base, head])
        elif base != "HEAD":
            cmd.append(base)
        
        # Also include staged changes if just checking HEAD
        if not head:
            result = subprocess.run(["git", "diff", "HEAD"], cwd=repo_path, capture_output=True, text=True, check=True)
        else:
            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=True)
            
        diff = result.stdout
        if not diff.strip():
            return "No changes detected in the specified range."
        if len(diff) > 10000:
            diff = diff[:10000] + "\n\n... [diff truncated]"
        return diff
    except Exception as exc:
        return f"Error running git diff: {exc}"


def get_git_status(repo_path: str) -> str:
    """Get the current git status (branch, modified files)."""
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=repo_path, capture_output=True, text=True, check=True)
        return result.stdout if result.stdout.strip() else "Clean working directory."
    except Exception as exc:
        return f"Error running git status: {exc}"


# ── GitHub API Tools (Proxies to Backend) ────────────────────────────────────

def get_github_issue_or_pr(repo: str, number: int) -> str:
    """Fetch details of an existing Issue or PR."""
    import requests
    import config
    # Note: Simplified for the agent to use. Real token logic is in github_gateway.
    # We'll use the token from config if available or assume the environment is set up.
    url = f"https://api.github.com/repos/{repo}/issues/{number}"
    headers = {"Accept": "application/vnd.github+json"}
    if config.GITHUB_TOKEN:
        headers["Authorization"] = f"token {config.GITHUB_TOKEN}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return f"TITLE: {data.get('title')}\nBODY:\n{data.get('body')}\nSTATE: {data.get('state')}"
    except Exception as exc:
        return f"Error fetching GitHub item: {exc}"

def create_issue(repo: str, title: str, body: str) -> str:
    """Draft an issue. NOTE: In this agent, this ONLY returns the intent. 
    The Pipeline handles the actual POST after human approval."""
    return f"DRAFT_ISSUE: {repo} | {title}\n{body}"

def create_pr(repo: str, title: str, body: str, head: str, base: str = "main") -> str:
    """Draft a PR. NOTE: In this agent, this ONLY returns the intent.
    The Pipeline handles the actual POST after human approval."""
    return f"DRAFT_PR: {repo} | {title} | {head}->{base}\n{body}"

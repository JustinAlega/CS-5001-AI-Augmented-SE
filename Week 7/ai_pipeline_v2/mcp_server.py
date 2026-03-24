import os
import subprocess
from pathlib import Path
from typing import Optional, List
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("RepositoryAgentTools")

_MAX_FILE_CHARS = 6000
_MAX_DIR_ENTRIES = 60

# --- File System Tools ---

@mcp.tool()
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

@mcp.tool()
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

# --- Git Tools ---

@mcp.tool()
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
            # result = subprocess.run(["git", "diff", "HEAD"], cwd=repo_path, capture_output=True, text=True, check=True)
            # Use a more robust check for both staged and unstaged
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

@mcp.tool()
def get_git_status(repo_path: str) -> str:
    """Get the current git status (branch, modified files)."""
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=repo_path, capture_output=True, text=True, check=True)
        return result.stdout if result.stdout.strip() else "Clean working directory."
    except Exception as exc:
        return f"Error running git status: {exc}"

# --- GitHub API Tools ---

@mcp.tool()
def get_github_issue_or_pr(repo: str, number: int, token: Optional[str] = None) -> str:
    """Fetch details of an existing Issue or PR."""
    import requests
    url = f"https://api.github.com/repos/{repo}/issues/{number}"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return f"TITLE: {data.get('title')}\nBODY:\n{data.get('body')}\nSTATE: {data.get('state')}"
    except Exception as exc:
        return f"Error fetching GitHub item: {exc}"

if __name__ == "__main__":
    mcp.run()

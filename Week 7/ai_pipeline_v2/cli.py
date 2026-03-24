"""
Terminal interface for the Week 7 Repository Agent (MCP + A2A).
"""
import asyncio
import click
from a2a_orchestrator import run_review_pipeline, perform_github_action

@click.group()
def cli():
    """Week 7 repository agent with MCP and A2A."""
    pass

@cli.command()
@click.argument('path')
def review(path):
    """Analyze a local git repo and draft GitHub items."""
    async def main():
        draft = await run_review_pipeline(path)
        if draft:
            await perform_github_action(draft)
    
    asyncio.run(main())

if __name__ == "__main__":
    cli()

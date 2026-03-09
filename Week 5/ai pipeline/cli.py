"""
CLI interface for the Repository Agent.
"""
import asyncio
import click
from rich.console import Console
from rich.panel import Panel

import pipeline

console = Console()

async def _emit(agent: str, msg: str):
    console.print(f"  [bold cyan]{agent}[/]: [dim]{msg}[/]")

@click.group()
def cli():
    """Repository AI Agent — Review, Draft, Improve."""

@cli.command()
@click.argument("path", default=".")
def review(path):
    """Task 1: Review git changes and decide on actions."""
    console.print(Panel(f"Analyzing repository at: [bold]{path}[/]", title="Review Mode"))
    
    async def run():
        analysis = await pipeline.review_changes(path, emit=_emit)
        console.print("\n[bold]Analysis Result:[/]")
        console.print(f"  Category: {analysis.get('category')}")
        console.print(f"  Risk:     {analysis.get('risk')}")
        console.print(f"  Decision: {analysis.get('decision')}")
        console.print(f"  Summary:  {analysis.get('summary')}")
        
        if analysis.get("decision") != "no_action":
            draft = await pipeline.draft_from_analysis(analysis, emit=_emit)
            await pipeline.perform_github_action(draft)
            
    asyncio.run(run())

@cli.command()
@click.argument("instruction")
def draft(instruction):
    """Task 2: Draft an issue or PR from explicit instruction."""
    console.print(Panel(f"Instruction: [italic]\"{instruction}\"[/]", title="Draft Mode"))
    
    async def run():
        draft = await pipeline.draft_from_instruction(instruction, emit=_emit)
        await pipeline.perform_github_action(draft)
        
    asyncio.run(run())

@cli.command()
@click.argument("repo")
@click.argument("number", type=int)
def improve(repo, number):
    """Task 3: Critique and improve an existing Issue or PR."""
    console.print(Panel(f"Improving: [bold]{repo}#{number}[/]", title="Improve Mode"))
    
    async def run():
        improvement = await pipeline.improve_item(repo, number, emit=_emit)
        console.print("\n[bold]Critique:[/]")
        console.print(improvement.get("critique"))
        
        console.print("\n[bold]Proposed Improvement:[/]")
        await pipeline.perform_github_action({
            "type": "IMPROVEMENT",
            "title": improvement.get("improvements", {}).get("title"),
            "body": improvement.get("improvements", {}).get("body")
        })
        
    asyncio.run(run())

if __name__ == "__main__":
    cli()

#!/usr/bin/env python3
"""
DevOps Automation Assistant
AI-powered CLI tool for analyzing and optimizing CI/CD pipelines.
"""
import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from dotenv import load_dotenv
import os
from pathlib import Path

from workflow_analyzer import WorkflowAnalyzer
from ai_agent import DevOpsAIAgent

# Load environment variables
load_dotenv()

console = Console()


@click.group()
def cli():
    """DevOps Automation Assistant - AI-powered CI/CD optimization tool."""
    pass


@cli.command()
@click.argument('workflow_file', type=click.Path(exists=True))
@click.option('--detailed', is_flag=True, help='Show detailed analysis')
def analyze(workflow_file, detailed):
    """Analyze a GitHub Actions workflow file."""
    console.print("\n[bold cyan]Analyzing GitHub Actions Workflow...[/bold cyan]\n")

    try:
        # Parse and analyze workflow
        analyzer = WorkflowAnalyzer(workflow_path=workflow_file)
        analysis = analyzer.get_full_analysis()

        # Display basic info
        basic_info = analysis['basic_info']
        console.print(Panel(
            f"[bold]Name:[/bold] {basic_info['name']}\n"
            f"[bold]Jobs:[/bold] {basic_info['job_count']}\n"
            f"[bold]Triggers:[/bold] {', '.join(basic_info['triggers'])}",
            title="Workflow Info",
            border_style="cyan"
        ))

        # Show optimization opportunities
        opportunities = analysis['optimization_opportunities']
        if opportunities:
            console.print("\n[bold yellow]Optimization Opportunities:[/bold yellow]\n")
            for opp in opportunities:
                console.print(f"  • [bold]{opp['type'].title()}[/bold] ({opp['severity']} priority)")
                console.print(f"    Job: {opp['job']}")
                console.print(f"    {opp['description']}\n")
        else:
            console.print("\n[bold green]No obvious optimization opportunities detected.[/bold green]\n")

        # Get AI recommendations
        if detailed:
            console.print("\n[bold cyan]Getting AI recommendations...[/bold cyan]\n")
            agent = DevOpsAIAgent()
            recommendations = agent.analyze_workflow(analysis)

            console.print(Panel(
                Markdown(recommendations),
                title="AI Recommendations",
                border_style="green"
            ))

        console.print("\n[bold green]✓ Analysis complete![/bold green]\n")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}\n")
        raise click.Abort()


@cli.command()
@click.argument('workflow_file', type=click.Path(exists=True))
@click.option('--context', default='', help='Additional context about your project')
def suggest(workflow_file, context):
    """Get AI-powered improvement suggestions with code examples."""
    console.print("\n[bold cyan]Generating improvement suggestions...[/bold cyan]\n")

    try:
        # Read workflow content
        with open(workflow_file, 'r') as f:
            workflow_content = f.read()

        # Display current workflow
        syntax = Syntax(workflow_content, "yaml", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Current Workflow", border_style="blue"))

        # Get AI suggestions
        agent = DevOpsAIAgent()
        suggestions = agent.suggest_improvements(workflow_content, context)

        console.print("\n")
        console.print(Panel(
            Markdown(suggestions),
            title="AI Improvement Suggestions",
            border_style="green"
        ))

        console.print("\n[bold green]✓ Suggestions generated![/bold green]\n")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}\n")
        raise click.Abort()


@cli.command()
@click.argument('workflow_file', type=click.Path(exists=True))
@click.argument('error_log_file', type=click.Path(exists=True))
def troubleshoot(workflow_file, error_log_file):
    """Troubleshoot a failed build using error logs."""
    console.print("\n[bold cyan]Troubleshooting build failure...[/bold cyan]\n")

    try:
        # Analyze workflow
        analyzer = WorkflowAnalyzer(workflow_path=workflow_file)
        analysis = analyzer.get_full_analysis()

        # Read error logs
        with open(error_log_file, 'r') as f:
            error_logs = f.read()

        # Display error logs
        console.print(Panel(
            error_logs[:1000] + ("..." if len(error_logs) > 1000 else ""),
            title="Error Logs (excerpt)",
            border_style="red"
        ))

        # Get AI troubleshooting
        console.print("\n[bold cyan]Analyzing errors...[/bold cyan]\n")
        agent = DevOpsAIAgent()
        diagnosis = agent.troubleshoot_failure(analysis, error_logs)

        console.print(Panel(
            Markdown(diagnosis),
            title="Troubleshooting Recommendations",
            border_style="yellow"
        ))

        console.print("\n[bold green]✓ Troubleshooting complete![/bold green]\n")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}\n")
        raise click.Abort()


@cli.command()
def examples():
    """Show example workflows and common patterns."""
    console.print("\n[bold cyan]Common GitHub Actions Patterns[/bold cyan]\n")

    examples = {
        "Basic CI with Caching": """
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
""",
        "Matrix Strategy for Multi-Version Testing": """
name: Test Multiple Versions
on: [push]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest
"""
    }

    for title, code in examples.items():
        syntax = Syntax(code.strip(), "yaml", theme="monokai")
        console.print(Panel(syntax, title=title, border_style="green"))
        console.print()


if __name__ == '__main__':
    cli()

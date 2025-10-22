# DevOps Automation Assistant

AI-powered tool that analyzes CI/CD pipelines, suggests optimizations, and helps troubleshoot build failures.

## Features

- **GitHub Actions Workflow Analysis**: Parse and analyze GitHub Actions YAML workflows
- **AI-Powered Optimization**: Get intelligent suggestions for improving pipeline efficiency
- **Build Failure Troubleshooting**: Diagnose and get recommendations for fixing failed builds
- **Performance Insights**: Identify bottlenecks and optimization opportunities

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with your API keys:

```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
GITHUB_TOKEN=your_github_token_here  # Optional, for fetching workflow runs
```

## Usage

```bash
# Analyze a GitHub Actions workflow file
python devops_assistant.py analyze workflow.yml

# Get detailed AI-powered analysis
python devops_assistant.py analyze workflow.yml --detailed

# Get improvement suggestions with code examples
python devops_assistant.py suggest workflow.yml --context "Your project description"

# Troubleshoot a failed build
python devops_assistant.py troubleshoot workflow.yml error.log

# View example patterns
python devops_assistant.py examples
```

## Architecture

- `devops_assistant.py`: Main CLI interface
- `workflow_analyzer.py`: GitHub Actions workflow parser and analyzer
- `ai_agent.py`: Claude AI agent for optimization suggestions
- `troubleshooter.py`: Build failure diagnosis and recommendations

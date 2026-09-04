"""
AI Agent for DevOps Optimization
Uses Claude to provide intelligent optimization suggestions for CI/CD pipelines.
"""
from anthropic import Anthropic
import os
import json
from typing import Dict, Any, List


class DevOpsAIAgent:
    """AI agent for analyzing workflows and providing optimization recommendations."""

    def __init__(self, api_key: str = None):
        """Initialize AI agent with Anthropic API key."""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")
        self.client = Anthropic(api_key=self.api_key)

    def analyze_workflow(self, workflow_analysis: Dict[str, Any]) -> str:
        """
        Analyze a workflow and provide optimization recommendations.

        Args:
            workflow_analysis: Full workflow analysis from WorkflowAnalyzer

        Returns:
            AI-generated optimization recommendations
        """
        prompt = self._build_analysis_prompt(workflow_analysis)

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def troubleshoot_failure(self, workflow_analysis: Dict[str, Any],
                           error_logs: str) -> str:
        """
        Troubleshoot a failed build and provide recommendations.

        Args:
            workflow_analysis: Full workflow analysis from WorkflowAnalyzer
            error_logs: Build failure logs

        Returns:
            AI-generated troubleshooting recommendations
        """
        prompt = self._build_troubleshooting_prompt(workflow_analysis, error_logs)

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def suggest_improvements(self, workflow_content: str,
                           context: str = "") -> str:
        """
        Suggest specific improvements to workflow YAML.

        Args:
            workflow_content: Raw workflow YAML content
            context: Additional context about the project

        Returns:
            AI-generated improvement suggestions with code examples
        """
        prompt = f"""You are a DevOps expert analyzing a GitHub Actions workflow.

Context: {context}

Current Workflow:
```yaml
{workflow_content}
```

Please provide:
1. Specific optimization suggestions
2. Code examples for improvements
3. Explanation of why each change would help
4. Prioritized recommendations (high/medium/low impact)

Focus on:
- Build speed improvements
- Resource optimization
- Better caching strategies
- Parallelization opportunities
- Security best practices
- Error handling improvements
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=3000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def _build_analysis_prompt(self, workflow_analysis: Dict[str, Any]) -> str:
        """Build prompt for workflow analysis."""
        basic_info = workflow_analysis['basic_info']
        jobs = workflow_analysis['jobs']
        opportunities = workflow_analysis['optimization_opportunities']

        return f"""You are a DevOps expert analyzing a GitHub Actions workflow.

Workflow: {basic_info['name']}
Jobs: {basic_info['job_count']}
Triggers: {', '.join(basic_info['triggers'])}

Job Details:
{json.dumps(jobs, indent=2)}

Detected Optimization Opportunities:
{json.dumps(opportunities, indent=2)}

Please provide:
1. An overall assessment of the workflow
2. Specific optimization recommendations with examples
3. Best practices that could be applied
4. Potential issues or risks
5. Priority order for implementing changes

Format your response in clear sections with actionable recommendations.
"""

    def _build_troubleshooting_prompt(self, workflow_analysis: Dict[str, Any],
                                     error_logs: str) -> str:
        """Build prompt for troubleshooting failed builds."""
        basic_info = workflow_analysis['basic_info']

        return f"""You are a DevOps expert troubleshooting a failed GitHub Actions build.

Workflow: {basic_info['name']}

Error Logs:
```
{error_logs}
```

Workflow Configuration:
{json.dumps(workflow_analysis['jobs'], indent=2)}

Please analyze the error and provide:
1. Root cause analysis
2. Step-by-step troubleshooting guide
3. Specific fixes with code examples
4. Prevention strategies for the future
5. Related issues to check

Be specific and actionable in your recommendations.
"""

"""
GitHub Actions Workflow Analyzer
Parses and analyzes GitHub Actions YAML workflows for optimization opportunities.
"""
import yaml
from typing import Dict, List, Any
from pathlib import Path


class WorkflowAnalyzer:
    """Analyzes GitHub Actions workflow files."""

    def __init__(self, workflow_path: str = None, workflow_content: str = None):
        """
        Initialize analyzer with either a file path or workflow content.

        Args:
            workflow_path: Path to GitHub Actions workflow YAML file
            workflow_content: Raw YAML content as string
        """
        if workflow_path:
            with open(workflow_path, 'r') as f:
                self.workflow = yaml.safe_load(f)
            self.workflow_path = workflow_path
        elif workflow_content:
            self.workflow = yaml.safe_load(workflow_content)
            self.workflow_path = None
        else:
            raise ValueError("Either workflow_path or workflow_content must be provided")

    def get_basic_info(self) -> Dict[str, Any]:
        """Extract basic workflow information."""
        return {
            'name': self.workflow.get('name', 'Unnamed Workflow'),
            'triggers': list(self.workflow.get('on', {}).keys()),
            'jobs': list(self.workflow.get('jobs', {}).keys()),
            'job_count': len(self.workflow.get('jobs', {}))
        }

    def analyze_jobs(self) -> List[Dict[str, Any]]:
        """Analyze all jobs in the workflow."""
        jobs = self.workflow.get('jobs', {})
        job_analysis = []

        for job_name, job_config in jobs.items():
            analysis = {
                'name': job_name,
                'runs_on': job_config.get('runs-on', 'unknown'),
                'steps_count': len(job_config.get('steps', [])),
                'dependencies': job_config.get('needs', []),
                'strategy': job_config.get('strategy', {}),
                'timeout': job_config.get('timeout-minutes', None),
                'steps': self._analyze_steps(job_config.get('steps', []))
            }
            job_analysis.append(analysis)

        return job_analysis

    def _analyze_steps(self, steps: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze individual steps within a job."""
        step_analysis = []

        for i, step in enumerate(steps):
            step_info = {
                'index': i,
                'name': step.get('name', f'Step {i+1}'),
                'uses': step.get('uses', None),
                'run': step.get('run', None),
                'with': step.get('with', {}),
                'env': step.get('env', {}),
                'if': step.get('if', None)
            }
            step_analysis.append(step_info)

        return step_analysis

    def identify_optimization_opportunities(self) -> List[Dict[str, str]]:
        """Identify potential optimization opportunities."""
        opportunities = []

        # Check for caching
        jobs = self.workflow.get('jobs', {})
        for job_name, job_config in jobs.items():
            steps = job_config.get('steps', [])

            # Check if there's dependency installation without caching
            has_npm_install = any('npm install' in step.get('run', '') for step in steps)
            has_pip_install = any('pip install' in step.get('run', '') for step in steps)
            has_cache = any('actions/cache' in step.get('uses', '') for step in steps)

            if (has_npm_install or has_pip_install) and not has_cache:
                opportunities.append({
                    'type': 'caching',
                    'job': job_name,
                    'severity': 'medium',
                    'description': 'Consider adding dependency caching to speed up builds'
                })

            # Check for missing parallelization
            if not job_config.get('strategy'):
                if any('test' in step.get('name', '').lower() for step in steps):
                    opportunities.append({
                        'type': 'parallelization',
                        'job': job_name,
                        'severity': 'low',
                        'description': 'Consider using matrix strategy to run tests in parallel'
                    })

            # Check for missing timeout
            if not job_config.get('timeout-minutes'):
                opportunities.append({
                    'type': 'timeout',
                    'job': job_name,
                    'severity': 'low',
                    'description': 'Consider adding timeout-minutes to prevent hanging jobs'
                })

        return opportunities

    def get_full_analysis(self) -> Dict[str, Any]:
        """Get complete workflow analysis."""
        return {
            'basic_info': self.get_basic_info(),
            'jobs': self.analyze_jobs(),
            'optimization_opportunities': self.identify_optimization_opportunities()
        }

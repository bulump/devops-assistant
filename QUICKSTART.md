# DevOps Assistant Quick Start

## Installation

```bash
cd ~/git/devops-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Basic Usage (No API Key Required)

### 1. Analyze a Workflow
```bash
python devops_assistant.py analyze example_workflow.yml
```

**Output:**
- Basic workflow information
- Job count and triggers
- Optimization opportunities (caching, parallelization, timeouts)

### 2. View Example Patterns
```bash
python devops_assistant.py examples
```

**Output:**
- Common GitHub Actions patterns
- Best practices for CI/CD
- Ready-to-use workflow templates

## Advanced Usage (Requires API Key)

### Setup
```bash
# Copy example and add your API key
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

### 3. Detailed AI Analysis
```bash
python devops_assistant.py analyze workflow.yml --detailed
```

**Output:**
- Everything from basic analysis
- AI-generated optimization recommendations
- Best practices specific to your workflow
- Priority-ordered action items

### 4. Get Improvement Suggestions
```bash
python devops_assistant.py suggest workflow.yml --context "Flask web app with pytest"
```

**Output:**
- Specific code improvements
- Example YAML snippets
- Explanation of why each change helps
- High/medium/low priority recommendations

### 5. Troubleshoot Build Failures
```bash
python devops_assistant.py troubleshoot workflow.yml error.log
```

**Output:**
- Root cause analysis
- Step-by-step troubleshooting guide
- Specific fixes with code examples
- Prevention strategies

## Real-World Examples

### Analyze Your Own Workflow
```bash
# For any GitHub repo with Actions
python devops_assistant.py analyze ~/.../my-project/.github/workflows/ci.yml
```

### Example: Database Security Scanner
```bash
python devops_assistant.py analyze ~/git/db-security-scanner/.github/workflows/test.yml
```

## What It Detects

**Automatic Detection:**
- ❌ Missing dependency caching → Slower builds
- ❌ No parallelization → Inefficient testing
- ❌ Missing timeouts → Hanging jobs
- ❌ Outdated actions → Security risks
- ❌ Inefficient workflows → Wasted CI minutes

**AI-Powered Insights:**
- Performance bottlenecks
- Security improvements
- Cost optimization
- Best practices alignment

## Demo Script

Run the interactive demo:
```bash
./demo.sh
```

## Tips

1. **Start with basic analysis** - No API key needed, instant results
2. **Use examples command** - Great for learning GitHub Actions patterns
3. **Add context** - When using `suggest`, provide project details for better recommendations
4. **Save error logs** - Copy GitHub Actions error output to a file for troubleshooting
5. **Iterate** - Run analysis after making changes to verify improvements

## File Structure

```
devops-assistant/
├── devops_assistant.py      # Main CLI (Click-based)
├── workflow_analyzer.py     # YAML parser & rule engine
├── ai_agent.py              # Claude AI integration
├── example_workflow.yml     # Sample workflow for testing
├── sample_error.log         # Example error log
└── requirements.txt         # Python dependencies
```

## Common Workflow Issues Detected

| Issue | Severity | Impact |
|-------|----------|--------|
| No dependency caching | Medium | 2-5x slower builds |
| Missing matrix strategy | Low | Missed compatibility issues |
| No job timeout | Low | Hanging jobs waste resources |
| Inefficient step order | Medium | Slow feedback loop |
| No failure notifications | Low | Delayed response to issues |

## Next Steps

1. Analyze your current workflows
2. Apply suggested optimizations
3. Re-run analysis to verify improvements
4. Share findings with your team
5. Set up regular workflow audits

#!/bin/bash
# Demo script for DevOps Automation Assistant

set -e

echo "============================================"
echo "DevOps Automation Assistant Demo"
echo "============================================"
echo

# Activate virtual environment
source venv/bin/activate

echo "1. Showing example patterns:"
echo "-------------------------------------------"
python devops_assistant.py examples
echo
read -p "Press Enter to continue..."

echo
echo "2. Analyzing example workflow:"
echo "-------------------------------------------"
python devops_assistant.py analyze example_workflow.yml
echo
read -p "Press Enter to continue..."

echo
echo "3. Analyzing production workflow from db-security-scanner:"
echo "-------------------------------------------"
python devops_assistant.py analyze /Users/cbielins/git/db-security-scanner/.github/workflows/test.yml
echo
read -p "Press Enter to continue..."

echo
echo "============================================"
echo "Demo Complete!"
echo "============================================"
echo
echo "To use AI-powered features (--detailed, suggest, troubleshoot):"
echo "1. Copy .env.example to .env"
echo "2. Add your ANTHROPIC_API_KEY"
echo "3. Run: python devops_assistant.py analyze example_workflow.yml --detailed"
echo

#!/bin/bash
# Run tests for each module and generate reports for n8n workflow

set -e

cd /root/automatos-testing

# Ensure reports directory exists
mkdir -p /root/reports

# Environment variables are loaded from .env file automatically by run_tests.py

# Define module mappings
declare -A modules=(
    ["agents"]="agents"
    ["workflows"]="workflow"
    ["context"]="context"
    ["knowledge"]="memory"
    ["playbooks"]="multi"
    ["settings"]="security"
    ["analytics"]="performance"
    ["dashboard"]="smoke"
    ["routers"]="routers"
    ["documents"]="documents"
    ["field_theory"]="field"
    ["evaluation"]="evaluation"
    ["context_policy"]="context_policy"
    ["code_graph"]="code_graph"
    ["playbooks_api"]="playbooks"
    ["patterns"]="patterns"
)

# Run tests for a specific module
run_module_test() {
    local module_name=$1
    local filter=${modules[$module_name]:-$module_name}
    
    echo "Running tests for $module_name (filter: $filter)..."
    
    # Run the tests (ignore exit code)
    python3 run_tests.py --filter "$filter" --reports || true
    
    # Find the latest report
    REPORT=$(ls -1t reports/test_report_*.json 2>/dev/null | head -1)
    if [ -n "$REPORT" ]; then
        cp "$REPORT" "/root/reports/${module_name}.json"
        echo "✓ Generated /root/reports/${module_name}.json"
        return 0
    else
        echo '{"ok":false,"error":"no report generated"}' > "/root/reports/${module_name}.json"
        echo "✗ No report generated for $module_name"
        return 1
    fi
}

# If called with argument, run specific module
if [ $# -eq 1 ]; then
    run_module_test "$1"
else
    # Run all modules
    for module in "${!modules[@]}"; do
        run_module_test "$module"
    done
fi

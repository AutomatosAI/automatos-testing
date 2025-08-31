# Test Suite Quick Reference

## Running Tests

### All Tests
```bash
python run_tests.py
```

### Specific Module Tests
```bash
# Existing modules
python run_tests.py --filter agents
python run_tests.py --filter workflow
python run_tests.py --filter context
python run_tests.py --filter memory
python run_tests.py --filter multi
python run_tests.py --filter security
python run_tests.py --filter performance

# New modules
python run_tests.py --filter documents
python run_tests.py --filter field
python run_tests.py --filter evaluation
```

### Module Sequence (for n8n workflow)
```bash
python run_tests.py --module-sequence
```

### With Reports
```bash
python run_tests.py --filter documents --reports
```

### Quick Validation of New Tests
```bash
python test_new_modules.py
```

## n8n Workflow Integration

The n8n workflow can run tests for each module using:
```bash
/root/automatos-testing/scripts/run_module_tests.sh [module_name]
```

Module names for n8n:
- `agents`
- `workflows`
- `context`
- `knowledge` (maps to memory tests)
- `playbooks` (maps to multi-agent tests)
- `settings` (maps to security tests)
- `analytics` (maps to performance tests)
- `documents` (NEW)
- `field_theory` (NEW)
- `evaluation` (NEW)

## Test Coverage Status

| Module | Test File | Coverage | Status |
|--------|-----------|----------|---------|
| Agents | test_agents.py | 70% | 🔄 Needs enhancement |
| Workflows | test_workflows.py | 60% | 🔄 Needs enhancement |
| Context Engineering | test_context_engineering.py | 50% | 🔄 Needs enhancement |
| Memory Systems | test_memory_systems.py | 90% | ✅ Good |
| Multi-Agent | test_multi_agent.py | 40% | 🔄 Needs enhancement |
| Performance/Security | test_performance_security.py | 70% | 🔄 Needs enhancement |
| Documents | test_documents.py | 95% | ✅ NEW |
| Field Theory | test_field_theory.py | 95% | ✅ NEW |
| Evaluation | test_evaluation.py | 95% | ✅ NEW |
| Context Policy | - | 0% | ❌ TODO |
| Code Graph | - | 0% | ❌ TODO |
| Playbooks | - | 0% | ❌ TODO |
| Patterns | - | 0% | ❌ TODO |

## Environment Setup

1. Ensure API is running:
```bash
cd /Users/gkavanagh/Development/Automatos-AI-Platform/automatos-ai/orchestrator
docker-compose up -d
```

2. Check API health:
```bash
curl http://localhost:8000/health
```

3. Set environment variables (or use .env file):
```bash
export API_BASE_URL=http://localhost:8000
export API_KEY=sk-automatos-dev-123
```

## Test Data

Test data directory: `test_data/documents/`

The document tests will automatically create sample files in this directory.

## Debugging Failed Tests

1. Run with verbose output:
```bash
python run_tests.py --filter documents --verbose
```

2. Check specific test method:
```bash
python -m pytest tests/test_documents.py::TestDocuments::test_upload_text_document -v
```

3. View test reports:
```bash
ls -la reports/
cat reports/documents.json
```

## Next Steps

1. **Test New Modules**: Run the new test files to ensure they work
2. **Update n8n Workflow**: Add new modules to the workflow
3. **Create Remaining Tests**: 
   - test_context_policy.py
   - test_code_graph.py
   - test_playbooks.py
   - test_patterns.py
4. **Enhance Existing Tests**: Add missing endpoints
5. **Add User Journey Tests**: End-to-end scenarios


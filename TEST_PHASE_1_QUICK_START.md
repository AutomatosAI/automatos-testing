# Test Phase 1 - Quick Start Guide

## 🚀 Quick Validation (5 minutes)

```bash
# 1. Navigate to testing directory
cd /Users/gkavanagh/Development/Automatos-AI-Platform/automatos-testing

# 2. Run quick validation
python test_phase2_modules.py

# 3. Check results
cat reports/phase2_validation_summary.json
```

## 🧪 Individual Module Tests (20 minutes)

```bash
# Test each new module
python run_tests.py --filter context_policy --reports --verbose
python run_tests.py --filter code_graph --reports --verbose  
python run_tests.py --filter playbooks --reports --verbose
python run_tests.py --filter patterns --reports --verbose
```

## 📊 Full Test Suite (30-45 minutes)

```bash
# Run all tests with comprehensive reporting
python run_tests.py --module-sequence --json reports/full_test_run.json --reports

# View HTML report
open reports/test_report_*.html
```

## 🔍 Check Coverage

```bash
# View current coverage status
cat TEST_COVERAGE_PROGRESS_REPORT.md | grep "Overall Progress"

# Check specific module results
ls -la reports/phase2_*.json
```

## 🐛 Debugging Failures

```bash
# If tests fail, check API health
curl http://localhost:8000/health

# Run failing test in isolation
python -m pytest tests/test_context_policy.py::test_create_policy -v

# Check API logs
docker logs automatos-ai-orchestrator-1
```

## 📈 n8n Workflow

```bash
# Run via n8n module script
./scripts/run_module_tests.sh context_policy
./scripts/run_module_tests.sh code_graph
./scripts/run_module_tests.sh playbooks_api
./scripts/run_module_tests.sh patterns
```

## ✅ Success Criteria

- All 4 new modules show 90%+ test pass rate
- No critical API errors
- Response times < 5 seconds per endpoint
- JSON reports generated successfully

## 📝 Next Steps After Phase 1

1. Review failing tests
2. Update API implementations if needed  
3. Re-run failed tests
4. Generate final coverage report
5. Proceed to Phase 3 (remaining enhancements)

---

**Estimated Time**: 30-60 minutes for complete Phase 1 execution


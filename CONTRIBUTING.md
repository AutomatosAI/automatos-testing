# Contributing to Automatos AI Testing Suite

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone git@github.com:yourusername/automatos-testing.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests to ensure everything works: `python3 run_all_tests.py`

## Adding New Tests

### Test Structure
- Place new tests in appropriate `phase*` directories
- Use the `ComprehensiveAPITester` utility class
- Follow existing naming conventions: `comprehensive_*_test.py`

### Test Requirements
- All tests must use real API calls (no mocking)
- Include proper error handling and logging
- Update configuration files if new test data needed
- Maintain 70% success threshold logic

### Code Style
- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Include docstrings for all classes and methods
- Add comments for complex logic

## Reporting Issues

### Bug Reports
Include the following information:
- Python version and OS
- Complete error messages and stack traces
- Steps to reproduce the issue
- Expected vs actual behavior
- Relevant log files

### Feature Requests
- Describe the new testing capability needed
- Explain why it would be valuable
- Suggest implementation approach if possible

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/new-test`
2. Make your changes and test thoroughly
3. Update documentation if needed
4. Commit with clear, descriptive messages
5. Push to your fork and create a pull request
6. Ensure all existing tests still pass

## Testing Your Changes

Before submitting:
```bash
# Run all tests
cd testing_suites/comprehensive_5phase
python3 run_all_tests.py

# Run individual phases
python3 phase1_agent_management/scripts/comprehensive_agent_test.py
python3 phase2_workflow_orchestration/scripts/comprehensive_workflow_test.py
# ... etc
```

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and improve
- Follow open source best practices
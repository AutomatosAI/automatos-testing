# Test Data Requirements for Automatos AI Platform

## Executive Summary

Your testing infrastructure has **basic test data setup** but needs **enhancements** for comprehensive testing. Here's what you have and what you need.

## Current Test Data Infrastructure ✅

### 1. **Database Seed Data** (init_db.sql)
- ✅ Basic seed data for agents, workflows, and documents
- ✅ Auto-loaded when PostgreSQL test container starts
- ✅ Test schemas: `test_data`, `test_results`, `test_history`

### 2. **Data Generators** (utils/data_generators.py)
- ✅ Agent data generator (5 agent types)
- ✅ Skill data generator (4 categories)
- ✅ Workflow data generator (5 workflow types)
- ✅ Random data utilities (emails, strings, timestamps)

### 3. **Mock Data Generator** (n8n/mock-data-generator.js)
- ✅ Comprehensive failure scenarios
- ✅ System log generation
- ✅ Performance metrics simulation
- ✅ Error pattern generation

### 4. **Dynamic Test Data**
- ✅ Tests create their own data during execution
- ✅ Cleanup after test completion
- ✅ Unique naming to avoid conflicts

## What's Missing for Proper Testing 🚨

### 1. **Comprehensive Seed Data**
```sql
-- Need more diverse test data:
-- • 10+ agents with different configurations
-- • 20+ workflows with complex steps
-- • 50+ documents for context testing
-- • Neural field test data
-- • Multi-tenant test data
```

### 2. **Test Data Files**
```bash
test_data/
├── documents/  # Currently EMPTY - needs sample files
│   ├── technical_docs/
│   ├── code_samples/
│   └── context_samples/
├── agents/     # Missing - need agent configs
├── workflows/  # Missing - need workflow definitions
└── neural_fields/  # Missing - need field data
```

### 3. **Performance Test Data**
- Large datasets for load testing
- Concurrent user simulations
- Stress test scenarios
- Memory pressure test data

### 4. **Edge Case Data**
- Unicode and special characters
- Very large documents (>10MB)
- Malformed JSON structures
- SQL injection attempts
- XSS payloads

## Quick Setup Guide 🚀

### Step 1: Start Test Database
```bash
cd /Users/gkavanagh/Development/Automatos-AI-Platform/automatos-testing
docker-compose up -d postgres-test redis-test
```

### Step 2: Verify Seed Data
```bash
docker exec -it automotas-test-postgres psql -U postgres -d automotas_test_db -c "SELECT * FROM test_data.sample_agents;"
```

### Step 3: Create Additional Test Data
```python
# create_test_data.py
from utils.data_generators import TestData

# Create 10 diverse agents
for i in range(10):
    agent = TestData.Agent.create_agent_data()
    # Save to database or file
    
# Create complex workflows
for workflow_type in TestData.Workflow.WORKFLOW_TYPES:
    workflow = TestData.Workflow.create_workflow_data(
        workflow_type=workflow_type
    )
    # Save to database or file
```

## Recommended Test Data Setup ⭐

### 1. **Create Test Data Directory Structure**
```bash
mkdir -p test_data/{documents,agents,workflows,neural_fields,performance}
mkdir -p test_data/documents/{technical_docs,code_samples,context_samples}
```

### 2. **Generate Sample Documents**
```python
# generate_documents.py
import json
from pathlib import Path

# Technical documentation samples
tech_docs = [
    {
        "title": "Neural Field Implementation Guide",
        "content": "Comprehensive guide to implementing neural fields...",
        "metadata": {"type": "technical", "category": "neural_fields"}
    },
    # Add 10+ more documents
]

for i, doc in enumerate(tech_docs):
    Path(f"test_data/documents/technical_docs/doc_{i}.json").write_text(
        json.dumps(doc, indent=2)
    )
```

### 3. **Create Agent Configurations**
```json
// test_data/agents/advanced_agents.json
{
  "agents": [
    {
      "name": "NeuralFieldProcessor",
      "type": "neural_field_specialist",
      "configuration": {
        "field_types": ["context_resonance", "collective_memory"],
        "processing_mode": "parallel",
        "memory_limit": "2GB"
      }
    },
    // Add more specialized agents
  ]
}
```

### 4. **Performance Test Data Generator**
```python
# generate_performance_data.py
def generate_large_dataset(size_mb=100):
    """Generate large dataset for performance testing"""
    data = []
    target_size = size_mb * 1024 * 1024  # Convert to bytes
    current_size = 0
    
    while current_size < target_size:
        doc = {
            "id": f"perf_test_{len(data)}",
            "content": "x" * 1000,  # 1KB per document
            "embeddings": [0.1] * 768,  # Simulated embeddings
            "metadata": {"test": True}
        }
        data.append(doc)
        current_size += len(json.dumps(doc))
    
    return data
```

## Integration with n8n Workflow 🔄

Your n8n workflow can now:
1. **Load test data** before running tests
2. **Generate dynamic data** during test execution
3. **Clean up** after test completion

Add this node to your workflow:
```javascript
// n8n Code Node: Load Test Data
const fs = require('fs');
const testData = {
  agents: JSON.parse(fs.readFileSync('/test_data/agents/agents.json')),
  workflows: JSON.parse(fs.readFileSync('/test_data/workflows/workflows.json')),
  documents: JSON.parse(fs.readFileSync('/test_data/documents/docs.json'))
};

// Make data available for tests
return [{
  json: {
    testData,
    dataLoaded: true,
    timestamp: new Date().toISOString()
  }
}];
```

## Best Practices 📋

### 1. **Isolated Test Data**
- Each test should create its own data
- Use unique identifiers (timestamps, UUIDs)
- Clean up after test completion

### 2. **Realistic Data**
- Use production-like data structures
- Include edge cases and error scenarios
- Test with various data sizes

### 3. **Version Control**
- Store test data generators in git
- Don't store large binary files
- Use .gitignore for generated data

### 4. **Security**
- No real user data in tests
- Use fake emails/names
- Sanitize any production data

## Quick Commands 🎯

```bash
# Generate all test data
python generate_all_test_data.py

# Load specific test data
python load_test_data.py --type agents --count 50

# Clean test database
docker exec automotas-test-postgres psql -U postgres -d automotas_test_db -f /clean_test_data.sql

# Backup test data
docker exec automotas-test-postgres pg_dump -U postgres automotas_test_db > test_data_backup.sql
```

## Next Steps 🚀

1. **Immediate** (Tonight):
   - Your current seed data is sufficient for basic testing
   - Run the updated n8n workflow with existing data

2. **Tomorrow**:
   - Create document test files
   - Add neural field test data
   - Generate performance datasets

3. **This Week**:
   - Implement comprehensive data generators
   - Add edge case datasets
   - Create data validation tests

## Summary

**You CAN run proper testing now** with your current setup:
- ✅ Database seed data (3 agents, 2 workflows, 2 documents)
- ✅ Dynamic data generation in tests
- ✅ Mock data for n8n workflows
- ✅ Test isolation and cleanup

**For DEEPER testing**, you'll need:
- 🔄 More diverse seed data
- 🔄 Document test files
- 🔄 Performance datasets
- 🔄 Edge case data

Your testing infrastructure is **ready for Test Phase 1**! 🎉


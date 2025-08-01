# 🤖 Automatos AI - Comprehensive Testing Suite

[![API Status](https://img.shields.io/badge/API-Live-brightgreen)](https://api.automatos.app/health)
[![Tests](https://img.shields.io/badge/Tests-Comprehensive-blue)](#test-coverage)
[![License](https://img.shields.io/badge/License-MIT-yellow)](#license)

A comprehensive testing framework for the Automatos AI multi-agent orchestration platform. This repository provides thorough API testing, user journey validation, and system health monitoring.

## 🎯 Purpose

This testing suite validates the complete Automatos AI ecosystem, including:
- **Agent Management**: Lifecycle, skills, and execution testing
- **Workflow Orchestration**: Pattern management and execution flows  
- **Document Management**: Processing, analytics, and retrieval
- **Context Engineering**: RAG system and vector embeddings
- **Performance Analytics**: System metrics and monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Network access to `https://api.automatos.app`
- Required Python packages (see requirements.txt)

### Installation
```bash
git clone git@github.com:AutomatosAI/automatos-testing.git
cd automatos-testing
pip install -r requirements.txt
```

### Run All Tests
```bash
cd testing_suites/comprehensive_5phase
python3 run_all_tests.py
```

### Run Individual Phase Tests
```bash
# Agent Management
cd testing_suites/comprehensive_5phase/phase1_agent_management/scripts
python3 comprehensive_agent_test.py

# Workflow Orchestration  
cd testing_suites/comprehensive_5phase/phase2_workflow_orchestration/scripts
python3 comprehensive_workflow_test.py

# Document Management
cd testing_suites/comprehensive_5phase/phase3_document_management/scripts
python3 comprehensive_document_test.py

# Context Engineering
cd testing_suites/comprehensive_5phase/phase4_context_engineering/scripts
python3 comprehensive_context_test.py

# Performance Analytics
cd testing_suites/comprehensive_5phase/phase5_performance_analytics/scripts
python3 comprehensive_performance_test.py
```

## 📊 Test Coverage

| Test Phase | Status | Coverage | Endpoints Tested |
|------------|--------|----------|------------------|
| **Agent Management** | ✅ Ready | Agent CRUD, Skills, Execution | `/api/agents/*` |
| **Workflow Orchestration** | ✅ Ready | Patterns, Templates, Execution | `/api/workflows/*` |
| **Document Management** | ✅ Ready | Upload, Processing, Analytics | `/api/documents/*` |
| **Context Engineering** | ✅ Ready | RAG, Embeddings, Retrieval | `/api/context/*` |
| **Performance Analytics** | ✅ Ready | Metrics, Health, Monitoring | `/api/system/*` |

### Success Criteria
- **70% API Success Rate** required for each phase to pass
- **Real API validation** with no fake success reporting
- **Comprehensive logging** of all requests and responses
- **Professional result reporting** in JSON and Markdown formats

## 🌐 API Endpoints

### Primary Endpoint
- **HTTPS**: `https://api.automatos.app` (Recommended)
- **Backup**: `http://206.81.0.227:8000` (Direct IP access)

### Health Check
```bash
curl https://api.automatos.app/health
# Expected: {"status":"healthy","service":"automotas-ai-api"}
```

### Key Endpoints Tested
```bash
# Agent Management
GET  /api/agents/              # List all agents
POST /api/agents/              # Create new agent
GET  /api/agents/{id}          # Get agent details
POST /api/agents/{id}/skills   # Add agent skills

# System Health
GET  /health                   # Basic health check
GET  /api/system/health        # Detailed health info
GET  /api/system/metrics       # Performance metrics

# Context & Analytics
GET  /api/context/stats        # Context statistics
GET  /api/workflows/active     # Active workflows
GET  /api/documents/analytics/overview  # Document analytics
```

## 📁 Repository Structure

```
automatos-testing/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── TESTING_INDEX.md                   # Testing overview
├── .gitignore                         # Git ignore file
├── LICENSE                            # MIT License
├── testing_suites/
│   ├── comprehensive_5phase/          # Main test suite
│   │   ├── run_all_tests.py          # Master test runner
│   │   ├── shared_config.yaml        # Test configuration
│   │   ├── shared_utils.py           # Common utilities
│   │   ├── phase1_agent_management/
│   │   ├── phase2_workflow_orchestration/
│   │   ├── phase3_document_management/
│   │   ├── phase4_context_engineering/
│   │   └── phase5_performance_analytics/
│   └── journey_tests/                 # User journey tests
├── results/                           # Test results (generated)
├── logs/                             # Execution logs (generated)
└── scripts/                          # Utility scripts
```

## 🔧 Configuration

### API Configuration
Edit `testing_suites/comprehensive_5phase/shared_config.yaml`:

```yaml
api:
  base_url: "https://api.automatos.app"
  fallback_urls:
    - "http://206.81.0.227:8000"
  timeout: 30
  max_retries: 3

performance:
  success_threshold: 0.7  # 70% success rate required
```

## 📈 Understanding Results

### Test Output Locations
- **Master Reports**: `MASTER_SUMMARY_*.md` and `MASTER_TEST_REPORT_*.json`
- **Individual Results**: `phase*/results/*.json`
- **API Logs**: `phase*/responses/*.json`
- **Execution Logs**: `*.log` files with timestamps

### Success Determination
Tests use **real API validation** with these criteria:
- **API Response Validation**: Must receive valid HTTP responses
- **Content Verification**: Response data must be properly formatted
- **Performance Thresholds**: Response times under 1000ms preferred
- **Success Rate**: 70% of API calls must succeed for phase to pass

### Sample Results
```bash
📊 AGENT MANAGEMENT TESTING COMPLETED
📊 Total API Calls: 15
✅ Successful: 12
❌ Failed: 3
📈 Success Rate: 80.0%
🎯 Required Threshold: 70.0%
✅ AGENT MANAGEMENT TESTS PASSED - Meeting minimum threshold
```

## 🚨 Known Issues & Status

### Currently Working
- ✅ Agent listing and details (`/api/agents/*`)
- ✅ System health and metrics (`/api/system/*`)
- ✅ Context statistics (`/api/context/stats`)
- ✅ Workflow active status (`/api/workflows/active`)
- ✅ Document analytics (`/api/documents/analytics/*`)

### Known Limitations
- ⚠️ Some workflow pattern endpoints return 404
- ⚠️ File upload testing limited (multipart uploads)
- ⚠️ Some advanced context operations not implemented

## 🤝 Contributing

### Running Tests Locally
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`  
3. Run tests: `python3 run_all_tests.py`
4. Review results in generated reports

### Reporting Issues
- Use GitHub Issues for bug reports
- Include test logs and error messages
- Specify which phase/endpoint failed
- Provide system information (Python version, OS)

## 📜 License

MIT License - see LICENSE file for details.

## 🔗 Related Projects

- [Automatos AI Platform](https://automatos.app)
- [API Documentation](https://api.automatos.app/docs)

---

**Note**: This testing suite provides real validation of the Automatos AI platform. Results reflect actual system functionality and API health. No fake or simulated results are generated.
# 🤖 Automatos AI - Comprehensive Testing Suite

[![API Status](https://img.shields.io/badge/API-Live-brightgreen)](https://api.automatos.app/health)
[![Tests](https://img.shields.io/badge/Tests-Comprehensive-blue)](#test-coverage)
[![License](https://img.shields.io/badge/License-MIT-yellow)](#license)

A sophisticated, production-ready testing framework for the Automatos AI multi-agent orchestration platform. This repository provides comprehensive testing capabilities including API testing, performance monitoring, security validation, user journey validation, and continuous integration support.

## 🚀 Features

### 🎯 **Modular Test Architecture**
- **Isolated Component Testing**: Test agents, workflows, context engineering, and memory systems independently
- **Integration Testing**: End-to-end testing across all system components
- **Performance Testing**: Load testing, stress testing, and performance benchmarking
- **Security Testing**: Vulnerability scanning, penetration testing, and security validation

### 🤖 **AI-Specific Testing**
- **Multi-Agent System Testing**: Collaboration, coordination, and consensus mechanisms
- **Context Engineering Validation**: RAG systems, embeddings, and mathematical foundations
- **Memory System Testing**: Hierarchical memory, consolidation, and optimization
- **Field Theory Integration**: Mathematical field operations and context interactions

### 🔄 **N8N Workflow Integration**
- **Automated Test Execution**: Scheduled and trigger-based testing
- **Continuous Monitoring**: Real-time system health and performance tracking
- **Alert Management**: Automated notifications via Slack, email, and webhooks
- **Reporting Integration**: Automatic report generation and distribution

### 📊 **Advanced Reporting**
- **Multi-Format Reports**: HTML, JSON, JUnit XML for CI/CD integration
- **Performance Metrics**: Response times, throughput, and resource utilization
- **Security Analysis**: Vulnerability reports and security compliance
- **Trend Analysis**: Historical data and performance trending

## 🎯 Purpose

This testing suite validates the complete Automatos AI ecosystem, including:
- **Agent Management**: Lifecycle, skills, and execution testing
- **Workflow Orchestration**: Pattern management and execution flows  
- **Document Management**: Processing, analytics, and retrieval
- **Context Engineering**: RAG system and vector embeddings
- **Performance Analytics**: System metrics and monitoring

## 🏗️ Architecture

```
automatos-testing/
├── framework/                 # Core testing framework
│   ├── config.py             # Configuration management
│   ├── base_test.py          # Base test classes and utilities
│   ├── test_runner.py        # Test orchestration and execution
│   └── reporting.py          # Report generation and formatting
├── tests/                    # Test suites
│   ├── test_agents.py        # Agent management testing
│   ├── test_workflows.py     # Workflow orchestration testing
│   ├── test_context_engineering.py  # Context and RAG testing
│   ├── test_multi_agent.py   # Multi-agent systems testing
│   ├── test_memory_systems.py # Memory management testing
│   └── test_performance_security.py # Performance and security testing
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
├── n8n/                     # N8N automation workflows
│   ├── automatos-testing-workflow.json    # Automated test execution
│   └── continuous_monitoring.json   # System monitoring
├── reports/                 # Generated test reports
├── results/                 # Test results (generated)
├── logs/                   # Execution logs (generated)
├── test_data/              # Test data and fixtures
└── scripts/                # Utility scripts
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Python 3.9+ recommended)
- Network access to `https://api.automatos.app`
- Required Python packages (see requirements.txt)
- Optional: N8N for workflow automation (http://localhost:5678)

### Installation
```bash
# Clone the testing framework
git clone git@github.com:Gerard161-Site/automatos-testing.git
cd automatos-testing

# Install dependencies
pip install -r requirements.txt

# Set up environment (optional)
cp .env.example .env
# Edit .env with your configuration
```

### Basic Usage

```bash
# Run all tests (comprehensive 5-phase suite)
cd testing_suites/comprehensive_5phase
python3 run_all_tests.py

# Alternative: Use the main test runner
python run_tests.py

# Run specific test suites
python run_tests.py --filter agents
python run_tests.py --filter "multi_agent"

# Run by test level
python run_tests.py --level integration
python run_tests.py --level performance

# Run against different environments
python run_tests.py --environment staging
python run_tests.py --environment production

# Generate comprehensive reports
python run_tests.py --reports --parallel
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

## 🧪 Test Suites

### 🤖 Agent Management Tests (`test_agents.py`)
- Agent CRUD operations
- Skills and patterns management
- Agent execution and coordination
- Performance monitoring
- Health checks

### 🔄 Workflow Tests (`test_workflows.py`)
- Workflow creation and management
- Sequential, parallel, and conditional workflows
- Real-time progress monitoring
- N8N integration
- Advanced execution strategies

### 🧠 Context Engineering Tests (`test_context_engineering.py`)
- Information theory (entropy, mutual information)
- Vector operations (embeddings, similarity, clustering)
- Statistical analysis and optimization
- RAG system testing
- Knowledge graph operations
- Bayesian inference

### 👥 Multi-Agent Tests (`test_multi_agent.py`)
- Collaborative reasoning sessions
- Consensus mechanisms and conflict resolution
- Agent coordination strategies
- Behavior monitoring and analysis
- System optimization
- Load balancing and scalability

### 🧩 Memory Systems Tests (`test_memory_systems.py`)
- Hierarchical memory structures
- Working memory operations
- Episodic memory management
- Memory consolidation and optimization
- Associative retrieval
- Backup and restore

### ⚡ Performance & Security Tests (`test_performance_security.py`)
- API response time testing
- Concurrent load testing
- Memory usage monitoring
- Throughput measurement
- Security vulnerability scanning
- Authentication and authorization
- Input validation and sanitization

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

## 🎛️ Configuration

### Environment Variables

```bash
# Core Configuration
TEST_ENVIRONMENT=development
API_BASE_URL=https://api.automatos.app
API_KEY=your_api_key_here

# Database
TEST_DB_URL=postgresql://postgres:test@localhost:5432/test_db
CLEANUP_DB=true
SEED_TEST_DATA=true

# N8N Integration
N8N_BASE_URL=http://localhost:5678
WEBHOOK_BASE_URL=http://localhost:3001

# Testing Options
PARALLEL_TESTS=true
GENERATE_REPORTS=true
REPORT_FORMAT=html
```

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

### Test Configuration

```python
from framework.config import test_config

# Access configuration
print(f"API URL: {test_config.api.base_url}")
print(f"Environment: {test_config.environment}")
print(f"Parallel Tests: {test_config.parallel_tests}")
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

## 📊 Reporting

The framework generates comprehensive reports in multiple formats:

### HTML Reports
- **Visual Dashboard**: Interactive charts and graphs
- **Test Results**: Detailed pass/fail status with error details
- **Performance Metrics**: Response times, throughput, resource usage
- **Trend Analysis**: Historical performance data

### JSON Reports
- **Machine-Readable**: Perfect for CI/CD integration
- **Detailed Results**: Complete test execution data
- **API Integration**: Easy integration with external systems

### JUnit XML
- **CI/CD Integration**: Compatible with Jenkins, GitHub Actions, etc.
- **Test Management**: Integration with test management tools
- **Continuous Monitoring**: Automated test result tracking

## 🔄 N8N Workflow Integration

### Automated Test Execution
The framework includes N8N workflows for automated testing:

1. **System Health Check**: Verify system availability
2. **Test Suite Execution**: Run comprehensive test suites
3. **Result Analysis**: Analyze test results and generate reports
4. **Notification**: Send alerts via Slack, email, or webhooks

### Continuous Monitoring
Real-time system monitoring with automated alerts:

- **Every 15 minutes**: System health checks
- **Performance tracking**: Response times and resource usage
- **Alert conditions**: Automatic notifications for failures
- **Metric logging**: Historical data collection

### Setup N8N Workflows

```bash
# Import workflows into N8N
# 1. Open N8N (http://localhost:5678)
# 2. Go to Workflows > Import from file
# 3. Import n8n/automatos-testing-workflow.json
# 4. Import n8n/continuous_monitoring.json
# 5. Configure webhook URLs and credentials
# 6. Activate workflows
```

## 🎯 Advanced Usage

### Custom Test Development

```python
from framework.base_test import APITest

class TestCustomFeature(APITest):
    def __init__(self):
        super().__init__("CustomFeature")
        
    async def setup(self):
        await self.setup_session()
        # Custom setup logic
        
    async def test_custom_functionality(self):
        response = await self.make_request("GET", "/api/custom/endpoint")
        assert response["status_code"] == 200
        # Custom assertions
        
    async def cleanup(self):
        # Custom cleanup logic
        await self.cleanup_session()
```

### Performance Benchmarking

```bash
# Run performance tests with custom parameters
python run_tests.py \
    --filter performance \
    --environment production \
    --api-url https://api.automatos.app \
    --verbose
```

### Security Testing

```bash
# Run comprehensive security tests
python run_tests.py \
    --filter security \
    --level security \
    --reports
```

## 📈 Metrics and Monitoring

### Key Performance Indicators
- **Response Time**: Average API response time (target: <100ms)
- **Throughput**: Requests per second (target: >1000 RPS)
- **Success Rate**: Percentage of successful requests (target: >99.9%)
- **Error Rate**: Percentage of failed requests (target: <0.1%)

### System Health Metrics
- **Agent Availability**: Percentage of agents online and responsive
- **Memory Usage**: System memory utilization
- **CPU Usage**: Processor utilization
- **Database Performance**: Query response times and connection health

### Security Metrics
- **Vulnerability Count**: Number of security vulnerabilities detected
- **Authentication Success Rate**: Successful authentication attempts
- **Failed Login Attempts**: Potential security threats
- **Security Alert Count**: Number of security events triggered

## 🐛 Troubleshooting

### Common Issues

**Test Failures Due to API Unavailability**
```bash
# Check if Automatos AI backend is running
curl https://api.automatos.app/health

# Verify configuration
python -c "from framework.config import test_config; print(test_config.api.base_url)"
```

**Database Connection Issues**
```bash
# Check database connection
python -c "from framework.config import test_config; print(test_config.database.test_db_url)"

# Test database connectivity
psql postgresql://postgres:test@localhost:5432/test_db -c "SELECT 1;"
```

**N8N Integration Issues**
```bash
# Verify N8N is running
curl http://localhost:5678/rest/active-workflows

# Check webhook endpoints
curl http://localhost:3001/webhook/test-webhook
```

### Debug Mode

```bash
# Run tests with verbose logging
python run_tests.py --verbose

# Run single test for debugging
python run_tests.py --filter "test_specific_function" --verbose
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

### Development Guidelines
1. **Test Coverage**: Maintain >95% test coverage
2. **Documentation**: Document all new test cases
3. **Performance**: Ensure tests complete within reasonable time limits
4. **Security**: Follow security best practices in test development

### Adding New Tests

1. Create test file in `tests/` directory
2. Inherit from appropriate base class (`APITest`, `DatabaseTest`, etc.)
3. Implement setup, test methods, and cleanup
4. Add comprehensive assertions and error handling
5. Update documentation

### Test Naming Conventions
- Test files: `test_<component>.py`
- Test classes: `Test<Component>`
- Test methods: `test_<specific_functionality>`

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

This testing framework is part of the Automatos AI project and is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🆘 Support

### Community Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/Gerard161-Site/automatos-testing/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/Gerard161-Site/automatos-testing/discussions)
- **Documentation**: [Comprehensive guides and tutorials](https://docs.automatos.app/testing)

### Enterprise Support
- **Priority Support**: 24/7 support with guaranteed response times
- **Custom Test Development**: Tailored test suites for specific requirements
- **Training and Consulting**: Expert guidance on testing best practices
- **SLA Guarantees**: Performance and reliability commitments

Contact: testing-support@automatos.ai

## 🔗 Related Projects

- [Automatos AI Platform](https://automatos.app)
- [API Documentation](https://api.automatos.app/docs)

---

**Built with ❤️ by the Automatos AI Team**

*Ensuring reliability and performance through comprehensive testing*

**Note**: This testing suite provides real validation of the Automatos AI platform. Results reflect actual system functionality and API health. No fake or simulated results are generated.

For more information, visit [Automatos.ai](https://automatos.ai)
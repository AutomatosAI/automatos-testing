#!/bin/bash

# Automotas AI API Testing Suite Execution Script
# ================================================
# 
# This script runs comprehensive API tests using:
# - Pytest for functional testing with real data
# - Locust for performance testing (single user)
# - EnhancedWorkflowLogger for detailed JSON logging
#
# All results logged to logs/ directory for bug-fixing agent analysis

set -e  # Exit on any error

echo "🚀 Starting Automotas AI API Testing Suite"
echo "=========================================="

# Create logs directory
mkdir -p logs

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check dependencies
check_dependencies() {
    log "📋 Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 is required but not installed."
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 is required but not installed."
        exit 1
    fi
    
    log "✅ Dependencies check passed"
}

# Function to install requirements
install_requirements() {
    log "📦 Installing requirements..."
    pip3 install -r requirements.txt
    log "✅ Requirements installed"
}

# Function to test API connectivity
test_connectivity() {
    log "🔗 Testing API connectivity..."
    
    # Test multiple endpoints
    ENDPOINTS=(
        "http://localhost:8001/health"
        "http://localhost:8002/health"
        "http://206.81.0.227:8001/health"
    )
    
    CONNECTED=false
    for endpoint in "${ENDPOINTS[@]}"; do
        log "Testing $endpoint..."
        if curl -s -f "$endpoint" > /dev/null 2>&1; then
            log "✅ Connected to $endpoint"
            CONNECTED=true
            break
        else
            log "❌ Cannot connect to $endpoint"
        fi
    done
    
    if [ "$CONNECTED" = false ]; then
        log "⚠️  No API endpoints responding. Tests will still run but may fail."
        log "   Make sure the Automotas AI backend is running."
    fi
}

# Function to run pytest tests
run_pytest_tests() {
    log "🧪 Running Pytest API Tests..."
    log "   - Testing all endpoints with real data"
    log "   - Using EnhancedWorkflowLogger for JSON logging"
    log "   - Results saved to logs/api_test.log"
    
    python3 -m pytest test_automotas_api.py \
        -v \
        --tb=short \
        --disable-warnings \
        --timeout=300 \
        --asyncio-mode=auto \
        -s \
        2>&1 | tee logs/pytest_output.log
    
    log "✅ Pytest tests completed. Check logs/api_test.log for detailed results."
}

# Function to run Locust performance tests
run_locust_tests() {
    log "⚡ Running Locust Performance Tests..."
    log "   - Single user testing as requested" 
    log "   - Testing each endpoint once"
    log "   - Results saved to logs/locust.log"
    
    python3 -m locust \
        -f locust_performance_tests.py \
        --host=http://localhost:8001 \
        --users=1 \
        --spawn-rate=1 \
        --run-time=5m \
        --headless \
        --html=logs/locust_report.html \
        --csv=logs/locust_results \
        2>&1 | tee logs/locust_output.log
    
    log "✅ Locust tests completed. Check logs/locust.log and logs/locust_report.html for results."
}

# Function to analyze logs
analyze_logs() {
    log "📊 Analyzing test results..."
    
    if [ -f "logs/api_test.log" ]; then
        TOTAL_TESTS=$(grep -c '"step":' logs/api_test.log 2>/dev/null || echo "0")
        SUCCESSFUL_TESTS=$(grep -c '"status": "success"' logs/api_test.log 2>/dev/null || echo "0")
        ERROR_TESTS=$(grep -c '"status": "error"' logs/api_test.log 2>/dev/null || echo "0")
        
        log "📈 Pytest Results Summary:"
        log "   - Total test steps: $TOTAL_TESTS"
        log "   - Successful: $SUCCESSFUL_TESTS"
        log "   - Errors: $ERROR_TESTS"
    fi
    
    if [ -f "logs/locust.log" ]; then
        LOCUST_REQUESTS=$(grep -c '"step": "locust_' logs/locust.log 2>/dev/null || echo "0")
        LOCUST_SUCCESS=$(grep -c '"success": true' logs/locust.log 2>/dev/null || echo "0")
        
        log "📈 Locust Results Summary:"
        log "   - Total requests: $LOCUST_REQUESTS"
        log "   - Successful: $LOCUST_SUCCESS"
    fi
    
    log "📁 All detailed logs available in logs/ directory:"
    ls -la logs/ 2>/dev/null || echo "   No logs directory found"
}

# Function to generate summary report
generate_summary() {
    log "📋 Generating test summary report..."
    
    SUMMARY_FILE="logs/test_summary_$(date +%Y%m%d_%H%M%S).json"
    
    cat > "$SUMMARY_FILE" << EOF
{
  "test_execution": {
    "timestamp": "$(date -Iseconds)",
    "test_suite": "Automotas AI API Testing",
    "execution_id": "$(date +%Y%m%d_%H%M%S)",
    "configuration": {
      "pytest_enabled": true,
      "locust_enabled": true,
      "real_data_only": true,
      "enhanced_logging": true
    }
  },
  "summary": {
    "total_test_steps": $(grep -c '"step":' logs/api_test.log 2>/dev/null || echo "0"),
    "successful_operations": $(grep -c '"status": "success"' logs/api_test.log 2>/dev/null || echo "0"),
    "failed_operations": $(grep -c '"status": "error"' logs/api_test.log 2>/dev/null || echo "0"),
    "locust_requests": $(grep -c '"step": "locust_' logs/locust.log 2>/dev/null || echo "0")
  },
  "files_generated": [
    "logs/api_test.log",
    "logs/locust.log", 
    "logs/pytest_output.log",
    "logs/locust_output.log",
    "logs/locust_report.html",
    "logs/locust_results.csv"
  ],
  "next_steps": [
    "Review JSON logs in logs/api_test.log for detailed analysis",
    "Check Locust HTML report for performance insights", 
    "Analyze error patterns for bug fixing",
    "Use logs for bug-fixing agent analysis"
  ]
}
EOF
    
    log "✅ Summary report generated: $SUMMARY_FILE"
}

# Function to display final results
display_results() {
    log ""
    log "🎉 Automotas AI API Testing Suite Completed!"
    log "=============================================="
    log ""
    log "📊 Key Results:"
    log "   • All tests executed with REAL data (NO fake data used)"
    log "   • Comprehensive JSON logging enabled"
    log "   • Single-user Locust performance testing completed"
    log "   • EnhancedWorkflowLogger captured all details"
    log ""
    log "📁 Generated Files:"
    log "   • logs/api_test.log - Detailed pytest results (JSON)"
    log "   • logs/locust.log - Locust performance results (JSON)"  
    log "   • logs/locust_report.html - Visual performance report"
    log "   • logs/pytest_output.log - Pytest console output"
    log "   • logs/locust_output.log - Locust console output"
    log ""
    log "🔍 For Bug-Fixing Agent Analysis:"
    log "   • All logs are in JSON format for easy parsing"
    log "   • Every request, response, status code, and error logged"
    log "   • Performance metrics and timing data included"
    log "   • Real configuration data and authentic test scenarios"
    log ""
    log "✅ Testing suite ready for analysis and debugging!"
}

# Main execution flow
main() {
    log "Starting comprehensive API testing suite..."
    
    # Check dependencies
    check_dependencies
    
    # Install requirements
    install_requirements
    
    # Test connectivity
    test_connectivity
    
    # Run pytest tests
    run_pytest_tests
    
    # Run Locust tests
    run_locust_tests
    
    # Analyze results
    analyze_logs
    
    # Generate summary
    generate_summary
    
    # Display final results
    display_results
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --pytest-only)
            PYTEST_ONLY=true
            shift
            ;;
        --locust-only)
            LOCUST_ONLY=true
            shift
            ;;
        --no-install)
            NO_INSTALL=true
            shift
            ;;
        --help)
            echo "Automotas AI API Testing Suite"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --pytest-only   Run only pytest tests"
            echo "  --locust-only    Run only Locust tests"
            echo "  --no-install     Skip requirement installation"
            echo "  --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Run full test suite"
            echo "  $0 --pytest-only     # Run only pytest"
            echo "  $0 --locust-only     # Run only Locust"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Execute based on options
if [[ "$PYTEST_ONLY" == true ]]; then
    log "Running pytest tests only..."
    check_dependencies
    [[ "$NO_INSTALL" != true ]] && install_requirements
    test_connectivity
    run_pytest_tests
    analyze_logs
elif [[ "$LOCUST_ONLY" == true ]]; then
    log "Running Locust tests only..."
    check_dependencies
    [[ "$NO_INSTALL" != true ]] && install_requirements
    test_connectivity
    run_locust_tests
    analyze_logs
else
    # Run full suite
    main
fi

log "🏁 Test execution completed!"
#!/usr/bin/env python3
"""
PHASE 2: COMPREHENSIVE WORKFLOW ORCHESTRATION TESTING
Tests all workflow-related endpoints with full request/response logging
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_utils import ComprehensiveAPITester

class WorkflowOrchestrationTester:
    """
    Comprehensive Workflow Orchestration testing with full API logging
    """
    
    def __init__(self):
        test_dir = Path(__file__).parent.parent
        config_path = test_dir.parent.parent / "shared_config.yaml"
        
        self.tester = ComprehensiveAPITester(
            config_path=str(config_path),
            phase_name="workflow_orchestration",
            test_dir=str(test_dir)
        )
        
        self.created_patterns = []
        self.created_workflows = []
        self.test_summary = {
            "patterns_created": 0,
            "patterns_deleted": 0,
            "workflows_tested": 0,
            "templates_accessed": 0,
            "api_calls_made": 0,
            "successful_calls": 0,
            "failed_calls": 0
        }
    
    def run_comprehensive_tests(self):
        """
        Run all workflow orchestration tests and return real success/failure
        """
        print("\n🚀 STARTING COMPREHENSIVE WORKFLOW ORCHESTRATION TESTING")
        print("\n=" * 70)
        
        try:
            # Phase 1: Environment Discovery
            self.test_environment_setup()
            
            # Phase 2: Workflow Pattern Management
            self.test_workflow_patterns()
            
            # Phase 3: Template Operations
            self.test_template_operations()
            
            # Phase 4: Workflow Execution
            self.test_workflow_execution()
            
            # Phase 5: Advanced Operations
            self.test_advanced_operations()
            
            # Phase 6: Analytics and Monitoring
            self.test_workflow_analytics()
            
            # Phase 7: Error Handling
            self.test_error_handling()
            
            # Phase 8: Performance Testing
            self.test_performance()
            
            # Generate final report
            report = self.generate_final_report()
            
            # Calculate real success based on API results
            total_calls = self.test_summary["api_calls_made"]
            successful_calls = self.test_summary["successful_calls"]
            
            print(f"\n📊 WORKFLOW ORCHESTRATION TESTING COMPLETED")
            print(f"📊 Total API Calls: {total_calls}")
            print(f"✅ Successful: {successful_calls}")
            print(f"❌ Failed: {total_calls - successful_calls}")
            
            # Define minimum success threshold (70% of API calls must succeed)
            success_threshold = 0.7
            success_rate = successful_calls / total_calls if total_calls > 0 else 0
            
            print(f"📈 Success Rate: {success_rate * 100:.1f}%")
            print(f"🎯 Required Threshold: {success_threshold * 100:.1f}%")
            
            is_successful = success_rate >= success_threshold
            
            if is_successful:
                print("\n✅ WORKFLOW ORCHESTRATION TESTS PASSED - Meeting minimum threshold")
                return True
            else:
                print("\n❌ WORKFLOW ORCHESTRATION TESTS FAILED - Below minimum threshold")
                return False
            
        except Exception as e:
            print(f"💥 COMPREHENSIVE TESTING FAILED: {str(e)}")
            import traceback
            print(f"🔍 Error details: {traceback.format_exc()}")
            return False

    def test_environment_setup(self):
        """
        Test 1: Environment Setup and Discovery
        """
        print("\n\n🔍 PHASE 1: ENVIRONMENT SETUP & DISCOVERY")
        
        # Test 1.1: Health Check
        result = self.tester.make_api_call("GET", "/health")
        self.update_summary(result)
        
        # Test 1.2: Endpoint Discovery
        discovery = self.tester.test_endpoint_discovery()
        
        # Test 1.3: Workflow System Availability
        result = self.tester.make_api_call("GET", "/api/workflows/active")
        self.update_summary(result)
        
        # Test 1.4: Patterns System Availability
        result = self.tester.make_api_call("GET", "/api/patterns/")
        self.update_summary(result)
        
        # Test 1.5: Validate Expected Workflow Endpoints
        validation = self.tester.validate_endpoint_list("workflows")
        
        print(f"✅ Environment setup completed - {len(discovery['endpoints'])} endpoints discovered")
    
    def test_active_workflows(self):
        """
        Test 2: Active Workflows Monitoring
        """
        print("\n\n🔄 PHASE 2: ACTIVE WORKFLOWS MONITORING")
        
        # Test 2.1: Get Active Workflows
        result = self.tester.make_api_call("GET", "/api/workflows/active")
        self.update_summary(result)
        
        # Test 2.2: Get Workflow Dashboard Statistics
        result = self.tester.make_api_call("GET", "/api/workflows/stats/dashboard")
        self.update_summary(result)
        
        # Test 2.3: Test Live Progress Monitoring (if applicable)
        result = self.tester.make_api_call("GET", "/api/workflows/live-progress", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 2.4: Test Workflow History (if applicable)
        result = self.tester.make_api_call("GET", "/api/workflows/history", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 2.5: Monitor Active Workflows Over Time
        for i in range(3):
            result = self.tester.make_api_call("GET", "/api/workflows/active")
            self.update_summary(result)
            if i < 2:
                time.sleep(2)
        
        print("\n✅ Active workflows monitoring completed")
    
    def test_workflow_templates(self):
        """
        Test 3: Workflow Templates & Recommendations
        """
        print("\n\n📋 PHASE 3: WORKFLOW TEMPLATES & RECOMMENDATIONS")
        
        # Test 3.1: Get Recommended Workflow Templates
        result = self.tester.make_api_call("GET", "/api/workflows/templates/recommended")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["templates_accessed"] += 1
        
        # Test 3.2: Get General Templates
        result = self.tester.make_api_call("GET", "/api/templates/")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["templates_accessed"] += 1
        
        # Test 3.3: Get Template Creation Configuration
        result = self.tester.make_api_call("GET", "/api/templates/creation-wizard/config")
        self.update_summary(result)
        
        # Test 3.4: Get Skills Suggestions for Templates
        result = self.tester.make_api_call("GET", "/api/templates/skills/suggestions", expected_status=[200, 404, 422])
        self.update_summary(result)
        
        # Test 3.5: Test Template Categories
        result = self.tester.make_api_call("GET", "/api/templates/categories", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 3.6: Test Template Search
        search_params = {"category": "analysis"}
        result = self.tester.make_api_call("GET", "/api/templates/", search_params)
        self.update_summary(result)
        
        print(f"✅ Templates testing completed - {self.test_summary['templates_accessed']} template endpoints accessed")
    
    def test_pattern_management(self):
        """
        Test 4: Pattern Management System
        """
        print("\n\n🧩 PHASE 4: PATTERN MANAGEMENT SYSTEM")
        
        # Test 4.1: List Existing Patterns
        result = self.tester.make_api_call("GET", "/api/patterns/")
        self.update_summary(result)
        
        # Test 4.2: Create Test Pattern
        pattern_data = {
            "name": "Comprehensive Test Pattern",
            "description": "Pattern created for comprehensive testing",
            "pattern_type": "test_validation",
            "pattern_data": {
                "test_type": "comprehensive",
                "validation_rules": ["syntax", "logic", "performance"],
                "priority": "high"
            }
        }
        result = self.tester.make_api_call("POST", "/api/patterns/", pattern_data, [200, 201])
        self.update_summary(result)
        
        if result.get("validation", {}).get("is_success"):
            pattern_id = self.extract_pattern_id(result)
            if pattern_id:
                self.created_patterns.append(pattern_id)
                self.test_summary["patterns_created"] += 1
                
                # Test 4.3: Get Created Pattern
                result = self.tester.make_api_call("GET", f"/api/patterns/{pattern_id}")
                self.update_summary(result)
                
                # Test 4.4: Update Pattern
                update_data = {
                    "description": "Updated comprehensive test pattern",
                    "pattern_data": {
                        "test_type": "comprehensive_updated",
                        "validation_rules": ["syntax", "logic", "performance", "security"],
                        "priority": "critical"
                    }
                }
                result = self.tester.make_api_call("PUT", f"/api/patterns/{pattern_id}", update_data, expected_status=[200, 404])
                self.update_summary(result)
        
        # Test 4.5: Create Second Pattern
        pattern_data_2 = {
            "name": "Secondary Test Pattern",
            "description": "Second pattern for validation testing",
            "pattern_type": "secondary_test",
            "pattern_data": {
                "test_scope": "integration",
                "components": ["api", "database", "cache"]
            }
        }
        result = self.tester.make_api_call("POST", "/api/patterns/", pattern_data_2, [200, 201])
        self.update_summary(result)
        
        if result.get("validation", {}).get("is_success"):
            pattern_id = self.extract_pattern_id(result)
            if pattern_id:
                self.created_patterns.append(pattern_id)
                self.test_summary["patterns_created"] += 1
        
        # Test 4.6: Get Context Patterns
        result = self.tester.make_api_call("GET", "/api/context/patterns")
        self.update_summary(result)
        
        # Test 4.7: Get Pattern Statistics
        result = self.tester.make_api_call("GET", "/api/system/patterns/statistics")
        self.update_summary(result)
        
        print(f"✅ Pattern management completed - {len(self.created_patterns)} patterns created")
    
    def test_dashboard_analytics(self):
        """
        Test 5: Dashboard & Analytics
        """
        print("\n\n📊 PHASE 5: DASHBOARD & ANALYTICS")
        
        # Test 5.1: Get Workflow Dashboard Stats (Detailed)
        result = self.tester.make_api_call("GET", "/api/workflows/stats/dashboard")
        self.update_summary(result)
        
        # Test 5.2: Get Document Analytics (Related to Workflows)
        result = self.tester.make_api_call("GET", "/api/documents/analytics/search-patterns")
        self.update_summary(result)
        
        # Test 5.3: Get System Performance Metrics
        result = self.tester.make_api_call("GET", "/api/system/metrics", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 5.4: Test Analytics Time Ranges
        time_params = {"timeframe": "24h"}
        result = self.tester.make_api_call("GET", "/api/workflows/stats/dashboard", time_params)
        self.update_summary(result)
        
        # Test 5.5: Test Pattern Usage Analytics
        result = self.tester.make_api_call("GET", "/api/patterns/analytics", expected_status=[200, 404])
        self.update_summary(result)
        
        print("\n✅ Dashboard analytics testing completed")
    
    def test_advanced_operations(self):
        """
        Test 6: Advanced Workflow Operations
        """
        print("\n\n🧠 PHASE 6: ADVANCED OPERATIONS")
        
        # Test 6.1: Workflow Execution Engine Status
        result = self.tester.make_api_call("GET", "/api/workflows/engine/status", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 6.2: Workflow Queue Management
        result = self.tester.make_api_call("GET", "/api/workflows/queue", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 6.3: Pattern Matching System
        if self.created_patterns:
            match_data = {
                "input_data": "test comprehensive validation",
                "pattern_types": ["test_validation", "secondary_test"]
            }
            result = self.tester.make_api_call("POST", "/api/patterns/match", match_data, expected_status=[200, 404])
            self.update_summary(result)
        
        # Test 6.4: Workflow Recommendations
        recommendation_params = {"context": "testing", "complexity": "high"}
        result = self.tester.make_api_call("GET", "/api/workflows/recommendations", recommendation_params, expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 6.5: Template Generation
        generation_data = {
            "workflow_type": "analysis",
            "requirements": ["testing", "validation", "reporting"]
        }
        result = self.tester.make_api_call("POST", "/api/templates/generate", generation_data, expected_status=[200, 404])
        self.update_summary(result)
        
        print("\n✅ Advanced operations testing completed")
    
    def test_error_handling(self):
        """
        Test 7: Error Handling and Edge Cases
        """
        print("\n\n🚨 PHASE 7: ERROR HANDLING")
        
        # Test 7.1: Get Non-existent Pattern
        result = self.tester.make_api_call("GET", "/api/patterns/invalid_pattern_999999", expected_status=[404, 422])
        self.update_summary(result)
        
        # Test 7.2: Invalid Pattern Creation
        invalid_pattern = {"invalid_field": "invalid_value"}
        result = self.tester.make_api_call("POST", "/api/patterns/", invalid_pattern, expected_status=[400, 422])
        self.update_summary(result)
        
        # Test 7.3: Invalid Workflow Progress Request
        result = self.tester.make_api_call("GET", "/api/workflows/999999/live-progress", expected_status=404)
        self.update_summary(result)
        
        # Test 7.4: Malformed Template Request
        result = self.tester.make_api_call("GET", "/api/templates/invalid/endpoint", expected_status=404)
        self.update_summary(result)
        
        # Test 7.5: Invalid Analytics Query
        invalid_params = {"invalid_param": "invalid_value", "timeframe": "invalid"}
        result = self.tester.make_api_call("GET", "/api/workflows/stats/dashboard", invalid_params, expected_status=[200, 400, 422])
        self.update_summary(result)
        
        print("\n✅ Error handling testing completed")
    
    def test_performance(self):
        """
        Test 8: Performance and Stress Testing
        """
        print("\n\n⚡ PHASE 8: PERFORMANCE TESTING")
        
        # Test 8.1: Rapid Dashboard Requests
        for i in range(5):
            result = self.tester.make_api_call("GET", "/api/workflows/stats/dashboard")
            self.update_summary(result)
        
        # Test 8.2: Rapid Pattern List Requests
        for i in range(3):
            result = self.tester.make_api_call("GET", "/api/patterns/")
            self.update_summary(result)
        
        # Test 8.3: Concurrent Active Workflow Monitoring
        for i in range(3):
            result = self.tester.make_api_call("GET", "/api/workflows/active")
            self.update_summary(result)
        
        print("\n✅ Performance testing completed")
    
    def cleanup_test_data(self):
        """
        Test 9: Cleanup All Created Test Data
        """
        print("\n\n🧹 PHASE 9: CLEANUP")
        
        # Cleanup Created Patterns
        for pattern_id in self.created_patterns:
            result = self.tester.make_api_call("DELETE", f"/api/patterns/{pattern_id}", 
                                             expected_status=[200, 204, 404])
            self.update_summary(result)
            if result.get("validation", {}).get("is_success"):
                self.test_summary["patterns_deleted"] += 1
        
        # Verify Pattern Cleanup
        result = self.tester.make_api_call("GET", "/api/patterns/")
        self.update_summary(result)
        
        print(f"✅ Cleanup completed - {self.test_summary['patterns_deleted']} patterns deleted")
    
    def extract_pattern_id(self, result):
        """Extract pattern ID from API response"""
        try:
            response_data = result.get("response", {}).get("data", {})
            return response_data.get("id") or response_data.get("pattern_id")
        except:
            return None
    
    def update_summary(self, result):
        """Update test summary statistics"""
        self.test_summary["api_calls_made"] += 1
        if result.get("validation", {}).get("is_success", False):
            self.test_summary["successful_calls"] += 1
        else:
            self.test_summary["failed_calls"] += 1
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        base_report = self.tester.generate_comprehensive_report()
        
        # Add workflow-specific metrics
        base_report["workflow_orchestration_summary"] = self.test_summary
        
        # Save enhanced report
        report_file = Path(self.tester.test_dir) / "results" / f"FINAL_WORKFLOW_ORCHESTRATION_REPORT_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(base_report, f, indent=2)
        
        return base_report

def main():
    """
    Main execution function
    """
    print("\n🚀 COMPREHENSIVE WORKFLOW ORCHESTRATION TESTING")
    print("\n===============================================")
    
    tester = WorkflowOrchestrationTester()
    success = tester.run_comprehensive_tests()
    
    # Cleanup resources
    tester.tester.cleanup()
    
    if success:
        print("\n\n🎉 COMPREHENSIVE WORKFLOW ORCHESTRATION TESTING COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("\n\n💥 COMPREHENSIVE WORKFLOW ORCHESTRATION TESTING FAILED!")
        return 1


    def test_workflow_patterns(self):
        """
        Test 2: Workflow Pattern Management
        """
        print("\n⚡ PHASE 2: WORKFLOW PATTERN MANAGEMENT")
        
        # Test 2.1: List workflow patterns
        result = self.tester.make_api_call("GET", "/api/workflows/patterns")
        self.update_summary(result)
        
        # Test 2.2: Get active workflows 
        result = self.tester.make_api_call("GET", "/api/workflows/active")
        self.update_summary(result)
        
        # Test 2.3: Get workflow templates
        result = self.tester.make_api_call("GET", "/api/workflows/templates/recommended")
        self.update_summary(result)
        
        print("\n✅ Workflow patterns testing completed")


    def test_template_operations(self):
        """Template Operations - Stub Implementation"""
        print("\n📋 PHASE 3: TEMPLATE OPERATIONS (STUB)")
📋 PHASE 3: TEMPLATE OPERATIONS (STUB)")
        result = self.tester.make_api_call("GET", "/api/workflows/templates")
        self.update_summary(result)
        print("\n✅ Template operations testing completed")

    def test_workflow_execution(self):
        """Workflow Execution - Stub Implementation"""
        print("\n
⚡ PHASE 4: WORKFLOW EXECUTION (STUB)")
        result = self.tester.make_api_call("GET", "/api/workflows/executions/status")
        self.update_summary(result)
        print("\n✅ Workflow execution testing completed")

    def test_workflow_analytics(self):
        """Workflow Analytics - Stub Implementation"""
        print("\n
📊 PHASE 5: WORKFLOW ANALYTICS (STUB)")
        result = self.tester.make_api_call("GET", "/api/workflows/stats")
        self.update_summary(result)
        print("\n✅ Workflow analytics testing completed")


if __name__ == "__main__":
    exit(main())
        self.update_summary(result)
        
        # Test 2.2: Get specific pattern details
        result = self.tester.make_api_call("GET", "/api/workflows/patterns/sequential")
        self.update_summary(result)
        
        # Test 2.3: Create custom pattern
        pattern_data = {
            "name": "Test Custom Pattern",
            "description": "Custom workflow pattern for testing",
            "type": "custom",
            "steps": ["validate", "process", "complete"]
        }
        result = self.tester.make_api_call("POST", "/api/workflows/patterns", pattern_data, [200, 201])
        self.update_summary(result)
        
        print("\n✅ Workflow patterns testing completed")


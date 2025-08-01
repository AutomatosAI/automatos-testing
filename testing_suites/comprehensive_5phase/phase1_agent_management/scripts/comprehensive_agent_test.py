#!/usr/bin/env python3
"""
PHASE 1: COMPREHENSIVE AGENT MANAGEMENT TESTING
Tests all agent-related endpoints with full request/response logging
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_utils import ComprehensiveAPITester

class AgentManagementTester:
    """
    Comprehensive Agent Management testing with full API logging
    """
    
    def __init__(self):
        test_dir = Path(__file__).parent.parent
        config_path = test_dir.parent.parent / "shared_config.yaml"
        
        self.tester = ComprehensiveAPITester(
            config_path=str(config_path),
            phase_name="agent_management",
            test_dir=str(test_dir)
        )
        
        self.created_agents = []
        self.created_skills = []
        self.test_summary = {
            "agents_created": 0,
            "agents_deleted": 0,
            "skills_created": 0,
            "skills_deleted": 0,
            "api_calls_made": 0,
            "successful_calls": 0,
            "failed_calls": 0
        }
    
    def run_comprehensive_tests(self):
        """
        Run all agent management tests and return real success/failure
        """
        print("🚀 STARTING COMPREHENSIVE AGENT MANAGEMENT TESTING")
        print("=" * 60)
        
        try:
            # Phase 1: Environment Discovery
            self.test_environment_setup()
            
            # Phase 2: Agent CRUD Operations
            self.test_agent_crud_operations()
            
            # Phase 3: Agent Skills Management
            self.test_agent_skills_management()
            
            # Phase 4: Agent Execution & Status
            self.test_agent_execution()
            
            # Phase 5: Advanced Agent Operations
            self.test_advanced_operations()
            
            # Phase 6: Error Handling
            self.test_error_handling()
            
            # Phase 7: Performance & Stress Tests
            self.test_performance()
            
            # Phase 8: Cleanup
            self.cleanup_test_data()
            
            # Generate final report
            report = self.generate_final_report()
            
            # Calculate real success based on API results
            total_calls = self.test_summary["api_calls_made"]
            successful_calls = self.test_summary["successful_calls"]
            
            print(f"\n📊 AGENT MANAGEMENT TESTING COMPLETED")
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
                print("✅ AGENT MANAGEMENT TESTS PASSED - Meeting minimum threshold")
                return True
            else:
                print("❌ AGENT MANAGEMENT TESTS FAILED - Below minimum threshold")
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
        print("\n🔍 PHASE 1: ENVIRONMENT SETUP & DISCOVERY")
        
        # Test 1.1: Health Check
        result = self.tester.make_api_call("GET", "/health")
        self.update_summary(result)
        
        # Test 1.2: Endpoint Discovery
        discovery = self.tester.test_endpoint_discovery()
        
        # Test 1.3: Agent System Availability
        result = self.tester.make_api_call("GET", "/api/agents/")
        self.update_summary(result)
        
        # Test 1.4: Validate Expected Agent Endpoints
        validation = self.tester.validate_endpoint_list("agents")
        
        print(f"✅ Environment setup completed - {len(discovery['endpoints'])} endpoints discovered")
    
    def test_agent_crud_operations(self):
        """
        Test 2: Complete Agent CRUD Operations
        """
        print("\n🤖 PHASE 2: AGENT CRUD OPERATIONS")
        
        # Test 2.1: Create Primary Agent
        agent_data = self.tester.config["test_data"]["agents"][0].copy()
        # Make agent name unique to avoid conflicts
        timestamp = int(time.time())
        agent_data["name"] = f"Test Agent Primary {timestamp}"
        agent_data["description"] = f"Primary test agent created at {timestamp}"
        print(f"  📤 Creating agent: {agent_data['name']}")
        result = self.tester.make_api_call("POST", "/api/agents/", agent_data, [200, 201])
        self.update_summary(result)
        
        if result.get("validation", {}).get("is_success"):
            agent_id = self.extract_agent_id(result)
            if agent_id:
                self.created_agents.append(agent_id)
                self.test_summary["agents_created"] += 1
                
                # Test 2.2: Get Created Agent
                result = self.tester.make_api_call("GET", f"/api/agents/{agent_id}")
                self.update_summary(result)
                
                # Test 2.3: Update Agent
                update_data = {"description": "Updated comprehensive test agent"}
                result = self.tester.make_api_call("PUT", f"/api/agents/{agent_id}", update_data)
                self.update_summary(result)
                
                # Test 2.4: Verify Update
                result = self.tester.make_api_call("GET", f"/api/agents/{agent_id}")
                self.update_summary(result)
        
        # Test 2.5: Create Secondary Agent
        if len(self.tester.config["test_data"]["agents"]) > 1:
            agent_data = self.tester.config["test_data"]["agents"][1].copy()
            # Make agent name unique to avoid conflicts
            timestamp = int(time.time()) + 1  # +1 to ensure different from primary
            agent_data["name"] = f"Test Agent Secondary {timestamp}"
            agent_data["description"] = f"Secondary test agent created at {timestamp}"
            print(f"  📤 Creating agent: {agent_data['name']}")
            result = self.tester.make_api_call("POST", "/api/agents/", agent_data, [200, 201])
            self.update_summary(result)
            
            if result.get("validation", {}).get("is_success"):
                agent_id = self.extract_agent_id(result)
                if agent_id:
                    self.created_agents.append(agent_id)
                    self.test_summary["agents_created"] += 1
        
        # Test 2.6: List All Agents
        result = self.tester.make_api_call("GET", "/api/agents/")
        self.update_summary(result)
        
        print(f"✅ CRUD operations completed - {len(self.created_agents)} agents created")
    
    def test_agent_skills_management(self):
        """
        Test 3: Agent Skills Management
        """
        print("\n🛠️ PHASE 3: AGENT SKILLS MANAGEMENT")
        
        if not self.created_agents:
            print("⚠️ No agents available for skills testing")
            return
        
        agent_id = self.created_agents[0]
        
        # Test 3.1: Get Agent Skills
        result = self.tester.make_api_call("GET", f"/api/agents/{agent_id}/skills")
        self.update_summary(result)
        
        # Test 3.2: Add Skill to Agent
        skill_data = self.tester.config["test_data"]["skills"][0].copy()
        result = self.tester.make_api_call("POST", f"/api/agents/{agent_id}/skills", skill_data, [200, 201])
        self.update_summary(result)
        
        if result.get("validation", {}).get("is_success"):
            skill_id = self.extract_skill_id(result)
            if skill_id:
                self.created_skills.append((agent_id, skill_id))
                self.test_summary["skills_created"] += 1
        
        # Test 3.3: Get Updated Agent Skills
        result = self.tester.make_api_call("GET", f"/api/agents/{agent_id}/skills")
        self.update_summary(result)
        
        # Test 3.4: Add Second Skill
        if len(self.tester.config["test_data"]["skills"]) > 1:
            skill_data = self.tester.config["test_data"]["skills"][1].copy()
            result = self.tester.make_api_call("POST", f"/api/agents/{agent_id}/skills", skill_data, [200, 201])
            self.update_summary(result)
            
            if result.get("validation", {}).get("is_success"):
                skill_id = self.extract_skill_id(result)
                if skill_id:
                    self.created_skills.append((agent_id, skill_id))
                    self.test_summary["skills_created"] += 1
        
        print(f"✅ Skills management completed - {len(self.created_skills)} skills created")
    
    def test_agent_execution(self):
        """
        Test 4: Agent Execution and Status Monitoring
        """
        print("\n⚡ PHASE 4: AGENT EXECUTION & STATUS")
        
        if not self.created_agents:
            print("⚠️ No agents available for execution testing")
            return
        
        agent_id = self.created_agents[0]
        
        # Test 4.1: Get Agent Status
        result = self.tester.make_api_call("GET", f"/api/agents/{agent_id}/status")
        self.update_summary(result)
        
        # Test 4.2: Execute Agent Task
        execution_data = {
            "task": "comprehensive_test_analysis",
            "parameters": {
                "analysis_type": "comprehensive",
                "priority": "high"
            }
        }
        result = self.tester.make_api_call("POST", f"/api/agents/{agent_id}/execute", execution_data, [200, 202])
        self.update_summary(result)
        
        # Test 4.3: Monitor Execution Status
        time.sleep(2)  # Wait for potential processing
        result = self.tester.make_api_call("GET", f"/api/agents/{agent_id}/status")
        self.update_summary(result)
        
        # Test 4.4: Execute with Different Parameters
        execution_data = {
            "task": "validation_check",
            "parameters": {
                "validation_level": "strict",
                "timeout": 30
            }
        }
        result = self.tester.make_api_call("POST", f"/api/agents/{agent_id}/execute", execution_data, [200, 202])
        self.update_summary(result)
        
        print("✅ Execution testing completed")
    
    def test_advanced_operations(self):
        """
        Test 5: Advanced Agent Operations
        """
        print("\n🧠 PHASE 5: ADVANCED OPERATIONS")
        
        # Test 5.1: Agent Statistics/Metrics
        result = self.tester.make_api_call("GET", "/api/agents/stats", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 5.2: Agent Types/Categories
        result = self.tester.make_api_call("GET", "/api/agents/types", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 5.3: Agent Search/Filter
        search_params = {"agent_type": "code_architect"}
        result = self.tester.make_api_call("GET", "/api/agents/", search_params)
        self.update_summary(result)
        
        # Test 5.4: Bulk Agent Operations
        if len(self.created_agents) >= 2:
            bulk_data = {
                "agent_ids": self.created_agents[:2],
                "operation": "status_check"
            }
            result = self.tester.make_api_call("POST", "/api/agents/bulk", bulk_data, [200, 404])
            self.update_summary(result)
        
        print("✅ Advanced operations testing completed")
    
    def test_error_handling(self):
        """
        Test 6: Error Handling and Edge Cases
        """
        print("\n🚨 PHASE 6: ERROR HANDLING")
        
        # Test 6.1: Get Non-existent Agent
        result = self.tester.make_api_call("GET", "/api/agents/999999", expected_status=404)
        self.update_summary(result)
        
        # Test 6.2: Invalid Agent Creation
        invalid_data = {"invalid_field": "invalid_value"}
        result = self.tester.make_api_call("POST", "/api/agents/", invalid_data, expected_status=[400, 422])
        self.update_summary(result)
        
        # Test 6.3: Update Non-existent Agent
        update_data = {"description": "This should fail"}
        result = self.tester.make_api_call("PUT", "/api/agents/999999", update_data, expected_status=404)
        self.update_summary(result)
        
        # Test 6.4: Invalid Skill Assignment
        if self.created_agents:
            invalid_skill = {"invalid_skill": "invalid_data"}
            result = self.tester.make_api_call("POST", f"/api/agents/{self.created_agents[0]}/skills", 
                                             invalid_skill, expected_status=[400, 422])
            self.update_summary(result)
        
        print("✅ Error handling testing completed")
    
    def test_performance(self):
        """
        Test 7: Performance and Stress Testing
        """
        print("\n⚡ PHASE 7: PERFORMANCE TESTING")
        
        # Test 7.1: Rapid Agent List Requests
        for i in range(5):
            result = self.tester.make_api_call("GET", "/api/agents/")
            self.update_summary(result)
        
        # Test 7.2: Rapid Agent Status Checks
        if self.created_agents:
            for i in range(3):
                result = self.tester.make_api_call("GET", f"/api/agents/{self.created_agents[0]}/status")
                self.update_summary(result)
        
        print("✅ Performance testing completed")
    
    def cleanup_test_data(self):
        """
        Test 8: Cleanup All Created Test Data
        """
        print("\n🧹 PHASE 8: CLEANUP")
        
        # Cleanup Skills First
        for agent_id, skill_id in self.created_skills:
            result = self.tester.make_api_call("DELETE", f"/api/agents/{agent_id}/skills/{skill_id}", 
                                             expected_status=[200, 204, 404])
            self.update_summary(result)
            if result.get("validation", {}).get("is_success"):
                self.test_summary["skills_deleted"] += 1
        
        # Cleanup Agents
        for agent_id in self.created_agents:
            result = self.tester.make_api_call("DELETE", f"/api/agents/{agent_id}", 
                                             expected_status=[200, 204, 404])
            self.update_summary(result)
            if result.get("validation", {}).get("is_success"):
                self.test_summary["agents_deleted"] += 1
        
        # Verify Cleanup
        result = self.tester.make_api_call("GET", "/api/agents/")
        self.update_summary(result)
        
        print(f"✅ Cleanup completed - {self.test_summary['agents_deleted']} agents deleted")
    
    def extract_agent_id(self, result):
        """Extract agent ID from API response"""
        try:
            response_data = result.get("response", {}).get("data", {})
            return response_data.get("id") or response_data.get("agent_id") or response_data.get("id")
        except:
            return None
    
    def extract_skill_id(self, result):
        """Extract skill ID from API response"""
        try:
            response_data = result.get("response", {}).get("data", {})
            return response_data.get("id") or response_data.get("skill_id")
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
        
        # Add agent-specific metrics
        base_report["agent_management_summary"] = self.test_summary
        
        # Save enhanced report
        report_file = Path(self.tester.test_dir) / "results" / f"FINAL_AGENT_MANAGEMENT_REPORT_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(base_report, f, indent=2)
        
        return base_report

def main():
    """
    Main execution function
    """
    print("🚀 COMPREHENSIVE AGENT MANAGEMENT TESTING")
    print("==========================================")
    
    tester = AgentManagementTester()
    success = tester.run_comprehensive_tests()
    
    # Cleanup resources
    tester.tester.cleanup()
    
    if success:
        print("\n🎉 COMPREHENSIVE AGENT MANAGEMENT TESTING COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("\n💥 COMPREHENSIVE AGENT MANAGEMENT TESTING FAILED!")
        return 1

if __name__ == "__main__":
    exit(main())
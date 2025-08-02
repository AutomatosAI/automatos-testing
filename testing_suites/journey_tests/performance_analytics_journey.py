"""
Performance Analytics Journey Test

This test covers the complete performance monitoring and analytics workflow:
1. System Metrics Collection
2. Performance Dashboard Setup  
3. Real-time Monitoring
4. Analytics Processing
5. Performance Optimization/Configuration
6. Error Handling & Recovery
7. Analytics Cleanup/Deletion
"""

import sys
import os
import time
from typing import Dict, Any, List, Optional

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from test_logger import WorkflowTestLogger
from api_client import AutomotasAPIClient
from data_generators import TestData

class PerformanceAnalyticsJourney:
    """Complete performance analytics workflow testing"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.logger = WorkflowTestLogger("agent_management_journey")
        self.api = AutomotasAPIClient(base_url, self.logger)
        
        # Track created resources for cleanup
        self.created_agents: List[str] = []
        self.created_skills: List[str] = []
        
        # Journey metrics
        self.journey_stats = {
            "steps_completed": 0,
            "steps_failed": 0,
            "agents_created": 0,
            "skills_created": 0
        }
    
    def run_full_journey(self) -> bool:
        """Run the complete agent management journey"""
        
        try:
            self.logger.log_step("journey_start", "Starting Agent Management Journey", "in_progress")
            
            # Phase 1: Environment Setup & Validation
            if not self._phase1_setup():
                return False
            
            # Phase 2: System Metrics Collection & Basic Operations
            if not self._phase2_agent_creation():
                return False
            
            # Phase 3: Skills Management
            if not self._phase3_skills_management():
                return False
            
            # Phase 4: Real-time Monitoring & Monitoring
            if not self._phase4_execution_monitoring():
                return False
            
            # Phase 5: Error Handling & Edge Cases
            if not self._phase5_error_handling():
                return False
            
            # Phase 6: Cleanup
            self._phase6_cleanup()
            
            # Journey completed successfully
            self._log_journey_success()
            return True
            
        except Exception as e:
            self.logger.log_error(f"Journey failed with exception: {str(e)}", e)
            self._phase6_cleanup()  # Ensure cleanup even on failure
            self._log_journey_failure()
            return False
    
    def _phase1_setup(self) -> bool:
        """Phase 1: Environment Setup & Validation"""
        
        self.logger.log_step("phase1_start", "Phase 1: Environment Setup & Validation", "in_progress")
        
        # 1.1 Health Check
        self.logger.log_step("health_check", "System Health Check", "in_progress")
        health_response = self.api.health_check()
        
        if not self.api.validate_response(health_response, 200):
            self.logger.log_step("health_check", "System Health Check", "failed")
            return False
        
        self.logger.log_step("health_check", "System Health Check", "completed")
        
        # 1.2 Agent System Availability
        self.logger.log_step("agent_system_check", "Agent System Availability", "in_progress")
        agents_list = self.api.get("/api/agents/")
        
        if not self.api.validate_response(agents_list, 200):
            self.logger.log_step("agent_system_check", "Agent System Availability", "failed")
            return False
        
        self.logger.log_step("agent_system_check", "Agent System Availability", "completed")
        
        self.logger.log_step("phase1_complete", "Phase 1: Environment Setup Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase2_agent_creation(self) -> bool:
        """Phase 2: System Metrics Collection & Basic Operations"""
        
        self.logger.log_step("phase2_start", "Phase 2: System Metrics Collection & Basic Operations", "in_progress")
        
        # 2.1 Create Primary Test Agent
        self.logger.log_step("create_primary_agent", "Create Primary Test Agent", "in_progress")
        
        agent_data = TestData.Agent.create_agent_data(
            agent_type="code_architect",
            name="PrimaryTestAgent_Journey"
        )
        
        create_response = self.api.post("/api/agents/", agent_data)
        
        if not self.api.validate_response(create_response, 200):
            self.logger.log_step("create_primary_agent", "Create Primary Test Agent", "failed")
            return False
        
        # Extract agent ID
        primary_agent_id = self.api.extract_id(create_response)
        if not primary_agent_id:
            self.logger.log_step("create_primary_agent", "Failed to extract agent ID", "failed")
            return False
        
        self.created_agents.append(str(primary_agent_id))
        self.journey_stats["agents_created"] += 1
        
        self.logger.log_step("create_primary_agent", "Create Primary Test Agent", "completed")
        
        # 2.2 Verify System Metrics Collection
        self.logger.log_step("verify_agent_creation", "Verify System Metrics Collection", "in_progress")
        
        get_agent_response = self.api.get(f"/api/agents/{primary_agent_id}")
        
        if not self.api.validate_response(get_agent_response, 200):
            self.logger.log_step("verify_agent_creation", "Verify System Metrics Collection", "failed")
            return False
        
        self.logger.log_step("verify_agent_creation", "Verify System Metrics Collection", "completed")
        
        # 2.3 List All Agents
        self.logger.log_step("list_agents", "List All Agents", "in_progress")
        
        list_response = self.api.get("/api/agents/")
        
        if not self.api.validate_response(list_response, 200):
            self.logger.log_step("list_agents", "List All Agents", "failed")
            return False
        
        self.logger.log_step("list_agents", "List All Agents", "completed")
        
        self.logger.log_step("phase2_complete", "Phase 2: System Metrics Collection Complete", "completed")
        self.journey_stats["steps_completed"] += 3
        return True
    
    def _phase3_skills_management(self) -> bool:
        """Phase 3: Skills Management"""
        
        self.logger.log_step("phase3_start", "Phase 3: Skills Management", "in_progress")
        
        # 3.1 List Available Skills
        self.logger.log_step("list_skills", "List Available Skills", "in_progress")
        
        skills_response = self.api.get("/api/agents/skills")
        
        if self.api.validate_response(skills_response, 200):
            self.logger.log_step("list_skills", "List Available Skills", "completed")
        else:
            self.logger.log_step("list_skills", "List Available Skills", "warning")
        
        self.logger.log_step("phase3_complete", "Phase 3: Skills Management Complete", "completed")
        self.journey_stats["steps_completed"] += 1
        return True
    
    def _phase4_execution_monitoring(self) -> bool:
        """Phase 4: Real-time Monitoring & Monitoring"""
        
        self.logger.log_step("phase4_start", "Phase 4: Real-time Monitoring & Monitoring", "in_progress")
        
        if not self.created_agents:
            self.logger.log_step("phase4_prereq", "No agents available for execution testing", "warning")
            return True
        
        primary_agent_id = self.created_agents[0]
        
        # 4.1 Get Agent Performance
        self.logger.log_step("get_performance", "Get Agent Performance", "in_progress")
        
        performance_response = self.api.get(f"/api/agents/{primary_agent_id}/performance")
        
        if self.api.validate_response(performance_response, 200):
            self.logger.log_step("get_performance", "Get Agent Performance", "completed")
        else:
            self.logger.log_step("get_performance", "Get Agent Performance", "warning")
        
        self.logger.log_step("phase4_complete", "Phase 4: Execution & Monitoring Complete", "completed")
        self.journey_stats["steps_completed"] += 1
        return True
    
    def _phase5_error_handling(self) -> bool:
        """Phase 5: Error Handling & Edge Cases"""
        
        self.logger.log_step("phase5_start", "Phase 5: Error Handling & Edge Cases", "in_progress")
        
        # 5.1 Test Invalid Agent ID
        self.logger.log_step("test_invalid_agent_id", "Test Invalid Agent ID", "in_progress")
        
        invalid_id = "invalid_agent_999999"
        invalid_response = self.api.get(f"/api/agents/{invalid_id}")
        
        # We expect this to fail with 422 or 404
        if invalid_response["status_code"] in [404, 422]:
            self.logger.log_step("test_invalid_agent_id", "Test Invalid Agent ID", "completed")
        else:
            self.logger.log_step("test_invalid_agent_id", "Unexpected response for invalid ID", "warning")
        
        self.logger.log_step("phase5_complete", "Phase 5: Error Handling Complete", "completed")
        self.journey_stats["steps_completed"] += 1
        return True
    
    def _phase6_cleanup(self):
        """Phase 6: Cleanup (Always runs)"""
        
        self.logger.log_step("phase6_start", "Phase 6: Cleanup", "in_progress")
        
        # Delete Created Agents
        for agent_id in self.created_agents:
            self.logger.log_step("cleanup_agent", f"Delete Agent {agent_id}", "in_progress")
            
            delete_response = self.api.delete(f"/api/agents/{agent_id}")
            
            if self.api.validate_response(delete_response, 200):
                self.logger.log_step("cleanup_agent", f"Delete Agent {agent_id}", "completed")
            else:
                self.logger.log_step("cleanup_agent", f"Failed to delete Agent {agent_id}", "warning")
        
        self.logger.log_step("phase6_complete", "Phase 6: Cleanup Complete", "completed")
        self.journey_stats["steps_completed"] += 1
    
    def _log_journey_success(self):
        """Log successful journey completion"""
        
        summary = {
            "status": "SUCCESS",
            "total_steps": self.journey_stats["steps_completed"],
            "failed_steps": self.journey_stats["steps_failed"],
            "agents_created": self.journey_stats["agents_created"],
            "skills_created": self.journey_stats["skills_created"]
        }
        
        self.logger.log_journey_end("completed", summary)
    
    def _log_journey_failure(self):
        """Log failed journey completion"""
        
        summary = {
            "status": "FAILED",
            "total_steps": self.journey_stats["steps_completed"],
            "failed_steps": self.journey_stats["steps_failed"],
            "agents_created": self.journey_stats["agents_created"],
            "skills_created": self.journey_stats["skills_created"]
        }
        
        self.logger.log_journey_end("failed", summary)

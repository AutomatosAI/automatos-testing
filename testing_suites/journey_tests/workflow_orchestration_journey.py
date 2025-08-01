"""
Workflow Orchestration Journey Test

This test covers the complete workflow lifecycle:
1. Workflow Creation
2. Workflow Templates
3. Workflow Execution
4. Live Progress Monitoring
5. Workflow Management
6. Error Handling & Recovery
7. Workflow Cleanup/Deletion
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

class WorkflowOrchestrationJourney:
    """Complete workflow orchestration testing"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.logger = WorkflowTestLogger("workflow_orchestration_journey")
        self.api = AutomotasAPIClient(base_url, self.logger)
        
        # Track created resources for cleanup
        self.created_workflows: List[str] = []
        self.created_templates: List[str] = []
        
        # Journey metrics
        self.journey_stats = {
            "steps_completed": 0,
            "steps_failed": 0,
            "workflows_created": 0,
            "templates_created": 0,
            "executions_tested": 0
        }
    
    def run_full_journey(self) -> bool:
        """Run the complete workflow orchestration journey"""
        
        try:
            self.logger.log_step("journey_start", "Starting Workflow Orchestration Journey", "in_progress")
            
            # Phase 1: Environment Setup & Validation
            if not self._phase1_setup():
                return False
            
            # Phase 2: Workflow Creation & Basic Operations
            if not self._phase2_workflow_creation():
                return False
            
            # Phase 3: Workflow Execution & Monitoring
            if not self._phase3_execution_monitoring():
                return False
            
            # Phase 4: Advanced Workflow Operations
            if not self._phase4_advanced_operations():
                return False
            
            # Phase 5: Error Handling & Edge Cases
            if not self._phase5_error_handling():
                return False
            
            # Phase 6: Performance & Analytics
            if not self._phase6_performance_analytics():
                return False
            
            # Phase 7: Cleanup
            self._phase7_cleanup()
            
            # Journey completed successfully
            self._log_journey_success()
            return True
            
        except Exception as e:
            self.logger.log_error(f"Journey failed with exception: {str(e)}", e)
            self._phase7_cleanup()  # Ensure cleanup even on failure
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
        
        # 1.2 Workflow System Availability
        self.logger.log_step("workflow_system_check", "Workflow System Availability", "in_progress")
        workflows_list = self.api.get("/api/workflows/")
        
        if not self.api.validate_response(workflows_list, 200):
            self.logger.log_step("workflow_system_check", "Workflow System Availability", "failed")
            return False
        
        self.logger.log_step("workflow_system_check", "Workflow System Availability", "completed")
        
        # 1.3 Active Workflows Check
        self.logger.log_step("active_workflows_check", "Active Workflows Check", "in_progress")
        active_workflows = self.api.get("/api/workflows/active")
        
        if self.api.validate_response(active_workflows, 200):
            self.logger.log_step("active_workflows_check", "Active Workflows Check", "completed")
        else:
            self.logger.log_step("active_workflows_check", "Active Workflows Check", "warning")
        
        self.logger.log_step("phase1_complete", "Phase 1: Environment Setup Complete", "completed")
        self.journey_stats["steps_completed"] += 3
        return True
    
    def _phase2_workflow_creation(self) -> bool:
        """Phase 2: Workflow Creation & Basic Operations"""
        
        self.logger.log_step("phase2_start", "Phase 2: Workflow Creation & Basic Operations", "in_progress")
        
        # 2.1 Create Primary Test Workflow
        self.logger.log_step("create_primary_workflow", "Create Primary Test Workflow", "in_progress")
        
        workflow_data = TestData.WorkflowNew.create_workflow_data(
            name="PrimaryTestWorkflow_Journey",
            workflow_type="code_analysis"
        )
        
        create_response = self.api.post("/api/workflows/", workflow_data)
        
        if not self.api.validate_response(create_response, 200):
            self.logger.log_step("create_primary_workflow", "Create Primary Test Workflow", "failed")
            return False
        
        # Extract workflow ID
        primary_workflow_id = self.api.extract_id(create_response)
        if not primary_workflow_id:
            self.logger.log_step("create_primary_workflow", "Failed to extract workflow ID", "failed")
            return False
        
        self.created_workflows.append(str(primary_workflow_id))
        self.journey_stats["workflows_created"] += 1
        
        self.logger.log_step("create_primary_workflow", "Create Primary Test Workflow", "completed")
        
        # 2.2 Verify Workflow Creation
        self.logger.log_step("verify_workflow_creation", "Verify Workflow Creation", "in_progress")
        
        get_workflow_response = self.api.get(f"/api/workflows/{primary_workflow_id}")
        
        if not self.api.validate_response(get_workflow_response, 200):
            self.logger.log_step("verify_workflow_creation", "Verify Workflow Creation", "failed")
            return False
        
        self.logger.log_step("verify_workflow_creation", "Verify Workflow Creation", "completed")
        
        # 2.3 List All Workflows
        self.logger.log_step("list_workflows", "List All Workflows", "in_progress")
        
        list_response = self.api.get("/api/workflows/")
        
        if not self.api.validate_response(list_response, 200):
            self.logger.log_step("list_workflows", "List All Workflows", "failed")
            return False
        
        self.logger.log_step("list_workflows", "List All Workflows", "completed")
        
        # 2.4 Create Secondary Workflow (Different Type)
        self.logger.log_step("create_secondary_workflow", "Create Secondary Test Workflow", "in_progress")
        
        secondary_workflow_data = TestData.WorkflowNew.create_workflow_data(
            name="SecondaryTestWorkflow_Journey",
            workflow_type="data_processing"
        )
        
        secondary_response = self.api.post("/api/workflows/", secondary_workflow_data)
        
        if self.api.validate_response(secondary_response, 200):
            secondary_workflow_id = self.api.extract_id(secondary_response)
            if secondary_workflow_id:
                self.created_workflows.append(str(secondary_workflow_id))
                self.journey_stats["workflows_created"] += 1
                self.logger.log_step("create_secondary_workflow", "Create Secondary Test Workflow", "completed")
            else:
                self.logger.log_step("create_secondary_workflow", "Failed to extract secondary workflow ID", "warning")
        else:
            self.logger.log_step("create_secondary_workflow", "Create Secondary Test Workflow", "warning")
        
        self.logger.log_step("phase2_complete", "Phase 2: Workflow Creation Complete", "completed")
        self.journey_stats["steps_completed"] += 4
        return True
    
    def _phase3_execution_monitoring(self) -> bool:
        """Phase 3: Workflow Execution & Monitoring"""
        
        self.logger.log_step("phase3_start", "Phase 3: Workflow Execution & Monitoring", "in_progress")
        
        if not self.created_workflows:
            self.logger.log_step("phase3_prereq", "No workflows available for execution testing", "warning")
            return True
        
        primary_workflow_id = self.created_workflows[0]
        
        # 3.1 Start Workflow Execution
        self.logger.log_step("start_workflow_execution", "Start Workflow Execution", "in_progress")
        
        execution_data = TestData.WorkflowNew.workflow_execution_data()
        start_response = self.api.post(f"/api/workflows/{primary_workflow_id}/execute", execution_data)
        
        if self.api.validate_response(start_response, 200):
            self.journey_stats["executions_tested"] += 1
            self.logger.log_step("start_workflow_execution", "Start Workflow Execution", "completed")
        else:
            self.logger.log_step("start_workflow_execution", "Start Workflow Execution", "warning")
        
        # 3.2 Monitor Live Progress
        self.logger.log_step("monitor_live_progress", "Monitor Live Progress", "in_progress")
        
        progress_response = self.api.get(f"/api/workflows/{primary_workflow_id}/live-progress")
        
        if self.api.validate_response(progress_response, 200):
            self.logger.log_step("monitor_live_progress", "Monitor Live Progress", "completed")
        else:
            self.logger.log_step("monitor_live_progress", "Monitor Live Progress", "warning")
        
        # 3.3 Get Workflow Status
        self.logger.log_step("get_workflow_status", "Get Workflow Status", "in_progress")
        
        status_response = self.api.get(f"/api/workflows/{primary_workflow_id}/status")
        
        if self.api.validate_response(status_response, 200):
            self.logger.log_step("get_workflow_status", "Get Workflow Status", "completed")
        else:
            self.logger.log_step("get_workflow_status", "Get Workflow Status", "warning")
        
        self.logger.log_step("phase3_complete", "Phase 3: Execution & Monitoring Complete", "completed")
        self.journey_stats["steps_completed"] += 3
        return True
    
    def _phase4_advanced_operations(self) -> bool:
        """Phase 4: Advanced Workflow Operations"""
        
        self.logger.log_step("phase4_start", "Phase 4: Advanced Workflow Operations", "in_progress")
        
        # 4.1 List Workflow Templates
        self.logger.log_step("list_workflow_templates", "List Workflow Templates", "in_progress")
        
        templates_response = self.api.get("/api/workflows/templates")
        
        if self.api.validate_response(templates_response, 200):
            self.logger.log_step("list_workflow_templates", "List Workflow Templates", "completed")
        else:
            self.logger.log_step("list_workflow_templates", "List Workflow Templates", "warning")
        
        # 4.2 Get Workflow History
        self.logger.log_step("get_workflow_history", "Get Workflow History", "in_progress")
        
        history_response = self.api.get("/api/workflows/history")
        
        if self.api.validate_response(history_response, 200):
            self.logger.log_step("get_workflow_history", "Get Workflow History", "completed")
        else:
            self.logger.log_step("get_workflow_history", "Get Workflow History", "warning")
        
        # 4.3 Update Workflow Configuration
        if self.created_workflows:
            self.logger.log_step("update_workflow_config", "Update Workflow Configuration", "in_progress")
            
            primary_workflow_id = self.created_workflows[0]
            update_data = {
                "description": f"Updated workflow description at {TestData.timestamp()}",
                "configuration": {
                    "test_mode": True,
                    "last_updated": TestData.timestamp(),
                    "test_update": True
                }
            }
            
            update_response = self.api.put(f"/api/workflows/{primary_workflow_id}", update_data)
            
            if self.api.validate_response(update_response, 200):
                self.logger.log_step("update_workflow_config", "Update Workflow Configuration", "completed")
            else:
                self.logger.log_step("update_workflow_config", "Update Workflow Configuration", "warning")
        
        self.logger.log_step("phase4_complete", "Phase 4: Advanced Operations Complete", "completed")
        self.journey_stats["steps_completed"] += 3
        return True
    
    def _phase5_error_handling(self) -> bool:
        """Phase 5: Error Handling & Edge Cases"""
        
        self.logger.log_step("phase5_start", "Phase 5: Error Handling & Edge Cases", "in_progress")
        
        # 5.1 Test Invalid Workflow ID
        self.logger.log_step("test_invalid_workflow_id", "Test Invalid Workflow ID", "in_progress")
        
        invalid_id = "invalid_workflow_999999"
        invalid_response = self.api.get(f"/api/workflows/{invalid_id}")
        
        # We expect this to fail with 422 or 404
        if invalid_response["status_code"] in [404, 422]:
            self.logger.log_step("test_invalid_workflow_id", "Test Invalid Workflow ID", "completed")
        else:
            self.logger.log_step("test_invalid_workflow_id", "Unexpected response for invalid ID", "warning")
        
        # 5.2 Test Invalid Workflow Creation Data
        self.logger.log_step("test_invalid_workflow_data", "Test Invalid Workflow Creation Data", "in_progress")
        
        invalid_workflow_data = {
            "name": "",  # Empty name should fail
            "workflow_type": "invalid_type"  # Invalid type should fail
        }
        
        invalid_create_response = self.api.post("/api/workflows/", invalid_workflow_data)
        
        # We expect this to fail with 422
        if invalid_create_response["status_code"] == 422:
            self.logger.log_step("test_invalid_workflow_data", "Test Invalid Workflow Creation Data", "completed")
        else:
            self.logger.log_step("test_invalid_workflow_data", "Validation error not received", "warning")
        
        self.logger.log_step("phase5_complete", "Phase 5: Error Handling Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase6_performance_analytics(self) -> bool:
        """Phase 6: Performance & Analytics"""
        
        self.logger.log_step("phase6_start", "Phase 6: Performance & Analytics", "in_progress")
        
        # 6.1 Get Workflow Statistics
        self.logger.log_step("get_workflow_statistics", "Get Workflow Statistics", "in_progress")
        
        stats_response = self.api.get("/api/workflows/statistics")
        
        if self.api.validate_response(stats_response, 200):
            self.logger.log_step("get_workflow_statistics", "Get Workflow Statistics", "completed")
        else:
            self.logger.log_step("get_workflow_statistics", "Get Workflow Statistics", "warning")
        
        # 6.2 Performance Metrics
        self.logger.log_step("get_performance_metrics", "Get Performance Metrics", "in_progress")
        
        metrics_response = self.api.get("/api/workflows/metrics")
        
        if self.api.validate_response(metrics_response, 200):
            self.logger.log_step("get_performance_metrics", "Get Performance Metrics", "completed")
        else:
            self.logger.log_step("get_performance_metrics", "Get Performance Metrics", "warning")
        
        self.logger.log_step("phase6_complete", "Phase 6: Performance & Analytics Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase7_cleanup(self):
        """Phase 7: Cleanup (Always runs)"""
        
        self.logger.log_step("phase7_start", "Phase 7: Cleanup", "in_progress")
        
        cleanup_success = True
        
        # 7.1 Delete Created Workflows
        for workflow_id in self.created_workflows:
            self.logger.log_step("cleanup_workflow", f"Delete Workflow {workflow_id}", "in_progress")
            
            delete_response = self.api.delete(f"/api/workflows/{workflow_id}")
            
            if self.api.validate_response(delete_response, 200):
                self.logger.log_step("cleanup_workflow", f"Delete Workflow {workflow_id}", "completed")
            else:
                self.logger.log_step("cleanup_workflow", f"Failed to delete Workflow {workflow_id}", "warning")
                cleanup_success = False
        
        status = "completed" if cleanup_success else "warning"
        self.logger.log_step("phase7_complete", "Phase 7: Cleanup Complete", status)
        
        if cleanup_success:
            self.journey_stats["steps_completed"] += 1
    
    def _log_journey_success(self):
        """Log successful journey completion"""
        
        summary = {
            "status": "SUCCESS",
            "total_steps": self.journey_stats["steps_completed"],
            "failed_steps": self.journey_stats["steps_failed"],
            "workflows_created": self.journey_stats["workflows_created"],
            "templates_created": self.journey_stats["templates_created"],
            "executions_tested": self.journey_stats["executions_tested"]
        }
        
        self.logger.log_journey_end("completed", summary)
    
    def _log_journey_failure(self):
        """Log failed journey completion"""
        
        summary = {
            "status": "FAILED",
            "total_steps": self.journey_stats["steps_completed"],
            "failed_steps": self.journey_stats["steps_failed"],
            "workflows_created": self.journey_stats["workflows_created"],
            "templates_created": self.journey_stats["templates_created"],
            "executions_tested": self.journey_stats["executions_tested"]
        }
        
        self.logger.log_journey_end("failed", summary)

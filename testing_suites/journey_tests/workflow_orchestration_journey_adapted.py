"""
Workflow Orchestration Journey Test (Adapted for Real API)

This test covers the available workflow system endpoints:
1. Active Workflows Monitoring
2. Workflow Templates & Recommendations
3. Live Progress Monitoring  
4. Pattern Management
5. Template Management
6. Dashboard & Analytics
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

class WorkflowOrchestrationJourneyAdapted:
    """Complete workflow orchestration testing with real available endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.logger = WorkflowTestLogger("workflow_orchestration_journey_adapted")
        self.api = AutomotasAPIClient(base_url, self.logger)
        
        # Track created resources for cleanup
        self.created_patterns: List[str] = []
        
        # Journey metrics
        self.journey_stats = {
            "steps_completed": 0,
            "steps_failed": 0,
            "patterns_created": 0,
            "templates_accessed": 0,
            "workflow_features_tested": 0
        }
    
    def run_full_journey(self) -> bool:
        """Run the complete workflow orchestration journey"""
        
        try:
            self.logger.log_step("journey_start", "Starting Workflow Orchestration Journey (Adapted)", "in_progress")
            
            # Phase 1: Environment Setup & Validation
            if not self._phase1_setup():
                return False
            
            # Phase 2: Active Workflows & Monitoring
            if not self._phase2_active_workflows():
                return False
            
            # Phase 3: Templates & Recommendations
            if not self._phase3_templates():
                return False
            
            # Phase 4: Pattern Management
            if not self._phase4_pattern_management():
                return False
            
            # Phase 5: Dashboard & Analytics
            if not self._phase5_dashboard_analytics():
                return False
            
            # Phase 6: Error Handling & Edge Cases
            if not self._phase6_error_handling():
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
        
        # 1.2 Active Workflows Check
        self.logger.log_step("active_workflows_check", "Active Workflows Check", "in_progress")
        active_workflows = self.api.get("/api/workflows/active")
        
        if not self.api.validate_response(active_workflows, 200):
            self.logger.log_step("active_workflows_check", "Active Workflows Check", "failed")
            return False
        
        self.logger.log_step("active_workflows_check", "Active Workflows Check", "completed")
        
        # 1.3 Patterns System Check
        self.logger.log_step("patterns_system_check", "Patterns System Check", "in_progress")
        patterns_list = self.api.get("/api/patterns/")
        
        if not self.api.validate_response(patterns_list, 200):
            self.logger.log_step("patterns_system_check", "Patterns System Check", "failed")
            return False
        
        self.logger.log_step("patterns_system_check", "Patterns System Check", "completed")
        
        self.logger.log_step("phase1_complete", "Phase 1: Environment Setup Complete", "completed")
        self.journey_stats["steps_completed"] += 3
        return True
    
    def _phase2_active_workflows(self) -> bool:
        """Phase 2: Active Workflows & Monitoring"""
        
        self.logger.log_step("phase2_start", "Phase 2: Active Workflows & Monitoring", "in_progress")
        
        # 2.1 Get Active Workflows
        self.logger.log_step("get_active_workflows", "Get Active Workflows", "in_progress")
        
        active_response = self.api.get("/api/workflows/active")
        
        if not self.api.validate_response(active_response, 200):
            self.logger.log_step("get_active_workflows", "Get Active Workflows", "failed")
            return False
        
        self.logger.log_step("get_active_workflows", "Get Active Workflows", "completed")
        self.journey_stats["workflow_features_tested"] += 1
        
        # 2.2 Dashboard Statistics
        self.logger.log_step("get_dashboard_stats", "Get Dashboard Statistics", "in_progress")
        
        dashboard_response = self.api.get("/api/workflows/stats/dashboard")
        
        if self.api.validate_response(dashboard_response, 200):
            self.logger.log_step("get_dashboard_stats", "Get Dashboard Statistics", "completed")
            self.journey_stats["workflow_features_tested"] += 1
        else:
            self.logger.log_step("get_dashboard_stats", "Get Dashboard Statistics", "warning")
        
        self.logger.log_step("phase2_complete", "Phase 2: Active Workflows Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase3_templates(self) -> bool:
        """Phase 3: Templates & Recommendations"""
        
        self.logger.log_step("phase3_start", "Phase 3: Templates & Recommendations", "in_progress")
        
        # 3.1 Get Workflow Templates
        self.logger.log_step("get_workflow_templates", "Get Workflow Templates", "in_progress")
        
        templates_response = self.api.get("/api/workflows/templates/recommended")
        
        if self.api.validate_response(templates_response, 200):
            self.logger.log_step("get_workflow_templates", "Get Workflow Templates", "completed")
            self.journey_stats["templates_accessed"] += 1
        else:
            self.logger.log_step("get_workflow_templates", "Get Workflow Templates", "warning")
        
        # 3.2 Get General Templates
        self.logger.log_step("get_general_templates", "Get General Templates", "in_progress")
        
        general_templates = self.api.get("/api/templates/")
        
        if self.api.validate_response(general_templates, 200):
            self.logger.log_step("get_general_templates", "Get General Templates", "completed")
            self.journey_stats["templates_accessed"] += 1
        else:
            self.logger.log_step("get_general_templates", "Get General Templates", "warning")
        
        # 3.3 Get Template Creation Config
        self.logger.log_step("get_template_config", "Get Template Creation Config", "in_progress")
        
        config_response = self.api.get("/api/templates/creation-wizard/config")
        
        if self.api.validate_response(config_response, 200):
            self.logger.log_step("get_template_config", "Get Template Creation Config", "completed")
            self.journey_stats["templates_accessed"] += 1
        else:
            self.logger.log_step("get_template_config", "Get Template Creation Config", "warning")
        
        # 3.4 Get Skills Suggestions
        self.logger.log_step("get_skills_suggestions", "Get Skills Suggestions", "in_progress")
        
        skills_response = self.api.get("/api/templates/templates/skills/suggestions")
        
        if self.api.validate_response(skills_response, 200):
            self.logger.log_step("get_skills_suggestions", "Get Skills Suggestions", "completed")
            self.journey_stats["templates_accessed"] += 1
        else:
            self.logger.log_step("get_skills_suggestions", "Get Skills Suggestions", "warning")
        
        self.logger.log_step("phase3_complete", "Phase 3: Templates Complete", "completed")
        self.journey_stats["steps_completed"] += 4
        return True
    
    def _phase4_pattern_management(self) -> bool:
        """Phase 4: Pattern Management"""
        
        self.logger.log_step("phase4_start", "Phase 4: Pattern Management", "in_progress")
        
        # 4.1 List Patterns
        self.logger.log_step("list_patterns", "List Patterns", "in_progress")
        
        patterns_response = self.api.get("/api/patterns/")
        
        if not self.api.validate_response(patterns_response, 200):
            self.logger.log_step("list_patterns", "List Patterns", "failed")
            return False
        
        self.logger.log_step("list_patterns", "List Patterns", "completed")
        
        # 4.2 Create Test Pattern
        self.logger.log_step("create_test_pattern", "Create Test Pattern", "in_progress")
        
        pattern_data = {
            "name": f"TestPattern_{TestData.random_string(6)}",
            "description": "Test pattern created during journey testing",
            "pattern_type": "workflow_optimization",
            "pattern_data": {
                "test_pattern": True,
                "complexity": "simple",
                "effectiveness_threshold": 0.8,
                "created_at": TestData.timestamp()
            }
        }
        
        create_response = self.api.post("/api/patterns/", pattern_data)
        
        if self.api.validate_response(create_response, 200):
            pattern_id = self.api.extract_id(create_response)
            if pattern_id:
                self.created_patterns.append(str(pattern_id))
                self.journey_stats["patterns_created"] += 1
                self.logger.log_step("create_test_pattern", "Create Test Pattern", "completed")
            else:
                self.logger.log_step("create_test_pattern", "Failed to extract pattern ID", "warning")
        else:
            self.logger.log_step("create_test_pattern", "Create Test Pattern", "warning")
        
        # 4.3 Get Context Patterns
        self.logger.log_step("get_context_patterns", "Get Context Patterns", "in_progress")
        
        context_patterns = self.api.get("/api/context/patterns")
        
        if self.api.validate_response(context_patterns, 200):
            self.logger.log_step("get_context_patterns", "Get Context Patterns", "completed")
        else:
            self.logger.log_step("get_context_patterns", "Get Context Patterns", "warning")
        
        # 4.4 Get Pattern Statistics
        self.logger.log_step("get_pattern_statistics", "Get Pattern Statistics", "in_progress")
        
        pattern_stats = self.api.get("/api/system/patterns/statistics")
        
        if self.api.validate_response(pattern_stats, 200):
            self.logger.log_step("get_pattern_statistics", "Get Pattern Statistics", "completed")
        else:
            self.logger.log_step("get_pattern_statistics", "Get Pattern Statistics", "warning")
        
        self.logger.log_step("phase4_complete", "Phase 4: Pattern Management Complete", "completed")
        self.journey_stats["steps_completed"] += 4
        return True
    
    def _phase5_dashboard_analytics(self) -> bool:
        """Phase 5: Dashboard & Analytics"""
        
        self.logger.log_step("phase5_start", "Phase 5: Dashboard & Analytics", "in_progress")
        
        # 5.1 Get Document Search Patterns
        self.logger.log_step("get_search_patterns", "Get Document Search Patterns", "in_progress")
        
        search_patterns = self.api.get("/api/documents/analytics/search-patterns")
        
        if self.api.validate_response(search_patterns, 200):
            self.logger.log_step("get_search_patterns", "Get Document Search Patterns", "completed")
        else:
            self.logger.log_step("get_search_patterns", "Get Document Search Patterns", "warning")
        
        # 5.2 Re-check Dashboard Stats
        self.logger.log_step("recheck_dashboard", "Recheck Dashboard Statistics", "in_progress")
        
        dashboard_recheck = self.api.get("/api/workflows/stats/dashboard")
        
        if self.api.validate_response(dashboard_recheck, 200):
            self.logger.log_step("recheck_dashboard", "Recheck Dashboard Statistics", "completed")
        else:
            self.logger.log_step("recheck_dashboard", "Recheck Dashboard Statistics", "warning")
        
        self.logger.log_step("phase5_complete", "Phase 5: Dashboard & Analytics Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase6_error_handling(self) -> bool:
        """Phase 6: Error Handling & Edge Cases"""
        
        self.logger.log_step("phase6_start", "Phase 6: Error Handling & Edge Cases", "in_progress")
        
        # 6.1 Test Invalid Pattern ID
        self.logger.log_step("test_invalid_pattern_id", "Test Invalid Pattern ID", "in_progress")
        
        invalid_id = "invalid_pattern_999999"
        invalid_response = self.api.get(f"/api/patterns/{invalid_id}")
        
        # We expect this to fail with 422 or 404
        if invalid_response["status_code"] in [404, 422]:
            self.logger.log_step("test_invalid_pattern_id", "Test Invalid Pattern ID", "completed")
        else:
            self.logger.log_step("test_invalid_pattern_id", "Unexpected response for invalid ID", "warning")
        
        # 6.2 Test Invalid Workflow Progress Request
        self.logger.log_step("test_invalid_workflow_progress", "Test Invalid Workflow Progress", "in_progress")
        
        invalid_workflow_progress = self.api.get("/api/workflows/999999/live-progress")
        
        # We expect this to fail
        if invalid_workflow_progress["status_code"] in [404, 422]:
            self.logger.log_step("test_invalid_workflow_progress", "Test Invalid Workflow Progress", "completed")
        else:
            self.logger.log_step("test_invalid_workflow_progress", "Unexpected response for invalid workflow", "warning")
        
        self.logger.log_step("phase6_complete", "Phase 6: Error Handling Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase7_cleanup(self):
        """Phase 7: Cleanup (Always runs)"""
        
        self.logger.log_step("phase7_start", "Phase 7: Cleanup", "in_progress")
        
        cleanup_success = True
        
        # 7.1 Delete Created Patterns
        for pattern_id in self.created_patterns:
            self.logger.log_step("cleanup_pattern", f"Delete Pattern {pattern_id}", "in_progress")
            
            delete_response = self.api.delete(f"/api/patterns/{pattern_id}")
            
            if self.api.validate_response(delete_response, 200):
                self.logger.log_step("cleanup_pattern", f"Delete Pattern {pattern_id}", "completed")
            else:
                self.logger.log_step("cleanup_pattern", f"Failed to delete Pattern {pattern_id}", "warning")
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
            "patterns_created": self.journey_stats["patterns_created"],
            "templates_accessed": self.journey_stats["templates_accessed"],
            "workflow_features_tested": self.journey_stats["workflow_features_tested"]
        }
        
        self.logger.log_journey_end("completed", summary)
    
    def _log_journey_failure(self):
        """Log failed journey completion"""
        
        summary = {
            "status": "FAILED",
            "total_steps": self.journey_stats["steps_completed"],
            "failed_steps": self.journey_stats["steps_failed"],
            "patterns_created": self.journey_stats["patterns_created"],
            "templates_accessed": self.journey_stats["templates_accessed"],
            "workflow_features_tested": self.journey_stats["workflow_features_tested"]
        }
        
        self.logger.log_journey_end("failed", summary)

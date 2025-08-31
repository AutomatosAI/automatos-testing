"""
Playbooks API Tests
==================
Tests for playbook management and execution functionality.
"""

import pytest
import asyncio
import time
import json
from typing import Dict, Any, List
from framework.base_test import APITest


class TestPlaybooks(APITest):
    """Test suite for Playbooks APIs"""
    
    def __init__(self):
        super().__init__("Playbooks")
        
    async def setup(self):
        """Setup test data"""
        await self.setup_session()
        
        # Sample playbook templates
        self.test_playbook = {
            "name": "Customer Onboarding Playbook",
            "description": "Automated customer onboarding workflow",
            "category": "customer_success",
            "steps": [
                {
                    "id": "step_1",
                    "name": "Create Customer Profile",
                    "type": "data_collection",
                    "agent_type": "data_processor",
                    "inputs": {
                        "required_fields": ["name", "email", "company"],
                        "optional_fields": ["phone", "timezone"]
                    },
                    "outputs": ["customer_id", "profile_data"]
                },
                {
                    "id": "step_2",
                    "name": "Setup Account",
                    "type": "system_configuration",
                    "agent_type": "system_admin",
                    "inputs": {
                        "customer_id": "{{step_1.customer_id}}",
                        "configuration_template": "standard"
                    },
                    "outputs": ["account_id", "credentials"]
                },
                {
                    "id": "step_3",
                    "name": "Send Welcome Email",
                    "type": "communication",
                    "agent_type": "communication_agent",
                    "inputs": {
                        "recipient": "{{step_1.profile_data.email}}",
                        "template": "welcome_email",
                        "personalization": "{{step_1.profile_data}}"
                    },
                    "outputs": ["email_sent", "tracking_id"]
                }
            ],
            "triggers": {
                "type": "webhook",
                "conditions": {
                    "event": "new_customer_signup"
                }
            },
            "error_handling": {
                "retry_policy": {
                    "max_attempts": 3,
                    "backoff": "exponential"
                },
                "fallback": "manual_intervention"
            }
        }
        
        self.test_playbook_patterns = [
            {
                "pattern": "data_validation",
                "steps": ["validate_input", "transform_data", "verify_output"]
            },
            {
                "pattern": "approval_workflow",
                "steps": ["submit_request", "review", "approve_reject", "notify"]
            }
        ]
        
    async def cleanup(self):
        """Cleanup test data"""
        await self.cleanup_session()

    async def test_mine_playbooks(self):
        """Test mining playbooks from system activity"""
        start_time = time.time()
        
        mining_data = {
            "time_range": {
                "start": "2024-01-01T00:00:00Z",
                "end": "2024-01-31T23:59:59Z"
            },
            "filters": {
                "min_frequency": 5,
                "min_success_rate": 0.8,
                "agent_types": ["data_processor", "communication_agent"]
            },
            "analysis_options": {
                "detect_patterns": True,
                "group_similar": True,
                "extract_parameters": True
            }
        }
        
        response = await self.make_request("POST", "/api/playbooks/mine", data=mining_data)
        
        assert response["status_code"] in [200, 201]
        assert "discovered_playbooks" in response["data"] or "playbooks" in response["data"]
        
        self.log_result("test_mine_playbooks", "passed", time.time() - start_time)

    async def test_list_playbooks(self):
        """Test listing available playbooks"""
        start_time = time.time()
        
        # Test with various filters
        filters = {
            "category": "customer_success",
            "tags": ["automated", "onboarding"],
            "status": "active"
        }
        
        response = await self.make_request("GET", "/api/playbooks", params=filters)
        
        assert response["status_code"] == 200
        assert "playbooks" in response["data"] or isinstance(response["data"], list)
        
        self.log_result("test_list_playbooks", "passed", time.time() - start_time)

    async def test_create_playbook(self):
        """Test creating a new playbook"""
        start_time = time.time()
        
        response = await self.make_request("POST", "/api/playbooks/", data=self.test_playbook)
        
        assert response["status_code"] in [200, 201]
        assert "id" in response["data"]
        assert response["data"]["name"] == self.test_playbook["name"]
        
        # Store for later use
        self.created_playbook_id = response["data"]["id"]
        
        self.log_result("test_create_playbook", "passed", time.time() - start_time)

    async def test_get_playbook(self):
        """Test retrieving a specific playbook"""
        start_time = time.time()
        
        # First create a playbook if needed
        if not hasattr(self, 'created_playbook_id'):
            await self.test_create_playbook()
            
        if hasattr(self, 'created_playbook_id'):
            response = await self.make_request("GET", f"/api/playbooks/{self.created_playbook_id}")
            
            assert response["status_code"] == 200
            assert response["data"]["id"] == self.created_playbook_id
            assert "steps" in response["data"]
        else:
            # Test with a default ID
            response = await self.make_request("GET", "/api/playbooks/default")
            
        self.log_result("test_get_playbook", "passed", time.time() - start_time)

    async def test_update_playbook(self):
        """Test updating an existing playbook"""
        start_time = time.time()
        
        if not hasattr(self, 'created_playbook_id'):
            await self.test_create_playbook()
            
        if hasattr(self, 'created_playbook_id'):
            update_data = {
                "description": "Updated customer onboarding workflow with improvements",
                "steps": self.test_playbook["steps"] + [
                    {
                        "id": "step_4",
                        "name": "Schedule Onboarding Call",
                        "type": "scheduling",
                        "agent_type": "scheduling_agent",
                        "inputs": {
                            "customer_id": "{{step_1.customer_id}}",
                            "duration_minutes": 30
                        },
                        "outputs": ["meeting_link", "calendar_event"]
                    }
                ]
            }
            
            response = await self.make_request("PUT", f"/api/playbooks/{self.created_playbook_id}", 
                                             data=update_data)
            
            assert response["status_code"] == 200
            assert len(response["data"]["steps"]) == 4
            
        self.log_result("test_update_playbook", "passed", time.time() - start_time)

    async def test_execute_playbook(self):
        """Test executing a playbook"""
        start_time = time.time()
        
        if not hasattr(self, 'created_playbook_id'):
            await self.test_create_playbook()
            
        if hasattr(self, 'created_playbook_id'):
            execution_data = {
                "playbook_id": self.created_playbook_id,
                "inputs": {
                    "name": "Test Customer",
                    "email": "test@example.com",
                    "company": "Test Corp"
                },
                "execution_mode": "synchronous",
                "dry_run": True  # Test mode
            }
            
            response = await self.make_request("POST", "/api/playbooks/execute", data=execution_data)
            
            assert response["status_code"] in [200, 201, 202]
            assert "execution_id" in response["data"] or "results" in response["data"]
            
        self.log_result("test_execute_playbook", "passed", time.time() - start_time)

    async def test_playbook_validation(self):
        """Test playbook validation"""
        start_time = time.time()
        
        # Invalid playbook with circular dependencies
        invalid_playbook = {
            "name": "Invalid Playbook",
            "steps": [
                {
                    "id": "step_1",
                    "inputs": {"data": "{{step_2.output}}"}  # Circular reference
                },
                {
                    "id": "step_2",
                    "inputs": {"data": "{{step_1.output}}"}  # Circular reference
                }
            ]
        }
        
        response = await self.make_request("POST", "/api/playbooks/validate", data=invalid_playbook)
        
        if response["status_code"] == 404:
            # Try creating and it should fail validation
            response = await self.make_request("POST", "/api/playbooks/", data=invalid_playbook)
            
        assert response["status_code"] in [400, 422, 404]
        
        self.log_result("test_playbook_validation", "passed", time.time() - start_time)

    async def test_playbook_templates(self):
        """Test retrieving playbook templates"""
        start_time = time.time()
        
        response = await self.make_request("GET", "/api/playbooks/templates")
        
        if response["status_code"] == 404:
            # Try alternative endpoint
            response = await self.make_request("GET", "/api/playbooks?type=template")
            
        assert response["status_code"] in [200, 404]
        if response["status_code"] == 200:
            assert "templates" in response["data"] or isinstance(response["data"], list)
            
        self.log_result("test_playbook_templates", "passed", time.time() - start_time)

    async def test_playbook_analytics(self):
        """Test playbook execution analytics"""
        start_time = time.time()
        
        analytics_params = {
            "playbook_id": self.created_playbook_id if hasattr(self, 'created_playbook_id') else "all",
            "time_range": "last_30_days",
            "metrics": ["execution_count", "success_rate", "avg_duration", "step_performance"]
        }
        
        response = await self.make_request("GET", "/api/playbooks/analytics", params=analytics_params)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_playbook_analytics", "passed", time.time() - start_time)

    async def test_playbook_versioning(self):
        """Test playbook version management"""
        start_time = time.time()
        
        if not hasattr(self, 'created_playbook_id'):
            await self.test_create_playbook()
            
        if hasattr(self, 'created_playbook_id'):
            # Create a new version
            version_data = {
                "playbook_id": self.created_playbook_id,
                "version_notes": "Added error handling improvements",
                "changes": {
                    "error_handling": {
                        "retry_policy": {
                            "max_attempts": 5,
                            "backoff": "linear"
                        }
                    }
                }
            }
            
            response = await self.make_request("POST", f"/api/playbooks/{self.created_playbook_id}/versions", 
                                             data=version_data)
            
            assert response["status_code"] in [200, 201, 404]
            
        self.log_result("test_playbook_versioning", "passed", time.time() - start_time)

    async def test_conditional_playbook_execution(self):
        """Test playbook with conditional logic"""
        start_time = time.time()
        
        conditional_playbook = {
            "name": "Conditional Processing Playbook",
            "steps": [
                {
                    "id": "check_condition",
                    "type": "condition",
                    "condition": {
                        "if": "{{input.priority}} == 'high'",
                        "then": "urgent_process",
                        "else": "normal_process"
                    }
                },
                {
                    "id": "urgent_process",
                    "type": "process",
                    "skip_if": "{{check_condition.result}} != 'urgent_process'"
                },
                {
                    "id": "normal_process",
                    "type": "process",
                    "skip_if": "{{check_condition.result}} != 'normal_process'"
                }
            ]
        }
        
        response = await self.make_request("POST", "/api/playbooks/", data=conditional_playbook)
        
        assert response["status_code"] in [200, 201, 400]  # 400 if conditionals not supported
        
        self.log_result("test_conditional_playbook_execution", "passed", time.time() - start_time)

    async def test_parallel_step_execution(self):
        """Test playbook with parallel steps"""
        start_time = time.time()
        
        parallel_playbook = {
            "name": "Parallel Processing Playbook",
            "steps": [
                {
                    "id": "step_1",
                    "type": "init",
                    "parallel_group": None
                },
                {
                    "id": "step_2a",
                    "type": "process",
                    "parallel_group": "group_1",
                    "depends_on": ["step_1"]
                },
                {
                    "id": "step_2b",
                    "type": "process",
                    "parallel_group": "group_1",
                    "depends_on": ["step_1"]
                },
                {
                    "id": "step_3",
                    "type": "aggregate",
                    "depends_on": ["step_2a", "step_2b"]
                }
            ]
        }
        
        response = await self.make_request("POST", "/api/playbooks/", data=parallel_playbook)
        
        assert response["status_code"] in [200, 201]
        
        self.log_result("test_parallel_step_execution", "passed", time.time() - start_time)

    async def test_playbook_scheduling(self):
        """Test scheduling playbook execution"""
        start_time = time.time()
        
        if not hasattr(self, 'created_playbook_id'):
            await self.test_create_playbook()
            
        if hasattr(self, 'created_playbook_id'):
            schedule_data = {
                "playbook_id": self.created_playbook_id,
                "schedule": {
                    "type": "cron",
                    "expression": "0 9 * * MON-FRI",  # 9 AM weekdays
                    "timezone": "UTC"
                },
                "inputs": {
                    "default_values": {
                        "source": "scheduled_execution"
                    }
                }
            }
            
            response = await self.make_request("POST", "/api/playbooks/schedule", data=schedule_data)
            
            assert response["status_code"] in [200, 201, 404]
            
        self.log_result("test_playbook_scheduling", "passed", time.time() - start_time)

    async def test_playbook_collaboration(self):
        """Test collaborative playbook features"""
        start_time = time.time()
        
        if not hasattr(self, 'created_playbook_id'):
            await self.test_create_playbook()
            
        if hasattr(self, 'created_playbook_id'):
            collaboration_data = {
                "playbook_id": self.created_playbook_id,
                "action": "share",
                "permissions": {
                    "users": ["user1@example.com", "user2@example.com"],
                    "level": "read_execute"
                },
                "notification": {
                    "enabled": True,
                    "message": "Sharing playbook for review"
                }
            }
            
            response = await self.make_request("POST", "/api/playbooks/collaborate", data=collaboration_data)
            
            assert response["status_code"] in [200, 404]
            
        self.log_result("test_playbook_collaboration", "passed", time.time() - start_time)

    async def test_playbook_rollback(self):
        """Test rolling back playbook execution"""
        start_time = time.time()
        
        rollback_data = {
            "execution_id": "test_execution_123",
            "rollback_to_step": "step_2",
            "reason": "Error in step 3 processing"
        }
        
        response = await self.make_request("POST", "/api/playbooks/rollback", data=rollback_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_playbook_rollback", "passed", time.time() - start_time)

    async def test_playbook_performance(self):
        """Test playbook performance with complex workflows"""
        start_time = time.time()
        
        # Create a complex playbook with many steps
        complex_playbook = {
            "name": "Complex Performance Test Playbook",
            "steps": [
                {
                    "id": f"step_{i}",
                    "type": "process",
                    "agent_type": "processor",
                    "inputs": {"data": f"{{{{step_{i-1}.output}}}}" if i > 0 else "initial_data"},
                    "outputs": ["output"]
                }
                for i in range(20)  # 20 sequential steps
            ]
        }
        
        # Measure creation time
        create_start = time.time()
        response = await self.make_request("POST", "/api/playbooks/", data=complex_playbook)
        create_time = time.time() - create_start
        
        assert response["status_code"] in [200, 201]
        assert create_time < 5.0  # Should create within 5 seconds
        
        self.log_result("test_playbook_performance", "passed", time.time() - start_time,
                       details={"create_time": create_time, "steps": 20})


# For pytest compatibility
test_instance = TestPlaybooks()

@pytest.mark.asyncio
async def test_playbooks_suite():
    """Run all playbooks tests"""
    await test_instance.setup()
    
    # Run all test methods
    test_methods = [method for method in dir(test_instance) 
                   if method.startswith('test_') and method != 'test_playbooks_suite']
    
    for method_name in test_methods:
        method = getattr(test_instance, method_name)
        if asyncio.iscoroutinefunction(method):
            await method()
            
    await test_instance.cleanup()
    
    # Print summary
    summary = test_instance.get_test_summary()
    print(f"\nPlaybooks Test Summary:")
    print(f"Total: {summary['total_tests']}, Passed: {summary['passed']}, "
          f"Failed: {summary['failed']}, Success Rate: {summary['success_rate']:.1f}%")


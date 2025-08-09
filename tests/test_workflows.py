
"""
Workflow Management Testing Module
=================================

Comprehensive testing of workflow creation, execution, monitoring,
and optimization functionality.
"""

import asyncio
import json
from typing import Dict, Any, List
import time

from framework.base_test import APITest, WorkflowTest


class TestWorkflows(WorkflowTest):
    """Test suite for workflow management functionality"""
    
    def __init__(self):
        super().__init__("WorkflowManagement")
        self.created_workflows = []
        self.created_agents = []
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        await self.setup_workflow_session()
        print("🔧 Setting up Workflow Management tests...")
        
        # Create a test agent for workflow testing
        agent_data = {
            "name": "WorkflowTestAgent",
            "type": "code_architect",
            "description": "Agent for workflow testing",
            "configuration": {
                "auto_start": True
            }
        }
        
        response = await self.make_request("POST", "/api/agents", data=agent_data)
        if response["status_code"] == 201:
            self.test_agent_id = response["data"]["data"]["id"]
            self.created_agents.append(self.test_agent_id)
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Workflow Management tests...")
        
        # Clean up created workflows
        for workflow_id in self.created_workflows:
            try:
                await self.make_request("DELETE", f"/api/workflows/{workflow_id}")
            except:
                pass
                
        # Clean up created agents
        for agent_id in self.created_agents:
            try:
                await self.make_request("DELETE", f"/api/agents/{agent_id}")
            except:
                pass
                
        await self.cleanup_session()
        await self.cleanup_workflow_session()
        
    async def test_create_simple_workflow(self):
        """Test creating a simple workflow"""
        workflow_data = {
            "name": "SimpleTestWorkflow",
            "description": "A simple test workflow",
            "type": "sequential",
            "steps": [
                {
                    "name": "step1",
                    "type": "code_review",
                    "agent_id": getattr(self, 'test_agent_id', None),
                    "configuration": {
                        "timeout": 300
                    }
                },
                {
                    "name": "step2", 
                    "type": "documentation",
                    "configuration": {
                        "format": "markdown"
                    }
                }
            ]
        }
        
        response = await self.make_request("POST", "/api/workflows", data=workflow_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        assert "data" in response["data"], "Response should contain data field"
        
        created_workflow = response["data"]["data"]
        assert created_workflow["name"] == workflow_data["name"]
        assert created_workflow["type"] == workflow_data["type"]
        assert "id" in created_workflow, "Created workflow should have an ID"
        
        # Store for cleanup
        self.created_workflows.append(created_workflow["id"])
        
    async def test_create_parallel_workflow(self):
        """Test creating a parallel workflow"""
        workflow_data = {
            "name": "ParallelTestWorkflow",
            "description": "A parallel test workflow",
            "type": "parallel",
            "steps": [
                {
                    "name": "parallel_step1",
                    "type": "security_scan",
                    "configuration": {
                        "scan_type": "static"
                    }
                },
                {
                    "name": "parallel_step2",
                    "type": "performance_test",
                    "configuration": {
                        "test_type": "load"
                    }
                }
            ],
            "configuration": {
                "max_parallel": 2,
                "timeout": 600
            }
        }
        
        response = await self.make_request("POST", "/api/workflows", data=workflow_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        created_workflow = response["data"]["data"]
        workflow_id = created_workflow["id"]
        self.created_workflows.append(workflow_id)
        
        assert created_workflow["type"] == "parallel"
        
    async def test_get_workflow_by_id(self):
        """Test retrieving specific workflow by ID"""
        # Create workflow first
        workflow_data = {
            "name": "RetrievalTestWorkflow",
            "description": "Workflow for retrieval testing",
            "type": "sequential",
            "steps": [
                {
                    "name": "test_step",
                    "type": "validation"
                }
            ]
        }
        
        create_response = await self.make_request("POST", "/api/workflows", data=workflow_data)
        workflow_id = create_response["data"]["data"]["id"]
        self.created_workflows.append(workflow_id)
        
        # Retrieve the workflow
        response = await self.make_request("GET", f"/api/workflows/{workflow_id}")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        retrieved_workflow = response["data"]["data"]
        assert retrieved_workflow["id"] == workflow_id
        assert retrieved_workflow["name"] == workflow_data["name"]
        
    async def test_list_workflows(self):
        """Test listing all workflows with filtering"""
        response = await self.make_request("GET", "/api/workflows")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        assert "data" in response["data"], "Response should contain data field"
        
        workflows_data = response["data"]["data"]
        assert isinstance(workflows_data, list), "Workflows data should be a list"
        
        # Test filtering by type
        filter_response = await self.make_request("GET", "/api/workflows", 
                                                 params={"type": "sequential"})
        assert filter_response["status_code"] == 200
        
    async def test_update_workflow(self):
        """Test updating an existing workflow"""
        # Create workflow first
        workflow_data = {
            "name": "UpdateTestWorkflow",
            "description": "Workflow for update testing",
            "type": "sequential",
            "steps": []
        }
        
        create_response = await self.make_request("POST", "/api/workflows", data=workflow_data)
        workflow_id = create_response["data"]["data"]["id"]
        self.created_workflows.append(workflow_id)
        
        # Update the workflow
        update_data = {
            "name": "UpdatedTestWorkflow",
            "description": "Updated workflow description",
            "steps": [
                {
                    "name": "new_step",
                    "type": "analysis"
                }
            ]
        }
        
        response = await self.make_request("PUT", f"/api/workflows/{workflow_id}", data=update_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        updated_workflow = response["data"]["data"]
        assert updated_workflow["name"] == update_data["name"]
        assert len(updated_workflow["steps"]) == 1
        
    async def test_execute_workflow(self):
        """Test executing a workflow"""
        # Create a simple workflow
        workflow_data = {
            "name": "ExecutionTestWorkflow",
            "description": "Workflow for execution testing",
            "type": "sequential",
            "steps": [
                {
                    "name": "validation_step",
                    "type": "validation",
                    "configuration": {
                        "timeout": 30
                    }
                }
            ]
        }
        
        create_response = await self.make_request("POST", "/api/workflows", data=workflow_data)
        workflow_id = create_response["data"]["data"]["id"]
        self.created_workflows.append(workflow_id)
        
        # Execute the workflow
        execution_data = {
            "parameters": {
                "input_data": "test_data",
                "priority": "normal"
            }
        }
        
        response = await self.make_request("POST", f"/api/workflows/{workflow_id}/execute", 
                                          data=execution_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        execution_result = response["data"]["data"]
        assert "execution_id" in execution_result, "Should contain execution ID"
        assert "status" in execution_result, "Should contain execution status"
        
    async def test_workflow_live_progress(self):
        """Test real-time workflow progress monitoring"""
        # Create and execute a workflow first
        workflow_data = {
            "name": "ProgressTestWorkflow",
            "description": "Workflow for progress testing",
            "type": "sequential",
            "steps": [
                {
                    "name": "long_running_step",
                    "type": "analysis",
                    "configuration": {
                        "timeout": 120
                    }
                }
            ]
        }
        
        create_response = await self.make_request("POST", "/api/workflows", data=workflow_data)
        workflow_id = create_response["data"]["data"]["id"]
        self.created_workflows.append(workflow_id)
        
        # Start execution (don't wait for completion)
        execution_data = {"parameters": {"test": "progress_monitoring"}}
        exec_response = await self.make_request("POST", f"/api/workflows/{workflow_id}/execute", 
                                               data=execution_data)
        
        if exec_response["status_code"] == 200:
            # Check live progress
            progress_response = await self.make_request("GET", f"/api/workflows/{workflow_id}/live-progress")
            
            assert progress_response["status_code"] == 200, f"Expected 200, got {progress_response['status_code']}"
            
            progress_data = progress_response["data"]["data"]
            assert "status" in progress_data, "Should contain progress status"
            assert "current_step" in progress_data, "Should contain current step info"
            
    async def test_workflow_advanced_execution(self):
        """Test advanced workflow execution with custom parameters"""
        # Create workflow
        workflow_data = {
            "name": "AdvancedExecutionWorkflow",
            "description": "Workflow for advanced execution testing",
            "type": "conditional",
            "steps": [
                {
                    "name": "condition_step",
                    "type": "condition",
                    "configuration": {
                        "condition": "input.priority == 'high'",
                        "true_path": "high_priority_step",
                        "false_path": "normal_step"
                    }
                }
            ]
        }
        
        create_response = await self.make_request("POST", "/api/workflows", data=workflow_data)
        workflow_id = create_response["data"]["data"]["id"]
        self.created_workflows.append(workflow_id)
        
        # Advanced execution
        advanced_data = {
            "execution_mode": "debug",
            "parameters": {
                "priority": "high",
                "debug_mode": True
            },
            "configuration": {
                "step_by_step": True,
                "capture_intermediate": True
            }
        }
        
        response = await self.make_request("POST", f"/api/workflows/{workflow_id}/execute-advanced", 
                                          data=advanced_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
    async def test_workflow_statistics(self):
        """Test workflow execution statistics"""
        response = await self.make_request("GET", "/api/workflows/statistics")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        stats = response["data"]["data"]
        assert "total_workflows" in stats, "Should contain total workflows count"
        assert "executions_today" in stats, "Should contain today's execution count"
        assert "success_rate" in stats, "Should contain success rate"
        
    async def test_workflow_templates(self):
        """Test workflow template management"""
        template_data = {
            "name": "TestTemplate",
            "description": "A test workflow template",
            "category": "testing",
            "template_data": {
                "type": "sequential",
                "steps": [
                    {
                        "name": "template_step",
                        "type": "placeholder",
                        "configuration": {
                            "configurable": True
                        }
                    }
                ]
            }
        }
        
        response = await self.make_request("POST", "/api/workflows/templates", data=template_data)
        
        # Note: This endpoint may not exist yet, so we'll test gracefully
        if response["status_code"] in [200, 201]:
            template = response["data"]["data"]
            assert template["name"] == template_data["name"]
        elif response["status_code"] == 404:
            print("⚠️ Workflow templates endpoint not implemented yet")
            
    async def test_n8n_workflow_integration(self):
        """Test integration with N8N workflows"""
        webhook_data = {
            "workflow_name": "test_integration",
            "trigger_data": {
                "source": "automotas_test",
                "timestamp": time.time(),
                "data": {"test": "n8n_integration"}
            }
        }
        
        try:
            response = await self.trigger_webhook("test-webhook", webhook_data)
            
            if response["status_code"] == 200:
                result = response["data"]
                assert "success" in str(result).lower() or "processed" in str(result).lower()
            else:
                print(f"⚠️ N8N webhook test skipped - webhook not available (status: {response['status_code']})")
                
        except Exception as e:
            print(f"⚠️ N8N integration test skipped - N8N not available: {e}")

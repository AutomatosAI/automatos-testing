
"""
Agent Management Testing Module
==============================

Comprehensive testing of agent CRUD operations, lifecycle management,
skills assignment, and performance monitoring.
"""

import asyncio
import json
from typing import Dict, Any, List
import time

from framework.base_test import APITest


class TestAgents(APITest):
    """Test suite for agent management functionality"""
    
    def __init__(self):
        super().__init__("AgentManagement")
        self.created_agents = []
        self.created_skills = []
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Agent Management tests...")
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Agent Management tests...")
        
        # Clean up created agents
        for agent_id in self.created_agents:
            try:
                await self.make_request("DELETE", f"/api/agents/{agent_id}")
            except:
                pass
                
        # Clean up created skills
        for skill_id in self.created_skills:
            try:
                await self.make_request("DELETE", f"/api/agents/skills/{skill_id}")
            except:
                pass
                
        await self.cleanup_session()
        
    async def test_get_agent_types(self):
        """Test retrieving available agent types"""
        response = await self.make_request("GET", "/api/agents/types")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        assert "data" in response["data"], "Response should contain data field"
        
        types = response["data"]["data"]
        assert isinstance(types, list), "Agent types should be a list"
        assert len(types) > 0, "Should have at least one agent type"
        
        # Check expected agent types
        expected_types = ["code_architect", "security_expert", "performance_optimizer", "data_analyst", "infrastructure_manager", "custom"]
        for expected in expected_types:
            assert expected in types, f"Should contain {expected} agent type"
            
    async def test_create_agent(self):
        """Test creating a new agent"""
        agent_data = {
            "name": "TestAgent",
            "type": "code_architect",
            "description": "Test agent for automated testing",
            "configuration": {
                "priority_level": "normal",
                "max_concurrent_tasks": 3,
                "auto_start": True
            },
            "skills": ["code_analysis", "architecture_design"]
        }
        
        response = await self.make_request("POST", "/api/agents", data=agent_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        assert "data" in response["data"], "Response should contain data field"
        
        created_agent = response["data"]["data"]
        assert created_agent["name"] == agent_data["name"]
        assert created_agent["type"] == agent_data["type"]
        assert "id" in created_agent, "Created agent should have an ID"
        
        # Store for cleanup
        self.created_agents.append(created_agent["id"])
        
    async def test_get_agent_by_id(self):
        """Test retrieving specific agent by ID"""
        # First create an agent
        agent_data = {
            "name": "RetrievalTestAgent",
            "type": "data_analyst",
            "description": "Agent for retrieval testing"
        }
        
        create_response = await self.make_request("POST", "/api/agents", data=agent_data)
        agent_id = create_response["data"]["data"]["id"]
        self.created_agents.append(agent_id)
        
        # Now retrieve it
        response = await self.make_request("GET", f"/api/agents/{agent_id}")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        retrieved_agent = response["data"]["data"]
        assert retrieved_agent["id"] == agent_id
        assert retrieved_agent["name"] == agent_data["name"]
        
    async def test_update_agent(self):
        """Test updating an existing agent"""
        # Create agent first
        agent_data = {
            "name": "UpdateTestAgent",
            "type": "security_expert",
            "description": "Agent for update testing"
        }
        
        create_response = await self.make_request("POST", "/api/agents", data=agent_data)
        agent_id = create_response["data"]["data"]["id"]
        self.created_agents.append(agent_id)
        
        # Update the agent
        update_data = {
            "name": "UpdatedTestAgent",
            "description": "Updated agent description",
            "configuration": {
                "priority_level": "high",
                "max_concurrent_tasks": 5
            }
        }
        
        response = await self.make_request("PUT", f"/api/agents/{agent_id}", data=update_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        updated_agent = response["data"]["data"]
        assert updated_agent["name"] == update_data["name"]
        assert updated_agent["description"] == update_data["description"]
        
    async def test_list_agents(self):
        """Test listing all agents with pagination"""
        response = await self.make_request("GET", "/api/agents")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        assert "data" in response["data"], "Response should contain data field"
        
        agents_data = response["data"]["data"]
        assert isinstance(agents_data, list), "Agents data should be a list"
        
    async def test_agent_skills_management(self):
        """Test agent skills assignment and management"""
        # Create a skill first
        skill_data = {
            "name": "test_skill",
            "description": "A test skill for agent testing",
            "category": "development",
            "difficulty": "intermediate",
            "requirements": ["python", "api_testing"]
        }
        
        skill_response = await self.make_request("POST", "/api/agents/skills", data=skill_data)
        assert skill_response["status_code"] == 201, f"Expected 201, got {skill_response['status_code']}"
        
        skill_id = skill_response["data"]["data"]["id"]
        self.created_skills.append(skill_id)
        
        # Create agent
        agent_data = {
            "name": "SkillTestAgent",
            "type": "code_architect",
            "description": "Agent for skill testing"
        }
        
        agent_response = await self.make_request("POST", "/api/agents", data=agent_data)
        agent_id = agent_response["data"]["data"]["id"]
        self.created_agents.append(agent_id)
        
        # Assign skill to agent
        assign_response = await self.make_request("POST", f"/api/agents/{agent_id}/skills", 
                                                 data={"skill_ids": [skill_id]})
        
        assert assign_response["status_code"] == 200, f"Expected 200, got {assign_response['status_code']}"
        
    async def test_agent_statistics(self):
        """Test retrieving agent performance statistics"""
        response = await self.make_request("GET", "/api/agents/statistics")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        stats = response["data"]["data"]
        assert "total_agents" in stats, "Should contain total agents count"
        assert "active_agents" in stats, "Should contain active agents count"
        assert "agent_types" in stats, "Should contain agent types breakdown"
        
    async def test_agent_patterns(self):
        """Test agent pattern management"""
        pattern_data = {
            "name": "test_coordination_pattern",
            "type": "coordination",
            "description": "A test coordination pattern",
            "configuration": {
                "strategy": "sequential",
                "timeout": 300,
                "retry_count": 3
            }
        }
        
        response = await self.make_request("POST", "/api/agents/patterns", data=pattern_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        # Test retrieving patterns
        get_response = await self.make_request("GET", "/api/agents/patterns")
        assert get_response["status_code"] == 200
        
    async def test_agent_execution(self):
        """Test agent task execution"""
        # Create agent first
        agent_data = {
            "name": "ExecutionTestAgent",
            "type": "code_architect",
            "description": "Agent for execution testing",
            "configuration": {
                "auto_start": True
            }
        }
        
        create_response = await self.make_request("POST", "/api/agents", data=agent_data)
        agent_id = create_response["data"]["data"]["id"]
        self.created_agents.append(agent_id)
        
        # Execute a simple task
        task_data = {
            "task_type": "code_review",
            "description": "Review test code",
            "parameters": {
                "code_snippet": "def test_function(): return True",
                "language": "python"
            }
        }
        
        response = await self.make_request("POST", f"/api/agents/{agent_id}/execute", data=task_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
    async def test_agent_health_check(self):
        """Test agent health monitoring"""
        response = await self.make_request("GET", "/api/agents/health")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        health_data = response["data"]["data"]
        assert "status" in health_data, "Should contain overall status"
        assert "agents_status" in health_data, "Should contain agents status"
        
    async def test_professional_skills(self):
        """Test professional skills catalog"""
        response = await self.make_request("GET", "/api/agents/professional-skills")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        skills = response["data"]["data"]
        assert isinstance(skills, list), "Professional skills should be a list"
        
        # Check for expected skill categories
        skill_names = [skill["name"] for skill in skills if isinstance(skill, dict)]
        expected_skills = ["code_analysis", "debugging", "security_audit", "performance_analysis"]
        
        for expected in expected_skills:
            assert any(expected in name for name in skill_names), f"Should contain skill related to {expected}"

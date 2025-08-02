"""
FOCUSED AGENT AND SKILLS TESTING
Tests agent creation, skills management, and execution with proper data structures
"""

import sys
import os
import time
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_utils import ComprehensiveAPITester

class FocusedAgentSkillsTester:
    def __init__(self):
        test_dir = Path(__file__).parent.parent
        config_path = test_dir.parent.parent / "shared_config.yaml"
        
        self.tester = ComprehensiveAPITester(
            config_path=str(config_path),
            phase_name="focused_agent_skills",
            test_dir=str(test_dir)
        )
        
        self.created_agents = []
        self.test_results = []
    
    def test_agent_types(self):
        """Test getting available agent types"""
        print("🔍 Testing Agent Types...")
        
        response = self.tester.make_api_call(
            method="GET",
            endpoint="/api/agents/types",
            expected_status=[200, 404]
        )
        
        if response and response.get('status_code') == 200:
            types_data = response.get('data', {})
            available_types = types_data.get('types', [])
            print(f"   ✅ Found {len(available_types)} agent types: {available_types}")
            return available_types
        else:
            print("   ❌ Failed to get agent types")
            return []
    
    def test_agent_creation(self, agent_type="custom"):
        """Test creating a proper agent with valid data"""
        print(f"🤖 Testing Agent Creation (type: {agent_type})...")
        
        agent_data = {
            "name": f"Test Agent {int(time.time())}",
            "agent_type": agent_type,
            "description": "Test agent for focused testing",
            "capabilities": ["testing", "automation"],
            "configuration": {
                "max_concurrent_tasks": 3,
                "timeout_seconds": 30
            }
        }
        
        response = self.tester.make_api_call(
            method="POST",
            endpoint="/api/agents/",
            data=agent_data,
            expected_status=[200, 201]
        )
        
        if response and response.get('status_code') in [200, 201]:
            agent_id = response.get('data', {}).get('id')
            if agent_id:
                self.created_agents.append(agent_id)
                print(f"   ✅ Created agent ID: {agent_id}")
                return agent_id
            else:
                print("   ⚠️ Agent created but no ID returned")
                return None
        else:
            print(f"   ❌ Failed to create agent: {response.get('status_code') if response else 'No response'}")
            return None
    
    def test_agent_skills(self, agent_id):
        """Test adding skills to an agent"""
        print(f"🛠️ Testing Skills Management for Agent {agent_id}...")
        
        # Test getting current skills
        response = self.tester.make_api_call(
            method="GET",
            endpoint=f"/api/agents/{agent_id}/skills",
            expected_status=[200, 404]
        )
        
        if response:
            print(f"   📋 Current skills status: {response.get('status_code')}")
        
        # Test adding a skill
        skill_data = {
            "name": "Python Programming",
            "description": "Ability to write and execute Python code",
            "skill_type": "programming",
            "proficiency_level": "expert",
            "metadata": {
                "languages": ["python"],
                "frameworks": ["fastapi", "django"]
            }
        }
        
        response = self.tester.make_api_call(
            method="POST",
            endpoint=f"/api/agents/{agent_id}/skills",
            data=skill_data,
            expected_status=[200, 201, 404]
        )
        
        if response and response.get('status_code') in [200, 201]:
            print(f"   ✅ Successfully added skill to agent {agent_id}")
            return True
        else:
            print(f"   ❌ Failed to add skill: {response.get('status_code') if response else 'No response'}")
            return False
    
    def test_agent_execution(self, agent_id):
        """Test agent execution capabilities"""
        print(f"⚡ Testing Agent Execution for Agent {agent_id}...")
        
        # Test getting agent status
        response = self.tester.make_api_call(
            method="GET",
            endpoint=f"/api/agents/{agent_id}/status",
            expected_status=[200, 404]
        )
        
        if response:
            print(f"   📊 Agent status: {response.get('status_code')}")
        
        # Test executing a simple task
        execution_data = {
            "task": "Simple test task",
            "task_type": "test",
            "parameters": {
                "message": "Hello from focused test"
            }
        }
        
        response = self.tester.make_api_call(
            method="POST",
            endpoint=f"/api/agents/{agent_id}/execute",
            data=execution_data,
            expected_status=[200, 201, 202, 404]
        )
        
        if response and response.get('status_code') in [200, 201, 202]:
            print(f"   ✅ Agent execution initiated successfully")
            return True
        else:
            print(f"   ❌ Failed to execute agent: {response.get('status_code') if response else 'No response'}")
            return False
    
    def test_agent_retrieval(self, agent_id):
        """Test retrieving specific agent details"""
        print(f"📖 Testing Agent Retrieval for Agent {agent_id}...")
        
        response = self.tester.make_api_call(
            method="GET",
            endpoint=f"/api/agents/{agent_id}",
            expected_status=[200, 404]
        )
        
        if response and response.get('status_code') == 200:
            agent_data = response.get('data', {})
            print(f"   ✅ Retrieved agent: {agent_data.get('name', 'Unknown')}")
            return True
        else:
            print(f"   ❌ Failed to retrieve agent: {response.get('status_code') if response else 'No response'}")
            return False
    
    def cleanup_agents(self):
        """Clean up created agents"""
        print(f"🧹 Cleaning up {len(self.created_agents)} created agents...")
        
        for agent_id in self.created_agents:
            response = self.tester.make_api_call(
                method="DELETE",
                endpoint=f"/api/agents/{agent_id}",
                expected_status=[200, 204, 404]
            )
            
            if response and response.get('status_code') in [200, 204]:
                print(f"   ✅ Deleted agent {agent_id}")
            else:
                print(f"   ⚠️ Could not delete agent {agent_id}")
    
    def run_focused_tests(self):
        """Run all focused agent and skills tests"""
        print("🚀 STARTING FOCUSED AGENT & SKILLS TESTING")
        print("=" * 50)
        
        try:
            # Test 1: Get available agent types
            agent_types = self.test_agent_types()
            
            # Test 2: Create agents with different types
            test_types = ["custom", "code_architect"] if agent_types else ["custom"]
            
            for agent_type in test_types[:2]:  # Test max 2 types
                agent_id = self.test_agent_creation(agent_type)
                
                if agent_id:
                    # Test 3: Agent retrieval
                    self.test_agent_retrieval(agent_id)
                    
                    # Test 4: Skills management
                    self.test_agent_skills(agent_id)
                    
                    # Test 5: Agent execution
                    self.test_agent_execution(agent_id)
            
            # Generate summary
            self.generate_summary()
            
        finally:
            # Cleanup
            self.cleanup_agents()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n📊 FOCUSED AGENT & SKILLS TEST SUMMARY")
        print("=" * 40)
        print(f"🤖 Agents Created: {len(self.created_agents)}")
        print(f"📝 Total API Calls: {len(self.tester.api_call_history)}")
        
        successful_calls = sum(1 for call in self.tester.api_call_history 
                              if call.get('validation', {}).get('is_success', False))
        success_rate = (successful_calls / len(self.tester.api_call_history) * 100) if self.tester.api_call_history else 0
        
        print(f"✅ Successful Calls: {successful_calls}")
        print(f"❌ Failed Calls: {len(self.tester.api_call_history) - successful_calls}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 70:
        else:

if __name__ == "__main__":
    tester = FocusedAgentSkillsTester()
    tester.run_focused_tests()

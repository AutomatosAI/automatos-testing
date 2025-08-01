import random
import string
from datetime import datetime
from typing import Dict, Any

class TestDataGenerator:
    """Generate realistic test data for Automotas AI workflow testing"""
    
    @staticmethod
    def random_string(length: int = 8, prefix: str = "") -> str:
        """Generate random string for unique identifiers"""
        chars = string.ascii_lowercase + string.digits
        random_part = ''.join(random.choices(chars, k=length))
        return f"{prefix}{random_part}" if prefix else random_part
    
    @staticmethod
    def random_email() -> str:
        """Generate random email"""
        username = TestDataGenerator.random_string(8)
        domains = ["test.com", "example.org", "automotas.dev"]
        return f"{username}@{random.choice(domains)}"
    
    @staticmethod
    def timestamp() -> str:
        """Generate current timestamp"""
        return datetime.now().isoformat()

class AgentDataGenerator:
    """Generate test data for agent management"""
    
    AGENT_TYPES = [
        "code_architect",
        "security_expert", 
        "performance_optimizer",
        "data_analyst",
        "infrastructure_manager"
    ]
    
    PRIORITY_LEVELS = ["low", "medium", "high", "critical"]
    
    @classmethod
    def create_agent_data(cls, agent_type: str = None, name: str = None) -> Dict[str, Any]:
        """Generate data for creating an agent"""
        
        if not agent_type:
            agent_type = random.choice(cls.AGENT_TYPES)
        
        if not name:
            name = f"TestAgent_{TestDataGenerator.random_string(6)}"
        
        return {
            "name": name,
            "description": f"Test agent for {agent_type} operations - created for journey testing",
            "agent_type": agent_type,
            "configuration": {
                "test_mode": True,
                "created_by": "journey_test",
                "environment": "testing"
            },
            "priority_level": random.choice(cls.PRIORITY_LEVELS),
            "max_concurrent_tasks": random.randint(1, 10)
        }
    
    @classmethod
    def update_agent_data(cls, existing_agent: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for updating an agent"""
        return {
            "description": f"Updated description at {TestDataGenerator.timestamp()}",
            "priority_level": random.choice(cls.PRIORITY_LEVELS),
            "max_concurrent_tasks": random.randint(5, 15),
            "configuration": {
                **existing_agent.get("configuration", {}),
                "last_updated": TestDataGenerator.timestamp(),
                "test_update": True
            }
        }

class SkillDataGenerator:
    """Generate test data for skills management"""
    
    SKILL_CATEGORIES = ["development", "security", "infrastructure", "analytics"]
    SKILL_TYPES = ["cognitive", "technical", "communication"]
    
    @classmethod
    def create_skill_data(cls, name: str = None, category: str = None) -> Dict[str, Any]:
        """Generate data for creating a skill"""
        
        if not name:
            name = f"TestSkill_{TestDataGenerator.random_string(6)}"
        
        if not category:
            category = random.choice(cls.SKILL_CATEGORIES)
        
        return {
            "name": name,
            "description": f"Test skill for {category} - created during journey testing",
            "skill_type": random.choice(cls.SKILL_TYPES),
            "category": category,
            "implementation": f"test_implementation_{TestDataGenerator.random_string(4)}",
            "parameters": {
                "test_mode": True,
                "complexity": random.choice(["beginner", "intermediate", "advanced"]),
                "estimated_time_minutes": random.randint(5, 60)
            }
        }

class WorkflowDataGenerator:
    """Generate test data for workflow management"""
    
    WORKFLOW_TYPES = [
        "data_processing",
        "code_analysis", 
        "security_audit",
        "performance_optimization",
        "system_monitoring"
    ]
    
    @classmethod
    def create_workflow_data(cls, name: str = None, workflow_type: str = None) -> Dict[str, Any]:
        """Generate data for creating a workflow"""
        
        if not name:
            name = f"TestWorkflow_{TestDataGenerator.random_string(6)}"
        
        if not workflow_type:
            workflow_type = random.choice(cls.WORKFLOW_TYPES)
        
        return {
            "name": name,
            "description": f"Test workflow for {workflow_type} - created during journey testing",
            "workflow_type": workflow_type,
            "configuration": {
                "test_mode": True,
                "created_by": "journey_test",
                "environment": "testing",
                "auto_start": False,
                "timeout_minutes": 30
            },
            "steps": [
                {
                    "step_id": "init",
                    "step_name": "Initialize workflow",
                    "step_type": "initialization",
                    "parameters": {"setup": True}
                },
                {
                    "step_id": "process", 
                    "step_name": "Process data",
                    "step_type": "processing",
                    "parameters": {"process_type": workflow_type}
                },
                {
                    "step_id": "finalize",
                    "step_name": "Finalize workflow", 
                    "step_type": "finalization",
                    "parameters": {"cleanup": True}
                }
            ],
            "metadata": {
                "priority": random.choice(["low", "medium", "high"]),
                "estimated_duration_minutes": random.randint(5, 60),
                "created_at": TestDataGenerator.timestamp()
            }
        }
    
    @classmethod
    def workflow_execution_data(cls) -> Dict[str, Any]:
        """Generate data for workflow execution"""
        return {
            "execution_mode": "test",
            "parameters": {
                "test_run": True,
                "notify_completion": False,
                "timeout_seconds": 120,
                "max_retries": 3
            },
            "metadata": {
                "triggered_by": "journey_test",
                "execution_time": TestDataGenerator.timestamp(),
                "test_execution": True
            }
        }

# Convenience class for easy access to all generators
class TestData:
    """Convenience class providing access to all data generators"""
    
    Agent = AgentDataGenerator
    Skill = SkillDataGenerator
    Workflow = WorkflowDataGenerator
    WorkflowNew = WorkflowDataGenerator  # Alias for consistency
    
    @staticmethod
    def random_string(length: int = 8, prefix: str = "") -> str:
        return TestDataGenerator.random_string(length, prefix)
    
    @staticmethod
    def random_email() -> str:
        return TestDataGenerator.random_email()
    
    @staticmethod
    def timestamp() -> str:
        return TestDataGenerator.timestamp()

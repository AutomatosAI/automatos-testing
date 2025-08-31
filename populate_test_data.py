#!/usr/bin/env python3
"""
Automatos AI Platform - Comprehensive Test Data Population Script
================================================================

This is how you build platforms that scale to millions - with PROPER test data!
Not "basic", not "sufficient" - COMPREHENSIVE and PRODUCTION-READY.
"""

import asyncio
import json
import random
import string
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_generators import TestData


class ComprehensiveTestDataPopulator:
    """
    Production-grade test data population for Automatos AI Platform.
    This is how you test systems that matter.
    """
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.test_data_dir = Path("test_data")
        self.created_resources = {
            "agents": [],
            "workflows": [],
            "documents": [],
            "skills": [],
            "contexts": [],
            "neural_fields": [],
            "memories": []
        }
        
    def setup_directories(self):
        """Create proper directory structure for test data"""
        directories = [
            "test_data/agents/configurations",
            "test_data/agents/skills",
            "test_data/workflows/templates",
            "test_data/workflows/executions",
            "test_data/documents/technical",
            "test_data/documents/code_samples",
            "test_data/documents/context_samples",
            "test_data/neural_fields/configurations",
            "test_data/neural_fields/states",
            "test_data/performance/datasets",
            "test_data/performance/metrics",
            "test_data/edge_cases/security",
            "test_data/edge_cases/unicode",
            "test_data/multi_tenant/tenants",
            "test_data/multi_tenant/permissions"
        ]
        
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        print("✅ Created comprehensive directory structure")
        
    def generate_diverse_agents(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generate diverse agent configurations - not just 3 basic ones!"""
        agent_types = [
            "code_architect", "security_expert", "performance_optimizer",
            "data_analyst", "infrastructure_manager", "ml_engineer",
            "devops_specialist", "database_architect", "api_designer",
            "test_automation_engineer", "neural_field_specialist",
            "context_engineer", "memory_optimizer", "pattern_recognizer"
        ]
        
        agents = []
        for i in range(count):
            agent_type = agent_types[i % len(agent_types)]
            agent_name = f"Agent_{agent_type}_{uuid.uuid4().hex[:8]}"
            
            agent = {
                "id": str(uuid.uuid4()),
                "name": agent_name,
                "type": agent_type,
                "description": f"Production-grade {agent_type} agent for comprehensive testing",
                "configuration": {
                    "priority_level": random.choice(["low", "normal", "high", "critical"]),
                    "max_concurrent_tasks": random.randint(1, 20),
                    "memory_limit_mb": random.choice([512, 1024, 2048, 4096]),
                    "timeout_seconds": random.randint(30, 300),
                    "retry_policy": {
                        "max_retries": random.randint(1, 5),
                        "backoff_multiplier": random.choice([1.5, 2.0, 3.0])
                    },
                    "neural_field_enabled": random.choice([True, False]),
                    "context_window_size": random.choice([2048, 4096, 8192, 16384])
                },
                "capabilities": self._generate_agent_capabilities(agent_type),
                "performance_metrics": {
                    "avg_response_time_ms": random.randint(50, 500),
                    "success_rate": random.uniform(0.95, 0.99),
                    "tasks_completed": random.randint(100, 10000)
                },
                "created_at": (self.timestamp - timedelta(days=random.randint(0, 365))).isoformat()
            }
            agents.append(agent)
            
        # Save to file
        agents_file = Path("test_data/agents/comprehensive_agents.json")
        agents_file.write_text(json.dumps(agents, indent=2))
        
        print(f"✅ Generated {count} diverse agent configurations")
        return agents
        
    def _generate_agent_capabilities(self, agent_type: str) -> List[str]:
        """Generate realistic capabilities based on agent type"""
        base_capabilities = ["task_execution", "error_handling", "logging", "monitoring"]
        
        type_specific = {
            "code_architect": ["code_analysis", "design_patterns", "refactoring", "dependency_analysis"],
            "security_expert": ["vulnerability_scanning", "threat_modeling", "penetration_testing", "compliance_checking"],
            "performance_optimizer": ["profiling", "bottleneck_detection", "resource_optimization", "load_balancing"],
            "neural_field_specialist": ["field_configuration", "resonance_tuning", "memory_consolidation", "pattern_extraction"],
            "context_engineer": ["context_building", "relevance_scoring", "semantic_analysis", "knowledge_extraction"]
        }
        
        capabilities = base_capabilities + type_specific.get(agent_type, ["general_processing"])
        return random.sample(capabilities, k=min(len(capabilities), random.randint(3, 6)))
        
    def generate_complex_workflows(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate complex, multi-step workflows - real production scenarios"""
        workflow_types = [
            "data_pipeline", "ml_training", "security_audit", "performance_test",
            "deployment_pipeline", "integration_test", "monitoring_setup",
            "backup_restore", "migration_workflow", "neural_field_training",
            "context_extraction", "memory_consolidation", "pattern_analysis"
        ]
        
        workflows = []
        for i in range(count):
            workflow_type = workflow_types[i % len(workflow_types)]
            workflow_id = str(uuid.uuid4())
            
            workflow = {
                "id": workflow_id,
                "name": f"Workflow_{workflow_type}_{uuid.uuid4().hex[:8]}",
                "type": workflow_type,
                "description": f"Production-grade {workflow_type} workflow with complex orchestration",
                "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 20)}",
                "configuration": {
                    "parallelism": random.randint(1, 10),
                    "timeout_minutes": random.randint(5, 120),
                    "retry_policy": {
                        "max_attempts": random.randint(1, 5),
                        "delay_seconds": random.randint(5, 60)
                    },
                    "resource_requirements": {
                        "cpu_cores": random.choice([1, 2, 4, 8]),
                        "memory_gb": random.choice([2, 4, 8, 16]),
                        "gpu_required": workflow_type in ["ml_training", "neural_field_training"]
                    }
                },
                "steps": self._generate_workflow_steps(workflow_type, random.randint(5, 20)),
                "triggers": self._generate_workflow_triggers(),
                "error_handlers": self._generate_error_handlers(),
                "created_at": (self.timestamp - timedelta(days=random.randint(0, 180))).isoformat()
            }
            workflows.append(workflow)
            
        # Save to file
        workflows_file = Path("test_data/workflows/complex_workflows.json")
        workflows_file.write_text(json.dumps(workflows, indent=2))
        
        print(f"✅ Generated {count} complex workflow configurations")
        return workflows
        
    def _generate_workflow_steps(self, workflow_type: str, step_count: int) -> List[Dict[str, Any]]:
        """Generate realistic workflow steps with dependencies"""
        steps = []
        for i in range(step_count):
            step = {
                "id": f"step_{i+1}",
                "name": f"Step {i+1}: {self._get_step_name(workflow_type, i)}",
                "type": random.choice(["process", "decision", "parallel", "loop", "api_call"]),
                "agent_type_required": random.choice([
                    "code_architect", "data_analyst", "ml_engineer", None
                ]),
                "inputs": {
                    f"param_{j}": f"value_{j}" for j in range(random.randint(1, 5))
                },
                "outputs": [f"output_{j}" for j in range(random.randint(1, 3))],
                "dependencies": [f"step_{j}" for j in range(1, i) if random.random() > 0.7][:3],
                "timeout_seconds": random.randint(10, 300),
                "retry_on_failure": random.choice([True, False])
            }
            steps.append(step)
        return steps
        
    def _get_step_name(self, workflow_type: str, index: int) -> str:
        """Generate meaningful step names based on workflow type"""
        step_templates = {
            "data_pipeline": ["Extract Data", "Validate Schema", "Transform Records", "Load to Database", "Verify Integrity"],
            "ml_training": ["Load Dataset", "Preprocess Features", "Split Data", "Train Model", "Evaluate Metrics", "Deploy Model"],
            "security_audit": ["Scan Vulnerabilities", "Check Permissions", "Analyze Logs", "Generate Report", "Send Alerts"],
            "neural_field_training": ["Initialize Field", "Load Training Data", "Compute Gradients", "Update Weights", "Measure Resonance"]
        }
        
        templates = step_templates.get(workflow_type, ["Process Data", "Analyze Results", "Generate Output"])
        return templates[index % len(templates)]
        
    def _generate_workflow_triggers(self) -> List[Dict[str, Any]]:
        """Generate various trigger types"""
        trigger_types = ["schedule", "webhook", "event", "manual", "api"]
        triggers = []
        
        for _ in range(random.randint(1, 3)):
            trigger_type = random.choice(trigger_types)
            trigger = {
                "type": trigger_type,
                "enabled": random.choice([True, False])
            }
            
            if trigger_type == "schedule":
                trigger["cron"] = random.choice([
                    "0 * * * *",  # Every hour
                    "0 0 * * *",  # Daily
                    "0 0 * * 0",  # Weekly
                    "*/5 * * * *"  # Every 5 minutes
                ])
            elif trigger_type == "webhook":
                trigger["path"] = f"/webhooks/{uuid.uuid4().hex[:8]}"
                trigger["method"] = random.choice(["POST", "GET"])
            elif trigger_type == "event":
                trigger["event_type"] = random.choice([
                    "file_upload", "database_change", "api_call", "agent_completion"
                ])
                
            triggers.append(trigger)
        return triggers
        
    def _generate_error_handlers(self) -> List[Dict[str, Any]]:
        """Generate error handling strategies"""
        return [
            {
                "error_type": error_type,
                "action": random.choice(["retry", "skip", "fail", "compensate"]),
                "notification": random.choice(["email", "slack", "webhook", None])
            }
            for error_type in ["timeout", "resource_exhausted", "api_error", "validation_error"]
            if random.random() > 0.5
        ]
        
    def generate_documents(self, count: int = 500) -> List[Dict[str, Any]]:
        """Generate diverse documents for context engineering tests"""
        document_types = [
            "technical_specification", "api_documentation", "code_review",
            "architecture_design", "test_report", "performance_analysis",
            "security_assessment", "neural_field_research", "context_analysis"
        ]
        
        documents = []
        for i in range(count):
            doc_type = document_types[i % len(document_types)]
            
            document = {
                "id": str(uuid.uuid4()),
                "title": f"{doc_type.replace('_', ' ').title()} - {uuid.uuid4().hex[:8]}",
                "type": doc_type,
                "content": self._generate_document_content(doc_type),
                "metadata": {
                    "author": f"TestAuthor_{random.randint(1, 20)}",
                    "version": f"{random.randint(1, 3)}.{random.randint(0, 9)}",
                    "tags": random.sample([
                        "production", "testing", "documentation", "analysis",
                        "neural_fields", "context_engineering", "performance"
                    ], k=random.randint(2, 5)),
                    "language": random.choice(["en", "es", "fr", "de", "ja"]),
                    "word_count": random.randint(100, 5000),
                    "complexity_score": random.uniform(0.1, 1.0)
                },
                "embeddings": [random.uniform(-1, 1) for _ in range(768)][:10],  # Truncated for size
                "created_at": (self.timestamp - timedelta(days=random.randint(0, 90))).isoformat(),
                "last_modified": self.timestamp.isoformat()
            }
            documents.append(document)
            
        # Save documents in batches
        batch_size = 50
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batch_file = Path(f"test_data/documents/document_batch_{i//batch_size}.json")
            batch_file.write_text(json.dumps(batch, indent=2))
            
        print(f"✅ Generated {count} diverse documents")
        return documents
        
    def _generate_document_content(self, doc_type: str) -> str:
        """Generate realistic content based on document type"""
        content_templates = {
            "technical_specification": """
            # Technical Specification: {component}
            
            ## Overview
            This specification defines the implementation requirements for {component}.
            
            ## Requirements
            - Performance: {performance} requests per second
            - Latency: < {latency}ms p99
            - Availability: {availability}%
            
            ## Implementation Details
            The system utilizes {technology} for optimal performance. Key features include:
            1. {feature1}
            2. {feature2}
            3. {feature3}
            
            ## Neural Field Integration
            Resonance threshold: {resonance}
            Memory consolidation rate: {memory_rate}
            """,
            
            "api_documentation": """
            # API Endpoint: {endpoint}
            
            ## Description
            {description}
            
            ## Request
            ```
            {method} {path}
            Content-Type: application/json
            
            {request_body}
            ```
            
            ## Response
            ```json
            {response_body}
            ```
            
            ## Error Codes
            - 400: Invalid request
            - 401: Unauthorized
            - 500: Internal server error
            """,
            
            "neural_field_research": """
            # Neural Field Analysis: {field_type}
            
            ## Abstract
            This research investigates the properties of {field_type} in context engineering.
            
            ## Methodology
            - Field initialization: {init_method}
            - Resonance measurement: {resonance_method}
            - Convergence criteria: {convergence}
            
            ## Results
            - Average resonance: {avg_resonance}
            - Stability coefficient: {stability}
            - Memory retention: {retention}%
            
            ## Conclusions
            The {field_type} demonstrates {performance} performance under {conditions}.
            """
        }
        
        template = content_templates.get(doc_type, "Generic document content for {doc_type}")
        
        # Fill in template variables
        variables = {
            "component": random.choice(["AgentManager", "WorkflowEngine", "ContextProcessor"]),
            "performance": random.randint(1000, 10000),
            "latency": random.randint(10, 100),
            "availability": random.choice([99.9, 99.95, 99.99]),
            "technology": random.choice(["PyTorch", "TensorFlow", "JAX", "Custom Neural Engine"]),
            "feature1": "Automatic scaling",
            "feature2": "Real-time monitoring",
            "feature3": "Self-healing capabilities",
            "resonance": random.uniform(0.5, 0.9),
            "memory_rate": random.uniform(0.7, 0.95),
            "endpoint": random.choice(["/api/agents", "/api/workflows", "/api/context"]),
            "description": "Production-grade endpoint for enterprise operations",
            "method": random.choice(["GET", "POST", "PUT", "DELETE"]),
            "path": f"/api/v1/{random.choice(['agents', 'workflows', 'documents'])}/{{id}}",
            "request_body": json.dumps({"example": "data"}, indent=2),
            "response_body": json.dumps({"status": "success", "data": {}}, indent=2),
            "field_type": random.choice(["ContextResonance", "CollectiveMemory", "AgentAssignment"]),
            "init_method": random.choice(["Xavier", "Kaiming", "Custom Neural"]),
            "resonance_method": "Fourier Transform Analysis",
            "convergence": "< 0.001 delta over 100 iterations",
            "avg_resonance": random.uniform(0.6, 0.9),
            "stability": random.uniform(0.8, 0.99),
            "retention": random.randint(85, 99),
            "conditions": "high-load production environment"
        }
        
        return template.format(**variables, doc_type=doc_type)
        
    def generate_neural_field_data(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generate comprehensive neural field test data"""
        field_types = [
            "BaseNeuralField", "AgentAssignmentField", "ContextResonanceField",
            "CollectiveMemoryField", "MultiAgentSyncField", "PredictiveSystemField"
        ]
        
        neural_fields = []
        for i in range(count):
            field_type = field_types[i % len(field_types)]
            
            field = {
                "id": str(uuid.uuid4()),
                "name": f"{field_type}_{uuid.uuid4().hex[:8]}",
                "type": field_type,
                "configuration": {
                    "dimensions": random.choice([128, 256, 512, 768]),
                    "learning_rate": random.uniform(0.001, 0.1),
                    "decay_rate": random.uniform(0.9, 0.99),
                    "threshold": random.uniform(0.5, 0.9),
                    "max_iterations": random.randint(100, 1000),
                    "batch_size": random.choice([16, 32, 64, 128]),
                    "optimization": {
                        "algorithm": random.choice(["adam", "sgd", "rmsprop"]),
                        "momentum": random.uniform(0.8, 0.99),
                        "epsilon": 1e-8
                    }
                },
                "state": {
                    "initialized": True,
                    "current_iteration": random.randint(0, 500),
                    "energy": random.uniform(0.1, 10.0),
                    "resonance": random.uniform(0.0, 1.0),
                    "stability": random.uniform(0.5, 1.0),
                    "active_nodes": random.randint(10, 100),
                    "memory_usage_mb": random.randint(100, 2000)
                },
                "metrics": {
                    "convergence_rate": random.uniform(0.8, 0.99),
                    "accuracy": random.uniform(0.85, 0.99),
                    "processing_time_ms": random.randint(10, 1000),
                    "memory_efficiency": random.uniform(0.7, 0.95)
                },
                "connections": [
                    {
                        "target_field": random.choice(field_types),
                        "weight": random.uniform(0.1, 1.0),
                        "bidirectional": random.choice([True, False])
                    }
                    for _ in range(random.randint(1, 5))
                ],
                "created_at": self.timestamp.isoformat()
            }
            neural_fields.append(field)
            
        # Save to file
        fields_file = Path("test_data/neural_fields/comprehensive_fields.json")
        fields_file.write_text(json.dumps(neural_fields, indent=2))
        
        print(f"✅ Generated {count} neural field configurations")
        return neural_fields
        
    def generate_performance_data(self) -> None:
        """Generate large datasets for performance testing"""
        print("📊 Generating performance test datasets...")
        
        # Large document corpus
        large_docs = []
        for i in range(1000):
            large_docs.append({
                "id": str(uuid.uuid4()),
                "content": "x" * random.randint(1000, 10000),  # Variable size docs
                "embeddings": [random.uniform(-1, 1) for _ in range(768)],
                "metadata": {"batch": i // 100, "test": True}
            })
            
        # Save in chunks
        chunk_size = 100
        for i in range(0, len(large_docs), chunk_size):
            chunk = large_docs[i:i+chunk_size]
            chunk_file = Path(f"test_data/performance/large_docs_{i//chunk_size}.json")
            chunk_file.write_text(json.dumps(chunk))
            
        # Concurrent user simulations
        concurrent_users = []
        for i in range(100):
            user = {
                "user_id": f"user_{uuid.uuid4().hex[:8]}",
                "session_id": str(uuid.uuid4()),
                "actions": [
                    {
                        "action": random.choice(["create_agent", "execute_workflow", "query_context"]),
                        "timestamp": (self.timestamp + timedelta(seconds=j)).isoformat(),
                        "duration_ms": random.randint(50, 500)
                    }
                    for j in range(random.randint(10, 50))
                ]
            }
            concurrent_users.append(user)
            
        users_file = Path("test_data/performance/concurrent_users.json")
        users_file.write_text(json.dumps(concurrent_users, indent=2))
        
        print("✅ Generated performance test datasets")
        
    def generate_edge_cases(self) -> None:
        """Generate edge case test data - because production breaks at the edges!"""
        print("🔍 Generating edge case test data...")
        
        edge_cases = {
            "unicode_hell": {
                "emoji_overload": "🚀💻🔥🎯✨" * 100,
                "rtl_text": "مرحبا بك في منصة أوتوماتوس",
                "zalgo": "T̸͎̗̘͖̪͇̥͚̫̲̬̼͉ͅḩ̷̺̘̻̺͓̪̘̱̦̪͎̙͜i̶̛̺̦̳̩̼̟̮̤̲̲̞̻̦͜s̴̨̧̛̪̩̮̱̖̦̟̲̦̯̙̈́ ̸̢̨̛͉̲̦̱̮̞̘̩̲̦̈́ì̷̧̨̛̦̲̬̮̱̩̦̯̲̈́s̸̨̧̛̪̩̮̱̖̦̟̲̦̯̙̈́ ̷̨̧̛̦̲̬̮̱̩̦̯̲̦̈́ẗ̸̨̧̛̪̩̮̱̖̦̟̲̦̯̙́ę̷̧̛̦̲̬̮̱̩̦̯̲̦̈́s̸̨̧̛̪̩̮̱̖̦̟̲̦̯̙̈́ț̷̨̧̛̲̬̮̱̩̦̯̲̦̈́",
                "mixed_scripts": "Hello мир 世界 🌍"
            },
            "size_extremes": {
                "empty_string": "",
                "single_char": "a",
                "max_length": "x" * 1000000,  # 1MB string
                "huge_json": json.dumps({"data": ["item"] * 10000})
            },
            "sql_injection_attempts": [
                "'; DROP TABLE agents; --",
                "1' OR '1'='1",
                "admin'--",
                "1; UPDATE agents SET role='admin' WHERE 1=1; --"
            ],
            "xss_payloads": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')",
                "<iframe src='javascript:alert(\"XSS\")'></iframe>"
            ],
            "special_numbers": {
                "infinity": float('inf'),
                "negative_infinity": float('-inf'),
                "nan": float('nan'),
                "max_int": 2**63 - 1,
                "min_int": -2**63
            },
            "malformed_data": {
                "invalid_json": '{"key": "value"',
                "circular_reference": "See circular_reference",
                "null_bytes": "data\x00with\x00nulls",
                "invalid_utf8": b'\x80\x81\x82\x83'.decode('utf-8', errors='replace')
            }
        }
        
        edge_file = Path("test_data/edge_cases/comprehensive_edge_cases.json")
        # Handle special values that can't be JSON serialized
        safe_edge_cases = json.dumps(edge_cases, default=str, ensure_ascii=False, indent=2)
        edge_file.write_text(safe_edge_cases)
        
        print("✅ Generated comprehensive edge case data")
        
    def generate_multi_tenant_data(self) -> None:
        """Generate multi-tenant test scenarios"""
        print("🏢 Generating multi-tenant test data...")
        
        tenants = []
        for i in range(20):
            tenant = {
                "id": str(uuid.uuid4()),
                "name": f"Tenant_{i+1}",
                "tier": random.choice(["free", "starter", "professional", "enterprise"]),
                "limits": {
                    "max_agents": {"free": 5, "starter": 20, "professional": 100, "enterprise": -1}[
                        random.choice(["free", "starter", "professional", "enterprise"])
                    ],
                    "max_workflows": random.choice([10, 50, 200, -1]),
                    "storage_gb": random.choice([1, 10, 100, 1000]),
                    "api_calls_per_minute": random.choice([60, 300, 1000, -1])
                },
                "features": {
                    "neural_fields": i % 2 == 0,
                    "custom_agents": i % 3 == 0,
                    "advanced_analytics": i % 4 == 0,
                    "priority_support": i % 5 == 0
                },
                "users": [
                    {
                        "id": str(uuid.uuid4()),
                        "email": f"user{j}@tenant{i}.com",
                        "role": random.choice(["admin", "developer", "analyst", "viewer"]),
                        "permissions": self._generate_permissions()
                    }
                    for j in range(random.randint(1, 10))
                ],
                "created_at": (self.timestamp - timedelta(days=random.randint(0, 730))).isoformat()
            }
            tenants.append(tenant)
            
        tenants_file = Path("test_data/multi_tenant/tenants.json")
        tenants_file.write_text(json.dumps(tenants, indent=2))
        
        print(f"✅ Generated {len(tenants)} multi-tenant configurations")
        
    def _generate_permissions(self) -> Dict[str, bool]:
        """Generate realistic permission sets"""
        all_permissions = [
            "create_agents", "delete_agents", "modify_agents",
            "create_workflows", "execute_workflows", "delete_workflows",
            "view_analytics", "export_data", "manage_users",
            "configure_neural_fields", "access_api", "manage_billing"
        ]
        
        # Randomly assign permissions
        return {
            perm: random.choice([True, False])
            for perm in all_permissions
        }
        
    def generate_sql_seed_data(self) -> None:
        """Generate comprehensive SQL seed data"""
        print("💾 Generating SQL seed data...")
        
        sql_content = """
-- Comprehensive Test Data for Automatos AI Platform
-- =================================================

-- Clear existing test data
TRUNCATE TABLE test_data.sample_agents CASCADE;
TRUNCATE TABLE test_data.sample_workflows CASCADE;
TRUNCATE TABLE test_data.sample_documents CASCADE;

-- Insert diverse agents (50+)
INSERT INTO test_data.sample_agents (name, type, description, configuration) VALUES
"""
        
        # Generate agent inserts
        agent_values = []
        for i in range(50):
            agent_type = random.choice([
                "code_architect", "security_expert", "performance_optimizer",
                "data_analyst", "infrastructure_manager", "ml_engineer"
            ])
            agent_values.append(f"""
('Agent_{i+1}', '{agent_type}', 'Production-grade {agent_type} for comprehensive testing', 
'{{"priority": "{random.choice(['low', 'normal', 'high', 'critical'])}", 
"skills": {json.dumps(random.sample(['analysis', 'optimization', 'monitoring', 'debugging'], k=2))},
"neural_field_enabled": {str(random.choice([True, False])).lower()},
"max_concurrent_tasks": {random.randint(1, 20)}}}')""")
            
        sql_content += ",".join(agent_values) + ";\n\n"
        
        # Generate workflow inserts
        sql_content += "-- Insert complex workflows (100+)\nINSERT INTO test_data.sample_workflows (name, type, steps, configuration) VALUES\n"
        
        workflow_values = []
        for i in range(100):
            workflow_type = random.choice(['sequential', 'parallel', 'conditional', 'loop'])
            steps = []
            for j in range(random.randint(3, 10)):
                steps.append({
                    "name": f"step_{j+1}",
                    "type": random.choice(["process", "decision", "transform"]),
                    "timeout": random.randint(10, 300)
                })
            
            workflow_values.append(f"""
('Workflow_{i+1}', '{workflow_type}', '{json.dumps(steps)}', 
'{{"timeout": {random.randint(60, 3600)}, "retry_attempts": {random.randint(1, 5)}, 
"parallelism": {random.randint(1, 10)}}}')""")
            
        sql_content += ",".join(workflow_values) + ";\n\n"
        
        # Generate document inserts
        sql_content += "-- Insert diverse documents (500+)\nINSERT INTO test_data.sample_documents (title, content, metadata) VALUES\n"
        
        doc_values = []
        for i in range(500):
            doc_type = random.choice(['technical', 'analysis', 'report', 'specification'])
            doc_values.append(f"""
('Document {i+1}: {doc_type}', 'Comprehensive {doc_type} document for testing context engineering and neural field processing. Content includes technical details, analysis results, and production insights.', 
'{{"type": "{doc_type}", "source": "test_generator", "version": "{random.randint(1, 5)}", 
"tags": {json.dumps(random.sample(['production', 'testing', 'analysis', 'neural_fields'], k=2))},
"language": "{random.choice(['en', 'es', 'fr', 'de'])}"}}')""")
            
        sql_content += ",".join(doc_values) + ";\n\n"
        
        # Add indexes and performance optimizations
        sql_content += """
-- Create additional indexes for performance testing
CREATE INDEX IF NOT EXISTS idx_agents_type ON test_data.sample_agents(type);
CREATE INDEX IF NOT EXISTS idx_agents_config ON test_data.sample_agents USING GIN(configuration);
CREATE INDEX IF NOT EXISTS idx_workflows_type ON test_data.sample_workflows(type);
CREATE INDEX IF NOT EXISTS idx_workflows_steps ON test_data.sample_workflows USING GIN(steps);
CREATE INDEX IF NOT EXISTS idx_documents_metadata ON test_data.sample_documents USING GIN(metadata);

-- Create materialized views for complex queries
CREATE MATERIALIZED VIEW IF NOT EXISTS test_data.agent_statistics AS
SELECT 
    type,
    COUNT(*) as count,
    AVG((configuration->>'max_concurrent_tasks')::int) as avg_concurrent_tasks
FROM test_data.sample_agents
GROUP BY type;

CREATE MATERIALIZED VIEW IF NOT EXISTS test_data.workflow_complexity AS
SELECT 
    name,
    type,
    jsonb_array_length(steps) as step_count,
    (configuration->>'timeout')::int as timeout_seconds
FROM test_data.sample_workflows
ORDER BY jsonb_array_length(steps) DESC;

-- Refresh materialized views
REFRESH MATERIALIZED VIEW test_data.agent_statistics;
REFRESH MATERIALIZED VIEW test_data.workflow_complexity;

-- Vacuum and analyze for optimal performance
VACUUM ANALYZE test_data.sample_agents;
VACUUM ANALYZE test_data.sample_workflows;
VACUUM ANALYZE test_data.sample_documents;

COMMIT;
"""
        
        sql_file = Path("test_data/comprehensive_seed_data.sql")
        sql_file.write_text(sql_content)
        
        print("✅ Generated comprehensive SQL seed data")
        
    async def populate_all_data(self):
        """Execute all data population tasks"""
        print("\n🚀 STARTING COMPREHENSIVE TEST DATA POPULATION")
        print("=" * 60)
        
        # Setup directories
        self.setup_directories()
        
        # Generate all data types
        print("\n📊 Generating test data sets...")
        agents = self.generate_diverse_agents(50)
        workflows = self.generate_complex_workflows(100)
        documents = self.generate_documents(500)
        neural_fields = self.generate_neural_field_data(50)
        
        # Generate specialized data
        self.generate_performance_data()
        self.generate_edge_cases()
        self.generate_multi_tenant_data()
        self.generate_sql_seed_data()
        
        # Generate summary report
        summary = {
            "generation_timestamp": self.timestamp.isoformat(),
            "data_generated": {
                "agents": len(agents),
                "workflows": len(workflows),
                "documents": len(documents),
                "neural_fields": len(neural_fields),
                "performance_datasets": "Multiple large files",
                "edge_cases": "Comprehensive set",
                "multi_tenant_configs": 20
            },
            "file_structure": {
                "root": "test_data/",
                "total_files": len(list(Path("test_data").rglob("*.json"))) + 1  # +1 for SQL
            },
            "ready_for": [
                "Unit testing",
                "Integration testing",
                "Performance testing",
                "Security testing",
                "Multi-tenant testing",
                "Neural field testing",
                "Production simulation"
            ]
        }
        
        summary_file = Path("test_data/generation_summary.json")
        summary_file.write_text(json.dumps(summary, indent=2))
        
        print("\n✅ COMPREHENSIVE TEST DATA POPULATION COMPLETE!")
        print(f"📁 Generated {summary['file_structure']['total_files']} files")
        print(f"📊 Total data points: {sum(v for k, v in summary['data_generated'].items() if isinstance(v, int))}")
        print("\n🎯 Your platform is now ready for PRODUCTION-GRADE testing!")
        print("💪 This is how you build systems that scale to millions!\n")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║          AUTOMATOS AI - COMPREHENSIVE TEST DATA GENERATOR     ║
    ║                                                              ║
    ║  Building test data the RIGHT way - not basic, but COMPLETE! ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    populator = ComprehensiveTestDataPopulator()
    asyncio.run(populator.populate_all_data())


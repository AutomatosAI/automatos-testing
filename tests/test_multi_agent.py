
"""
Multi-Agent Systems Testing Module
==================================

Comprehensive testing of multi-agent collaboration, coordination,
behavior monitoring, and system optimization.
"""

import asyncio
import json
from typing import Dict, Any, List
import time

from framework.base_test import APITest


class TestMultiAgentSystems(APITest):
    """Test suite for multi-agent systems functionality"""
    
    def __init__(self):
        super().__init__("MultiAgentSystems")
        self.created_agents = []
        self.active_collaborations = []
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Multi-Agent Systems tests...")
        
        # Create test agents for collaboration testing
        agent_configs = [
            {
                "name": "CollaborationAgent1",
                "type": "code_architect",
                "description": "First agent for collaboration testing",
                "configuration": {"priority_level": "normal", "auto_start": True}
            },
            {
                "name": "CollaborationAgent2", 
                "type": "security_expert",
                "description": "Second agent for collaboration testing",
                "configuration": {"priority_level": "normal", "auto_start": True}
            },
            {
                "name": "CollaborationAgent3",
                "type": "performance_optimizer",
                "description": "Third agent for collaboration testing",
                "configuration": {"priority_level": "high", "auto_start": True}
            }
        ]
        
        for agent_config in agent_configs:
            response = await self.make_request("POST", "/api/agents", data=agent_config)
            if response["status_code"] == 201:
                agent_id = response["data"]["data"]["id"]
                self.created_agents.append(agent_id)
                
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Multi-Agent Systems tests...")
        
        # Clean up active collaborations
        for collab_id in self.active_collaborations:
            try:
                await self.make_request("DELETE", f"/api/multi-agent/reasoning/sessions/{collab_id}")
            except:
                pass
                
        # Clean up created agents
        for agent_id in self.created_agents:
            try:
                await self.make_request("DELETE", f"/api/agents/{agent_id}")
            except:
                pass
                
        await self.cleanup_session()
        
    async def test_multi_agent_health(self):
        """Test multi-agent system health monitoring"""
        response = await self.make_request("GET", "/api/multi-agent/health")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        health_data = response["data"]["data"]
        assert "status" in health_data, "Should contain overall status"
        assert "components" in health_data, "Should contain component health"
        
        components = health_data["components"]
        expected_components = ["reasoning_engine", "coordination_system", "behavior_monitor", "optimization_engine"]
        
        for component in expected_components:
            if component in components:
                assert components[component] in ["healthy", "degraded", "unhealthy"], f"{component} should have valid status"
                
    async def test_collaborative_reasoning_session(self):
        """Test creating and managing collaborative reasoning sessions"""
        if len(self.created_agents) < 2:
            print("⚠️ Skipping collaborative reasoning test - insufficient agents")
            return
            
        session_data = {
            "name": "TestCollaborationSession",
            "description": "Test session for collaborative reasoning",
            "agent_ids": self.created_agents[:2],  # Use first two agents
            "problem_statement": "Design a secure and scalable web application architecture",
            "reasoning_strategy": "consensus_building",
            "configuration": {
                "max_rounds": 5,
                "timeout": 300,
                "consensus_threshold": 0.8
            }
        }
        
        response = await self.make_request("POST", "/api/multi-agent/reasoning/sessions", 
                                          data=session_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        session = response["data"]["data"]
        assert "session_id" in session, "Should contain session ID"
        assert "status" in session, "Should contain session status"
        assert session["agent_count"] == len(session_data["agent_ids"]), "Should have correct agent count"
        
        session_id = session["session_id"]
        self.active_collaborations.append(session_id)
        
    async def test_consensus_mechanisms(self):
        """Test different consensus mechanisms"""
        if len(self.created_agents) < 3:
            print("⚠️ Skipping consensus mechanism test - insufficient agents")
            return
            
        consensus_data = {
            "agent_ids": self.created_agents,
            "decision_topic": "Choose optimal deployment strategy",
            "options": [
                {"id": "blue_green", "description": "Blue-green deployment"},
                {"id": "rolling", "description": "Rolling deployment"}, 
                {"id": "canary", "description": "Canary deployment"}
            ],
            "mechanism": "weighted_voting",
            "weights": {
                self.created_agents[0]: 1.0,
                self.created_agents[1]: 1.5,  # Security expert gets higher weight
                self.created_agents[2]: 1.2   # Performance optimizer gets higher weight
            }
        }
        
        response = await self.make_request("POST", "/api/multi-agent/reasoning/consensus", 
                                          data=consensus_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "decision" in result, "Should contain consensus decision"
        assert "confidence" in result, "Should contain confidence level"
        assert "votes" in result, "Should contain voting breakdown"
        
    async def test_conflict_resolution(self):
        """Test conflict resolution mechanisms"""
        conflict_data = {
            "conflict_type": "resource_allocation",
            "conflicting_agents": self.created_agents[:2] if len(self.created_agents) >= 2 else [],
            "resource": {
                "type": "computational",
                "capacity": 100,
                "requests": [
                    {"agent_id": self.created_agents[0] if self.created_agents else "agent1", "amount": 60},
                    {"agent_id": self.created_agents[1] if len(self.created_agents) > 1 else "agent2", "amount": 70}
                ]
            },
            "resolution_strategy": "priority_based"
        }
        
        response = await self.make_request("POST", "/api/multi-agent/reasoning/resolve-conflict", 
                                          data=conflict_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "resolution" in result, "Should contain conflict resolution"
        assert "allocation" in result, "Should contain resource allocation"
        
    async def test_reasoning_statistics(self):
        """Test collaborative reasoning statistics"""
        response = await self.make_request("GET", "/api/multi-agent/reasoning/statistics")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        stats = response["data"]["data"]
        assert "active_sessions" in stats, "Should contain active sessions count"
        assert "completed_sessions" in stats, "Should contain completed sessions count"
        assert "consensus_rate" in stats, "Should contain consensus success rate"
        assert "average_resolution_time" in stats, "Should contain average resolution time"
        
    async def test_agent_coordination_strategies(self):
        """Test different agent coordination strategies"""
        coordination_strategies = ["sequential", "parallel", "hierarchical", "mesh", "adaptive"]
        
        for strategy in coordination_strategies:
            coordination_data = {
                "strategy": strategy,
                "agent_ids": self.created_agents,
                "task": {
                    "type": "analysis",
                    "description": f"Test {strategy} coordination",
                    "parameters": {"coordination_test": True}
                },
                "configuration": {
                    "timeout": 120,
                    "retry_count": 2
                }
            }
            
            response = await self.make_request("POST", "/api/multi-agent/coordination/execute", 
                                              data=coordination_data)
            
            assert response["status_code"] == 200, f"Expected 200 for {strategy}, got {response['status_code']}"
            
            result = response["data"]["data"]
            assert "coordination_id" in result, f"Should contain coordination ID for {strategy}"
            assert "status" in result, f"Should contain status for {strategy}"
            
    async def test_coordination_statistics(self):
        """Test coordination system statistics"""
        response = await self.make_request("GET", "/api/multi-agent/coordination/statistics")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        stats = response["data"]["data"]
        assert "active_coordinations" in stats, "Should contain active coordinations"
        assert "strategy_usage" in stats, "Should contain strategy usage statistics"
        assert "success_rate" in stats, "Should contain coordination success rate"
        
    async def test_behavior_monitoring(self):
        """Test agent behavior monitoring"""
        if not self.created_agents:
            print("⚠️ Skipping behavior monitoring test - no agents available")
            return
            
        monitoring_data = {
            "agent_id": self.created_agents[0],
            "monitoring_period": 60,  # seconds
            "metrics": ["performance", "resource_usage", "decision_patterns", "collaboration_score"]
        }
        
        response = await self.make_request("POST", "/api/multi-agent/behavior/monitor", 
                                          data=monitoring_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "monitoring_session_id" in result, "Should contain monitoring session ID"
        assert "metrics_collected" in result, "Should contain metrics being collected"
        
    async def test_realtime_behavior_monitoring(self):
        """Test real-time behavior monitoring"""
        response = await self.make_request("GET", "/api/multi-agent/behavior/monitor/realtime")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "active_agents" in result, "Should contain active agents info"
        assert "system_metrics" in result, "Should contain system-wide metrics"
        
    async def test_emergent_behavior_analysis(self):
        """Test emergent behavior analysis"""
        analysis_data = {
            "time_window": 3600,  # 1 hour
            "agent_group": self.created_agents,
            "behavior_patterns": ["collaboration", "competition", "adaptation", "learning"],
            "analysis_depth": "detailed"
        }
        
        response = await self.make_request("POST", "/api/multi-agent/behavior/analyze-emergence", 
                                          data=analysis_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "emergent_patterns" in result, "Should contain emergent patterns"
        assert "complexity_metrics" in result, "Should contain complexity metrics"
        assert "recommendations" in result, "Should contain behavioral recommendations"
        
    async def test_behavior_statistics(self):
        """Test behavior monitoring statistics"""
        response = await self.make_request("GET", "/api/multi-agent/behavior/statistics")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        stats = response["data"]["data"]
        assert "monitored_agents" in stats, "Should contain monitored agents count"
        assert "behavior_trends" in stats, "Should contain behavior trends"
        assert "anomaly_detection" in stats, "Should contain anomaly detection info"
        
    async def test_system_optimization_objectives(self):
        """Test multi-objective system optimization"""
        optimization_data = {
            "objectives": [
                {
                    "name": "minimize_response_time",
                    "weight": 0.4,
                    "current_value": 150,  # ms
                    "target_value": 100
                },
                {
                    "name": "maximize_throughput", 
                    "weight": 0.3,
                    "current_value": 1000,  # requests/min
                    "target_value": 1500
                },
                {
                    "name": "minimize_resource_usage",
                    "weight": 0.3,
                    "current_value": 80,  # % CPU
                    "target_value": 60
                }
            ],
            "constraints": [
                {"type": "resource", "limit": 100, "metric": "cpu_usage"},
                {"type": "quality", "min_value": 0.95, "metric": "success_rate"}
            ],
            "optimization_method": "pareto_frontier"
        }
        
        response = await self.make_request("POST", "/api/multi-agent/optimization/objectives", 
                                          data=optimization_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "optimization_plan" in result, "Should contain optimization plan"
        assert "pareto_solutions" in result, "Should contain Pareto-optimal solutions"
        assert "recommended_configuration" in result, "Should contain recommended configuration"
        
    async def test_resource_allocation_optimization(self):
        """Test resource allocation optimization"""
        allocation_data = {
            "resources": [
                {"type": "cpu", "total": 1000, "unit": "cores"},
                {"type": "memory", "total": 16384, "unit": "MB"},
                {"type": "network", "total": 1000, "unit": "Mbps"}
            ],
            "agents": [
                {
                    "id": agent_id,
                    "requirements": {
                        "cpu": 100 + i * 50,
                        "memory": 1024 + i * 512,
                        "network": 50 + i * 25
                    },
                    "priority": 1.0 + i * 0.2
                }
                for i, agent_id in enumerate(self.created_agents[:3])
            ],
            "allocation_strategy": "fair_share_with_priority"
        }
        
        response = await self.make_request("POST", "/api/multi-agent/optimization/allocate-resources", 
                                          data=allocation_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "allocation_plan" in result, "Should contain allocation plan"
        assert "utilization_efficiency" in result, "Should contain utilization efficiency"
        
    async def test_optimization_statistics(self):
        """Test system optimization statistics"""
        response = await self.make_request("GET", "/api/multi-agent/optimization/statistics")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        stats = response["data"]["data"]
        assert "optimization_runs" in stats, "Should contain optimization runs count"
        assert "performance_improvements" in stats, "Should contain performance improvements"
        assert "resource_efficiency" in stats, "Should contain resource efficiency metrics"
        
    async def test_load_balancing(self):
        """Test agent load balancing"""
        load_balancing_data = {
            "agent_pool": self.created_agents,
            "tasks": [
                {"id": f"task_{i}", "complexity": i + 1, "priority": "normal"}
                for i in range(10)
            ],
            "balancing_strategy": "least_loaded",
            "consider_agent_capabilities": True
        }
        
        response = await self.make_request("POST", "/api/multi-agent/coordination/load-balance", 
                                          data=load_balancing_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "task_assignments" in result, "Should contain task assignments"
        assert "load_distribution" in result, "Should contain load distribution"
        
    async def test_scalability_analysis(self):
        """Test system scalability analysis"""
        scalability_data = {
            "current_agent_count": len(self.created_agents),
            "target_agent_count": 100,
            "workload_projection": {
                "tasks_per_minute": 1000,
                "peak_multiplier": 3,
                "growth_rate": 1.2  # 20% monthly growth
            },
            "resource_constraints": {
                "max_cpu": 10000,  # cores
                "max_memory": 102400,  # MB
                "max_network": 10000  # Mbps
            }
        }
        
        response = await self.make_request("POST", "/api/multi-agent/optimization/analyze-scalability", 
                                          data=scalability_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "scalability_report" in result, "Should contain scalability report"
        assert "bottlenecks" in result, "Should contain identified bottlenecks"
        assert "scaling_recommendations" in result, "Should contain scaling recommendations"

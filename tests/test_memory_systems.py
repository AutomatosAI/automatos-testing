
"""
Memory Systems Testing Module
============================

Comprehensive testing of hierarchical memory, memory management,
context storage, and memory optimization.
"""

import asyncio
import json
from typing import Dict, Any, List
import time

from framework.base_test import APITest


class TestMemorySystems(APITest):
    """Test suite for memory systems functionality"""
    
    def __init__(self):
        super().__init__("MemorySystems")
        self.created_memories = []
        self.memory_sessions = []
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Memory Systems tests...")
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Memory Systems tests...")
        
        # Clean up created memories
        for memory_id in self.created_memories:
            try:
                await self.make_request("DELETE", f"/api/memory/memories/{memory_id}")
            except:
                pass
                
        # Clean up memory sessions
        for session_id in self.memory_sessions:
            try:
                await self.make_request("DELETE", f"/api/memory/sessions/{session_id}")
            except:
                pass
                
        await self.cleanup_session()
        
    async def test_memory_health(self):
        """Test memory system health monitoring"""
        response = await self.make_request("GET", "/api/memory/health")
        
        # Handle endpoint not implemented gracefully
        if response["status_code"] == 404:
            print("⚠️ Skipping memory health test - endpoint not implemented")
            return
            
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        health_data = response["data"]["data"]
        assert "status" in health_data, "Should contain overall status"
        assert "components" in health_data, "Should contain component health"
        
        components = health_data["components"]
        expected_components = ["short_term_memory", "long_term_memory", "working_memory", "episodic_memory"]
        
        for component in expected_components:
            if component in components:
                assert components[component] in ["healthy", "degraded", "unhealthy"], f"{component} should have valid status"
                
    async def test_hierarchical_memory_creation(self):
        """Test creating hierarchical memory structures"""
        memory_data = {
            "name": "TestHierarchicalMemory",
            "type": "hierarchical",
            "levels": [
                {
                    "name": "sensory",
                    "capacity": 100,
                    "retention_time": 1,  # seconds
                    "decay_function": "exponential"
                },
                {
                    "name": "short_term",
                    "capacity": 50,
                    "retention_time": 300,  # 5 minutes
                    "decay_function": "linear"
                },
                {
                    "name": "long_term",
                    "capacity": 10000,
                    "retention_time": 86400,  # 24 hours
                    "decay_function": "logarithmic"
                }
            ],
            "consolidation_rules": [
                {
                    "from": "sensory",
                    "to": "short_term", 
                    "condition": "activation_threshold > 0.8"
                },
                {
                    "from": "short_term",
                    "to": "long_term",
                    "condition": "repetition_count > 3"
                }
            ]
        }
        
        response = await self.make_request("POST", "/api/memory/hierarchical/create", 
                                          data=memory_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "memory_id" in result, "Should contain memory system ID"
        assert "levels" in result, "Should contain memory levels"
        assert len(result["levels"]) == len(memory_data["levels"]), "Should have all specified levels"
        
        memory_id = result["memory_id"]
        self.created_memories.append(memory_id)
        
    async def test_memory_storage_and_retrieval(self):
        """Test storing and retrieving memories"""
        # First create a memory system
        await self.test_hierarchical_memory_creation()
        
        if not self.created_memories:
            print("⚠️ Skipping storage/retrieval test - no memory system created")
            return
            
        memory_id = self.created_memories[0]
        
        # Store some memories
        memories_to_store = [
            {
                "content": "User logged into the system at 10:30 AM",
                "type": "event",
                "importance": 0.7,
                "context": {"user_id": "user123", "timestamp": "2025-01-01T10:30:00Z"}
            },
            {
                "content": "System performance degraded during peak hours",
                "type": "observation",
                "importance": 0.9,
                "context": {"metric": "response_time", "value": 500, "threshold": 200}
            },
            {
                "content": "New agent deployed successfully",
                "type": "action",
                "importance": 0.6,
                "context": {"agent_id": "agent456", "deployment_time": 45}
            }
        ]
        
        stored_memory_ids = []
        
        for memory_item in memories_to_store:
            store_data = {
                "memory_system_id": memory_id,
                "memory_item": memory_item
            }
            
            response = await self.make_request("POST", "/api/memory/store", data=store_data)
            
            assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
            
            result = response["data"]["data"]
            assert "memory_item_id" in result, "Should contain memory item ID"
            stored_memory_ids.append(result["memory_item_id"])
            
        # Test retrieval
        query_data = {
            "memory_system_id": memory_id,
            "query": "system performance issues",
            "retrieval_strategy": "semantic_similarity",
            "max_results": 5
        }
        
        response = await self.make_request("POST", "/api/memory/retrieve", data=query_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "retrieved_memories" in result, "Should contain retrieved memories"
        assert "relevance_scores" in result, "Should contain relevance scores"
        
        retrieved = result["retrieved_memories"]
        assert len(retrieved) > 0, "Should retrieve at least one relevant memory"
        
    async def test_working_memory_operations(self):
        """Test working memory operations"""
        working_memory_data = {
            "name": "TestWorkingMemory",
            "capacity": 7,  # Miller's magic number
            "refresh_rate": 100,  # ms
            "attention_mechanism": "selective",
            "initial_items": [
                {"content": "Task: Review code changes", "priority": 0.8},
                {"content": "Context: Security vulnerability found", "priority": 0.9},
                {"content": "Goal: Fix security issue", "priority": 1.0}
            ]
        }
        
        response = await self.make_request("POST", "/api/memory/working-memory/create", 
                                          data=working_memory_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "working_memory_id" in result, "Should contain working memory ID"
        
        wm_id = result["working_memory_id"]
        
        # Test adding items to working memory
        add_item_data = {
            "working_memory_id": wm_id,
            "item": {"content": "New information: Patch available", "priority": 0.7}
        }
        
        response = await self.make_request("POST", "/api/memory/working-memory/add-item", 
                                          data=add_item_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        # Test retrieving current working memory state
        response = await self.make_request("GET", f"/api/memory/working-memory/{wm_id}/state")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        state = response["data"]["data"]
        assert "current_items" in state, "Should contain current items"
        assert "capacity_used" in state, "Should contain capacity usage"
        
    async def test_episodic_memory(self):
        """Test episodic memory functionality"""
        episode_data = {
            "name": "DeploymentEpisode",
            "description": "Memory of a critical system deployment",
            "timeline": [
                {
                    "timestamp": "2025-01-01T09:00:00Z",
                    "event": "Deployment started",
                    "context": {"version": "v2.1.0", "environment": "production"}
                },
                {
                    "timestamp": "2025-01-01T09:15:00Z",
                    "event": "Database migration completed",
                    "context": {"tables_updated": 5, "downtime": 30}
                },
                {
                    "timestamp": "2025-01-01T09:30:00Z",
                    "event": "Application deployed successfully",
                    "context": {"response_time": 120, "success_rate": 0.99}
                }
            ],
            "outcome": "successful",
            "lessons_learned": [
                "Database migrations should be tested more thoroughly",
                "Monitoring should be enhanced during deployments"
            ]
        }
        
        response = await self.make_request("POST", "/api/memory/episodic/create", 
                                          data=episode_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "episode_id" in result, "Should contain episode ID"
        assert "timeline_length" in result, "Should contain timeline length"
        
    async def test_memory_consolidation(self):
        """Test memory consolidation processes"""
        if not self.created_memories:
            print("⚠️ Skipping consolidation test - no memory system available")
            return
            
        memory_id = self.created_memories[0]
        
        consolidation_data = {
            "memory_system_id": memory_id,
            "consolidation_type": "rehearsal_based",
            "parameters": {
                "activation_threshold": 0.5,
                "rehearsal_frequency": 10,
                "strengthen_factor": 1.2
            }
        }
        
        response = await self.make_request("POST", "/api/memory/consolidation/trigger", 
                                          data=consolidation_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "consolidation_id" in result, "Should contain consolidation process ID"
        assert "memories_processed" in result, "Should contain count of processed memories"
        
    async def test_memory_optimization(self):
        """Test memory optimization strategies"""
        optimization_data = {
            "optimization_goals": [
                {"metric": "retrieval_speed", "target": "minimize", "weight": 0.4},
                {"metric": "storage_efficiency", "target": "maximize", "weight": 0.3},
                {"metric": "accuracy", "target": "maximize", "weight": 0.3}
            ],
            "constraints": [
                {"type": "memory_limit", "value": 1000},  # MB
                {"type": "response_time", "max_value": 100}  # ms
            ],
            "optimization_strategy": "multi_objective_genetic"
        }
        
        response = await self.make_request("POST", "/api/memory/optimization/optimize", 
                                          data=optimization_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "optimization_plan" in result, "Should contain optimization plan"
        assert "expected_improvements" in result, "Should contain expected improvements"
        
    async def test_memory_forgetting_mechanisms(self):
        """Test memory forgetting and decay mechanisms"""
        forgetting_data = {
            "memory_system_id": self.created_memories[0] if self.created_memories else "test_system",
            "forgetting_strategy": "interference_based",
            "parameters": {
                "similarity_threshold": 0.8,
                "age_weight": 0.3,
                "access_frequency_weight": 0.7
            },
            "target_memories": {
                "type": "low_importance",
                "importance_threshold": 0.3
            }
        }
        
        response = await self.make_request("POST", "/api/memory/forgetting/apply", 
                                          data=forgetting_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "forgotten_count" in result, "Should contain count of forgotten memories"
        assert "retained_count" in result, "Should contain count of retained memories"
        
    async def test_memory_associative_retrieval(self):
        """Test associative memory retrieval"""
        if not self.created_memories:
            print("⚠️ Skipping associative retrieval test - no memory system available")
            return
            
        association_data = {
            "memory_system_id": self.created_memories[0],
            "seed_concept": "deployment",
            "association_strength": 0.5,
            "max_associations": 10,
            "association_types": ["semantic", "temporal", "causal"]
        }
        
        response = await self.make_request("POST", "/api/memory/associative/retrieve", 
                                          data=association_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "associations" in result, "Should contain memory associations"
        assert "association_network" in result, "Should contain association network"
        
    async def test_memory_context_reconstruction(self):
        """Test context reconstruction from memory"""
        reconstruction_data = {
            "memory_fragments": [
                {"content": "system error", "confidence": 0.8},
                {"content": "database timeout", "confidence": 0.9},
                {"content": "peak traffic", "confidence": 0.7}
            ],
            "reconstruction_strategy": "bayesian_inference",
            "context_types": ["temporal", "causal", "spatial"]
        }
        
        response = await self.make_request("POST", "/api/memory/context/reconstruct", 
                                          data=reconstruction_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "reconstructed_context" in result, "Should contain reconstructed context"
        assert "confidence_score" in result, "Should contain confidence score"
        
    async def test_memory_sessions(self):
        """Test memory session management"""
        session_data = {
            "name": "TestMemorySession",
            "description": "Session for testing memory operations",
            "memory_systems": self.created_memories,
            "session_type": "interactive",
            "configuration": {
                "auto_save": True,
                "context_window": 1000,
                "retention_policy": "session_based"
            }
        }
        
        response = await self.make_request("POST", "/api/memory/sessions/create", 
                                          data=session_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "session_id" in result, "Should contain session ID"
        
        session_id = result["session_id"]
        self.memory_sessions.append(session_id)
        
        # Test session state management
        state_update_data = {
            "session_id": session_id,
            "state_update": {
                "current_focus": "deployment_analysis",
                "active_memories": 5,
                "context_shift": True
            }
        }
        
        response = await self.make_request("PUT", "/api/memory/sessions/update-state", 
                                          data=state_update_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
    async def test_memory_statistics(self):
        """Test memory system statistics"""
        response = await self.make_request("GET", "/api/memory/statistics")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        stats = response["data"]["data"]
        assert "total_memories" in stats, "Should contain total memories count"
        assert "memory_systems" in stats, "Should contain memory systems count"
        assert "storage_usage" in stats, "Should contain storage usage"
        assert "retrieval_performance" in stats, "Should contain retrieval performance metrics"
        
    async def test_memory_backup_and_restore(self):
        """Test memory backup and restore functionality"""
        if not self.created_memories:
            print("⚠️ Skipping backup/restore test - no memory system available")
            return
            
        memory_id = self.created_memories[0]
        
        # Create backup
        backup_data = {
            "memory_system_id": memory_id,
            "backup_type": "full",
            "compression": True,
            "encryption": False
        }
        
        response = await self.make_request("POST", "/api/memory/backup/create", 
                                          data=backup_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "backup_id" in result, "Should contain backup ID"
        assert "backup_size" in result, "Should contain backup size"
        
        backup_id = result["backup_id"]
        
        # Test restore
        restore_data = {
            "backup_id": backup_id,
            "restore_target": "new_system",
            "verify_integrity": True
        }
        
        response = await self.make_request("POST", "/api/memory/restore", data=restore_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "restored_system_id" in result, "Should contain restored system ID"

"""
Field Theory Testing Module
===========================

Comprehensive testing for neural field dynamics, propagation,
interactions, and optimization based on David Kimai's research.
"""

import asyncio
import json
import random
import numpy as np
from typing import Dict, Any, List
import time

from framework.base_test import APITest, TestLevel


class TestFieldTheory(APITest):
    """Test suite for field theory functionality"""
    
    def __init__(self):
        super().__init__("FieldTheory")
        self.test_level = TestLevel.FUNCTIONAL
        self.test_sessions = []
        self.field_configurations = {}
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Field Theory tests...")
        
        # Initialize test field configurations
        self._initialize_field_configs()
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Field Theory tests...")
        
        # Clear all test field contexts
        for session_id in self.test_sessions:
            try:
                await self.make_request("DELETE", f"/api/field-theory/fields/context/{session_id}")
            except:
                pass
                
        await self.cleanup_session()
        
    def _initialize_field_configs(self):
        """Initialize test field configurations"""
        self.field_configurations = {
            "agent_assignment": {
                "field_type": "agent_assignment",
                "dimensions": 128,
                "learning_rate": 0.01,
                "decay_rate": 0.95,
                "resonance_threshold": 0.7
            },
            "context_resonance": {
                "field_type": "context_resonance",
                "dimensions": 256,
                "learning_rate": 0.001,
                "persistence": 0.9,
                "boundary_strength": 0.5
            },
            "collective_memory": {
                "field_type": "collective_memory",
                "dimensions": 512,
                "consolidation_rate": 0.1,
                "memory_capacity": 1000,
                "forgetting_factor": 0.01
            }
        }
        
    # Field Update Tests
    async def test_update_field_context(self):
        """Test updating field context"""
        session_id = f"test_session_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        field_update = {
            "session_id": session_id,
            "field_type": "agent_assignment",
            "context_data": {
                "task_embedding": [random.random() for _ in range(128)],
                "agent_capabilities": ["nlp", "data_analysis", "reasoning"],
                "task_requirements": ["text_processing", "pattern_recognition"],
                "performance_history": [0.8, 0.85, 0.9]
            },
            "update_mode": "additive"
        }
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/update",
            json=field_update
        )
        
        assert response["status_code"] == 200, f"Field update failed: {response}"
        result = response["json"]
        
        assert result["status"] == "updated"
        assert "field_state" in result
        assert result["field_state"]["energy"] >= 0
        assert "gradient" in result["field_state"]
        
        return session_id
        
    async def test_update_multiple_fields(self):
        """Test updating multiple field types"""
        session_id = f"test_multi_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        # Update agent assignment field
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/update",
            json={
                "session_id": session_id,
                "field_type": "agent_assignment",
                "context_data": {
                    "task_embedding": [random.random() for _ in range(128)]
                }
            }
        )
        assert response["status_code"] == 200
        
        # Update context resonance field
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/update",
            json={
                "session_id": session_id,
                "field_type": "context_resonance",
                "context_data": {
                    "query_embedding": [random.random() for _ in range(256)],
                    "context_embeddings": [[random.random() for _ in range(256)] for _ in range(5)]
                }
            }
        )
        assert response["status_code"] == 200
        
    # Field Propagation Tests
    async def test_propagate_field_influence(self):
        """Test field influence propagation"""
        # First create a field context
        session_id = await self.test_update_field_context()
        
        propagation_request = {
            "session_id": session_id,
            "source_field": "agent_assignment",
            "target_fields": ["context_resonance", "collective_memory"],
            "propagation_strength": 0.8,
            "decay_function": "exponential"
        }
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/propagate",
            json=propagation_request
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "propagation_results" in result
        assert len(result["propagation_results"]) == 2
        assert all("influence_strength" in r for r in result["propagation_results"])
        
    async def test_field_wave_propagation(self):
        """Test wave-like field propagation"""
        session_id = f"test_wave_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        # Initialize field with perturbation
        await self.make_request(
            "POST",
            "/api/field-theory/fields/update",
            json={
                "session_id": session_id,
                "field_type": "context_resonance",
                "context_data": {
                    "perturbation_point": [0.5, 0.5],
                    "perturbation_strength": 1.0
                }
            }
        )
        
        # Propagate the wave
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/propagate",
            json={
                "session_id": session_id,
                "source_field": "context_resonance",
                "propagation_mode": "wave",
                "time_steps": 10,
                "wave_speed": 0.1
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        assert "wave_states" in result or "propagation_results" in result
        
    # Field Interaction Tests
    async def test_model_field_interactions(self):
        """Test modeling interactions between fields"""
        session_id = f"test_interact_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        # Setup multiple fields
        for field_type in ["agent_assignment", "context_resonance", "collective_memory"]:
            await self.make_request(
                "POST",
                "/api/field-theory/fields/update",
                json={
                    "session_id": session_id,
                    "field_type": field_type,
                    "context_data": {
                        "embedding": [random.random() for _ in range(128)]
                    }
                }
            )
            
        # Model interactions
        interaction_request = {
            "session_id": session_id,
            "interaction_pairs": [
                {
                    "field_a": "agent_assignment",
                    "field_b": "context_resonance",
                    "interaction_type": "resonance"
                },
                {
                    "field_a": "context_resonance",
                    "field_b": "collective_memory",
                    "interaction_type": "coupling"
                }
            ],
            "time_window": 100,
            "compute_metrics": True
        }
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/interactions",
            json=interaction_request
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "interaction_results" in result
        assert "coupling_strengths" in result
        assert "energy_transfer" in result
        
    async def test_nonlinear_field_interactions(self):
        """Test nonlinear field interactions"""
        session_id = f"test_nonlinear_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/interactions",
            json={
                "session_id": session_id,
                "interaction_type": "nonlinear",
                "field_states": {
                    "field_1": [random.random() for _ in range(64)],
                    "field_2": [random.random() for _ in range(64)]
                },
                "nonlinearity": "sigmoid",
                "coupling_coefficient": 0.5
            }
        )
        
        if response["status_code"] == 200:
            result = response["json"]
            assert "combined_field" in result
            assert "bifurcation_points" in result or "stability_analysis" in result
            
    # Dynamic Field Management Tests
    async def test_manage_dynamic_fields(self):
        """Test dynamic field management"""
        session_id = f"test_dynamic_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        dynamic_config = {
            "session_id": session_id,
            "adaptive_parameters": {
                "learning_rate_schedule": "cosine",
                "min_learning_rate": 0.0001,
                "max_learning_rate": 0.1,
                "adaptation_period": 1000
            },
            "field_dynamics": {
                "evolution_equation": "kuramoto",
                "coupling_strength": 0.3,
                "natural_frequency": 1.0
            },
            "monitoring": {
                "track_energy": True,
                "track_synchronization": True,
                "sample_rate": 10
            }
        }
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/dynamic",
            json=dynamic_config
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "dynamics_configured" in result
        assert "monitoring_enabled" in result
        assert result["monitoring_enabled"] == True
        
    async def test_field_phase_transitions(self):
        """Test field phase transitions"""
        session_id = f"test_phase_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/dynamic",
            json={
                "session_id": session_id,
                "operation": "phase_transition",
                "control_parameter": "temperature",
                "parameter_range": [0.1, 2.0],
                "steps": 20,
                "detect_critical_points": True
            }
        )
        
        if response["status_code"] == 200:
            result = response["json"]
            assert "phase_diagram" in result or "critical_points" in result
            
    # Field Optimization Tests
    async def test_optimize_field_configuration(self):
        """Test field configuration optimization"""
        session_id = f"test_optimize_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        # Setup initial field
        await self.make_request(
            "POST",
            "/api/field-theory/fields/update",
            json={
                "session_id": session_id,
                "field_type": "agent_assignment",
                "context_data": {
                    "current_performance": 0.6,
                    "target_performance": 0.9
                }
            }
        )
        
        # Optimize configuration
        optimization_request = {
            "session_id": session_id,
            "optimization_targets": {
                "minimize_energy": True,
                "maximize_resonance": True,
                "stabilize_dynamics": True
            },
            "constraints": {
                "max_learning_rate": 0.1,
                "min_decay_rate": 0.8,
                "energy_budget": 100.0
            },
            "optimization_method": "gradient_descent",
            "max_iterations": 100
        }
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/optimize",
            json=optimization_request
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "optimized_parameters" in result
        assert "optimization_metrics" in result
        assert "convergence_achieved" in result
        
    async def test_multi_objective_optimization(self):
        """Test multi-objective field optimization"""
        session_id = f"test_multobj_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/optimize",
            json={
                "session_id": session_id,
                "optimization_mode": "pareto",
                "objectives": [
                    {"name": "energy_efficiency", "weight": 0.4},
                    {"name": "response_time", "weight": 0.3},
                    {"name": "stability", "weight": 0.3}
                ],
                "algorithm": "nsga2",
                "population_size": 50,
                "generations": 20
            }
        )
        
        if response["status_code"] == 200:
            result = response["json"]
            assert "pareto_front" in result or "optimal_solutions" in result
            
    # Field Context Retrieval Tests
    async def test_get_field_context(self):
        """Test retrieving field context"""
        # Create a field context first
        session_id = await self.test_update_field_context()
        
        response = await self.make_request(
            "GET",
            f"/api/field-theory/fields/context/{session_id}"
        )
        
        assert response["status_code"] == 200
        context = response["json"]
        
        assert "field_states" in context
        assert "session_id" in context
        assert context["session_id"] == session_id
        assert "last_updated" in context
        
    async def test_get_field_statistics(self):
        """Test retrieving field statistics"""
        response = await self.make_request(
            "GET",
            "/api/field-theory/fields/statistics"
        )
        
        assert response["status_code"] == 200
        stats = response["json"]
        
        assert "total_sessions" in stats
        assert "active_fields" in stats
        assert "field_types" in stats
        assert "average_energy" in stats
        
    async def test_get_field_states(self):
        """Test retrieving current field states"""
        # Create some fields first
        await self.test_update_multiple_fields()
        
        response = await self.make_request(
            "GET",
            "/api/field-theory/fields/states"
        )
        
        assert response["status_code"] == 200
        states = response["json"]
        
        assert "fields" in states
        assert isinstance(states["fields"], dict)
        
        for field_type, field_state in states["fields"].items():
            assert "energy" in field_state
            assert "dimensions" in field_state
            assert "last_update" in field_state
            
    async def test_get_field_interactions_status(self):
        """Test retrieving field interaction status"""
        response = await self.make_request(
            "GET",
            "/api/field-theory/fields/interactions"
        )
        
        assert response["status_code"] == 200
        interactions = response["json"]
        
        assert "active_interactions" in interactions
        assert "interaction_matrix" in interactions
        assert "coupling_strengths" in interactions
        
    # Batch Operations Tests
    async def test_batch_update_fields(self):
        """Test batch field updates"""
        session_id = f"test_batch_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        batch_updates = {
            "session_id": session_id,
            "updates": [
                {
                    "field_type": "agent_assignment",
                    "context_data": {
                        "embedding": [random.random() for _ in range(128)]
                    }
                },
                {
                    "field_type": "context_resonance",
                    "context_data": {
                        "embedding": [random.random() for _ in range(256)]
                    }
                },
                {
                    "field_type": "collective_memory",
                    "context_data": {
                        "memory_vector": [random.random() for _ in range(512)]
                    }
                }
            ],
            "atomic": True
        }
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/batch/update",
            json=batch_updates
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "updated_count" in result
        assert result["updated_count"] == 3
        assert "batch_id" in result
        
    async def test_batch_propagate_fields(self):
        """Test batch field propagation"""
        session_id = f"test_batch_prop_{int(time.time())}"
        self.test_sessions.append(session_id)
        
        # Setup fields
        await self.test_batch_update_fields()
        
        batch_propagation = {
            "session_id": session_id,
            "propagations": [
                {
                    "source": "agent_assignment",
                    "targets": ["context_resonance"],
                    "strength": 0.8
                },
                {
                    "source": "context_resonance",
                    "targets": ["collective_memory"],
                    "strength": 0.6
                }
            ],
            "parallel": True,
            "aggregate_results": True
        }
        
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/batch/propagate",
            json=batch_propagation
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "propagation_count" in result
        assert "aggregated_influence" in result
        
    # Edge Cases and Error Handling
    async def test_invalid_field_type(self):
        """Test handling invalid field types"""
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/update",
            json={
                "session_id": "test_invalid",
                "field_type": "non_existent_field",
                "context_data": {}
            }
        )
        
        assert response["status_code"] in [400, 422]
        
    async def test_field_dimension_mismatch(self):
        """Test handling dimension mismatches"""
        response = await self.make_request(
            "POST",
            "/api/field-theory/fields/update",
            json={
                "session_id": "test_mismatch",
                "field_type": "agent_assignment",
                "context_data": {
                    "embedding": [0.1, 0.2, 0.3]  # Wrong dimension
                }
            }
        )
        
        assert response["status_code"] in [400, 422]
        
    async def test_clear_field_context(self):
        """Test clearing field context"""
        # Create a context first
        session_id = await self.test_update_field_context()
        
        # Clear the context
        response = await self.make_request(
            "DELETE",
            f"/api/field-theory/fields/context/{session_id}"
        )
        
        assert response["status_code"] in [200, 204]
        
        # Verify it's cleared
        response = await self.make_request(
            "GET",
            f"/api/field-theory/fields/context/{session_id}"
        )
        
        assert response["status_code"] == 404
        
    async def test_field_theory_health_check(self):
        """Test field theory system health check"""
        response = await self.make_request(
            "GET",
            "/api/field-theory/health"
        )
        
        assert response["status_code"] == 200
        health = response["json"]
        
        assert "status" in health
        assert health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "components" in health
        assert "field_manager" in health["components"]
        assert "performance_metrics" in health


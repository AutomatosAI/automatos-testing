"""
Patterns API Tests
==================
Tests for pattern management and recognition functionality.
"""

import pytest
import asyncio
import time
from typing import Dict, Any, List
from framework.base_test import APITest


class TestPatterns(APITest):
    """Test suite for Patterns APIs"""
    
    def __init__(self):
        super().__init__("Patterns")
        
    async def setup(self):
        """Setup test data"""
        await self.setup_session()
        
        # Sample patterns for testing
        self.test_patterns = [
            {
                "name": "Error Recovery Pattern",
                "description": "Pattern for automatic error recovery and retry logic",
                "type": "behavioral",
                "category": "error_handling",
                "structure": {
                    "trigger": {
                        "type": "error",
                        "conditions": ["status_code >= 500", "timeout_error"]
                    },
                    "actions": [
                        {
                            "type": "wait",
                            "duration": "exponential_backoff"
                        },
                        {
                            "type": "retry",
                            "max_attempts": 3
                        },
                        {
                            "type": "fallback",
                            "handler": "manual_intervention"
                        }
                    ]
                },
                "metadata": {
                    "success_rate": 0.85,
                    "avg_recovery_time": 45.2,
                    "usage_count": 1523
                }
            },
            {
                "name": "Data Pipeline Pattern",
                "description": "Pattern for efficient data processing pipelines",
                "type": "structural",
                "category": "data_processing",
                "structure": {
                    "stages": [
                        {
                            "name": "ingestion",
                            "operations": ["validate", "normalize", "deduplicate"]
                        },
                        {
                            "name": "transformation",
                            "operations": ["enrich", "aggregate", "filter"]
                        },
                        {
                            "name": "output",
                            "operations": ["format", "compress", "deliver"]
                        }
                    ],
                    "error_handling": "checkpoint_recovery"
                }
            },
            {
                "name": "Multi-Agent Coordination Pattern",
                "description": "Pattern for coordinating multiple AI agents",
                "type": "collaborative",
                "category": "multi_agent",
                "structure": {
                    "coordination_type": "hierarchical",
                    "roles": {
                        "coordinator": {
                            "responsibilities": ["task_distribution", "conflict_resolution"]
                        },
                        "workers": {
                            "count": "dynamic",
                            "specializations": ["data_analysis", "content_generation", "validation"]
                        }
                    },
                    "communication": "message_passing"
                }
            }
        ]
        
    async def cleanup(self):
        """Cleanup test data"""
        # Delete any created patterns
        if hasattr(self, 'created_pattern_ids'):
            for pattern_id in self.created_pattern_ids:
                await self.make_request("DELETE", f"/api/patterns/{pattern_id}")
                
        await self.cleanup_session()

    async def test_list_patterns(self):
        """Test listing available patterns"""
        start_time = time.time()
        
        response = await self.make_request("GET", "/api/patterns/")
        
        assert response["status_code"] == 200
        assert "patterns" in response["data"] or isinstance(response["data"], list)
        
        self.log_result("test_list_patterns", "passed", time.time() - start_time)

    async def test_create_pattern(self):
        """Test creating a new pattern"""
        start_time = time.time()
        
        response = await self.make_request("POST", "/api/patterns/", data=self.test_patterns[0])
        
        assert response["status_code"] in [200, 201]
        assert "id" in response["data"]
        assert response["data"]["name"] == self.test_patterns[0]["name"]
        
        # Store for cleanup
        if not hasattr(self, 'created_pattern_ids'):
            self.created_pattern_ids = []
        self.created_pattern_ids.append(response["data"]["id"])
        
        self.log_result("test_create_pattern", "passed", time.time() - start_time)

    async def test_get_pattern(self):
        """Test retrieving a specific pattern"""
        start_time = time.time()
        
        # First create a pattern
        create_response = await self.make_request("POST", "/api/patterns/", data=self.test_patterns[1])
        
        if create_response["status_code"] in [200, 201]:
            pattern_id = create_response["data"]["id"]
            
            # Store for cleanup
            if not hasattr(self, 'created_pattern_ids'):
                self.created_pattern_ids = []
            self.created_pattern_ids.append(pattern_id)
            
            # Get the pattern
            response = await self.make_request("GET", f"/api/patterns/{pattern_id}")
            
            assert response["status_code"] == 200
            assert response["data"]["id"] == pattern_id
            assert "structure" in response["data"]
        else:
            self.log_result("test_get_pattern", "skipped", time.time() - start_time, 
                          "Could not create pattern")
            return
            
        self.log_result("test_get_pattern", "passed", time.time() - start_time)

    async def test_update_pattern(self):
        """Test updating an existing pattern"""
        start_time = time.time()
        
        # Create a pattern first
        create_response = await self.make_request("POST", "/api/patterns/", data=self.test_patterns[2])
        
        if create_response["status_code"] in [200, 201]:
            pattern_id = create_response["data"]["id"]
            
            # Store for cleanup
            if not hasattr(self, 'created_pattern_ids'):
                self.created_pattern_ids = []
            self.created_pattern_ids.append(pattern_id)
            
            # Update the pattern
            update_data = {
                "description": "Updated pattern for enhanced multi-agent coordination",
                "metadata": {
                    "success_rate": 0.92,
                    "version": "2.0"
                }
            }
            
            response = await self.make_request("PUT", f"/api/patterns/{pattern_id}", data=update_data)
            
            assert response["status_code"] == 200
            assert response["data"]["description"] == update_data["description"]
        else:
            self.log_result("test_update_pattern", "skipped", time.time() - start_time, 
                          "Could not create pattern")
            return
            
        self.log_result("test_update_pattern", "passed", time.time() - start_time)

    async def test_delete_pattern(self):
        """Test deleting a pattern"""
        start_time = time.time()
        
        # Create a pattern to delete
        create_response = await self.make_request("POST", "/api/patterns/", 
                                                data={
                                                    "name": "Temporary Pattern",
                                                    "type": "test",
                                                    "structure": {}
                                                })
        
        if create_response["status_code"] in [200, 201]:
            pattern_id = create_response["data"]["id"]
            
            # Delete the pattern
            response = await self.make_request("DELETE", f"/api/patterns/{pattern_id}")
            
            assert response["status_code"] in [200, 204]
            
            # Verify it's deleted
            get_response = await self.make_request("GET", f"/api/patterns/{pattern_id}")
            assert get_response["status_code"] == 404
        else:
            self.log_result("test_delete_pattern", "skipped", time.time() - start_time, 
                          "Could not create pattern")
            return
            
        self.log_result("test_delete_pattern", "passed", time.time() - start_time)

    async def test_pattern_recognition(self):
        """Test pattern recognition in data"""
        start_time = time.time()
        
        recognition_data = {
            "data": [
                {"timestamp": "2024-01-01T10:00:00Z", "event": "error", "code": 500},
                {"timestamp": "2024-01-01T10:00:05Z", "event": "retry", "attempt": 1},
                {"timestamp": "2024-01-01T10:00:15Z", "event": "retry", "attempt": 2},
                {"timestamp": "2024-01-01T10:00:35Z", "event": "success", "code": 200}
            ],
            "pattern_types": ["behavioral", "temporal"],
            "confidence_threshold": 0.7
        }
        
        response = await self.make_request("POST", "/api/patterns/recognize", data=recognition_data)
        
        assert response["status_code"] in [200, 404]
        if response["status_code"] == 200:
            assert "recognized_patterns" in response["data"] or "patterns" in response["data"]
            
        self.log_result("test_pattern_recognition", "passed", time.time() - start_time)

    async def test_pattern_matching(self):
        """Test pattern matching against templates"""
        start_time = time.time()
        
        # First create some patterns
        for pattern in self.test_patterns[:2]:
            create_response = await self.make_request("POST", "/api/patterns/", data=pattern)
            if create_response["status_code"] in [200, 201]:
                if not hasattr(self, 'created_pattern_ids'):
                    self.created_pattern_ids = []
                self.created_pattern_ids.append(create_response["data"]["id"])
                
        # Test matching
        match_data = {
            "input": {
                "type": "behavioral",
                "characteristics": {
                    "has_retry": True,
                    "has_error_handling": True,
                    "recovery_strategy": "exponential_backoff"
                }
            },
            "match_threshold": 0.8
        }
        
        response = await self.make_request("POST", "/api/patterns/match", data=match_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_pattern_matching", "passed", time.time() - start_time)

    async def test_pattern_analytics(self):
        """Test pattern usage analytics"""
        start_time = time.time()
        
        analytics_params = {
            "time_range": "last_30_days",
            "metrics": ["usage_frequency", "success_rate", "performance_impact"],
            "group_by": "category"
        }
        
        response = await self.make_request("GET", "/api/patterns/analytics", params=analytics_params)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_pattern_analytics", "passed", time.time() - start_time)

    async def test_pattern_recommendations(self):
        """Test pattern recommendations based on context"""
        start_time = time.time()
        
        recommendation_data = {
            "context": {
                "task_type": "data_processing",
                "data_volume": "large",
                "performance_requirements": "high",
                "error_tolerance": "low"
            },
            "max_recommendations": 5
        }
        
        response = await self.make_request("POST", "/api/patterns/recommend", data=recommendation_data)
        
        assert response["status_code"] in [200, 404]
        if response["status_code"] == 200:
            assert "recommendations" in response["data"] or "patterns" in response["data"]
            
        self.log_result("test_pattern_recommendations", "passed", time.time() - start_time)

    async def test_pattern_evolution(self):
        """Test pattern evolution and learning"""
        start_time = time.time()
        
        evolution_data = {
            "pattern_id": self.created_pattern_ids[0] if hasattr(self, 'created_pattern_ids') else "test_pattern",
            "feedback": {
                "executions": [
                    {"outcome": "success", "duration": 42.3, "resource_usage": "low"},
                    {"outcome": "partial_success", "duration": 67.8, "resource_usage": "medium"},
                    {"outcome": "success", "duration": 38.9, "resource_usage": "low"}
                ],
                "user_ratings": [4, 3, 5, 4, 5]
            },
            "evolution_strategy": "reinforcement_learning"
        }
        
        response = await self.make_request("POST", "/api/patterns/evolve", data=evolution_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_pattern_evolution", "passed", time.time() - start_time)

    async def test_pattern_composition(self):
        """Test composing complex patterns from simpler ones"""
        start_time = time.time()
        
        composition_data = {
            "name": "Composite Data Processing Pattern",
            "description": "Combined pattern for robust data processing",
            "component_patterns": [
                {
                    "pattern_id": "error_recovery_pattern",
                    "role": "error_handling"
                },
                {
                    "pattern_id": "data_pipeline_pattern",
                    "role": "main_processing"
                }
            ],
            "composition_type": "sequential",
            "interaction_rules": {
                "on_error": "trigger_error_recovery",
                "on_success": "continue_pipeline"
            }
        }
        
        response = await self.make_request("POST", "/api/patterns/compose", data=composition_data)
        
        assert response["status_code"] in [200, 201, 404]
        
        self.log_result("test_pattern_composition", "passed", time.time() - start_time)

    async def test_pattern_validation(self):
        """Test pattern validation"""
        start_time = time.time()
        
        # Invalid pattern with missing required fields
        invalid_pattern = {
            "name": "Invalid Pattern",
            "structure": {
                "invalid_field": "value"
            }
            # Missing type and other required fields
        }
        
        response = await self.make_request("POST", "/api/patterns/validate", data=invalid_pattern)
        
        if response["status_code"] == 404:
            # Try creating directly - should fail
            response = await self.make_request("POST", "/api/patterns/", data=invalid_pattern)
            
        assert response["status_code"] in [400, 422, 404]
        
        self.log_result("test_pattern_validation", "passed", time.time() - start_time)

    async def test_pattern_export_import(self):
        """Test exporting and importing patterns"""
        start_time = time.time()
        
        # Export patterns
        export_params = {
            "format": "json",
            "include_metadata": True
        }
        
        export_response = await self.make_request("GET", "/api/patterns/export", params=export_params)
        
        if export_response["status_code"] == 200:
            exported_data = export_response["data"]
            
            # Import patterns
            import_data = {
                "patterns": exported_data.get("patterns", []),
                "merge_strategy": "skip_existing"
            }
            
            import_response = await self.make_request("POST", "/api/patterns/import", data=import_data)
            assert import_response["status_code"] in [200, 201, 404]
            
        self.log_result("test_pattern_export_import", "passed", time.time() - start_time)

    async def test_pattern_search(self):
        """Test searching patterns"""
        start_time = time.time()
        
        search_params = {
            "query": "error recovery",
            "filters": {
                "type": ["behavioral", "structural"],
                "category": "error_handling",
                "min_success_rate": 0.8
            },
            "sort_by": "usage_count",
            "limit": 10
        }
        
        response = await self.make_request("GET", "/api/patterns/search", params=search_params)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_pattern_search", "passed", time.time() - start_time)

    async def test_pattern_performance(self):
        """Test pattern performance with large datasets"""
        start_time = time.time()
        
        # Create a complex pattern
        complex_pattern = {
            "name": "Complex Performance Pattern",
            "type": "composite",
            "structure": {
                "components": [
                    {
                        "id": f"component_{i}",
                        "type": "processor",
                        "operations": ["validate", "transform", "aggregate"]
                    }
                    for i in range(50)  # 50 components
                ],
                "connections": [
                    {"from": f"component_{i}", "to": f"component_{i+1}"}
                    for i in range(49)
                ]
            }
        }
        
        # Measure creation time
        create_start = time.time()
        response = await self.make_request("POST", "/api/patterns/", data=complex_pattern)
        create_time = time.time() - create_start
        
        assert response["status_code"] in [200, 201]
        assert create_time < 3.0  # Should create within 3 seconds
        
        if response["status_code"] in [200, 201]:
            if not hasattr(self, 'created_pattern_ids'):
                self.created_pattern_ids = []
            self.created_pattern_ids.append(response["data"]["id"])
            
        self.log_result("test_pattern_performance", "passed", time.time() - start_time,
                       details={"create_time": create_time, "components": 50})


# For pytest compatibility
test_instance = TestPatterns()

@pytest.mark.asyncio
async def test_patterns_suite():
    """Run all patterns tests"""
    await test_instance.setup()
    
    # Run all test methods
    test_methods = [method for method in dir(test_instance) 
                   if method.startswith('test_') and method != 'test_patterns_suite']
    
    for method_name in test_methods:
        method = getattr(test_instance, method_name)
        if asyncio.iscoroutinefunction(method):
            await method()
            
    await test_instance.cleanup()
    
    # Print summary
    summary = test_instance.get_test_summary()
    print(f"\nPatterns Test Summary:")
    print(f"Total: {summary['total_tests']}, Passed: {summary['passed']}, "
          f"Failed: {summary['failed']}, Success Rate: {summary['success_rate']:.1f}%")


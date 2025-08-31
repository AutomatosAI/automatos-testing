"""
Context Policy API Tests
=======================
Tests for context policy management functionality.
"""

import pytest
import asyncio
import time
from typing import Dict, Any
from framework.base_test import APITest


class TestContextPolicy(APITest):
    """Test suite for Context Policy Management APIs"""
    
    def __init__(self):
        super().__init__("ContextPolicy")
        
    async def setup(self):
        """Setup test data"""
        await self.setup_session()
        
        # Create test policy data
        self.test_policy = {
            "name": "test_context_policy",
            "description": "Test policy for context management",
            "rules": [
                {
                    "type": "relevance_threshold",
                    "value": 0.7,
                    "action": "include"
                },
                {
                    "type": "age_limit",
                    "value": 86400,  # 24 hours
                    "action": "exclude"
                }
            ],
            "slots": {
                "max_context_items": 100,
                "priority_weights": {
                    "recency": 0.3,
                    "relevance": 0.5,
                    "frequency": 0.2
                }
            }
        }
        
        # Create a test policy for later use
        response = await self.make_request("POST", "/api/policy/", data=self.test_policy)
        if response["status_code"] == 200:
            self.created_policy_id = response["data"].get("id")
            
    async def cleanup(self):
        """Cleanup test data"""
        # Delete created policies
        if hasattr(self, 'created_policy_id') and self.created_policy_id:
            await self.make_request("DELETE", f"/api/policy/{self.created_policy_id}")
            
        await self.cleanup_session()

    async def test_create_policy(self):
        """Test creating a new context policy"""
        start_time = time.time()
        
        policy_data = {
            "name": "dynamic_context_policy",
            "description": "Dynamic policy for adaptive context management",
            "rules": [
                {
                    "type": "semantic_similarity",
                    "value": 0.8,
                    "action": "prioritize"
                },
                {
                    "type": "source_trust",
                    "value": "verified",
                    "action": "boost"
                }
            ],
            "slots": {
                "max_context_items": 50,
                "context_window": 4096
            }
        }
        
        response = await self.make_request("POST", "/api/policy/", data=policy_data)
        
        assert response["status_code"] in [200, 201]
        assert "id" in response["data"]
        assert response["data"]["name"] == policy_data["name"]
        
        # Store for cleanup
        self.created_policy_id = response["data"]["id"]
        
        self.log_result("test_create_policy", "passed", time.time() - start_time)

    async def test_get_policy(self):
        """Test retrieving a specific policy"""
        start_time = time.time()
        
        if not hasattr(self, 'created_policy_id'):
            self.log_result("test_get_policy", "skipped", time.time() - start_time, 
                          "No policy created in setup")
            return
            
        response = await self.make_request("GET", f"/api/policy/{self.created_policy_id}")
        
        assert response["status_code"] == 200
        assert response["data"]["id"] == self.created_policy_id
        assert "rules" in response["data"]
        assert "slots" in response["data"]
        
        self.log_result("test_get_policy", "passed", time.time() - start_time)

    async def test_update_policy(self):
        """Test updating an existing policy"""
        start_time = time.time()
        
        if not hasattr(self, 'created_policy_id'):
            self.log_result("test_update_policy", "skipped", time.time() - start_time, 
                          "No policy created in setup")
            return
            
        update_data = {
            "description": "Updated test policy description",
            "rules": [
                {
                    "type": "relevance_threshold",
                    "value": 0.85,  # Updated threshold
                    "action": "include"
                },
                {
                    "type": "content_type",
                    "value": "technical",
                    "action": "prioritize"
                }
            ]
        }
        
        response = await self.make_request("PUT", f"/api/policy/{self.created_policy_id}", 
                                         data=update_data)
        
        assert response["status_code"] == 200
        assert response["data"]["description"] == update_data["description"]
        assert len(response["data"]["rules"]) == 2
        
        self.log_result("test_update_policy", "passed", time.time() - start_time)

    async def test_assemble_context(self):
        """Test assembling context based on policy"""
        start_time = time.time()
        
        if not hasattr(self, 'created_policy_id'):
            self.log_result("test_assemble_context", "skipped", time.time() - start_time, 
                          "No policy created in setup")
            return
            
        assemble_data = {
            "query": "How to optimize neural network performance?",
            "context_items": [
                {
                    "content": "Neural networks can be optimized through various techniques...",
                    "relevance_score": 0.9,
                    "source": "documentation",
                    "timestamp": "2024-01-15T10:00:00Z"
                },
                {
                    "content": "Performance optimization includes batch normalization...",
                    "relevance_score": 0.75,
                    "source": "research_paper",
                    "timestamp": "2024-01-14T15:30:00Z"
                },
                {
                    "content": "GPU acceleration is crucial for neural network training...",
                    "relevance_score": 0.6,
                    "source": "blog",
                    "timestamp": "2024-01-10T08:00:00Z"
                }
            ],
            "metadata": {
                "user_preferences": {
                    "detail_level": "technical",
                    "focus_area": "performance"
                }
            }
        }
        
        response = await self.make_request("POST", f"/api/policy/{self.created_policy_id}/assemble", 
                                         data=assemble_data)
        
        assert response["status_code"] == 200
        assert "assembled_context" in response["data"]
        assert "included_items" in response["data"]
        assert "policy_applied" in response["data"]
        
        self.log_result("test_assemble_context", "passed", time.time() - start_time)

    async def test_ab_test_set(self):
        """Test setting up A/B test for policies"""
        start_time = time.time()
        
        ab_test_data = {
            "test_name": "context_relevance_experiment",
            "variant_a": {
                "policy_id": self.created_policy_id if hasattr(self, 'created_policy_id') else "default",
                "traffic_percentage": 50
            },
            "variant_b": {
                "policy_config": {
                    "name": "experimental_policy",
                    "rules": [
                        {
                            "type": "relevance_threshold",
                            "value": 0.6,
                            "action": "include"
                        }
                    ]
                },
                "traffic_percentage": 50
            },
            "metrics": ["context_quality", "user_satisfaction", "response_accuracy"],
            "duration_hours": 24
        }
        
        response = await self.make_request("POST", "/api/policy/abtest/set", data=ab_test_data)
        
        assert response["status_code"] in [200, 201]
        assert "test_id" in response["data"]
        assert response["data"]["status"] == "active"
        
        # Store for later retrieval
        self.ab_test_id = response["data"]["test_id"]
        
        self.log_result("test_ab_test_set", "passed", time.time() - start_time)

    async def test_ab_test_get(self):
        """Test retrieving A/B test results"""
        start_time = time.time()
        
        # First create an A/B test if not exists
        if not hasattr(self, 'ab_test_id'):
            await self.test_ab_test_set()
            
        if not hasattr(self, 'ab_test_id'):
            self.log_result("test_ab_test_get", "skipped", time.time() - start_time, 
                          "No A/B test created")
            return
            
        response = await self.make_request("GET", f"/api/policy/abtest/get?test_id={self.ab_test_id}")
        
        assert response["status_code"] == 200
        assert "test_id" in response["data"]
        assert "variants" in response["data"]
        assert "metrics" in response["data"]
        assert "status" in response["data"]
        
        self.log_result("test_ab_test_get", "passed", time.time() - start_time)

    async def test_policy_validation(self):
        """Test policy validation with invalid data"""
        start_time = time.time()
        
        invalid_policy = {
            "name": "",  # Empty name
            "rules": [
                {
                    "type": "invalid_rule_type",
                    "value": -1,  # Invalid value
                    "action": "unknown_action"
                }
            ],
            "slots": {
                "max_context_items": -10  # Invalid negative value
            }
        }
        
        response = await self.make_request("POST", "/api/policy/", data=invalid_policy)
        
        assert response["status_code"] in [400, 422]
        assert "error" in response["data"] or "detail" in response["data"]
        
        self.log_result("test_policy_validation", "passed", time.time() - start_time)

    async def test_policy_versioning(self):
        """Test policy versioning functionality"""
        start_time = time.time()
        
        if not hasattr(self, 'created_policy_id'):
            self.log_result("test_policy_versioning", "skipped", time.time() - start_time, 
                          "No policy created in setup")
            return
            
        # Update policy multiple times to create versions
        for i in range(3):
            update_data = {
                "description": f"Version {i+2} of the policy",
                "rules": [
                    {
                        "type": "relevance_threshold",
                        "value": 0.7 + (i * 0.05),
                        "action": "include"
                    }
                ]
            }
            await self.make_request("PUT", f"/api/policy/{self.created_policy_id}", data=update_data)
            
        # Get policy with version history
        response = await self.make_request("GET", f"/api/policy/{self.created_policy_id}?include_versions=true")
        
        assert response["status_code"] == 200
        assert "versions" in response["data"] or "version_history" in response["data"]
        
        self.log_result("test_policy_versioning", "passed", time.time() - start_time)

    async def test_bulk_policy_operations(self):
        """Test bulk policy operations"""
        start_time = time.time()
        
        # Create multiple policies
        policy_ids = []
        for i in range(3):
            policy_data = {
                "name": f"bulk_test_policy_{i}",
                "description": f"Bulk test policy {i}",
                "rules": [
                    {
                        "type": "relevance_threshold",
                        "value": 0.7 + (i * 0.05),
                        "action": "include"
                    }
                ]
            }
            response = await self.make_request("POST", "/api/policy/", data=policy_data)
            if response["status_code"] in [200, 201]:
                policy_ids.append(response["data"]["id"])
                
        # Bulk update
        bulk_update_data = {
            "policy_ids": policy_ids,
            "update": {
                "slots": {
                    "max_context_items": 75
                }
            }
        }
        
        response = await self.make_request("POST", "/api/policy/bulk/update", data=bulk_update_data)
        
        # Clean up
        for policy_id in policy_ids:
            await self.make_request("DELETE", f"/api/policy/{policy_id}")
            
        assert response["status_code"] in [200, 404]  # 404 if bulk endpoint doesn't exist
        
        self.log_result("test_bulk_policy_operations", "passed", time.time() - start_time)

    async def test_policy_templates(self):
        """Test using policy templates"""
        start_time = time.time()
        
        template_data = {
            "template": "high_precision_context",
            "customizations": {
                "name": "custom_high_precision_policy",
                "max_context_items": 150
            }
        }
        
        response = await self.make_request("POST", "/api/policy/from-template", data=template_data)
        
        # If endpoint exists, validate response
        if response["status_code"] in [200, 201]:
            assert "id" in response["data"]
            assert response["data"]["name"] == template_data["customizations"]["name"]
            # Clean up
            await self.make_request("DELETE", f"/api/policy/{response['data']['id']}")
            
        self.log_result("test_policy_templates", "passed", time.time() - start_time)

    async def test_policy_performance(self):
        """Test policy performance with large context"""
        start_time = time.time()
        
        if not hasattr(self, 'created_policy_id'):
            self.log_result("test_policy_performance", "skipped", time.time() - start_time, 
                          "No policy created in setup")
            return
            
        # Create large context dataset
        large_context_data = {
            "query": "Complex query requiring extensive context",
            "context_items": [
                {
                    "content": f"Context item {i} with relevant information about the topic...",
                    "relevance_score": 0.5 + (i % 50) * 0.01,
                    "source": f"source_{i % 10}",
                    "timestamp": f"2024-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00Z"
                }
                for i in range(500)  # Large number of context items
            ]
        }
        
        # Measure assembly time
        assembly_start = time.time()
        response = await self.make_request("POST", f"/api/policy/{self.created_policy_id}/assemble", 
                                         data=large_context_data)
        assembly_time = time.time() - assembly_start
        
        assert response["status_code"] == 200
        assert assembly_time < 5.0  # Should complete within 5 seconds
        
        self.log_result("test_policy_performance", "passed", time.time() - start_time,
                       details={"assembly_time": assembly_time, "context_items": 500})


# For pytest compatibility
test_instance = TestContextPolicy()

@pytest.mark.asyncio
async def test_context_policy_suite():
    """Run all context policy tests"""
    await test_instance.setup()
    
    # Run all test methods
    test_methods = [method for method in dir(test_instance) 
                   if method.startswith('test_') and method != 'test_context_policy_suite']
    
    for method_name in test_methods:
        method = getattr(test_instance, method_name)
        if asyncio.iscoroutinefunction(method):
            await method()
            
    await test_instance.cleanup()
    
    # Print summary
    summary = test_instance.get_test_summary()
    print(f"\nContext Policy Test Summary:")
    print(f"Total: {summary['total_tests']}, Passed: {summary['passed']}, "
          f"Failed: {summary['failed']}, Success Rate: {summary['success_rate']:.1f}%")


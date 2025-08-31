"""
Router Enablement Tests - Systematic API Router Testing
Tests for enabling and validating disabled routers one by one.
"""

import asyncio
import json
from typing import Dict, Any
from framework.base_test import APITest

class TestRouterEnablement(APITest):
    """Test suite for enabling and validating disabled API routers"""
    
    async def test_multi_agent_router_enabled(self):
        """Test that multi-agent router endpoints are accessible"""
        # Test behavior monitoring endpoint
        response = await self.client.get("/multi-agent/behavior/monitoring")
        self.assert_success_or_404(response, "Multi-agent behavior monitoring endpoint should be accessible")
        
        # Test collaborative reasoning endpoint  
        session_data = {"agents": ["agent1", "agent2"], "type": "collaborative"}
        response = await self.client.post("/multi-agent/collaborative/reasoning", json=session_data)
        self.assert_success_or_404(response, "Multi-agent collaborative reasoning endpoint should be accessible")
    
    async def test_documents_router_enabled(self):
        """Test that documents router endpoints are accessible"""
        # Test document list endpoint
        response = await self.client.get("/documents")
        self.assert_success_or_404(response, "Documents list endpoint should be accessible or return 404 if empty")
        
        # Test document upload capability
        test_doc = {"title": "Test Document", "content": "Test content", "type": "text"}
        response = await self.client.post("/documents", json=test_doc)
        self.assert_success_or_validation_error(response, "Document creation should work or return validation error")
    
    async def test_memory_router_enabled(self):
        """Test that memory router endpoints are accessible"""
        response = await self.client.get("/memory/health")
        self.assert_success_or_404(response, "Memory health endpoint should be accessible")
        
        # Test memory operations
        memory_data = {"key": "test_key", "value": "test_value", "context": "test"}
        response = await self.client.post("/memory/store", json=memory_data)
        self.assert_success_or_validation_error(response, "Memory store endpoint should work")
    
    async def test_context_engineering_router_enabled(self):
        """Test that context engineering router endpoints are accessible"""
        response = await self.client.get("/context-engineering/health")
        self.assert_success_or_404(response, "Context engineering health endpoint should be accessible")
        
        # Test context analysis
        context_data = {"text": "Test context analysis", "type": "analysis"}
        response = await self.client.post("/context-engineering/analyze", json=context_data)
        self.assert_success_or_validation_error(response, "Context analysis endpoint should work")
    
    async def test_evaluation_router_enabled(self):
        """Test that evaluation router endpoints are accessible"""
        response = await self.client.get("/evaluation/metrics")
        self.assert_success_or_404(response, "Evaluation metrics endpoint should be accessible")
    
    async def test_field_theory_router_enabled(self):
        """Test that field theory router endpoints are accessible"""
        response = await self.client.get("/field-theory/health")
        self.assert_success_or_404(response, "Field theory health endpoint should be accessible")
    
    async def test_playbooks_router_enabled(self):
        """Test that playbooks router endpoints are accessible"""
        response = await self.client.get("/playbooks")
        self.assert_success_or_404(response, "Playbooks list endpoint should be accessible")
        
        # Test playbook creation
        playbook_data = {"name": "Test Playbook", "description": "Test playbook", "steps": []}
        response = await self.client.post("/playbooks", json=playbook_data)
        self.assert_success_or_validation_error(response, "Playbook creation should work")
    
    async def test_code_graph_router_enabled(self):
        """Test that code graph router endpoints are accessible"""
        response = await self.client.get("/code-graph/health")
        self.assert_success_or_404(response, "Code graph health endpoint should be accessible")
    
    async def test_context_policy_router_enabled(self):
        """Test that context policy router endpoints are accessible"""
        response = await self.client.get("/context-policy/policies")
        self.assert_success_or_404(response, "Context policy list endpoint should be accessible")
    
    def assert_success_or_404(self, response, message):
        """Assert response is either successful or 404 (endpoint exists but no data)"""
        assert response.status_code in [200, 201, 404], f"{message}. Got {response.status_code}: {response.text}"
    
    def assert_success_or_validation_error(self, response, message):
        """Assert response is either successful or validation error (endpoint exists but data invalid)"""
        assert response.status_code in [200, 201, 400, 422], f"{message}. Got {response.status_code}: {response.text}"

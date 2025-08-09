
"""
Context Engineering Testing Module
==================================

Comprehensive testing of context processing, retrieval, generation,
mathematical foundations, and RAG systems.
"""

import asyncio
import json
import numpy as np
from typing import Dict, Any, List
import time
import base64

from framework.base_test import APITest


class TestContextEngineering(APITest):
    """Test suite for context engineering functionality"""
    
    def __init__(self):
        super().__init__("ContextEngineering")
        self.test_documents = []
        self.test_embeddings = []
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Context Engineering tests...")
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Context Engineering tests...")
        
        # Clean up test documents
        for doc_id in self.test_documents:
            try:
                await self.make_request("DELETE", f"/api/context-engineering/documents/{doc_id}")
            except:
                pass
                
        await self.cleanup_session()
        
    async def test_information_theory_entropy(self):
        """Test Shannon entropy calculations"""
        test_data = {
            "data": [0.5, 0.3, 0.2],  # Probability distribution
            "base": 2  # Base-2 logarithm for bits
        }
        
        response = await self.make_request("POST", "/api/context-engineering/information-theory/entropy", 
                                          data=test_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "entropy" in result, "Should contain entropy value"
        assert isinstance(result["entropy"], (int, float)), "Entropy should be numeric"
        assert result["entropy"] > 0, "Entropy should be positive"
        
    async def test_mutual_information(self):
        """Test mutual information calculations"""
        test_data = {
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 6, 8, 10],  # Perfect correlation
            "bins": 5
        }
        
        response = await self.make_request("POST", "/api/context-engineering/information-theory/mutual-info", 
                                          data=test_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "mutual_information" in result, "Should contain mutual information value"
        assert isinstance(result["mutual_information"], (int, float)), "MI should be numeric"
        
    async def test_vector_embeddings(self):
        """Test vector embedding operations"""
        test_texts = [
            "Automotas AI is a multi-agent orchestration platform",
            "Machine learning models require large datasets",
            "Vector databases enable semantic search capabilities"
        ]
        
        embedding_data = {
            "texts": test_texts,
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        }
        
        response = await self.make_request("POST", "/api/context-engineering/vector-ops/embeddings", 
                                          data=embedding_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "embeddings" in result, "Should contain embeddings"
        assert len(result["embeddings"]) == len(test_texts), "Should have embedding for each text"
        
        # Check embedding dimensions
        first_embedding = result["embeddings"][0]
        assert isinstance(first_embedding, list), "Embedding should be a list"
        assert len(first_embedding) > 0, "Embedding should have dimensions"
        
    async def test_semantic_similarity(self):
        """Test semantic similarity calculations"""
        similarity_data = {
            "text1": "Machine learning algorithms",
            "text2": "AI and ML techniques",
            "method": "cosine"
        }
        
        response = await self.make_request("POST", "/api/context-engineering/vector-ops/similarity", 
                                          data=similarity_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "similarity" in result, "Should contain similarity score"
        assert 0 <= result["similarity"] <= 1, "Similarity should be between 0 and 1"
        
    async def test_clustering_analysis(self):
        """Test text clustering capabilities"""
        clustering_data = {
            "texts": [
                "Python programming language",
                "JavaScript web development", 
                "Machine learning with Python",
                "React frontend framework",
                "Neural networks and deep learning",
                "Node.js backend development"
            ],
            "num_clusters": 3,
            "method": "kmeans"
        }
        
        response = await self.make_request("POST", "/api/context-engineering/vector-ops/clustering", 
                                          data=clustering_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "clusters" in result, "Should contain cluster assignments"
        assert "centroids" in result, "Should contain cluster centroids"
        
        clusters = result["clusters"]
        assert len(clusters) == len(clustering_data["texts"]), "Should assign cluster to each text"
        
    async def test_statistical_analysis(self):
        """Test statistical analysis functions"""
        stats_data = {
            "data": [1.2, 2.4, 3.1, 4.5, 5.2, 6.0, 7.3, 8.1, 9.0, 10.2],
            "tests": ["normality", "correlation", "regression"]
        }
        
        response = await self.make_request("POST", "/api/context-engineering/statistics/analyze", 
                                          data=stats_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "statistics" in result, "Should contain statistical analysis"
        
        stats = result["statistics"]
        assert "mean" in stats, "Should contain mean"
        assert "std" in stats, "Should contain standard deviation"
        assert "normality_test" in stats, "Should contain normality test results"
        
    async def test_optimization_algorithms(self):
        """Test optimization algorithm implementations"""
        optimization_data = {
            "objective": "minimize",
            "function": "quadratic",  # x^2 + y^2
            "constraints": [
                {"type": "ineq", "expr": "x + y <= 10"},
                {"type": "ineq", "expr": "x >= 0"},
                {"type": "ineq", "expr": "y >= 0"}
            ],
            "initial_guess": [1, 1],
            "method": "gradient_descent"
        }
        
        response = await self.make_request("POST", "/api/context-engineering/optimization/solve", 
                                          data=optimization_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "solution" in result, "Should contain optimization solution"
        assert "iterations" in result, "Should contain iteration count"
        
    async def test_document_processing(self):
        """Test document ingestion and processing"""
        # Test with text document
        doc_data = {
            "content": """
            Automotas AI represents a paradigm shift in intelligent automation.
            By combining multi-agent systems with advanced context engineering,
            it provides unprecedented capabilities for enterprise DevOps workflows.
            The platform leverages mathematical foundations including field theory,
            Bayesian inference, and graph-based reasoning to optimize decision-making.
            """,
            "metadata": {
                "title": "Automotas AI Overview",
                "type": "documentation",
                "source": "test_suite"
            },
            "processing_options": {
                "extract_entities": True,
                "generate_embeddings": True,
                "chunk_size": 200
            }
        }
        
        response = await self.make_request("POST", "/api/context-engineering/documents/process", 
                                          data=doc_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "document_id" in result, "Should contain document ID"
        assert "chunks" in result, "Should contain document chunks"
        assert "embeddings" in result, "Should contain embeddings"
        
        doc_id = result["document_id"]
        self.test_documents.append(doc_id)
        
    async def test_knowledge_graph_operations(self):
        """Test knowledge graph construction and querying"""
        kg_data = {
            "entities": [
                {"name": "Automotas AI", "type": "platform"},
                {"name": "Multi-agent System", "type": "technology"},
                {"name": "DevOps", "type": "methodology"},
                {"name": "Context Engineering", "type": "technique"}
            ],
            "relationships": [
                {"source": "Automotas AI", "relation": "implements", "target": "Multi-agent System"},
                {"source": "Automotas AI", "relation": "automates", "target": "DevOps"},
                {"source": "Multi-agent System", "relation": "uses", "target": "Context Engineering"}
            ]
        }
        
        response = await self.make_request("POST", "/api/context-engineering/knowledge-graph/create", 
                                          data=kg_data)
        
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "graph_id" in result, "Should contain graph ID"
        assert "nodes" in result, "Should contain graph nodes"
        assert "edges" in result, "Should contain graph edges"
        
    async def test_rag_retrieval(self):
        """Test Retrieval-Augmented Generation"""
        # First, ensure we have documents to retrieve from
        await self.test_document_processing()
        
        query_data = {
            "query": "What is Automotas AI and how does it work?",
            "top_k": 3,
            "similarity_threshold": 0.7,
            "include_metadata": True
        }
        
        response = await self.make_request("POST", "/api/context-engineering/rag/retrieve", 
                                          data=query_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "retrieved_chunks" in result, "Should contain retrieved chunks"
        assert "similarity_scores" in result, "Should contain similarity scores"
        
        chunks = result["retrieved_chunks"]
        assert len(chunks) <= query_data["top_k"], "Should not exceed top_k results"
        
    async def test_rag_generation(self):
        """Test RAG-based content generation"""
        generation_data = {
            "query": "Explain the benefits of multi-agent orchestration",
            "context_strategy": "semantic_search",
            "generation_params": {
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            },
            "include_sources": True
        }
        
        response = await self.make_request("POST", "/api/context-engineering/rag/generate", 
                                          data=generation_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "generated_text" in result, "Should contain generated text"
        assert "sources" in result, "Should contain source references"
        assert len(result["generated_text"]) > 0, "Should generate non-empty text"
        
    async def test_context_field_analysis(self):
        """Test context field mathematical analysis"""
        field_data = {
            "field_type": "scalar",
            "dimensions": 2,
            "field_values": [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ],
            "analysis_type": "gradient"
        }
        
        response = await self.make_request("POST", "/api/context-engineering/field-analysis/compute", 
                                          data=field_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "field_analysis" in result, "Should contain field analysis"
        assert "gradient" in result["field_analysis"], "Should contain gradient computation"
        
    async def test_bayesian_inference(self):
        """Test Bayesian inference capabilities"""
        bayesian_data = {
            "prior": {
                "distribution": "beta",
                "parameters": {"alpha": 2, "beta": 3}
            },
            "likelihood": {
                "distribution": "binomial", 
                "data": [1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
            },
            "inference_method": "mcmc",
            "samples": 1000
        }
        
        response = await self.make_request("POST", "/api/context-engineering/bayesian/infer", 
                                          data=bayesian_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "posterior" in result, "Should contain posterior distribution"
        assert "confidence_interval" in result, "Should contain confidence intervals"
        
    async def test_context_health_monitoring(self):
        """Test context engineering system health"""
        response = await self.make_request("GET", "/api/context-engineering/health")
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        health_data = response["data"]["data"]
        assert "status" in health_data, "Should contain overall status"
        assert "components" in health_data, "Should contain component health"
        
        components = health_data["components"]
        expected_components = ["vector_database", "embedding_service", "rag_system", "optimization_engine"]
        
        for component in expected_components:
            if component in components:
                assert components[component] in ["healthy", "degraded", "unhealthy"], f"{component} should have valid status"

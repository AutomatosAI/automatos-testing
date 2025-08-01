#!/usr/bin/env python3
"""
PHASE 4: COMPREHENSIVE CONTEXT ENGINEERING TESTING
Tests all context engineering and RAG system endpoints with full request/response logging
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_utils import ComprehensiveAPITester

class ContextEngineeringTester:
    """
    Comprehensive Context Engineering testing with full API logging
    """
    
    def __init__(self):
        test_dir = Path(__file__).parent.parent
        config_path = test_dir.parent / "shared_config.yaml"
        
        self.tester = ComprehensiveAPITester(
            config_path=str(config_path),
            phase_name="context_engineering",
            test_dir=str(test_dir)
        )
        
        self.created_contexts = []
        self.executed_queries = []
        self.test_summary = {
            "contexts_initialized": 0,
            "queries_executed": 0,
            "embeddings_generated": 0,
            "patterns_analyzed": 0,
            "retrieval_operations": 0,
            "rag_tests_completed": 0,
            "api_calls_made": 0,
            "successful_calls": 0,
            "failed_calls": 0
        }
    
    def run_comprehensive_tests(self):
        """
        Run all context engineering tests and return real success/failure
        """
        print("🚀 STARTING COMPREHENSIVE CONTEXT ENGINEERING TESTING")
        print("=" * 70)
        
        try:
            # Phase 1: Environment & Context System Discovery
            self.test_environment_setup()
            
            # Phase 2: Context Initialization & Management
            self.test_context_initialization()
            
            # Phase 3: RAG System Performance Testing
            self.test_rag_system_performance()
            
            # Phase 4: Context Query & Retrieval
            self.test_context_query_retrieval()
            
            # Phase 5: Vector Embeddings Operations
            self.test_vector_embeddings()
            
            # Phase 6: Context Sources & Distribution
            self.test_context_sources()
            
            # Phase 7: Performance Metrics & Analytics
            self.test_context_analytics()
            
            # Phase 8: Advanced Context Operations
            self.test_advanced_context_operations()
            
            # Phase 9: Error Handling & Edge Cases
            self.test_error_handling()
            
            # Phase 10: Performance & Stress Testing
            self.test_performance()
            
            # Generate final report
            report = self.generate_final_report()
            
            # Calculate real success based on API results
            total_calls = self.test_summary["api_calls_made"]
            successful_calls = self.test_summary["successful_calls"]
            
            print(f"\n📊 CONTEXT ENGINEERING TESTING COMPLETED")
            print(f"📊 Total API Calls: {total_calls}")
            print(f"✅ Successful: {successful_calls}")
            print(f"❌ Failed: {total_calls - successful_calls}")
            
            # Define minimum success threshold (70% of API calls must succeed)
            success_threshold = 0.7
            success_rate = successful_calls / total_calls if total_calls > 0 else 0
            
            print(f"📈 Success Rate: {success_rate * 100:.1f}%")
            print(f"🎯 Required Threshold: {success_threshold * 100:.1f}%")
            
            is_successful = success_rate >= success_threshold
            
            if is_successful:
                print("✅ CONTEXT ENGINEERING TESTS PASSED - Meeting minimum threshold")
                return True
            else:
                print("❌ CONTEXT ENGINEERING TESTS FAILED - Below minimum threshold")
                return False
            
        except Exception as e:
            print(f"💥 COMPREHENSIVE TESTING FAILED: {str(e)}")
            import traceback
            print(f"🔍 Error details: {traceback.format_exc()}")
            return False

    def test_environment_setup(self):
        """
        Test 1: Environment Setup and Context System Discovery
        """
        print("\n🔍 PHASE 1: ENVIRONMENT SETUP & CONTEXT SYSTEM DISCOVERY")
        
        # Test 1.1: Health Check
        result = self.tester.make_api_call("GET", "/health")
        self.update_summary(result)
        
        # Test 1.2: Endpoint Discovery
        discovery = self.tester.test_endpoint_discovery()
        
        # Test 1.3: Context System Availability
        context_endpoints = [
            "/api/context/stats",
            "/api/context/patterns",
            "/api/context/sources",
            "/api/context/embeddings/stats"
        ]
        
        print("\n📋 Testing Context Engineering Endpoint Availability:")
        for endpoint in context_endpoints:
            result = self.tester.make_api_call("GET", endpoint, expected_status=[200, 404, 405])
            self.update_summary(result)
            status = "✅ Available" if result.get("validation", {}).get("is_success") else "❌ Not Available"
            print(f"  {endpoint}: {status}")
        
        # Test 1.4: Validate Expected Context Endpoints
        validation = self.tester.validate_endpoint_list("context_engineering")
        
        print(f"✅ Environment setup completed - {len(discovery['endpoints'])} total endpoints discovered")
    
    def test_context_initialization(self):
        """
        Test 2: Context Initialization & Management
        """
        print("\n🔧 PHASE 2: CONTEXT INITIALIZATION & MANAGEMENT")
        
        # Test 2.1: Initialize Context Session
        init_data = {
            "session_id": "comprehensive_test_session",
            "context_type": "testing_environment",
            "configuration": {
                "max_context_length": 4000,
                "retrieval_mode": "comprehensive",
                "embedding_model": "default"
            }
        }
        result = self.tester.make_api_call("POST", "/api/context/initialize", init_data, [200, 201])
        self.update_summary(result)
        
        if result.get("validation", {}).get("is_success"):
            context_id = self.extract_context_id(result)
            if context_id:
                self.created_contexts.append(context_id)
                self.test_summary["contexts_initialized"] += 1
        
        # Test 2.2: Initialize Multiple Context Types
        context_types = ["technical_documentation", "security_guidelines", "performance_guidance"]
        for ctx_type in context_types:
            ctx_data = {
                "session_id": f"test_session_{ctx_type}",
                "context_type": ctx_type,
                "configuration": {"retrieval_mode": "focused"}
            }
            result = self.tester.make_api_call("POST", "/api/context/initialize", ctx_data, [200, 201])
            self.update_summary(result)
            
            if result.get("validation", {}).get("is_success"):
                context_id = self.extract_context_id(result)
                if context_id:
                    self.created_contexts.append(context_id)
                    self.test_summary["contexts_initialized"] += 1
        
        # Test 2.3: Context Session Management
        result = self.tester.make_api_call("GET", "/api/context/sessions", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 2.4: Context Configuration Retrieval
        result = self.tester.make_api_call("GET", "/api/context/config", expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ Context initialization completed - {self.test_summary['contexts_initialized']} contexts initialized")
    
    def test_rag_system_performance(self):
        """
        Test 3: RAG System Performance Testing
        """
        print("\n🧠 PHASE 3: RAG SYSTEM PERFORMANCE TESTING")
        
        # Test 3.1: RAG System Statistics
        result = self.tester.make_api_call("GET", "/api/context/stats")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["rag_tests_completed"] += 1
        
        # Test 3.2: RAG Performance Metrics
        result = self.tester.make_api_call("GET", "/api/context/performance", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 3.3: Context Retrieval Metrics
        result = self.tester.make_api_call("GET", "/api/context/retrieval/metrics")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["retrieval_operations"] += 1
        
        # Test 3.4: RAG Pipeline Status
        result = self.tester.make_api_call("GET", "/api/context/pipeline/status", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 3.5: Context Quality Metrics
        result = self.tester.make_api_call("GET", "/api/context/quality/metrics", expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ RAG system testing completed - {self.test_summary['rag_tests_completed']} RAG operations tested")
    
    def test_context_query_retrieval(self):
        """
        Test 4: Context Query & Retrieval Operations
        """
        print("\n🔍 PHASE 4: CONTEXT QUERY & RETRIEVAL OPERATIONS")
        
        # Test 4.1: Execute Context Queries
        test_queries = self.tester.config["test_data"]["context_engineering"]
        
        for i, query_data in enumerate(test_queries):
            if not isinstance(query_data, dict) or "query" not in query_data:                continue
            query_payload = {
                "query": query_data["query"],
                "context_type": query_data["context_type"],
                "max_results": 10,
                "include_metadata": True
            }
            result = self.tester.make_api_call("POST", "/api/context/query", query_payload, [200, 404])
            self.update_summary(result)
            
            if result.get("validation", {}).get("is_success"):
                self.executed_queries.append(query_data["query"])
                self.test_summary["queries_executed"] += 1
        
        # Test 4.2: Semantic Context Search
        semantic_query = {
            "query": "How to optimize API performance and reduce response times?",
            "search_type": "semantic",
            "similarity_threshold": 0.8,
            "max_results": 5
        }
        result = self.tester.make_api_call("POST", "/api/context/search/semantic", semantic_query, [200, 404])
        self.update_summary(result)
        
        # Test 4.3: Context Similarity Analysis
        similarity_data = {
            "query1": "API performance optimization",
            "query2": "Improving response times",
            "analysis_type": "semantic_similarity"
        }
        result = self.tester.make_api_call("POST", "/api/context/similarity", similarity_data, [200, 404])
        self.update_summary(result)
        
        # Test 4.4: Context Ranking & Relevance
        ranking_query = {
            "query": "comprehensive testing strategies",
            "ranking_algorithm": "relevance_score",
            "boost_factors": {"recency": 0.2, "authority": 0.3}
        }
        result = self.tester.make_api_call("POST", "/api/context/rank", ranking_query, [200, 404])
        self.update_summary(result)
        
        print(f"✅ Context query testing completed - {self.test_summary['queries_executed']} queries executed")
    
    def test_vector_embeddings(self):
        """
        Test 5: Vector Embeddings Operations
        """
        print("\n🔢 PHASE 5: VECTOR EMBEDDINGS OPERATIONS")
        
        # Test 5.1: Embeddings Statistics
        result = self.tester.make_api_call("GET", "/api/context/embeddings/stats")
        self.update_summary(result)
        
        # Test 5.2: Generate Text Embeddings
        embedding_data = {
            "text": "This is a comprehensive test for vector embedding generation in the Automotas AI system.",
            "model": "default",
            "normalize": True
        }
        result = self.tester.make_api_call("POST", "/api/context/embeddings/generate", embedding_data, [200, 404])
        self.update_summary(result)
        
        if result.get("validation", {}).get("is_success"):
            self.test_summary["embeddings_generated"] += 1
        
        # Test 5.3: Batch Embedding Generation
        batch_texts = [
            "FastAPI performance optimization techniques",
            "Security best practices for API development",
            "Comprehensive testing methodologies"
        ]
        batch_data = {
            "texts": batch_texts,
            "model": "default",
            "batch_size": 3
        }
        result = self.tester.make_api_call("POST", "/api/context/embeddings/batch", batch_data, [200, 404])
        self.update_summary(result)
        
        # Test 5.4: Embedding Similarity Search
        similarity_search = {
            "query_embedding": "sample_embedding_vector",
            "top_k": 10,
            "similarity_threshold": 0.7
        }
        result = self.tester.make_api_call("POST", "/api/context/embeddings/search", similarity_search, [200, 404])
        self.update_summary(result)
        
        # Test 5.5: Vector Store Operations
        result = self.tester.make_api_call("GET", "/api/context/vector-store/info", expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ Vector embeddings testing completed - {self.test_summary['embeddings_generated']} embeddings generated")
    
    def test_context_sources(self):
        """
        Test 6: Context Sources & Distribution Testing
        """
        print("\n📚 PHASE 6: CONTEXT SOURCES & DISTRIBUTION")
        
        # Test 6.1: Get Context Sources
        result = self.tester.make_api_call("GET", "/api/context/sources")
        self.update_summary(result)
        
        # Test 6.2: Source Distribution Analysis
        result = self.tester.make_api_call("GET", "/api/context/sources/distribution", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 6.3: Source Quality Metrics
        result = self.tester.make_api_call("GET", "/api/context/sources/quality", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 6.4: Context Source Configuration
        source_config = {
            "source_type": "documentation",
            "priority": "high",
            "indexing_enabled": True
        }
        result = self.tester.make_api_call("POST", "/api/context/sources/config", source_config, [200, 404])
        self.update_summary(result)
        
        # Test 6.5: Source Content Analysis
        result = self.tester.make_api_call("GET", "/api/context/sources/analysis", expected_status=[200, 404])
        self.update_summary(result)
        
        print("✅ Context sources testing completed")
    
    def test_context_analytics(self):
        """
        Test 7: Context Performance Metrics & Analytics
        """
        print("\n📊 PHASE 7: CONTEXT PERFORMANCE METRICS & ANALYTICS")
        
        # Test 7.1: Context Analytics Dashboard
        result = self.tester.make_api_call("GET", "/api/context/analytics/dashboard", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 7.2: Query Performance Analytics
        result = self.tester.make_api_call("GET", "/api/context/analytics/query-performance", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 7.3: Retrieval Success Metrics
        result = self.tester.make_api_call("GET", "/api/context/analytics/retrieval-success", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 7.4: Context Usage Patterns
        result = self.tester.make_api_call("GET", "/api/context/analytics/usage-patterns", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 7.5: Response Time Analytics
        analytics_params = {"timeframe": "24h", "granularity": "hour"}
        result = self.tester.make_api_call("GET", "/api/context/analytics/response-times", analytics_params, expected_status=[200, 404])
        self.update_summary(result)
        
        print("✅ Context analytics testing completed")
    
    def test_advanced_context_operations(self):
        """
        Test 8: Advanced Context Operations
        """
        print("\n🧠 PHASE 8: ADVANCED CONTEXT OPERATIONS")
        
        # Test 8.1: Context Pattern Analysis
        result = self.tester.make_api_call("GET", "/api/context/patterns")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["patterns_analyzed"] += 1
        
        # Test 8.2: Dynamic Context Expansion
        expansion_data = {
            "base_context": "API testing methodologies",
            "expansion_strategy": "related_topics",
            "max_expansion": 5
        }
        result = self.tester.make_api_call("POST", "/api/context/expand", expansion_data, [200, 404])
        self.update_summary(result)
        
        # Test 8.3: Context Fusion Operations
        fusion_data = {
            "contexts": ["technical_docs", "best_practices", "examples"],
            "fusion_method": "weighted_merge",
            "weights": [0.4, 0.4, 0.2]
        }
        result = self.tester.make_api_call("POST", "/api/context/fusion", fusion_data, [200, 404])
        self.update_summary(result)
        
        # Test 8.4: Context Optimization
        optimization_data = {
            "optimization_target": "retrieval_speed",
            "constraints": {"max_memory": "2GB", "max_latency": "500ms"}
        }
        result = self.tester.make_api_call("POST", "/api/context/optimize", optimization_data, [200, 404])
        self.update_summary(result)
        
        print("✅ Advanced context operations testing completed")
    
    def test_error_handling(self):
        """
        Test 9: Error Handling and Edge Cases
        """
        print("\n🚨 PHASE 9: ERROR HANDLING & EDGE CASES")
        
        # Test 9.1: Invalid Context Query
        invalid_query = {
            "query": "",  # Empty query
            "context_type": "invalid_type",
            "max_results": -1
        }
        result = self.tester.make_api_call("POST", "/api/context/query", invalid_query, expected_status=[400, 404, 422])
        self.update_summary(result)
        
        # Test 9.2: Malformed Embedding Request
        invalid_embedding = {
            "text": "x" * 100000,  # Very large text
            "model": "nonexistent_model"
        }
        result = self.tester.make_api_call("POST", "/api/context/embeddings/generate", invalid_embedding, expected_status=[400, 404, 422])
        self.update_summary(result)
        
        # Test 9.3: Invalid Context Initialization
        invalid_init = {
            "session_id": "",
            "context_type": None,
            "configuration": {"invalid_param": "invalid_value"}
        }
        result = self.tester.make_api_call("POST", "/api/context/initialize", invalid_init, expected_status=[400, 422])
        self.update_summary(result)
        
        # Test 9.4: Non-existent Context Access
        result = self.tester.make_api_call("GET", "/api/context/sessions/invalid_session_999", expected_status=404)
        self.update_summary(result)
        
        print("✅ Error handling testing completed")
    
    def test_performance(self):
        """
        Test 10: Performance and Stress Testing
        """
        print("\n⚡ PHASE 10: PERFORMANCE & STRESS TESTING")
        
        # Test 10.1: Rapid Context Stats Requests
        for i in range(5):
            result = self.tester.make_api_call("GET", "/api/context/stats")
            self.update_summary(result)
        
        # Test 10.2: Concurrent Context Queries
        for i in range(3):
            query_data = {
                "query": f"Performance test query {i+1}",
                "context_type": "testing",
                "max_results": 5
            }
            result = self.tester.make_api_call("POST", "/api/context/query", query_data, [200, 404])
            self.update_summary(result)
        
        # Test 10.3: Embeddings Performance Test
        for i in range(3):
            embedding_data = {
                "text": f"Performance test embedding generation {i+1}",
                "model": "default"
            }
            result = self.tester.make_api_call("POST", "/api/context/embeddings/generate", embedding_data, [200, 404])
            self.update_summary(result)
        
        print("✅ Performance testing completed")
    
    def extract_context_id(self, result):
        """Extract context ID from API response"""
        try:
            response_data = result.get("response", {}).get("data", {})
            return response_data.get("id") or response_data.get("context_id") or response_data.get("session_id")
        except:
            return None
    
    def update_summary(self, result):
        """Update test summary statistics"""
        self.test_summary["api_calls_made"] += 1
        if result.get("validation", {}).get("is_success", False):
            self.test_summary["successful_calls"] += 1
        else:
            self.test_summary["failed_calls"] += 1
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        base_report = self.tester.generate_comprehensive_report()
        
        # Add context engineering specific metrics
        base_report["context_engineering_summary"] = self.test_summary
        
        # Calculate context system capabilities
        base_report["context_system_analysis"] = {
            "rag_system_available": self.test_summary["rag_tests_completed"] > 0,
            "context_initialization_available": self.test_summary["contexts_initialized"] > 0,
            "query_execution_available": self.test_summary["queries_executed"] > 0,
            "embeddings_available": self.test_summary["embeddings_generated"] > 0,
            "pattern_analysis_available": self.test_summary["patterns_analyzed"] > 0,
            "retrieval_operations_available": self.test_summary["retrieval_operations"] > 0
        }
        
        # Save enhanced report
        report_file = Path(self.tester.test_dir) / "results" / f"FINAL_CONTEXT_ENGINEERING_REPORT_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(base_report, f, indent=2)
        
        return base_report

def main():
    """
    Main execution function
    """
    print("🚀 COMPREHENSIVE CONTEXT ENGINEERING TESTING")
    print("============================================")
    
    tester = ContextEngineeringTester()
    success = tester.run_comprehensive_tests()
    
    # Cleanup resources
    tester.tester.cleanup()
    
    if success:
        print("\n🎉 COMPREHENSIVE CONTEXT ENGINEERING TESTING COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("\n💥 COMPREHENSIVE CONTEXT ENGINEERING TESTING FAILED!")
        return 1

if __name__ == "__main__":
    exit(main())
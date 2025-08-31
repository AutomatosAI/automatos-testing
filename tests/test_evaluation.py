"""
Evaluation System Testing Module
================================

Comprehensive testing for system evaluation, quality assessment,
component analysis, and benchmark validation functionality.
"""

import asyncio
import json
import time
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta

from framework.base_test import APITest, TestLevel


class TestEvaluation(APITest):
    """Test suite for evaluation system functionality"""
    
    def __init__(self):
        super().__init__("Evaluation")
        self.test_level = TestLevel.FUNCTIONAL
        self.evaluation_ids = []
        self.benchmark_ids = []
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Evaluation tests...")
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Evaluation tests...")
        
        # No specific cleanup needed as evaluations are read-only
        await self.cleanup_session()
        
    # System Evaluation Tests
    async def test_evaluate_system(self):
        """Test comprehensive system evaluation"""
        evaluation_request = {
            "evaluation_type": "comprehensive",
            "components": [
                "agents",
                "workflows", 
                "memory",
                "context_engineering",
                "multi_agent",
                "field_theory"
            ],
            "metrics": {
                "performance": True,
                "reliability": True,
                "scalability": True,
                "security": True
            },
            "test_scenarios": [
                {
                    "name": "Basic Operations",
                    "load": "light",
                    "duration": 60
                },
                {
                    "name": "Stress Test",
                    "load": "heavy",
                    "duration": 300
                }
            ],
            "generate_report": True
        }
        
        response = await self.make_request(
            "POST",
            "/api/evaluation/evaluate",
            json=evaluation_request
        )
        
        assert response["status_code"] == 200, f"System evaluation failed: {response}"
        result = response["json"]
        
        assert "evaluation_id" in result
        assert "status" in result
        assert result["status"] in ["running", "completed", "queued"]
        assert "estimated_duration" in result
        
        self.evaluation_ids.append(result["evaluation_id"])
        return result["evaluation_id"]
        
    async def test_quick_system_evaluation(self):
        """Test quick system evaluation"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/evaluate",
            json={
                "evaluation_type": "quick",
                "components": ["agents", "workflows"],
                "skip_stress_tests": True
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        self.evaluation_ids.append(result["evaluation_id"])
        
    # System Quality Tests
    async def test_evaluate_system_quality(self):
        """Test system quality evaluation"""
        quality_request = {
            "quality_dimensions": {
                "code_quality": {
                    "check_complexity": True,
                    "check_coverage": True,
                    "check_documentation": True
                },
                "architecture_quality": {
                    "check_modularity": True,
                    "check_coupling": True,
                    "check_patterns": True
                },
                "operational_quality": {
                    "check_monitoring": True,
                    "check_logging": True,
                    "check_error_handling": True
                }
            },
            "thresholds": {
                "min_code_coverage": 80,
                "max_complexity": 10,
                "max_coupling": 0.5
            }
        }
        
        response = await self.make_request(
            "POST",
            "/api/evaluation/system-quality",
            json=quality_request
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "quality_score" in result
        assert 0 <= result["quality_score"] <= 100
        assert "dimension_scores" in result
        assert "recommendations" in result
        
    async def test_code_quality_metrics(self):
        """Test code quality metrics evaluation"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/system-quality",
            json={
                "focus": "code_metrics",
                "include_details": True
            }
        )
        
        if response["status_code"] == 200:
            result = response["json"]
            assert "metrics" in result
            assert "cyclomatic_complexity" in result["metrics"]
            assert "test_coverage" in result["metrics"]
            assert "technical_debt" in result["metrics"]
            
    # Component Assessment Tests
    async def test_assess_component(self):
        """Test individual component assessment"""
        components_to_test = [
            "agent_manager",
            "workflow_engine",
            "memory_system",
            "context_processor",
            "field_manager"
        ]
        
        for component in components_to_test:
            response = await self.make_request(
                "POST",
                "/api/evaluation/component-assessment",
                json={
                    "component_name": component,
                    "assessment_type": "full",
                    "include_dependencies": True
                }
            )
            
            assert response["status_code"] == 200
            result = response["json"]
            
            assert "component_health" in result
            assert "performance_metrics" in result
            assert "dependency_status" in result
            
    async def test_component_performance_profiling(self):
        """Test component performance profiling"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/component-assessment",
            json={
                "component_name": "workflow_engine",
                "assessment_type": "performance",
                "profiling_options": {
                    "measure_latency": True,
                    "measure_throughput": True,
                    "measure_resource_usage": True,
                    "duration_seconds": 60
                }
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "latency_percentiles" in result
        assert "throughput_rps" in result
        assert "resource_usage" in result
        
    # Integration Analysis Tests
    async def test_analyze_integration(self):
        """Test integration analysis between components"""
        integration_pairs = [
            {
                "source": "agents",
                "target": "workflows",
                "integration_type": "api"
            },
            {
                "source": "context_engineering",
                "target": "memory",
                "integration_type": "data_flow"
            },
            {
                "source": "multi_agent",
                "target": "field_theory",
                "integration_type": "event_driven"
            }
        ]
        
        response = await self.make_request(
            "POST",
            "/api/evaluation/integration-analysis",
            json={
                "integrations": integration_pairs,
                "analysis_depth": "detailed",
                "check_contracts": True,
                "check_performance": True
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "integration_health" in result
        assert "contract_violations" in result
        assert "performance_bottlenecks" in result
        assert "recommendations" in result
        
    async def test_data_flow_analysis(self):
        """Test data flow analysis across system"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/integration-analysis",
            json={
                "analysis_type": "data_flow",
                "trace_paths": [
                    {
                        "start": "document_upload",
                        "end": "rag_response"
                    },
                    {
                        "start": "agent_creation",
                        "end": "task_execution"
                    }
                ],
                "include_transformations": True
            }
        )
        
        if response["status_code"] == 200:
            result = response["json"]
            assert "data_paths" in result
            assert "transformation_points" in result
            assert "data_integrity_checks" in result
            
    # Benchmark Validation Tests
    async def test_validate_benchmark(self):
        """Test benchmark validation"""
        benchmark_config = {
            "benchmark_name": "AutomatosAI Performance Benchmark v1",
            "scenarios": [
                {
                    "name": "Agent Creation Speed",
                    "operations": ["create_agent"],
                    "target_rps": 100,
                    "duration": 60
                },
                {
                    "name": "Workflow Execution Throughput",
                    "operations": ["execute_workflow"],
                    "target_rps": 50,
                    "duration": 120
                },
                {
                    "name": "Context Retrieval Latency",
                    "operations": ["retrieve_context"],
                    "target_p99_ms": 100,
                    "duration": 60
                }
            ],
            "baseline_comparison": True,
            "generate_report": True
        }
        
        response = await self.make_request(
            "POST",
            "/api/evaluation/benchmark-validation",
            json=benchmark_config
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "benchmark_id" in result
        assert "validation_status" in result
        assert "results_summary" in result
        
        self.benchmark_ids.append(result["benchmark_id"])
        return result["benchmark_id"]
        
    async def test_regression_benchmark(self):
        """Test regression benchmark against baseline"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/benchmark-validation",
            json={
                "benchmark_type": "regression",
                "baseline_version": "1.0.0",
                "current_version": "1.1.0",
                "tolerance_percentage": 5,
                "fail_on_regression": True
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "regression_detected" in result
        assert "performance_delta" in result
        
    # Comprehensive Evaluation Tests
    async def test_comprehensive_evaluation(self):
        """Test comprehensive system evaluation"""
        comprehensive_config = {
            "evaluation_name": "Full System Assessment",
            "include_all_components": True,
            "evaluation_categories": {
                "functionality": {
                    "test_core_features": True,
                    "test_edge_cases": True,
                    "test_error_handling": True
                },
                "performance": {
                    "load_testing": True,
                    "stress_testing": True,
                    "endurance_testing": True
                },
                "security": {
                    "vulnerability_scanning": True,
                    "penetration_testing": True,
                    "compliance_check": True
                },
                "usability": {
                    "api_consistency": True,
                    "documentation_quality": True,
                    "error_messages": True
                }
            },
            "parallel_execution": True,
            "time_limit_hours": 2
        }
        
        response = await self.make_request(
            "POST",
            "/api/evaluation/comprehensive",
            json=comprehensive_config
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "evaluation_id" in result
        assert "estimated_completion" in result
        assert "evaluation_plan" in result
        
        self.evaluation_ids.append(result["evaluation_id"])
        
    async def test_ml_model_evaluation(self):
        """Test ML model evaluation"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/comprehensive",
            json={
                "evaluation_focus": "ml_models",
                "models": ["embedding_model", "classification_model"],
                "metrics": ["accuracy", "precision", "recall", "f1", "latency"],
                "test_datasets": ["validation_set", "test_set"],
                "compare_versions": True
            }
        )
        
        if response["status_code"] == 200:
            result = response["json"]
            assert "model_metrics" in result
            assert "performance_comparison" in result
            
    # Assessment Report Generation Tests
    async def test_generate_assessment_report(self):
        """Test assessment report generation"""
        # First run an evaluation
        eval_id = await self.test_evaluate_system()
        
        # Wait a bit for evaluation to complete
        await asyncio.sleep(2)
        
        report_config = {
            "evaluation_id": eval_id,
            "report_format": "detailed",
            "include_sections": {
                "executive_summary": True,
                "detailed_findings": True,
                "recommendations": True,
                "technical_metrics": True,
                "visualizations": True
            },
            "output_formats": ["json", "markdown", "pdf"]
        }
        
        response = await self.make_request(
            "POST",
            "/api/evaluation/assessment-report",
            json=report_config
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "report_id" in result
        assert "report_urls" in result
        assert "generation_timestamp" in result
        
    async def test_custom_report_generation(self):
        """Test custom report generation"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/assessment-report",
            json={
                "report_type": "custom",
                "title": "Automatos AI Performance Analysis",
                "sections": [
                    {
                        "name": "API Performance",
                        "metrics": ["latency", "throughput", "error_rate"]
                    },
                    {
                        "name": "System Reliability",
                        "metrics": ["uptime", "mtbf", "recovery_time"]
                    }
                ],
                "time_range": {
                    "start": (datetime.now() - timedelta(days=7)).isoformat(),
                    "end": datetime.now().isoformat()
                }
            }
        )
        
        if response["status_code"] == 200:
            result = response["json"]
            assert "report_content" in result
            
    # Result Retrieval Tests
    async def test_get_evaluation_result(self):
        """Test retrieving evaluation results"""
        # Run an evaluation first
        eval_id = await self.test_quick_system_evaluation()
        
        # Wait for completion
        await asyncio.sleep(3)
        
        response = await self.make_request(
            "GET",
            f"/api/evaluation/results/{eval_id}"
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert "evaluation_id" in result
        assert result["evaluation_id"] == eval_id
        assert "status" in result
        assert "results" in result
        assert "completion_time" in result
        
    async def test_get_evaluation_history(self):
        """Test retrieving evaluation history"""
        response = await self.make_request(
            "GET",
            "/api/evaluation/history",
            params={
                "limit": 10,
                "offset": 0,
                "filter_type": "all"
            }
        )
        
        assert response["status_code"] == 200
        history = response["json"]
        
        assert "evaluations" in history
        assert isinstance(history["evaluations"], list)
        assert "total_count" in history
        
        if history["evaluations"]:
            eval_entry = history["evaluations"][0]
            assert "evaluation_id" in eval_entry
            assert "timestamp" in eval_entry
            assert "type" in eval_entry
            assert "status" in eval_entry
            
    # Performance Metrics Tests
    async def test_get_performance_metrics(self):
        """Test retrieving system performance metrics"""
        response = await self.make_request(
            "GET",
            "/api/evaluation/performance-metrics"
        )
        
        assert response["status_code"] == 200
        metrics = response["json"]
        
        assert "current_metrics" in metrics
        assert "historical_trends" in metrics
        assert "component_breakdown" in metrics
        
        current = metrics["current_metrics"]
        assert "cpu_usage" in current
        assert "memory_usage" in current
        assert "request_rate" in current
        assert "error_rate" in current
        
    async def test_performance_metrics_with_filters(self):
        """Test performance metrics with time filters"""
        response = await self.make_request(
            "GET",
            "/api/evaluation/performance-metrics",
            params={
                "time_range": "last_hour",
                "components": ["agents", "workflows"],
                "metrics": ["latency", "throughput"],
                "aggregation": "5min"
            }
        )
        
        if response["status_code"] == 200:
            metrics = response["json"]
            assert "time_series_data" in metrics
            assert "aggregated_stats" in metrics
            
    # Health Check Tests
    async def test_evaluation_health_check(self):
        """Test evaluation system health check"""
        response = await self.make_request(
            "GET",
            "/api/evaluation/health"
        )
        
        assert response["status_code"] == 200
        health = response["json"]
        
        assert "status" in health
        assert health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "evaluation_queue_size" in health
        assert "active_evaluations" in health
        assert "last_evaluation_time" in health
        
    # Edge Cases and Error Handling
    async def test_invalid_evaluation_type(self):
        """Test handling invalid evaluation types"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/evaluate",
            json={
                "evaluation_type": "invalid_type",
                "components": ["agents"]
            }
        )
        
        assert response["status_code"] in [400, 422]
        
    async def test_evaluation_timeout_handling(self):
        """Test evaluation timeout handling"""
        response = await self.make_request(
            "POST",
            "/api/evaluation/evaluate",
            json={
                "evaluation_type": "comprehensive",
                "timeout_seconds": 1,  # Very short timeout
                "components": ["all"]
            }
        )
        
        if response["status_code"] == 200:
            eval_id = response["json"]["evaluation_id"]
            self.evaluation_ids.append(eval_id)
            
            # Wait and check status
            await asyncio.sleep(2)
            
            status_response = await self.make_request(
                "GET",
                f"/api/evaluation/results/{eval_id}"
            )
            
            if status_response["status_code"] == 200:
                assert status_response["json"]["status"] in ["timeout", "failed"]
                
    async def test_concurrent_evaluations(self):
        """Test handling concurrent evaluations"""
        eval_tasks = []
        
        for i in range(3):
            task = self.make_request(
                "POST",
                "/api/evaluation/evaluate",
                json={
                    "evaluation_type": "quick",
                    "components": ["agents"],
                    "evaluation_name": f"Concurrent Test {i}"
                }
            )
            eval_tasks.append(task)
            
        responses = await asyncio.gather(*eval_tasks, return_exceptions=True)
        
        successful = 0
        for response in responses:
            if isinstance(response, dict) and response.get("status_code") == 200:
                successful += 1
                self.evaluation_ids.append(response["json"]["evaluation_id"])
                
        assert successful >= 2, "At least 2 concurrent evaluations should succeed"
        
    async def test_evaluation_result_pagination(self):
        """Test pagination of evaluation results"""
        # Get history with pagination
        page_size = 5
        response = await self.make_request(
            "GET",
            "/api/evaluation/history",
            params={
                "limit": page_size,
                "offset": 0
            }
        )
        
        assert response["status_code"] == 200
        first_page = response["json"]
        
        if first_page["total_count"] > page_size:
            # Get second page
            response = await self.make_request(
                "GET",
                "/api/evaluation/history",
                params={
                    "limit": page_size,
                    "offset": page_size
                }
            )
            
            assert response["status_code"] == 200
            second_page = response["json"]
            
            # Ensure no overlap
            first_ids = [e["evaluation_id"] for e in first_page["evaluations"]]
            second_ids = [e["evaluation_id"] for e in second_page["evaluations"]]
            assert not set(first_ids).intersection(set(second_ids))


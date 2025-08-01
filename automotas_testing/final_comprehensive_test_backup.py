"""
FINAL COMPREHENSIVE API TEST REPORT FOR AUTOMOTAS AI SYSTEM
==========================================================

This test discovers and tests ALL available endpoints using real data and provides
detailed analysis for bug-fixing agents.

Based on OpenAPI discovery, available endpoints:
- GET /health  
- GET /api/system/metrics

Missing expected endpoints:
- POST /api/agents (404 Not Found)
- POST /api/workflows (404 Not Found) 
- POST /api/admin/documents/upload (404 Not Found)
"""

import asyncio
import json
import os
import sys
import time
import traceback
from datetime import datetime
from typing import Dict, Any, List

import httpx
import pytest
import yaml

# Import the EnhancedWorkflowLogger from the system
sys.path.append('/root/automotas-ai/orchestrator')
from logging_utils import EnhancedWorkflowLogger

# Initialize logger
logger = EnhancedWorkflowLogger(
    workflow_id='final_api_testing', 
    log_file='logs/final_test_results.log'
)

class APIAnalyzer:
    """Comprehensive API analysis and testing"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.available_endpoints = []
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": base_url,
            "total_endpoints_discovered": 0,
            "successful_tests": 0,
            "failed_tests": 0,
            "endpoint_results": {},
            "missing_endpoints": [],
            "recommendations": []
        }

    async def discover_endpoints(self) -> List[Dict[str, str]]:
        """Discover all available endpoints using OpenAPI spec"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/openapi.json")
                if response.status_code == 200:
                    spec = response.json()
                    endpoints = []
                    for path, methods in spec.get('paths', {}).items():
                        for method in methods.keys():
                            endpoints.append({
                                "method": method.upper(),
                                "path": path,
                                "full_url": f"{self.base_url}{path}"
                            })
                    
                    self.available_endpoints = endpoints
                    self.test_results["total_endpoints_discovered"] = len(endpoints)
                    
                    logger.log_workflow_step(
                        step_id="endpoint_discovery",
                        step_name="API Endpoint Discovery",
                        agent_id="api_analyzer",
                        status="completed",
                        metadata={
                            "endpoints_found": len(endpoints),
                            "endpoints": endpoints
                        }
                    )
                    return endpoints
        except Exception as e:
            logger.log_workflow_step(
                step_id="endpoint_discovery_error",
                step_name="Failed to discover endpoints",
                agent_id="api_analyzer", 
                status="failed",
                metadata={"error": str(e)}
            )
        return []

    async def test_endpoint(self, endpoint: Dict[str, str]) -> Dict[str, Any]:
        """Test a specific endpoint and return detailed results"""
        method = endpoint["method"]
        url = endpoint["full_url"]
        
        start_time = time.time()
        result = {
            "method": method,
            "url": url,
            "success": False,
            "status_code": 0,
            "response": None,
            "duration": 0,
            "error": None
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Add authentication headers for all requests
                headers = {
                    "Content-Type": "application/json",
                    "X-API-Key": "test_api_key_for_backend_validation_2025",
                    "Authorization": "Bearer test_api_key_for_backend_validation_2025"
                }
                
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    # Use real test data for POST requests
                    test_data = self.get_test_data_for_endpoint(endpoint["path"])
                    response = await client.post(url, headers=headers, json=test_data)
                elif method == "PUT":
                    test_data = self.get_test_data_for_endpoint(endpoint["path"])
                    response = await client.put(url, headers=headers, json=test_data)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    response = await client.request(method, url, headers=headers)
                
                result["status_code"] = response.status_code
                result["duration"] = time.time() - start_time
                result["success"] = response.status_code < 400
                
                # Parse response
                try:
                    result["response"] = response.json() if response.content else {}
                except:
                    result["response"] = {"raw_content": response.text[:1000]}
                    
        except Exception as e:
            result["duration"] = time.time() - start_time
            result["error"] = str(e)
            result["success"] = False
            
        # Log the result
        status = "completed" if result["success"] else "failed"
        logger.log_workflow_step(
            step_id=f"test_{method.lower()}_{endpoint['path'].replace('/', '_')}",
            step_name=f"Testing {method} {endpoint['path']}",
            agent_id="api_tester",
            status=status,
            metadata=result
        )
        
        # Update test results
        if result["success"]:
            self.test_results["successful_tests"] += 1
        else:
            self.test_results["failed_tests"] += 1
            
        self.test_results["endpoint_results"][f"{method} {endpoint['path']}"] = result
        
        return result

    def get_test_data_for_endpoint(self, path: str) -> Dict[str, Any]:
        """Get appropriate test data for specific endpoints"""
        if "agent" in path.lower():
            return {
                "name": "Test Context Engineering Agent",
                "description": "Agent specialized in context engineering and retrieval",
                "agent_type": "specialist",
                "configuration": {
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "specialization": "context_engineering",
                    "capabilities": ["document_analysis", "context_retrieval", "knowledge_synthesis"]
                }
            }
        elif "workflow" in path.lower():
            return {
                "name": "Code Analysis Workflow",
                "description": "Multi-step workflow for comprehensive code analysis",
                "type": "analysis",
                "steps": [
                    {"step": "code_scanning", "agent": "code_analyzer", "priority": 1},
                    {"step": "security_check", "agent": "security_specialist", "priority": 2},
                    {"step": "performance_analysis", "agent": "performance_optimizer", "priority": 3}
                ],
                "triggers": ["code_commit", "manual_request"],
                "output_format": "detailed_report"
            }
        elif "document" in path.lower():
            return {
                "title": "Context Engineering Research",
                "content": "Research on context engineering principles and applications in AI systems",
                "document_type": "research_paper",
                "metadata": {
                    "author": "Context Engineering Team",
                    "tags": ["context", "AI", "research"],
                    "importance": "high"
                }
            }
        else:
            return {"test": "data", "timestamp": datetime.now().isoformat()}

    def generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final analysis report"""
        
        # Analyze missing endpoints
        expected_endpoints = [
            "POST /api/agents",
            "GET /api/agents", 
            "POST /api/workflows",
            "GET /api/workflows",
            "POST /api/admin/documents/upload",
            "GET /api/context/search"
        ]
        
        found_endpoints = set(f"{ep['method']} {ep['path']}" for ep in self.available_endpoints)
        missing = [ep for ep in expected_endpoints if ep not in found_endpoints]
        self.test_results["missing_endpoints"] = missing
        
        # Generate recommendations
        recommendations = []
        if missing:
            recommendations.append({
                "category": "Missing Endpoints",
                "severity": "HIGH", 
                "issue": f"Expected endpoints not implemented: {', '.join(missing)}",
                "recommendation": "Implement missing API endpoints according to system design"
            })
            
        if self.test_results["failed_tests"] > 0:
            recommendations.append({
                "category": "Failed Tests",
                "severity": "MEDIUM",
                "issue": f"{self.test_results['failed_tests']} endpoint tests failed",
                "recommendation": "Review failed endpoint implementations and error handling"
            })
            
        # Success rate analysis
        total_tests = self.test_results["successful_tests"] + self.test_results["failed_tests"]
        success_rate = (self.test_results["successful_tests"] / total_tests * 100) if total_tests > 0 else 0
        
        if success_rate < 50:
            recommendations.append({
                "category": "Low Success Rate",
                "severity": "HIGH",
                "issue": f"Only {success_rate:.1f}% of tests passed",
                "recommendation": "Major API implementation issues need attention"
            })
        elif success_rate < 80:
            recommendations.append({
                "category": "Moderate Success Rate", 
                "severity": "MEDIUM",
                "issue": f"{success_rate:.1f}% success rate indicates some issues",
                "recommendation": "Address failing endpoints and improve error handling"
            })
            
        self.test_results["recommendations"] = recommendations
        self.test_results["success_rate"] = success_rate
        
        return self.test_results

class TestCompleteAPI:
    """Complete API testing with real endpoint discovery"""
    
    @pytest.mark.asyncio
    async def test_complete_api_suite(self):
        """Comprehensive test of entire API"""
        
        # Test against the working API server
        analyzer = APIAnalyzer("http://localhost:8000")
        
        print("🔍 Discovering available API endpoints...")
        endpoints = await analyzer.discover_endpoints()
        
        assert len(endpoints) > 0, "No API endpoints discovered"
        print(f"✅ Discovered {len(endpoints)} endpoints")
        
        # Test each discovered endpoint
        print("🧪 Testing all discovered endpoints...")
        for endpoint in endpoints:
            result = await analyzer.test_endpoint(endpoint)
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"  {status} {endpoint['method']} {endpoint['path']} (Status: {result['status_code']})")
            
        # Generate final report
        final_report = analyzer.generate_final_report()
        
        # Save detailed report
        os.makedirs('logs', exist_ok=True)
        with open('logs/comprehensive_api_analysis.json', 'w') as f:
            json.dump(final_report, f, indent=2)
            
        print(f"\n📊 TEST SUMMARY:")
        print(f"  • Total Endpoints Tested: {final_report['total_endpoints_discovered']}")
        print(f"  • Successful Tests: {final_report['successful_tests']}")
        print(f"  • Failed Tests: {final_report['failed_tests']}")
        print(f"  • Success Rate: {final_report['success_rate']:.1f}%")
        print(f"  • Missing Expected Endpoints: {len(final_report['missing_endpoints'])}")
        
        if final_report['missing_endpoints']:
            print(f"\n🚨 MISSING ENDPOINTS:")
            for endpoint in final_report['missing_endpoints']:
                print(f"  ❌ {endpoint}")
                
        if final_report['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in final_report['recommendations']:
                print(f"  🔴 {rec['severity']}: {rec['issue']}")
                print(f"     → {rec['recommendation']}")
        
        print(f"\n📁 Detailed logs saved to: logs/comprehensive_api_analysis.json")
        
        # The test passes if we successfully tested at least the health endpoint
        assert final_report['successful_tests'] > 0, "No endpoints passed testing"

if __name__ == "__main__":
    print("🎯 FINAL COMPREHENSIVE API TESTING")
    print("==================================")
    pytest.main([__file__, "-v", "--tb=short", "-s"])
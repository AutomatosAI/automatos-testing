#!/usr/bin/env python3
"""
Shared utilities for comprehensive Automotas AI testing
Provides full API response logging and validation
"""

import httpx
import json
import time
import yaml
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

# Fallback logger if EnhancedWorkflowLogger is not available
class FallbackLogger:
    def __init__(self, workflow_id: str, log_file: str):
        self.workflow_id = workflow_id
        self.log_file = log_file
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    def log_workflow_step(self, step_id: str, step_name: str, agent_id: str, 
                         status: str = "pending", metadata: Dict[str, Any] = None):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "workflow_id": self.workflow_id,
            "step_id": step_id,
            "step_name": step_name,
            "agent_id": agent_id,
            "status": status,
            "metadata": metadata or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(f"{json.dumps(log_entry, indent=2)}\n")

class ComprehensiveAPITester:
    """
    Comprehensive API testing class with full request/response logging
    """
    
    def __init__(self, config_path: str, phase_name: str, test_dir: str):
        self.phase_name = phase_name
        self.test_dir = Path(test_dir)
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize logger
        log_file = self.test_dir / "logs" / f"{phase_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        try:
            # Try to use the user's EnhancedWorkflowLogger
            from logging_utils import EnhancedWorkflowLogger
            self.logger = EnhancedWorkflowLogger(
                workflow_id=f"comprehensive_{phase_name}_testing",
                log_file=str(log_file)
            )
        except ImportError:
            # Fallback to our own logger
            self.logger = FallbackLogger(
                workflow_id=f"comprehensive_{phase_name}_testing",
                log_file=str(log_file)
            )
        
        # Initialize HTTP client
        self.client = httpx.Client(
            timeout=self.config['api']['timeout'],
            headers=self.config['api']['authentication']['headers']
        )
        
        # Initialize tracking
        self.test_results = []
        self.api_responses = {}
        self.performance_metrics = {}
        
        # Create directories
        for subdir in ['logs', 'results', 'responses']:
            (self.test_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def make_api_call(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                      expected_status: Union[int, List[int]] = 200) -> Dict[str, Any]:
        """
        Make API call with comprehensive logging
        """
        start_time = time.time()
        full_url = f"{self.config['api']['base_url']}{endpoint}"
        
        # Log request details
        request_details = {
            "method": method,
            "endpoint": endpoint,
            "full_url": full_url,
            "headers": dict(self.client.headers),
            "data": data,
            "expected_status": expected_status,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Make the actual API call
            if method.upper() == "GET":
                response = self.client.get(full_url, params=data)
            elif method.upper() == "POST":
                response = self.client.post(full_url, json=data)
            elif method.upper() == "PUT":
                response = self.client.put(full_url, json=data)
            elif method.upper() == "DELETE":
                response = self.client.delete(full_url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Parse response
            try:
                response_data = response.json() if response.content else {}
            except json.JSONDecodeError:
                response_data = {"raw_content": response.text}
            
            # Determine success
            expected_statuses = expected_status if isinstance(expected_status, list) else [expected_status]
            is_success = response.status_code in expected_statuses
            
            # Create comprehensive result
            result = {
                "request": request_details,
                "response": {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "data": response_data,
                    "raw_text": response.text[:1000] if len(response.text) > 1000 else response.text,  # Truncate if too long
                    "content_length": len(response.content),
                    "response_time_ms": round(response_time, 2)
                },
                "validation": {
                    "is_success": is_success,
                    "expected_status": expected_status,
                    "actual_status": response.status_code
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Log the result
            self.logger.log_workflow_step(
                step_id=f"api_call_{method}_{endpoint.replace('/', '_')}",
                step_name=f"{method} {endpoint}",
                agent_id="comprehensive_tester",
                status="completed" if is_success else "failed",
                metadata=result
            )
            
            # Store for analysis
            self.test_results.append(result)
            response_key = f"{method}_{endpoint}"
            self.api_responses[response_key] = result
            
            # Save individual response file
            response_file = self.test_dir / "responses" / f"{response_key.replace('/', '_')}_{int(time.time())}.json"
            with open(response_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            # Log error
            error_result = {
                "request": request_details,
                "error": {
                    "type": type(e).__name__,
                    "message": str(e),
                    "traceback": traceback.format_exc()
                },
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.log_workflow_step(
                step_id=f"api_call_{method}_{endpoint.replace('/', '_')}_error",
                step_name=f"{method} {endpoint} - ERROR",
                agent_id="comprehensive_tester",
                status="error",
                metadata=error_result
            )
            
            self.test_results.append(error_result)
            return error_result
    
    def test_endpoint_discovery(self) -> Dict[str, Any]:
        """
        Discover available endpoints from OpenAPI spec
        """
        self.logger.log_workflow_step(
            step_id="endpoint_discovery_start",
            step_name="Starting Endpoint Discovery",
            agent_id="comprehensive_tester",
            status="in_progress"
        )
        
        # Get OpenAPI spec
        openapi_result = self.make_api_call("GET", "/openapi.json")
        
        endpoints = []
        if openapi_result.get("validation", {}).get("is_success"):
            try:
                openapi_data = openapi_result["response"]["data"]
                paths = openapi_data.get("paths", {})
                
                for path, methods in paths.items():
                    for method in methods.keys():
                        if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                            endpoints.append({
                                "method": method.upper(),
                                "path": path,
                                "full_endpoint": f"{method.upper()} {path}"
                            })
            except Exception as e:
                self.logger.log_workflow_step(
                    step_id="endpoint_discovery_error",
                    step_name="Endpoint Discovery Failed",
                    agent_id="comprehensive_tester",
                    status="error",
                    metadata={"error": str(e)}
                )
        
        discovery_result = {
            "total_endpoints": len(endpoints),
            "endpoints": endpoints,
            "openapi_result": openapi_result
        }
        
        # Save discovery results
        discovery_file = self.test_dir / "results" / f"endpoint_discovery_{int(time.time())}.json"
        with open(discovery_file, 'w') as f:
            json.dump(discovery_result, f, indent=2)
        
        self.logger.log_workflow_step(
            step_id="endpoint_discovery_complete",
            step_name="Endpoint Discovery Complete",
            agent_id="comprehensive_tester",
            status="completed",
            metadata=discovery_result
        )
        
        return discovery_result
    
    def validate_endpoint_list(self, endpoint_category: str) -> Dict[str, Any]:
        """
        Validate expected endpoints against discovered endpoints
        """
        expected = self.config.get("expected_endpoints", {}).get(endpoint_category, [])
        
        # Get current endpoint discovery
        discovery = self.test_endpoint_discovery()
        discovered_endpoints = [ep["full_endpoint"] for ep in discovery["endpoints"]]
        
        validation_results = {
            "category": endpoint_category,
            "expected_count": len(expected),
            "discovered_count": len(discovered_endpoints),
            "expected_endpoints": expected,
            "discovered_endpoints": discovered_endpoints,
            "missing_endpoints": [],
            "unexpected_endpoints": [],
            "matching_endpoints": []
        }
        
        # Find missing and unexpected endpoints
        for expected_ep in expected:
            if expected_ep in discovered_endpoints:
                validation_results["matching_endpoints"].append(expected_ep)
            else:
                validation_results["missing_endpoints"].append(expected_ep)
        
        # Save validation results
        validation_file = self.test_dir / "results" / f"endpoint_validation_{endpoint_category}_{int(time.time())}.json"
        with open(validation_file, 'w') as f:
            json.dump(validation_results, f, indent=2)
        
        return validation_results
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive test report
        """
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r.get("validation", {}).get("is_success", False)])
        failed_tests = total_tests - successful_tests
        
        # Calculate performance metrics
        response_times = []
        for result in self.test_results:
            if "response" in result and "response_time_ms" in result["response"]:
                response_times.append(result["response"]["response_time_ms"])
        
        performance = {
            "total_requests": len(response_times),
            "avg_response_time_ms": round(sum(response_times) / len(response_times), 2) if response_times else 0,
            "min_response_time_ms": min(response_times) if response_times else 0,
            "max_response_time_ms": max(response_times) if response_times else 0,
            "fast_responses": len([rt for rt in response_times if rt < self.config["performance"]["excellent_response_time_ms"]]),
            "slow_responses": len([rt for rt in response_times if rt > self.config["performance"]["acceptable_response_time_ms"]])
        }
        
        report = {
            "phase": self.phase_name,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": round((successful_tests / total_tests) * 100, 2) if total_tests > 0 else 0
            },
            "performance": performance,
            "test_results": self.test_results,
            "api_responses": self.api_responses
        }
        
        # Save comprehensive report
        report_file = self.test_dir / "results" / f"comprehensive_report_{self.phase_name}_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def cleanup(self):
        """
        Cleanup resources
        """
        if hasattr(self.client, 'close'):
            self.client.close()
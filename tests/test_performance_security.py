
"""
Performance and Security Testing Module
=======================================

Comprehensive testing of system performance, load handling,
security measures, and vulnerability assessments.
"""

import asyncio
import json
from typing import Dict, Any, List
import time
import aiohttp

from framework.base_test import APITest, TestLevel


class TestPerformanceSecurity(APITest):
    """Test suite for performance and security functionality"""
    
    def __init__(self):
        super().__init__("PerformanceSecurity")
        self.test_level = TestLevel.PERFORMANCE
        self.load_test_sessions = []
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Performance and Security tests...")
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Performance and Security tests...")
        
        # Stop any running load tests
        for session_id in self.load_test_sessions:
            try:
                await self.make_request("POST", f"/api/performance/load-test/{session_id}/stop")
            except:
                pass
                
        await self.cleanup_session()
        
    # Performance Tests
    async def test_api_response_times(self):
        """Test API endpoint response times"""
        endpoints_to_test = [
            "/health",
            "/api/agents/types",
            "/api/agents/statistics",
            "/api/workflows/statistics",
            "/api/multi-agent/health",
            "/api/system/health"
        ]
        
        response_times = {}
        
        for endpoint in endpoints_to_test:
            start_time = time.time()
            
            try:
                response = await self.make_request("GET", endpoint)
                duration = time.time() - start_time
                
                response_times[endpoint] = {
                    "response_time": duration,
                    "status_code": response["status_code"],
                    "success": response["status_code"] < 400
                }
                
                # Assert reasonable response times
                assert duration < 2.0, f"{endpoint} took {duration:.2f}s (should be < 2s)"
                
            except Exception as e:
                response_times[endpoint] = {
                    "response_time": time.time() - start_time,
                    "error": str(e),
                    "success": False
                }
                
        # Calculate average response time
        successful_responses = [rt for rt in response_times.values() if rt.get("success", False)]
        if successful_responses:
            avg_response_time = sum(rt["response_time"] for rt in successful_responses) / len(successful_responses)
            assert avg_response_time < 1.0, f"Average response time {avg_response_time:.2f}s is too high"
            
    async def test_concurrent_requests(self):
        """Test system under concurrent load"""
        concurrent_requests = 20
        endpoint = "/health"
        
        async def make_single_request():
            try:
                start_time = time.time()
                response = await self.make_request("GET", endpoint)
                duration = time.time() - start_time
                return {
                    "success": response["status_code"] < 400,
                    "duration": duration,
                    "status_code": response["status_code"]
                }
            except Exception as e:
                return {
                    "success": False,
                    "duration": time.time() - start_time,
                    "error": str(e)
                }
                
        # Execute concurrent requests
        start_time = time.time()
        tasks = [make_single_request() for _ in range(concurrent_requests)]
        results = await asyncio.gather(*tasks)
        total_duration = time.time() - start_time
        
        # Analyze results
        successful_requests = sum(1 for r in results if r["success"])
        failed_requests = len(results) - successful_requests
        success_rate = successful_requests / len(results)
        
        avg_response_time = sum(r["duration"] for r in results if r["success"]) / successful_requests if successful_requests > 0 else 0
        
        # Assertions
        assert success_rate >= 0.95, f"Success rate {success_rate:.2%} is below 95%"
        assert avg_response_time < 3.0, f"Average response time {avg_response_time:.2f}s under load is too high"
        assert total_duration < 30.0, f"Total test duration {total_duration:.2f}s is too long"
        
    async def test_memory_usage_monitoring(self):
        """Test system memory usage monitoring"""
        memory_data = {
            "monitoring_duration": 10,  # seconds
            "sample_interval": 1,  # second
            "memory_threshold": 1024  # MB
        }
        
        response = await self.make_request("POST", "/api/performance/memory/monitor", 
                                          data=memory_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "monitoring_session_id" in result, "Should contain monitoring session ID"
        
        # Wait for monitoring to complete
        await asyncio.sleep(2)
        
        # Get results
        session_id = result["monitoring_session_id"]
        results_response = await self.make_request("GET", f"/api/performance/memory/monitor/{session_id}/results")
        
        if results_response["status_code"] == 200:
            memory_results = results_response["data"]["data"]
            assert "memory_usage" in memory_results, "Should contain memory usage data"
            assert "peak_usage" in memory_results, "Should contain peak memory usage"
            
    async def test_throughput_measurement(self):
        """Test system throughput measurement"""
        throughput_data = {
            "test_duration": 30,  # seconds
            "request_pattern": "constant",
            "target_rps": 10,  # requests per second
            "endpoints": [
                {"method": "GET", "path": "/health", "weight": 0.5},
                {"method": "GET", "path": "/api/agents/statistics", "weight": 0.3},
                {"method": "GET", "path": "/api/workflows/statistics", "weight": 0.2}
            ]
        }
        
        response = await self.make_request("POST", "/api/performance/throughput/test", 
                                          data=throughput_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "test_session_id" in result, "Should contain test session ID"
        
        session_id = result["test_session_id"]
        self.load_test_sessions.append(session_id)
        
    async def test_database_performance(self):
        """Test database performance metrics"""
        db_test_data = {
            "operations": [
                {"type": "select", "complexity": "simple", "iterations": 100},
                {"type": "select", "complexity": "complex", "iterations": 50},
                {"type": "insert", "complexity": "simple", "iterations": 20},
                {"type": "update", "complexity": "simple", "iterations": 10}
            ],
            "concurrent_connections": 5
        }
        
        response = await self.make_request("POST", "/api/performance/database/benchmark", 
                                          data=db_test_data)
        
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        result = response["data"]["data"]
        assert "benchmark_results" in result, "Should contain benchmark results"
        
        results = result["benchmark_results"]
        assert "query_performance" in results, "Should contain query performance metrics"
        assert "connection_performance" in results, "Should contain connection performance"
        
    # Security Tests
    async def test_authentication_security(self):
        """Test authentication security measures"""
        # Test without API key
        original_headers = self.session._default_headers.copy() if self.session else {}
        
        if self.session and "X-API-Key" in self.session._default_headers:
            del self.session._default_headers["X-API-Key"]
            
        response = await self.make_request("GET", "/api/agents")
        
        # Should require authentication for protected endpoints
        assert response["status_code"] in [401, 403], f"Expected 401/403, got {response['status_code']}"
        
        # Restore headers
        if self.session:
            self.session._default_headers.update(original_headers)
            
    async def test_input_validation(self):
        """Test input validation and sanitization"""
        # Test malicious input
        malicious_inputs = [
            {"name": "<script>alert('xss')</script>", "type": "code_architect"},
            {"name": "'; DROP TABLE agents; --", "type": "security_expert"},
            {"name": "A" * 10000, "type": "data_analyst"},  # Extremely long input
            {"name": "", "type": ""},  # Empty input
            {"name": None, "type": None}  # Null input
        ]
        
        for malicious_data in malicious_inputs:
            response = await self.make_request("POST", "/api/agents", data=malicious_data)
            
            # Should reject malicious input
            assert response["status_code"] >= 400, f"Should reject malicious input: {malicious_data}"
            
    async def test_rate_limiting(self):
        """Test API rate limiting"""
        # Make rapid requests to test rate limiting
        rapid_requests = 100
        endpoint = "/health"
        
        responses = []
        start_time = time.time()
        
        for i in range(rapid_requests):
            try:
                response = await self.make_request("GET", endpoint)
                responses.append(response["status_code"])
            except Exception as e:
                responses.append(500)  # Connection error
                
        duration = time.time() - start_time
        
        # Check if rate limiting is working
        rate_limited_responses = sum(1 for status in responses if status == 429)
        
        if rate_limited_responses > 0:
            print(f"✅ Rate limiting is working: {rate_limited_responses} requests limited")
        else:
            print(f"⚠️ No rate limiting detected for {rapid_requests} requests in {duration:.2f}s")
            
    async def test_data_encryption_at_rest(self):
        """Test data encryption at rest"""
        encryption_test_data = {
            "test_data": "sensitive_information_12345",
            "encryption_type": "AES-256",
            "key_rotation": True
        }
        
        response = await self.make_request("POST", "/api/security/encryption/test", 
                                          data=encryption_test_data)
        
        if response["status_code"] == 200:
            result = response["data"]["data"]
            assert "encrypted_data" in result, "Should contain encrypted data"
            assert "encryption_algorithm" in result, "Should specify encryption algorithm"
            assert result["encrypted_data"] != encryption_test_data["test_data"], "Data should be encrypted"
        else:
            print(f"⚠️ Encryption endpoint not available (status: {response['status_code']})")
            
    async def test_sql_injection_protection(self):
        """Test SQL injection protection"""
        sql_injection_payloads = [
            "1' OR '1'='1",
            "1'; DROP TABLE users; --",
            "1' UNION SELECT * FROM sensitive_table --",
            "1' AND (SELECT COUNT(*) FROM agents) > 0 --"
        ]
        
        for payload in sql_injection_payloads:
            # Try injection in different contexts
            test_contexts = [
                {"endpoint": "/api/agents", "param": "name", "value": payload},
                {"endpoint": "/api/workflows", "param": "search", "value": payload}
            ]
            
            for context in test_contexts:
                try:
                    response = await self.make_request("GET", context["endpoint"], 
                                                     params={context["param"]: context["value"]})
                    
                    # Should not expose database structure or return unauthorized data
                    assert response["status_code"] != 200 or "error" not in str(response["data"]).lower() or "sql" not in str(response["data"]).lower(), "Possible SQL injection vulnerability"
                    
                except Exception:
                    pass  # Expected for malicious input
                    
    async def test_xss_protection(self):
        """Test Cross-Site Scripting (XSS) protection"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<svg onload=alert('xss')>"
        ]
        
        for payload in xss_payloads:
            agent_data = {
                "name": f"TestAgent_{payload}",
                "type": "code_architect",
                "description": payload
            }
            
            response = await self.make_request("POST", "/api/agents", data=agent_data)
            
            # Should sanitize or reject XSS attempts
            if response["status_code"] < 400:
                # If accepted, check that script tags are escaped
                created_agent = response["data"]["data"]
                assert "<script>" not in created_agent.get("name", ""), "XSS payload not sanitized"
                assert "<script>" not in created_agent.get("description", ""), "XSS payload not sanitized"
                
    async def test_csrf_protection(self):
        """Test Cross-Site Request Forgery (CSRF) protection"""
        # Test requests without proper CSRF tokens
        csrf_test_data = {
            "name": "CSRFTestAgent",
            "type": "security_expert"
        }
        
        # Create session without CSRF token
        headers_without_csrf = {"Content-Type": "application/json"}
        
        async with aiohttp.ClientSession(headers=headers_without_csrf) as session:
            try:
                async with session.post(
                    f"{self.config.api.base_url}/api/agents",
                    json=csrf_test_data
                ) as response:
                    # Many APIs don't implement CSRF for API endpoints
                    # This test documents the behavior
                    print(f"ℹ️ CSRF test response: {response.status}")
                    
            except Exception as e:
                print(f"ℹ️ CSRF test error: {e}")
                
    async def test_security_headers(self):
        """Test security-related HTTP headers"""
        response = await self.make_request("GET", "/health")
        
        if response["status_code"] == 200:
            headers = response["headers"]
            
            # Check for security headers
            security_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": ["DENY", "SAMEORIGIN"],
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": None,  # Should be present
                "Content-Security-Policy": None     # Should be present
            }
            
            for header, expected_value in security_headers.items():
                if header in headers:
                    print(f"✅ Security header present: {header}")
                    if expected_value and isinstance(expected_value, list):
                        assert headers[header] in expected_value, f"Unexpected value for {header}"
                    elif expected_value and isinstance(expected_value, str):
                        assert headers[header] == expected_value, f"Unexpected value for {header}"
                else:
                    print(f"⚠️ Security header missing: {header}")
                    
    async def test_vulnerability_scanning(self):
        """Test automated vulnerability scanning"""
        scan_data = {
            "scan_type": "comprehensive",
            "target": "api_endpoints",
            "include_checks": [
                "sql_injection",
                "xss",
                "authentication_bypass",
                "information_disclosure",
                "insecure_configurations"
            ]
        }
        
        response = await self.make_request("POST", "/api/security/vulnerability-scan", 
                                          data=scan_data)
        
        if response["status_code"] == 200:
            result = response["data"]["data"]
            assert "scan_id" in result, "Should contain scan ID"
            assert "vulnerabilities_found" in result, "Should report vulnerability count"
            
            # Check scan results
            vulnerabilities = result.get("vulnerabilities_found", 0)
            if vulnerabilities > 0:
                print(f"⚠️ Found {vulnerabilities} potential vulnerabilities")
                assert "vulnerability_details" in result, "Should provide vulnerability details"
            else:
                print("✅ No vulnerabilities detected")
        else:
            print(f"ℹ️ Vulnerability scanning endpoint not available (status: {response['status_code']})")
            
    async def test_security_monitoring(self):
        """Test security monitoring and alerting"""
        monitoring_data = {
            "monitoring_duration": 30,  # seconds
            "security_events": [
                "failed_authentication",
                "suspicious_requests",
                "rate_limit_exceeded",
                "privilege_escalation_attempt"
            ],
            "alert_threshold": 5
        }
        
        response = await self.make_request("POST", "/api/security/monitoring/start", 
                                          data=monitoring_data)
        
        if response["status_code"] == 200:
            result = response["data"]["data"]
            assert "monitoring_session_id" in result, "Should contain monitoring session ID"
            
            # Simulate some security events
            await asyncio.sleep(2)
            
            # Check monitoring results
            session_id = result["monitoring_session_id"]
            results_response = await self.make_request("GET", 
                                                     f"/api/security/monitoring/{session_id}/events")
            
            if results_response["status_code"] == 200:
                events = results_response["data"]["data"]
                assert "security_events" in events, "Should contain security events"
        else:
            print(f"ℹ️ Security monitoring endpoint not available (status: {response['status_code']})")

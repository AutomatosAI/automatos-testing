"""
Simple Locust Performance Test for Available Endpoints
=====================================================

Testing only the endpoints that are actually implemented:
- GET /health
- GET /api/system/metrics
"""

import json
import time
from datetime import datetime

from locust import HttpUser, task, between, events

class AutomotasAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts"""
        self.test_results = []
        
    @task(3)
    def test_health_endpoint(self):
        """Test the health endpoint (higher frequency)"""
        start_time = time.time()
        with self.client.get("/health", catch_response=True) as response:
            duration = time.time() - start_time
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "endpoint": "/health",
                "method": "GET",
                "status_code": response.status_code,
                "duration": duration,
                "success": response.status_code == 200
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "status" in data and data["status"] == "healthy":
                        response.success()
                        result["response"] = data
                    else:
                        response.failure("Invalid health response")
                        result["error"] = "Invalid health response"
                except:
                    response.failure("Invalid JSON response")
                    result["error"] = "Invalid JSON response"
            else:
                response.failure(f"Status code: {response.status_code}")
                result["error"] = f"HTTP {response.status_code}"
            
            self.test_results.append(result)
    
    @task(1)  
    def test_system_metrics(self):
        """Test the system metrics endpoint (lower frequency)"""
        start_time = time.time()
        with self.client.get("/api/system/metrics", catch_response=True) as response:
            duration = time.time() - start_time
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "endpoint": "/api/system/metrics", 
                "method": "GET",
                "status_code": response.status_code,
                "duration": duration,
                "success": response.status_code == 200
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    expected_keys = ["cpu", "memory", "disk", "network"]
                    if all(key in data for key in expected_keys):
                        response.success()
                        result["response"] = data
                    else:
                        response.failure("Missing expected metrics")
                        result["error"] = "Missing expected metrics"
                except:
                    response.failure("Invalid JSON response")
                    result["error"] = "Invalid JSON response"
            else:
                response.failure(f"Status code: {response.status_code}")
                result["error"] = f"HTTP {response.status_code}"
            
            self.test_results.append(result)

# Event handlers for logging
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Save results when test stops"""
    print("📊 Locust test completed. Saving results...")
    
    # Aggregate results from all users
    all_results = []
    for user in environment.runner.user_classes:
        # This is a simplified approach - in practice you'd need better result aggregation
        pass
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "locust_performance",
        "endpoints_tested": ["/health", "/api/system/metrics"],
        "total_requests": environment.stats.total.num_requests,
        "total_failures": environment.stats.total.num_failures,
        "average_response_time": environment.stats.total.avg_response_time,
        "min_response_time": environment.stats.total.min_response_time,
        "max_response_time": environment.stats.total.max_response_time,
        "requests_per_second": environment.stats.total.current_rps,
        "failure_rate": environment.stats.total.fail_ratio
    }
    
    with open("logs/locust_performance_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("✅ Locust results saved to logs/locust_performance_results.json")
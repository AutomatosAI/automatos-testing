import httpx
import time
import json
from typing import Dict, Any, Optional, Union

class AutomotasAPIClient:
    """Enhanced API client for Automotas AI with automatic logging and error handling"""
    
    def __init__(self, base_url: str = "http://localhost:8000", logger = None):
        self.base_url = base_url.rstrip('/')
        self.logger = logger
        
        # Default headers
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": "test_api_key_for_backend_validation_2025",
            "Authorization": "Bearer test_api_key_for_backend_validation_2025"
        }
        
        # HTTP client
        self.client = httpx.Client(timeout=30.0)
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request with timing and logging"""
        
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            # Prepare request data
            request_kwargs = {
                "headers": self.headers,
                "params": params
            }
            
            if data and method.upper() in ['POST', 'PUT', 'PATCH']:
                request_kwargs["json"] = data
            
            # Make request
            response = self.client.request(method.upper(), url, **request_kwargs)
            
            # Calculate response time
            response_time_ms = (time.time() - start_time) * 1000
            
            # Parse response
            try:
                response_data = response.json() if response.content else {}
            except json.JSONDecodeError:
                response_data = {"raw_response": response.text}
            
            # Log API call
            if self.logger:
                self.logger.log_api_call(
                    method=method.upper(),
                    endpoint=endpoint,
                    status_code=response.status_code,
                    response_time_ms=response_time_ms,
                    response_data=response_data,
                    request_data=data
                )
            
            # Return structured result
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "data": response_data,
                "response_time_ms": response_time_ms,
                "raw_response": response
            }
            
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            
            if self.logger:
                self.logger.log_error(f"API request failed: {method} {endpoint}", e)
            
            return {
                "success": False,
                "status_code": 0,
                "data": {"error": str(e)},
                "response_time_ms": response_time_ms,
                "exception": e
            }
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request"""
        return self._make_request("POST", endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self._make_request("PUT", endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._make_request("DELETE", endpoint)
    
    def health_check(self) -> Dict[str, Any]:
        """Quick health check"""
        return self.get("/health")
    
    def validate_response(self, response: Dict[str, Any], expected_status: int = 200) -> bool:
        """Validate API response"""
        success = response["status_code"] == expected_status
        
        if self.logger:
            self.logger.log_validation(
                validation_name=f"HTTP Status Code",
                expected=expected_status,
                actual=response["status_code"],
                passed=success
            )
        
        return success
    
    def validate_data_contains(self, response: Dict[str, Any], key: str, expected_value: Any = None) -> bool:
        """Validate that response data contains a specific key/value"""
        data = response.get("data", {})
        has_key = key in data
        
        if expected_value is not None:
            has_correct_value = data.get(key) == expected_value
            success = has_key and has_correct_value
        else:
            success = has_key
        
        return success
    
    def extract_id(self, response: Dict[str, Any], id_field: str = "id") -> Optional[Union[str, int]]:
        """Extract ID from response data"""
        data = response.get("data", {})
        
        # Try common ID field names
        for field in [id_field, "id", "agent_id", "workflow_id", "skill_id", "config_id", "_id"]:
            if field in data:
                return data[field]
        
        return None

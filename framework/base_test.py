
"""
Base Test Classes for Automotas AI Testing Framework
====================================================

Provides base classes and utilities for all test types.
"""

import asyncio
import pytest
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone
import json
import aiohttp
from dataclasses import dataclass

from .config import test_config, TestLevel

@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    status: str  # passed, failed, skipped
    duration: float
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()

class BaseTest:
    """Base class for all Automotas AI tests"""
    
    def __init__(self, test_name: str, test_level: TestLevel):
        self.test_name = test_name
        self.test_level = test_level
        self.logger = logging.getLogger(f"test.{test_name}")
        self.config = test_config
        self.results: List[TestResult] = []
        
    def log_result(self, test_name: str, status: str, duration: float, 
                   error: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """Log test result"""
        result = TestResult(
            test_name=test_name,
            status=status,
            duration=duration,
            error=error,
            details=details
        )
        self.results.append(result)
        
        status_emoji = "✅" if status == "passed" else "❌" if status == "failed" else "⏭️"
        self.logger.info(f"{status_emoji} {test_name} - {status} ({duration:.2f}s)")
        
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of test results"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        skipped = sum(1 for r in self.results if r.status == "skipped")
        
        return {
            "test_suite": self.test_name,
            "test_level": self.test_level.value,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "results": [
                {
                    "name": r.test_name,
                    "status": r.status,
                    "duration": r.duration,
                    "error": r.error,
                    "timestamp": r.timestamp
                } for r in self.results
            ]
        }

class APITest(BaseTest):
    """Base class for API testing"""
    
    def __init__(self, test_name: str):
        super().__init__(test_name, TestLevel.INTEGRATION)
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def setup_session(self):
        """Setup HTTP session"""
        headers = self.config.api.headers.copy() if self.config.api.headers else {}
        if self.config.api.api_key:
            headers["X-API-Key"] = self.config.api.api_key
            
        timeout = aiohttp.ClientTimeout(total=self.config.api.timeout)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout
        )
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    async def make_request(self, method: str, endpoint: str, 
                          data: Optional[Dict] = None, 
                          params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        if not self.session:
            await self.setup_session()
            
        url = f"{self.config.api.base_url}{endpoint}"
        
        for attempt in range(self.config.api.retry_count):
            try:
                async with self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params
                ) as response:
                    response_data = {
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "data": await response.json() if response.content_type == 'application/json' else await response.text()
                    }
                    return response_data
                    
            except Exception as e:
                if attempt == self.config.api.retry_count - 1:
                    raise e
                await asyncio.sleep(1)
                
        raise Exception("Max retries exceeded")

class DatabaseTest(BaseTest):
    """Base class for database testing"""
    
    def __init__(self, test_name: str):
        super().__init__(test_name, TestLevel.INTEGRATION)
        self.db_session = None
        
    async def setup_database(self):
        """Setup test database"""
        # Database setup logic would go here
        pass
        
    async def cleanup_database(self):
        """Cleanup test database"""
        if self.config.database.cleanup_after_test:
            # Database cleanup logic would go here
            pass

class WorkflowTest(BaseTest):
    """Base class for workflow testing"""
    
    def __init__(self, test_name: str):
        super().__init__(test_name, TestLevel.E2E)
        self.workflow_session: Optional[aiohttp.ClientSession] = None
        
    async def setup_workflow_session(self):
        """Setup N8N workflow session"""
        self.workflow_session = aiohttp.ClientSession()
        
    async def cleanup_workflow_session(self):
        """Cleanup workflow session"""
        if self.workflow_session:
            await self.workflow_session.close()
            
    async def trigger_webhook(self, webhook_path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger N8N webhook"""
        if not self.workflow_session:
            await self.setup_workflow_session()
            
        url = f"{self.config.n8n.webhook_base_url}/{webhook_path}"
        
        async with self.workflow_session.post(url, json=data) as response:
            return {
                "status_code": response.status,
                "data": await response.json() if response.content_type == 'application/json' else await response.text()
            }

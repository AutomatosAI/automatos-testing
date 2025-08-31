
from dotenv import load_dotenv
load_dotenv()

"""
Automotas AI Testing Framework Configuration
===========================================

Central configuration management for the testing framework.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, List
from enum import Enum

class TestEnvironment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class TestLevel(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"

@dataclass
class APITestConfig:
    """Configuration for API testing"""
    base_url: str
    timeout: int = 30
    retry_count: int = 3
    api_key: str = None
    headers: Dict[str, str] = None

@dataclass
class DatabaseTestConfig:
    """Configuration for database testing"""
    test_db_url: str
    cleanup_after_test: bool = True
    seed_data: bool = True

@dataclass
class N8NTestConfig:
    """Configuration for N8N workflow testing"""
    n8n_base_url: str = "http://localhost:5678"
    webhook_base_url: str = "http://localhost:3001"
    workflow_timeout: int = 300

@dataclass
class TestConfiguration:
    """Main test configuration"""
    environment: TestEnvironment
    api: APITestConfig
    database: DatabaseTestConfig
    n8n: N8NTestConfig
    parallel_tests: bool = True
    generate_reports: bool = True
    report_format: str = "html"
    test_data_path: str = "test_data"
    
    @classmethod
    def from_env(cls) -> 'TestConfiguration':
        """Load configuration from environment variables"""
        env = TestEnvironment(os.getenv("TEST_ENVIRONMENT", "development"))
        
        api_config = APITestConfig(
            base_url=os.getenv("API_BASE_URL", "http://localhost:8000"),
            timeout=int(os.getenv("API_TIMEOUT", "30")),
            retry_count=int(os.getenv("API_RETRY_COUNT", "3")),
            api_key=os.getenv("API_KEY"),
            headers={"Content-Type": "application/json"}
        )
        
        db_config = DatabaseTestConfig(
            test_db_url=os.getenv("TEST_DB_URL", "postgresql://postgres:test@localhost:5432/test_db"),
            cleanup_after_test=os.getenv("CLEANUP_DB", "true").lower() == "true",
            seed_data=os.getenv("SEED_TEST_DATA", "true").lower() == "true"
        )
        
        n8n_config = N8NTestConfig(
            n8n_base_url=os.getenv("N8N_BASE_URL", "http://localhost:5678"),
            webhook_base_url=os.getenv("WEBHOOK_BASE_URL", "http://localhost:3001"),
            workflow_timeout=int(os.getenv("WORKFLOW_TIMEOUT", "300"))
        )
        
        return cls(
            environment=env,
            api=api_config,
            database=db_config,
            n8n=n8n_config,
            parallel_tests=os.getenv("PARALLEL_TESTS", "true").lower() == "true",
            generate_reports=os.getenv("GENERATE_REPORTS", "true").lower() == "true",
            report_format=os.getenv("REPORT_FORMAT", "html"),
            test_data_path=os.getenv("TEST_DATA_PATH", "test_data")
        )

# Global configuration instance
test_config = TestConfiguration.from_env()

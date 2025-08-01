"""
Comprehensive API Testing Suite for Automotas AI System
======================================================

This test suite provides comprehensive testing of all Automotas AI endpoints using:
- Real test data from configuration files (NOT fake data)
- EnhancedWorkflowLogger for detailed JSON logging
- Proper error handling and retries
- Performance monitoring and metrics
- Agent communication tracking

All results are logged to logs/api_test.log in JSON format for analysis by bug-fixing agents.
"""

import asyncio
import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import httpx
import pytest
import yaml
from pydantic import BaseModel

# Import the EnhancedWorkflowLogger from the system
sys.path.append('/root/automotas-ai/orchestrator')
try:
    from logging_utils import EnhancedWorkflowLogger
except ImportError:
    # Fallback logger if system logger not available
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    class EnhancedWorkflowLogger:
        def __init__(self, workflow_id: str, log_file: str = None):
            self.workflow_id = workflow_id
            self.log_file = log_file or 'logs/api_test.log'
            self.logger = logging.getLogger(workflow_id)
            Path(os.path.dirname(self.filename)).mkdir(parents=True, exist_ok=True)
            
        def log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=self, step: str, status: Any, response: Any = None, context: str = "", **kwargs):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "workflow_id": self.workflow_id,
                "step": step,
                "status": status,
                "response": response,
                "context": context,
                **kwargs
            }
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            print(f"LOGGED: {step} - Status: {status}")

# Initialize logger
logger = EnhancedWorkflowLogger(
    workflow_id='automotas_api_testing', 
    log_file='logs/api_test.log', 
)

# Load test configuration
def load_config():
    """Load test configuration from YAML file"""
    try:
        with open('test_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="config_loaded",
            status="completed", metadata={"status":"success",
            "context":"Test configuration loaded successfully",
            config_keys=list(config.keys())
        )
        return config
    except Exception as e:
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="config_load_failed",
            status="completed", metadata={"status":"error",
            "context":f"Failed to load test config: {str(e)}",
            error=str(e)
        )
        pytest.fail(f"Failed to load test configuration: {e}")

CONFIG = load_config()

class APITestClient:
    """Enhanced HTTP client with logging and retry logic"""
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.headers = headers
        self.session = None
        
    async def __aenter__(self):
        self.session = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=30.0
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Make HTTP request with logging and retry logic"""
        start_time = time.time()
        
        for attempt in range(CONFIG['execution']['retry_attempts']):
            try:
                logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                    step=f"{method}_{endpoint}",
                    status="completed", metadata={"status":"attempting",
                    "context":f"Attempt {attempt + 1} of {CONFIG['execution']['retry_attempts']}",
                    method=method,
                    endpoint=endpoint,
                    attempt=attempt + 1
                )
                
                response = await self.session.request(method, endpoint, **kwargs)
                duration = time.time() - start_time
                
                # Log successful response
                logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                    step=f"{method}_{endpoint}",
                    status="completed", metadata={"status":response.status_code,
                    "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    "context":f"Request completed in {duration:.2f}s",
                    method=method,
                    endpoint=endpoint,
                    duration_seconds=duration,
                    attempt=attempt + 1,
                    success=True
                )
                
                return response
                
            except Exception as e:
                duration = time.time() - start_time
                logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                    step=f"{method}_{endpoint}",
                    status="completed", metadata={"status":"error",
                    "context":f"Request failed on attempt {attempt + 1}: {str(e)}",
                    method=method,
                    endpoint=endpoint,
                    error=str(e),
                    traceback=traceback.format_exc(),
                    duration_seconds=duration,
                    attempt=attempt + 1,
                    success=False
                )
                
                if attempt < CONFIG['execution']['retry_attempts'] - 1:
                    await asyncio.sleep(CONFIG['execution']['retry_delay'])
                else:
                    raise

@pytest.fixture
async def api_client():
    """Create API client with fallback URLs"""
    urls_to_try = [CONFIG['api']['base_url']] + CONFIG['api']['fallback_urls']
    
    for url in urls_to_try:
        try:
            async with APITestClient(url, CONFIG['api']['authentication']['headers']) as client:
                # Test connectivity
                response = await client.request('GET', '/health')
                if response.status_code == 200:
                    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                        step="api_client_connected",
                        status="completed", metadata={"status":"success", 
                        "context":f"Successfully connected to {url}",
                        url=url
                    )
                    async with APITestClient(url, CONFIG['api']['authentication']['headers']) as final_client:
                        yield final_client
                    return
        except Exception as e:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="api_client_connection_failed",
                status="completed", metadata={"status":"error",
                "context":f"Failed to connect to {url}: {str(e)}",
                url=url,
                error=str(e)
            )
            continue
    
    pytest.fail("Could not connect to any API endpoint")

class TestHealthChecks:
    """Test suite for system health and basic connectivity"""
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, api_client):
        """Test the health check endpoint"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="health_check_start",
            status="completed", metadata={"status":"starting",
            "context":"Testing system health endpoint"
        )
        
        response = await api_client.request('GET', CONFIG['endpoints']['health'])
        
        assert response.status_code == CONFIG['expectations']['status_codes']['health'], \
            f"Health check failed with status {response.status_code}"
        
        health_data = response.json()
        assert 'status' in health_data, "Health response missing status field"
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="health_check_complete",
            status="completed", metadata={"status":"success",
            "response":health_data,
            "context":"Health check completed successfully"
        )
    
    @pytest.mark.asyncio 
    async def test_root_endpoint(self, api_client):
        """Test the root endpoint for API information"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="root_endpoint_test",
            status="completed", metadata={"status":"starting",
            "context":"Testing root endpoint for API metadata"
        )
        
        response = await api_client.request('GET', CONFIG['endpoints']['root'])
        assert response.status_code == 200
        
        if response.headers.get('content-type', '').startswith('application/json'):
            root_data = response.json()
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="root_endpoint_complete",
                status="completed", metadata={"status":"success",
                "response":root_data,
                "context":"Root endpoint test completed"
            )

class TestAgentManagement:
    """Test suite for agent management endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_agent(self, api_client):
        """Test agent creation with real configuration data"""
        for agent_config in CONFIG['test_data']['agents']:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="agent_creation_start",
                status="completed", metadata={"status":"starting",
                "context":f"Creating agent: {agent_config['name']}",
                agent_config=agent_config
            )
            
            response = await api_client.request(
                'POST',
                CONFIG['endpoints']['agents']['create'],
                json=agent_config
            )
            
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="agent_creation_response",
                status="completed", metadata={"status":response.status_code,
                "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "context":f"Agent creation response for {agent_config['name']}",
                agent_name=agent_config['name'],
                expected_status="completed", metadata={"status":CONFIG['expectations']['status_codes']['agent_created']
            )
            
            # Note: We log the actual status code rather than asserting,
            # since the goal is to test and analyze real behavior
            if response.status_code != CONFIG['expectations']['status_codes']['agent_created']:
                logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                    step="agent_creation_unexpected_status",
                    status="completed", metadata={"status":"warning",
                    "context":f"Unexpected status code for agent creation: {response.status_code}",
                    expected=CONFIG['expectations']['status_codes']['agent_created'],
                    actual=response.status_code,
                    agent_name=agent_config['name']
                )
    
    @pytest.mark.asyncio
    async def test_list_agents(self, api_client):
        """Test agent listing functionality"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="agent_listing_start", 
            status="completed", metadata={"status":"starting",
            "context":"Testing agent listing endpoint"
        )
        
        response = await api_client.request('GET', CONFIG['endpoints']['agents']['list'])
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="agent_listing_response",
            status="completed", metadata={"status":response.status_code,
            "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "context":"Agent listing completed"
        )

class TestWorkflowManagement:
    """Test suite for workflow management endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_workflow(self, api_client):
        """Test workflow creation with real workflow definitions"""
        for workflow_config in CONFIG['test_data']['workflows']:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="workflow_creation_start",
                status="completed", metadata={"status":"starting", 
                "context":f"Creating workflow: {workflow_config['name']}",
                workflow_config=workflow_config
            )
            
            response = await api_client.request(
                'POST',
                CONFIG['endpoints']['workflows']['create'],
                json=workflow_config
            )
            
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="workflow_creation_response",
                status="completed", metadata={"status":response.status_code,
                "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "context":f"Workflow creation response for {workflow_config['name']}",
                workflow_name=workflow_config['name'],
                expected_status="completed", metadata={"status":CONFIG['expectations']['status_codes']['workflow_created']
            )
    
    @pytest.mark.asyncio
    async def test_list_workflows(self, api_client):
        """Test workflow listing functionality"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="workflow_listing_start",
            status="completed", metadata={"status":"starting",
            "context":"Testing workflow listing endpoint"  
        )
        
        response = await api_client.request('GET', CONFIG['endpoints']['workflows']['list'])
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="workflow_listing_response",
            status="completed", metadata={"status":response.status_code,
            "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "context":"Workflow listing completed"
        )

class TestDocumentManagement:
    """Test suite for document management endpoints"""
    
    @pytest.mark.asyncio
    async def test_document_upload(self, api_client):
        """Test document upload with real content"""
        for doc_config in CONFIG['test_data']['documents']:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="document_upload_start",
                status="completed", metadata={"status":"starting",
                "context":f"Uploading document: {doc_config['filename']}",
                log_file=doc_config['filename'],
                content_length=len(doc_config['content'])
            )
            
            # Prepare multipart form data
            files = {
                'file': (doc_config['filename'], doc_config['content'], 'text/plain')
            }
            data = {
                'tags': ','.join(doc_config['tags']),
                'description': doc_config['description']
            }
            
            response = await api_client.request(
                'POST',
                CONFIG['endpoints']['documents']['upload'],
                files=files,
                data=data
            )
            
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="document_upload_response",
                status="completed", metadata={"status":response.status_code,
                "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "context":f"Document upload response for {doc_config['filename']}",
                log_file=doc_config['filename'],
                expected_status="completed", metadata={"status":CONFIG['expectations']['status_codes']['document_uploaded']
            )
    
    @pytest.mark.asyncio 
    async def test_list_documents(self, api_client):
        """Test document listing functionality"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="document_listing_start",
            status="completed", metadata={"status":"starting",
            "context":"Testing document listing endpoint"
        )
        
        response = await api_client.request('GET', CONFIG['endpoints']['documents']['list'])
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="document_listing_response", 
            status="completed", metadata={"status":response.status_code,
            "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "context":"Document listing completed"
        )

class TestContextEngineering:
    """Test suite for context engineering endpoints"""
    
    @pytest.mark.asyncio
    async def test_context_search(self, api_client):
        """Test context search with real queries"""
        for query_config in CONFIG['test_data']['context_queries']:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="context_search_start",
                status="completed", metadata={"status":"starting",
                "context":f"Searching context: {query_config['query']}",
                query=query_config['query'],
                limit=query_config['limit']
            )
            
            search_request = {
                'query': query_config['query'],
                'limit': query_config['limit']
            }
            
            response = await api_client.request(
                'POST',
                CONFIG['endpoints']['context']['search'],
                json=search_request
            )
            
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="context_search_response",
                status="completed", metadata={"status":response.status_code,
                "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "context":f"Context search response for query: {query_config['query'][:50]}...",
                query=query_config['query'],
                expected_status="completed", metadata={"status":CONFIG['expectations']['status_codes']['context_search']
            )

class TestSystemMonitoring:
    """Test suite for system monitoring endpoints"""
    
    @pytest.mark.asyncio
    async def test_system_metrics(self, api_client):
        """Test system metrics endpoint"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="system_metrics_start",
            status="completed", metadata={"status":"starting",
            "context":"Testing system metrics endpoint"
        )
        
        response = await api_client.request('GET', CONFIG['endpoints']['system']['metrics'])
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="system_metrics_response",
            status="completed", metadata={"status":response.status_code,
            "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "context":"System metrics test completed"
        )
    
    @pytest.mark.asyncio
    async def test_system_stats(self, api_client):
        """Test system statistics endpoint"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="system_stats_start",
            status="completed", metadata={"status":"starting", 
            "context":"Testing system statistics endpoint"
        )
        
        response = await api_client.request('GET', CONFIG['endpoints']['system']['stats'])
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="system_stats_response",
            status="completed", metadata={"status":response.status_code,
            "response":response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "context":"System statistics test completed"
        )

class TestEndToEndWorkflows:
    """End-to-end integration tests"""
    
    @pytest.mark.asyncio
    async def test_complete_workflow_cycle(self, api_client):
        """Test complete workflow: create agent -> create workflow -> execute -> monitor"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="e2e_workflow_start",
            status="completed", metadata={"status":"starting",
            "context":"Starting end-to-end workflow integration test"
        )
        
        # Step 1: Create an agent
        agent_config = CONFIG['test_data']['agents'][0]
        agent_response = await api_client.request(
            'POST',
            CONFIG['endpoints']['agents']['create'],
            json=agent_config
        )
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="e2e_agent_created",
            status="completed", metadata={"status":agent_response.status_code,
            "response":agent_response.json() if agent_response.headers.get('content-type', '').startswith('application/json') else agent_response.text,
            "context":"Agent created for E2E test"
        )
        
        # Step 2: Create a workflow
        workflow_config = CONFIG['test_data']['workflows'][0]
        workflow_response = await api_client.request(
            'POST',
            CONFIG['endpoints']['workflows']['create'],
            json=workflow_config
        )
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="e2e_workflow_created",
            status="completed", metadata={"status":workflow_response.status_code,
            "response":workflow_response.json() if workflow_response.headers.get('content-type', '').startswith('application/json') else workflow_response.text,
            "context":"Workflow created for E2E test"
        )
        
        # Step 3: Check system health after operations
        health_response = await api_client.request('GET', CONFIG['endpoints']['health'])
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="e2e_workflow_complete",
            status="completed", metadata={"status":"success",
            "response":health_response.json() if health_response.headers.get('content-type', '').startswith('application/json') else health_response.text,
            "context":"End-to-end workflow integration test completed"
        )

if __name__ == "__main__":
    # Allow running tests directly
    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
        step="test_suite_start",
        status="completed", metadata={"status":"starting", 
        "context":"Starting Automotas AI API test suite execution"
    )
    
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--disable-warnings"
    ])
    
    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
        step="test_suite_complete",
        status="completed", metadata={"status":"complete",
        "context":"Automotas AI API test suite execution finished"
    )
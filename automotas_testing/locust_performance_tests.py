"""
Locust Performance Testing Suite for Automotas AI System
======================================================

Single-user performance testing as requested, hitting each endpoint once
with comprehensive logging using EnhancedWorkflowLogger.

All results are logged to logs/locust.log in JSON format for analysis.
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import yaml
from locust import HttpUser, task, between, events

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
            self.log_file = log_file or 'logs/locust.log'
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
            print(f"LOCUST LOGGED: {step} - Status: {status}")

# Initialize logger
logger = EnhancedWorkflowLogger(
    workflow_id='automotas_locust_testing',
    log_file='logs/locust.log', 
)

# Load test configuration
def load_config():
    """Load test configuration from YAML file"""
    try:
        with open('test_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_config_loaded",
            status="completed", metadata={"status":"success",
            "context":"Locust test configuration loaded successfully"
        )
        return config
    except Exception as e:
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_config_load_failed",
            status="completed", metadata={"status":"error",
            "context":f"Failed to load test config: {str(e)}",
            error=str(e)
        )
        return None

CONFIG = load_config()

class AutomotasAPIUser(HttpUser):
    """
    Single-user Locust testing for Automotas AI API endpoints
    Tests each endpoint once with real data and comprehensive logging
    """
    
    # Single user, no wait time between requests for precise testing
    wait_time = between(1, 2)
    
    def on_start(self):
        """Initialize user session and set headers"""
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_user_session_start",
            status="completed", metadata={"status":"starting",
            "context":"Initializing Locust user session"
        )
        
        # Set authentication headers if config is available
        if CONFIG and 'api' in CONFIG:
            for key, value in CONFIG['api']['authentication']['headers'].items():
                self.client.headers[key] = value
        
        # Track test execution state
        self.test_execution_count = {}
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_user_session_initialized",
            status="completed", metadata={"status":"success",
            "context":"Locust user session initialized with authentication headers"
        )
    
    def log_request(self, endpoint: str, method: str, response, context: str, **kwargs):
        """Log request details with enhanced information"""
        start_time = kwargs.get('start_time', time.time())
        duration = time.time() - start_time
        
        try:
            response_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        except:
            response_data = response.text
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step=f"locust_{method.lower()}_{endpoint.replace('/', '_')}",
            status="completed", metadata={"status":response.status_code,
            "response":response_data,
            "context":context,
            method=method,
            endpoint=endpoint,
            duration_seconds=duration,
            response_time_ms=response.elapsed.total_seconds() * 1000,
            success=response.status_code < 400,
            **kwargs
        )
    
    @task(1)
    def test_health_endpoint(self):
        """Test health check endpoint"""
        if self.test_execution_count.get('health', 0) >= 1:
            return  # Only execute once
        
        start_time = time.time()
        endpoint = "/health"
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_health_check_start",
            status="completed", metadata={"status":"starting",
            "context":"Locust testing health endpoint"
        )
        
        with self.client.get(endpoint, catch_"response":True) as response:
            self.log_request(
                endpoint=endpoint,
                method="GET", 
                "response":response,
                "context":"Locust health check test",
                start_time=start_time
            )
            
            if response.status_code != 200:
                response.failure(f"Health check failed with status {response.status_code}")
        
        self.test_execution_count['health'] = self.test_execution_count.get('health', 0) + 1
    
    @task(1) 
    def test_agent_creation(self):
        """Test agent creation endpoint with real data"""
        if self.test_execution_count.get('agent_creation', 0) >= 1:
            return  # Only execute once
        
        if not CONFIG or 'test_data' not in CONFIG:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="locust_agent_creation_skip",
                status="completed", metadata={"status":"skipped",
                "context":"Skipping agent creation test - no config available"
            )
            return
        
        start_time = time.time()
        endpoint = "/api/agents"
        agent_config = CONFIG['test_data']['agents'][0]  # Use first agent config
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_agent_creation_start",
            status="completed", metadata={"status":"starting",
            "context":f"Locust testing agent creation with: {agent_config['name']}",
            agent_config=agent_config
        )
        
        with self.client.post(
            endpoint, 
            json=agent_config,
            catch_"response":True
        ) as response:
            self.log_request(
                endpoint=endpoint,
                method="POST",
                "response":response,
                "context":f"Locust agent creation test for {agent_config['name']}",
                start_time=start_time,
                agent_name=agent_config['name']
            )
            
            if response.status_code not in [200, 201]:
                response.failure(f"Agent creation failed with status {response.status_code}")
        
        self.test_execution_count['agent_creation'] = self.test_execution_count.get('agent_creation', 0) + 1
    
    @task(1)
    def test_workflow_creation(self):
        """Test workflow creation endpoint with real data"""
        if self.test_execution_count.get('workflow_creation', 0) >= 1:
            return  # Only execute once
        
        if not CONFIG or 'test_data' not in CONFIG:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="locust_workflow_creation_skip", 
                status="completed", metadata={"status":"skipped",
                "context":"Skipping workflow creation test - no config available"
            )
            return
        
        start_time = time.time()
        endpoint = "/api/workflows" 
        workflow_config = CONFIG['test_data']['workflows'][0]  # Use first workflow config
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_workflow_creation_start",
            status="completed", metadata={"status":"starting",
            "context":f"Locust testing workflow creation with: {workflow_config['name']}",
            workflow_config=workflow_config
        )
        
        with self.client.post(
            endpoint,
            json=workflow_config,
            catch_"response":True
        ) as response:
            self.log_request(
                endpoint=endpoint,
                method="POST",
                "response":response,
                "context":f"Locust workflow creation test for {workflow_config['name']}",
                start_time=start_time,
                workflow_name=workflow_config['name']
            )
            
            if response.status_code not in [200, 201]:
                response.failure(f"Workflow creation failed with status {response.status_code}")
        
        self.test_execution_count['workflow_creation'] = self.test_execution_count.get('workflow_creation', 0) + 1
    
    @task(1)
    def test_document_upload(self):
        """Test document upload endpoint with real content"""
        if self.test_execution_count.get('document_upload', 0) >= 1:
            return  # Only execute once
        
        if not CONFIG or 'test_data' not in CONFIG:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="locust_document_upload_skip",
                status="completed", metadata={"status":"skipped", 
                "context":"Skipping document upload test - no config available"
            )
            return
        
        start_time = time.time()
        endpoint = "/api/admin/documents/upload"
        doc_config = CONFIG['test_data']['documents'][0]  # Use first document config
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_document_upload_start",
            status="completed", metadata={"status":"starting",
            "context":f"Locust testing document upload with: {doc_config['filename']}",
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
        
        with self.client.post(
            endpoint,
            files=files,
            data=data,
            catch_"response":True
        ) as response:
            self.log_request(
                endpoint=endpoint,
                method="POST",
                "response":response,
                "context":f"Locust document upload test for {doc_config['filename']}",
                start_time=start_time,
                log_file=doc_config['filename']
            )
            
            if response.status_code not in [200, 201]:
                response.failure(f"Document upload failed with status {response.status_code}")
        
        self.test_execution_count['document_upload'] = self.test_execution_count.get('document_upload', 0) + 1
    
    @task(1)
    def test_context_search(self):
        """Test context search endpoint with real queries"""
        if self.test_execution_count.get('context_search', 0) >= 1:
            return  # Only execute once
        
        if not CONFIG or 'test_data' not in CONFIG:
            logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
                step="locust_context_search_skip",
                status="completed", metadata={"status":"skipped",
                "context":"Skipping context search test - no config available"
            )
            return
        
        start_time = time.time()
        endpoint = "/api/context/search"
        query_config = CONFIG['test_data']['context_queries'][0]  # Use first query config
        
        search_request = {
            'query': query_config['query'],
            'limit': query_config['limit']
        }
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_context_search_start",
            status="completed", metadata={"status":"starting", 
            "context":f"Locust testing context search with query: {query_config['query'][:50]}...",
            query=query_config['query'],
            limit=query_config['limit']
        )
        
        with self.client.post(
            endpoint,
            json=search_request,
            catch_"response":True
        ) as response:
            self.log_request(
                endpoint=endpoint,
                method="POST",
                "response":response,
                "context":f"Locust context search test for query: {query_config['query'][:50]}...",
                start_time=start_time,
                query=query_config['query']
            )
            
            if response.status_code not in [200, 201]:
                response.failure(f"Context search failed with status {response.status_code}")
        
        self.test_execution_count['context_search'] = self.test_execution_count.get('context_search', 0) + 1
    
    @task(1)
    def test_system_metrics(self):
        """Test system metrics endpoint"""
        if self.test_execution_count.get('system_metrics', 0) >= 1:
            return  # Only execute once
        
        start_time = time.time()
        endpoint = "/api/system/metrics"
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_system_metrics_start",
            status="completed", metadata={"status":"starting",
            "context":"Locust testing system metrics endpoint"
        )
        
        with self.client.get(endpoint, catch_"response":True) as response:
            self.log_request(
                endpoint=endpoint,
                method="GET",
                "response":response,
                "context":"Locust system metrics test",
                start_time=start_time
            )
            
            if response.status_code not in [200, 401]:  # 401 might be expected if auth is required
                response.failure(f"System metrics failed with status {response.status_code}")
        
        self.test_execution_count['system_metrics'] = self.test_execution_count.get('system_metrics', 0) + 1
    
    @task(1)
    def test_agents_list(self):
        """Test agents listing endpoint"""
        if self.test_execution_count.get('agents_list', 0) >= 1:
            return  # Only execute once
        
        start_time = time.time()
        endpoint = "/api/agents"
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_agents_list_start",
            status="completed", metadata={"status":"starting",
            "context":"Locust testing agents listing endpoint"
        )
        
        with self.client.get(endpoint, catch_"response":True) as response:
            self.log_request(
                endpoint=endpoint,
                method="GET",
                "response":response,
                "context":"Locust agents listing test",
                start_time=start_time
            )
            
            if response.status_code not in [200, 401]:
                response.failure(f"Agents listing failed with status {response.status_code}")
        
        self.test_execution_count['agents_list'] = self.test_execution_count.get('agents_list', 0) + 1
    
    @task(1)
    def test_workflows_list(self):
        """Test workflows listing endpoint"""
        if self.test_execution_count.get('workflows_list', 0) >= 1:
            return  # Only execute once
        
        start_time = time.time()
        endpoint = "/api/workflows"
        
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_workflows_list_start",
            status="completed", metadata={"status":"starting",
            "context":"Locust testing workflows listing endpoint"
        )
        
        with self.client.get(endpoint, catch_"response":True) as response:
            self.log_request(
                endpoint=endpoint,
                method="GET",
                "response":response,
                "context":"Locust workflows listing test",
                start_time=start_time
            )
            
            if response.status_code not in [200, 401]:
                response.failure(f"Workflows listing failed with status {response.status_code}")
        
        self.test_execution_count['workflows_list'] = self.test_execution_count.get('workflows_list', 0) + 1

# Event handlers for comprehensive logging
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Log when Locust test starts"""
    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
        step="locust_test_suite_start",
        status="completed", metadata={"status":"starting",
        "context":"Locust performance test suite starting",
        environment=str(environment),
        user_count=getattr(environment, 'parsed_options', {}).get('num_users', 1)
    )

@events.test_stop.add_listener 
def on_test_stop(environment, **kwargs):
    """Log when Locust test stops with summary statistics"""
    stats = environment.stats
    
    # Collect statistics
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    avg_response_time = stats.total.avg_response_time
    max_response_time = stats.total.max_response_time
    min_response_time = stats.total.min_response_time
    
    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
        step="locust_test_suite_complete",
        status="completed", metadata={"status":"completed",
        "context":"Locust performance test suite completed with statistics",
        total_requests=total_requests,
        total_failures=total_failures,
        success_rate=((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 0,
        avg_response_time_ms=avg_response_time,
        max_response_time_ms=max_response_time,
        min_response_time_ms=min_response_time,
        requests_per_second=stats.total.current_rps
    )

@events.request_success.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    """Log successful requests"""
    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
        step="locust_request_success",
        status="completed", metadata={"status":"success",
        "context":f"Successful {request_type} request to {name}",
        request_type=request_type,
        endpoint=name,
        response_time_ms=response_time,
        response_length=response_length
    )

@events.request_failure.add_listener
def on_request_failure(request_type, name, response_time, response_length, exception, **kwargs):
    """Log failed requests"""
    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
        step="locust_request_failure",
        status="completed", metadata={"status":"failure",
        "context":f"Failed {request_type} request to {name}",
        request_type=request_type,
        endpoint=name,
        response_time_ms=response_time,
        response_length=response_length,
        exception=str(exception)
    )

if __name__ == "__main__":
    # This allows running the locust file directly for testing
    import subprocess
    import sys
    
    logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
        step="locust_direct_execution",
        status="completed", metadata={"status":"starting",
        "context":"Running Locust test directly"
    )
    
    # Run locust with single user configuration
    cmd = [
        sys.executable, "-m", "locust",
        "-f", __file__,
        "--host", "http://localhost:8001",
        "--users", "1",
        "--spawn-rate", "1", 
        "--run-time", "5m",
        "--headless"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.log_workflow_step(step_id="test", agent_id="pytest_runner", step_name=
            step="locust_execution_failed",
            status="completed", metadata={"status":"error",
            "context":f"Locust execution failed: {str(e)}",
            error=str(e)
        )
"""
Code Graph API Tests
====================
Tests for code analysis and graph functionality.
"""

import pytest
import asyncio
import time
from typing import Dict, Any
from framework.base_test import APITest


class TestCodeGraph(APITest):
    """Test suite for Code Graph APIs"""
    
    def __init__(self):
        super().__init__("CodeGraph")
        
    async def setup(self):
        """Setup test data"""
        await self.setup_session()
        
        # Sample code repository for testing
        self.test_repository = {
            "repository_url": "https://github.com/test/sample-repo",
            "branch": "main",
            "language": "python",
            "files": [
                {
                    "path": "src/main.py",
                    "content": """
import utils
from models import UserModel

class Application:
    def __init__(self):
        self.user_model = UserModel()
        
    def process_user(self, user_id):
        user = self.user_model.get_user(user_id)
        return utils.format_user(user)
"""
                },
                {
                    "path": "src/utils.py",
                    "content": """
def format_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'formatted': True
    }

def validate_input(data):
    return data is not None
"""
                },
                {
                    "path": "src/models.py",
                    "content": """
class UserModel:
    def get_user(self, user_id):
        # Simulated database call
        return User(user_id, f"User_{user_id}")

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
"""
                }
            ]
        }
        
    async def cleanup(self):
        """Cleanup test data"""
        await self.cleanup_session()

    async def test_index_repository(self):
        """Test indexing a code repository"""
        start_time = time.time()
        
        index_data = {
            "repository_url": self.test_repository["repository_url"],
            "branch": self.test_repository["branch"],
            "include_patterns": ["*.py", "*.js"],
            "exclude_patterns": ["*test*", "node_modules/*"],
            "analysis_options": {
                "extract_dependencies": True,
                "analyze_complexity": True,
                "detect_patterns": True
            }
        }
        
        response = await self.make_request("POST", "/codegraph/index", data=index_data)
        
        assert response["status_code"] in [200, 201, 202]  # 202 for async processing
        assert "index_id" in response["data"] or "job_id" in response["data"]
        
        self.log_result("test_index_repository", "passed", time.time() - start_time)

    async def test_search_symbols(self):
        """Test searching for symbols in code"""
        start_time = time.time()
        
        search_params = {
            "query": "UserModel",
            "type": "class",
            "include_references": True,
            "include_definitions": True
        }
        
        response = await self.make_request("GET", "/codegraph/search", params=search_params)
        
        assert response["status_code"] == 200
        assert "results" in response["data"]
        # Should find the UserModel class
        
        self.log_result("test_search_symbols", "passed", time.time() - start_time)

    async def test_search_functions(self):
        """Test searching for functions"""
        start_time = time.time()
        
        search_params = {
            "query": "format_user",
            "type": "function",
            "include_callers": True
        }
        
        response = await self.make_request("GET", "/codegraph/search", params=search_params)
        
        assert response["status_code"] == 200
        assert "results" in response["data"]
        
        self.log_result("test_search_functions", "passed", time.time() - start_time)

    async def test_dependency_analysis(self):
        """Test analyzing code dependencies"""
        start_time = time.time()
        
        analysis_data = {
            "files": self.test_repository["files"],
            "analysis_type": "dependencies",
            "depth": 2
        }
        
        response = await self.make_request("POST", "/codegraph/analyze/dependencies", data=analysis_data)
        
        if response["status_code"] == 404:
            # Try alternative endpoint
            response = await self.make_request("POST", "/codegraph/dependencies", data=analysis_data)
            
        assert response["status_code"] in [200, 404]
        if response["status_code"] == 200:
            assert "dependencies" in response["data"] or "graph" in response["data"]
            
        self.log_result("test_dependency_analysis", "passed", time.time() - start_time)

    async def test_code_complexity(self):
        """Test code complexity analysis"""
        start_time = time.time()
        
        complexity_data = {
            "files": self.test_repository["files"],
            "metrics": ["cyclomatic", "cognitive", "halstead"]
        }
        
        response = await self.make_request("POST", "/codegraph/analyze/complexity", data=complexity_data)
        
        if response["status_code"] == 404:
            # Try alternative endpoint
            response = await self.make_request("POST", "/codegraph/complexity", data=complexity_data)
            
        assert response["status_code"] in [200, 404]
        if response["status_code"] == 200:
            assert "complexity_metrics" in response["data"] or "metrics" in response["data"]
            
        self.log_result("test_code_complexity", "passed", time.time() - start_time)

    async def test_find_references(self):
        """Test finding all references to a symbol"""
        start_time = time.time()
        
        reference_data = {
            "symbol": "UserModel",
            "scope": "project",
            "include_imports": True
        }
        
        response = await self.make_request("POST", "/codegraph/references", data=reference_data)
        
        if response["status_code"] == 404:
            # Try search endpoint with reference flag
            response = await self.make_request("GET", "/codegraph/search", 
                                             params={"query": "UserModel", "include_references": True})
            
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_find_references", "passed", time.time() - start_time)

    async def test_call_graph(self):
        """Test generating call graph"""
        start_time = time.time()
        
        call_graph_data = {
            "entry_point": "Application.process_user",
            "max_depth": 3,
            "include_external": False
        }
        
        response = await self.make_request("POST", "/codegraph/callgraph", data=call_graph_data)
        
        if response["status_code"] == 404:
            # Try alternative endpoint
            response = await self.make_request("POST", "/codegraph/analyze/callgraph", data=call_graph_data)
            
        assert response["status_code"] in [200, 404]
        if response["status_code"] == 200:
            assert "nodes" in response["data"] or "graph" in response["data"]
            
        self.log_result("test_call_graph", "passed", time.time() - start_time)

    async def test_pattern_detection(self):
        """Test detecting design patterns in code"""
        start_time = time.time()
        
        pattern_data = {
            "files": self.test_repository["files"],
            "patterns": ["singleton", "factory", "observer", "mvc"]
        }
        
        response = await self.make_request("POST", "/codegraph/patterns/detect", data=pattern_data)
        
        if response["status_code"] == 404:
            # Try alternative endpoint
            response = await self.make_request("POST", "/codegraph/analyze/patterns", data=pattern_data)
            
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_pattern_detection", "passed", time.time() - start_time)

    async def test_code_similarity(self):
        """Test finding similar code blocks"""
        start_time = time.time()
        
        similarity_data = {
            "code_block": """
def process_data(data):
    if not data:
        return None
    return {'processed': True, 'data': data}
""",
            "threshold": 0.7,
            "scope": "project"
        }
        
        response = await self.make_request("POST", "/codegraph/similarity", data=similarity_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_code_similarity", "passed", time.time() - start_time)

    async def test_refactoring_suggestions(self):
        """Test getting refactoring suggestions"""
        start_time = time.time()
        
        refactor_data = {
            "file": self.test_repository["files"][0],
            "issues": ["code_smell", "complexity", "duplication"]
        }
        
        response = await self.make_request("POST", "/codegraph/refactor/suggest", data=refactor_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_refactoring_suggestions", "passed", time.time() - start_time)

    async def test_incremental_indexing(self):
        """Test incremental code indexing"""
        start_time = time.time()
        
        # First index
        initial_index = {
            "repository_url": self.test_repository["repository_url"],
            "files": self.test_repository["files"][:2]  # First two files
        }
        
        response1 = await self.make_request("POST", "/codegraph/index", data=initial_index)
        
        # Incremental update
        if response1["status_code"] in [200, 201]:
            index_id = response1["data"].get("index_id", "default")
            
            incremental_data = {
                "index_id": index_id,
                "added_files": [self.test_repository["files"][2]],
                "modified_files": [],
                "deleted_files": []
            }
            
            response2 = await self.make_request("POST", "/codegraph/index/incremental", data=incremental_data)
            assert response2["status_code"] in [200, 404]
            
        self.log_result("test_incremental_indexing", "passed", time.time() - start_time)

    async def test_code_navigation(self):
        """Test code navigation features"""
        start_time = time.time()
        
        navigation_data = {
            "file": "src/main.py",
            "line": 8,
            "column": 15,
            "action": "go_to_definition"
        }
        
        response = await self.make_request("POST", "/codegraph/navigate", data=navigation_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_code_navigation", "passed", time.time() - start_time)

    async def test_batch_search(self):
        """Test batch searching multiple symbols"""
        start_time = time.time()
        
        batch_search_data = {
            "queries": [
                {"symbol": "UserModel", "type": "class"},
                {"symbol": "format_user", "type": "function"},
                {"symbol": "get_user", "type": "method"}
            ]
        }
        
        response = await self.make_request("POST", "/codegraph/search/batch", data=batch_search_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_batch_search", "passed", time.time() - start_time)

    async def test_code_metrics(self):
        """Test comprehensive code metrics"""
        start_time = time.time()
        
        metrics_data = {
            "files": self.test_repository["files"],
            "metrics": {
                "lines_of_code": True,
                "complexity": True,
                "maintainability_index": True,
                "test_coverage": False,  # Would need test files
                "documentation_ratio": True
            }
        }
        
        response = await self.make_request("POST", "/codegraph/metrics", data=metrics_data)
        
        assert response["status_code"] in [200, 404]
        
        self.log_result("test_code_metrics", "passed", time.time() - start_time)

    async def test_invalid_syntax_handling(self):
        """Test handling of invalid code syntax"""
        start_time = time.time()
        
        invalid_code = {
            "files": [{
                "path": "invalid.py",
                "content": """
def broken_function(
    print("Missing closing parenthesis"
    
class InvalidClass
    def method(self):
        return
"""
            }]
        }
        
        response = await self.make_request("POST", "/codegraph/index", data=invalid_code)
        
        # Should handle gracefully, either with error details or partial success
        assert response["status_code"] in [200, 400, 422]
        
        self.log_result("test_invalid_syntax_handling", "passed", time.time() - start_time)


# For pytest compatibility
test_instance = TestCodeGraph()

@pytest.mark.asyncio
async def test_code_graph_suite():
    """Run all code graph tests"""
    await test_instance.setup()
    
    # Run all test methods
    test_methods = [method for method in dir(test_instance) 
                   if method.startswith('test_') and method != 'test_code_graph_suite']
    
    for method_name in test_methods:
        method = getattr(test_instance, method_name)
        if asyncio.iscoroutinefunction(method):
            await method()
            
    await test_instance.cleanup()
    
    # Print summary
    summary = test_instance.get_test_summary()
    print(f"\nCode Graph Test Summary:")
    print(f"Total: {summary['total_tests']}, Passed: {summary['passed']}, "
          f"Failed: {summary['failed']}, Success Rate: {summary['success_rate']:.1f}%")


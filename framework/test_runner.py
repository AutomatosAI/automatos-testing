
"""
Test Runner for Automotas AI Testing Framework
==============================================

Orchestrates and runs all test suites with reporting.
"""

import asyncio
import importlib
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Type
import json
from datetime import datetime

from .base_test import BaseTest, TestLevel
from .config import test_config
from .reporting import TestReporter

class TestSuiteDiscovery:
    """Discovers and loads test suites"""
    
    def __init__(self, test_directory: str = "tests"):
        self.test_directory = Path(test_directory)
        self.test_classes: List[Type[BaseTest]] = []
        
    def discover_tests(self) -> List[Type[BaseTest]]:
        """Discover all test classes in the test directory"""
        test_files = list(self.test_directory.rglob("test_*.py"))
        
        for test_file in test_files:
            module_name = str(test_file).replace("/", ".").replace(".py", "")
            try:
                module = importlib.import_module(module_name)
                
                # Find all BaseTest subclasses in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BaseTest) and 
                        attr != BaseTest):
                        self.test_classes.append(attr)
                        
            except Exception as e:
                print(f"Warning: Could not import test module {module_name}: {e}")
                
        return self.test_classes

class TestRunner:
    """Main test runner for the Automotas AI testing framework"""
    
    def __init__(self):
        self.config = test_config
        self.reporter = TestReporter()
        self.discovery = TestSuiteDiscovery()
        self.test_results: Dict[str, Any] = {}
        
    async def run_test_class(self, test_class: Type[BaseTest]) -> Dict[str, Any]:
        """Run a single test class"""
        print(f"\n🧪 Running {test_class.__name__}")
        print("=" * 50)
        
        test_instance = test_class()
        start_time = time.time()
        
        try:
            # Setup
            if hasattr(test_instance, 'setup'):
                await test_instance.setup()
            
            # Run tests
            test_methods = [method for method in dir(test_instance) 
                          if method.startswith('test_') and callable(getattr(test_instance, method))]
            
            for method_name in test_methods:
                method = getattr(test_instance, method_name)
                method_start = time.time()
                
                try:
                    if asyncio.iscoroutinefunction(method):
                        await method()
                    else:
                        method()
                    test_instance.log_result(method_name, "passed", time.time() - method_start)
                except Exception as e:
                    test_instance.log_result(method_name, "failed", time.time() - method_start, str(e))
                    
            # Cleanup
            if hasattr(test_instance, 'cleanup'):
                await test_instance.cleanup()
                
        except Exception as e:
            print(f"❌ Test suite {test_class.__name__} failed during setup/cleanup: {e}")
            
        duration = time.time() - start_time
        summary = test_instance.get_test_summary()
        summary['total_duration'] = duration
        
        return summary
        
    async def run_tests(self, test_filter: str = None, 
                       test_level: TestLevel = None) -> Dict[str, Any]:
        """Run all discovered tests"""
        print("🚀 Automotas AI Testing Framework")
        print("=" * 60)
        print(f"Environment: {self.config.environment.value}")
        print(f"API Base URL: {self.config.api.base_url}")
        print(f"Parallel Tests: {self.config.parallel_tests}")
        
        # Discover tests
        test_classes = self.discovery.discover_tests()
        
        # Apply filters
        if test_filter:
            test_classes = [tc for tc in test_classes if test_filter.lower() in tc.__name__.lower()]
            
        if test_level:
            # This would require test classes to have a level attribute
            pass
            
        print(f"\nDiscovered {len(test_classes)} test suites")
        
        # Run tests
        start_time = time.time()
        all_results = {}
        
        if self.config.parallel_tests and len(test_classes) > 1:
            # Run tests in parallel
            tasks = [self.run_test_class(tc) for tc in test_classes]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for test_class, result in zip(test_classes, results):
                if isinstance(result, Exception):
                    print(f"❌ Test suite {test_class.__name__} failed: {result}")
                else:
                    all_results[test_class.__name__] = result
        else:
            # Run tests sequentially
            for test_class in test_classes:
                result = await self.run_test_class(test_class)
                all_results[test_class.__name__] = result
                
        total_duration = time.time() - start_time
        
        # Generate summary
        test_summary = self._generate_test_summary(all_results, total_duration)
        
        # Generate reports
        if self.config.generate_reports:
            await self.reporter.generate_report(test_summary, all_results)
            
        return test_summary
        
    def _generate_test_summary(self, all_results: Dict[str, Any], 
                              total_duration: float) -> Dict[str, Any]:
        """Generate overall test summary"""
        total_tests = sum(r.get('total_tests', 0) for r in all_results.values())
        total_passed = sum(r.get('passed', 0) for r in all_results.values())
        total_failed = sum(r.get('failed', 0) for r in all_results.values())
        total_skipped = sum(r.get('skipped', 0) for r in all_results.values())
        
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        summary = {
            "test_run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "environment": self.config.environment.value,
            "timestamp": datetime.now().isoformat(),
            "duration": total_duration,
            "total_suites": len(all_results),
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "skipped": total_skipped,
            "success_rate": success_rate,
            "status": "passed" if total_failed == 0 else "failed"
        }
        
        # Print summary
        print(f"\n📊 Test Run Summary")
        print("=" * 40)
        print(f"Total Suites: {summary['total_suites']}")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {total_passed}")
        print(f"❌ Failed: {total_failed}")
        print(f"⏭️ Skipped: {total_skipped}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Duration: {total_duration:.2f}s")
        
        status_emoji = "🎉" if total_failed == 0 else "⚠️"
        print(f"\n{status_emoji} Overall Status: {summary['status'].upper()}")
        
        return summary

async def main():
    """Main entry point for test runner"""
    runner = TestRunner()
    
    # Parse command line arguments (simplified)
    test_filter = sys.argv[1] if len(sys.argv) > 1 else None
    
    await runner.run_tests(test_filter=test_filter)

if __name__ == "__main__":
    asyncio.run(main())

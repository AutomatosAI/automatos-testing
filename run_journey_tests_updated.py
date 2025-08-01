"""
Automotas AI Journey Test Runner (Updated)

This script runs individual journey tests or all available journey tests.
"""

import os
import sys
import argparse
import time
from datetime import datetime
from typing import List, Dict, Any

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from test_logger import WorkflowTestLogger

class JourneyTestRunner:
    """Master test runner for all journey tests"""
    
    def __init__(self):
        self.available_journeys = {
            "agent_management": {
                "module": "journey_tests.agent_management_journey",
                "class": "AgentManagementJourney",
                "description": "Complete agent lifecycle testing"
            },
            "workflow_orchestration": {
                "module": "journey_tests.workflow_orchestration_journey",
                "class": "WorkflowOrchestrationJourney",
                "description": "Complete workflow lifecycle and execution testing"
            }
            # Future journeys will be added here
            # "document_management": {...},
            # "context_engineering": {...},
            # "performance_analytics": {...}
        }
        
        self.logger = WorkflowTestLogger("journey_test_runner")
        self.results = {}
    
    def list_available_journeys(self):
        """List all available journey tests"""
        print("\n🚀 Available Journey Tests:")
        print("=" * 50)
        
        for journey_name, info in self.available_journeys.items():
            print(f"  📋 {journey_name}")
            print(f"     Description: {info['description']}")
            print()
    
    def run_journey(self, journey_name: str) -> bool:
        """Run a specific journey test"""
        
        if journey_name not in self.available_journeys:
            print(f"❌ Journey '{journey_name}' not found")
            self.list_available_journeys()
            return False
        
        journey_info = self.available_journeys[journey_name]
        
        print(f"\n🔬 Running Journey: {journey_name}")
        print(f"📖 Description: {journey_info['description']}")
        print("=" * 60)
        
        try:
            # Import and instantiate the journey class
            module_path = journey_info["module"]
            class_name = journey_info["class"]
            
            # Dynamic import
            module = __import__(module_path, fromlist=[class_name])
            journey_class = getattr(module, class_name)
            
            # Run the journey
            start_time = time.time()
            journey_instance = journey_class()
            success = journey_instance.run_full_journey()
            duration = time.time() - start_time
            
            # Record results
            self.results[journey_name] = {
                "success": success,
                "duration": duration,
                "timestamp": datetime.now().isoformat()
            }
            
            # Log results
            self.logger.log_step(
                f"journey_{journey_name}",
                f"Journey {journey_name} completed",
                "completed" if success else "failed",
                metadata={
                    "duration_seconds": duration,
                    "success": success
                }
            )
            
            if success:
                print(f"\n✅ Journey '{journey_name}' completed successfully")
                print(f"⏱️  Duration: {duration:.2f} seconds")
            else:
                print(f"\n❌ Journey '{journey_name}' failed")
                print(f"⏱️  Duration: {duration:.2f} seconds")
            
            return success
            
        except Exception as e:
            print(f"\n💥 Error running journey '{journey_name}': {str(e)}")
            self.logger.log_error(f"Journey {journey_name} failed with exception", e)
            
            self.results[journey_name] = {
                "success": False,
                "duration": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            return False
    
    def generate_summary_report(self):
        """Generate a summary report of all test results"""
        
        if not self.results:
            print("\n📊 No test results to report.")
            return
        
        print("\n" + "="*60)
        print("📊 JOURNEY TESTING SUMMARY REPORT")
        print("="*60)
        
        successful_journeys = [name for name, result in self.results.items() if result["success"]]
        failed_journeys = [name for name, result in self.results.items() if not result["success"]]
        
        total_duration = sum(result["duration"] for result in self.results.values())
        
        print(f"\n📈 OVERALL RESULTS:")
        print(f"   Total Journeys: {len(self.results)}")
        print(f"   ✅ Successful: {len(successful_journeys)}")
        print(f"   ❌ Failed: {len(failed_journeys)}")
        print(f"   �� Success Rate: {(len(successful_journeys)/len(self.results)*100):.1f}%")
        print(f"   ⏱️  Total Duration: {total_duration:.2f} seconds")
        
        if successful_journeys:
            print(f"\n✅ SUCCESSFUL JOURNEYS:")
            for journey in successful_journeys:
                duration = self.results[journey]["duration"]
                print(f"   🟢 {journey} ({duration:.2f}s)")
        
        if failed_journeys:
            print(f"\n❌ FAILED JOURNEYS:")
            for journey in failed_journeys:
                duration = self.results[journey]["duration"]
                error = self.results[journey].get("error", "Unknown error")
                print(f"   🔴 {journey} ({duration:.2f}s) - {error}")
        
        print(f"\n📁 Detailed logs available in: ~/automotas_tests/logs/")
        print("="*60)

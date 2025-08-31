#!/usr/bin/env python3
"""
Quick validation script for Phase 2 test modules
"""

import subprocess
import sys
import time
import json
from pathlib import Path

def run_test_module(module_name):
    """Run a specific test module and return results"""
    print(f"\n🧪 Testing {module_name}...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Run the test with JSON output
        result = subprocess.run(
            [sys.executable, "run_tests.py", "--filter", module_name, "--json", f"reports/phase2_{module_name}.json"],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        duration = time.time() - start_time
        
        # Parse output to get summary
        if result.returncode == 0:
            # Try to read the JSON report
            report_path = Path(f"reports/phase2_{module_name}.json")
            if report_path.exists():
                with open(report_path) as f:
                    report = json.load(f)
                    summary = report.get("summary", {})
                    print(f"✅ {module_name}: PASSED")
                    print(f"   Total Tests: {summary.get('total_tests', 0)}")
                    print(f"   Passed: {summary.get('passed', 0)}")
                    print(f"   Failed: {summary.get('failed', 0)}")
                    print(f"   Success Rate: {summary.get('success_rate', 0):.1f}%")
            else:
                print(f"✅ {module_name}: Completed (no report found)")
        else:
            print(f"❌ {module_name}: FAILED")
            print(f"   Error: {result.stderr[:200]}")
            
        print(f"   Duration: {duration:.2f}s")
        
        return {
            "module": module_name,
            "success": result.returncode == 0,
            "duration": duration,
            "output": result.stdout,
            "error": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print(f"❌ {module_name}: TIMEOUT")
        return {
            "module": module_name,
            "success": False,
            "duration": 120,
            "error": "Test timed out after 120 seconds"
        }
    except Exception as e:
        print(f"❌ {module_name}: ERROR - {str(e)}")
        return {
            "module": module_name,
            "success": False,
            "duration": time.time() - start_time,
            "error": str(e)
        }

def main():
    """Run all Phase 2 test modules"""
    print("🚀 Phase 2 Test Module Validation")
    print("=" * 60)
    
    # Phase 2 modules
    modules = [
        "context_policy",
        "code_graph", 
        "playbooks",
        "patterns"
    ]
    
    # Create reports directory
    Path("reports").mkdir(exist_ok=True)
    
    # Run all tests
    results = []
    total_start = time.time()
    
    for module in modules:
        result = run_test_module(module)
        results.append(result)
        
    total_duration = time.time() - total_start
    
    # Summary
    print("\n📊 Phase 2 Test Summary")
    print("=" * 60)
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print(f"Total Modules: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"Total Duration: {total_duration:.2f}s")
    
    # Save summary report
    summary_report = {
        "phase": "Phase 2 Test Implementation",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_modules": len(results),
        "successful": successful,
        "failed": failed,
        "duration": total_duration,
        "results": results
    }
    
    with open("reports/phase2_validation_summary.json", "w") as f:
        json.dump(summary_report, f, indent=2)
        
    print(f"\n📄 Summary report saved to: reports/phase2_validation_summary.json")
    
    # Exit code based on success
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()


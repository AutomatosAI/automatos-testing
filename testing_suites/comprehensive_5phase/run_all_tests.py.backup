#!/usr/bin/env python3
"""
COMPREHENSIVE AUTOMOTAS AI TESTING - MASTER TEST RUNNER
Executes all five phases of testing with full logging and reporting
"""

import sys
import os
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

class MasterTestRunner:
    """
    Master test runner for all comprehensive testing phases
    """
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.phases = [
            {
                "name": "Phase 1: Agent Management",
                "script": "phase1_agent_management/scripts/comprehensive_agent_test.py",
                "description": "Complete agent lifecycle, skills, and execution testing"
            },
            {
                "name": "Phase 2: Workflow Orchestration",
                "script": "phase2_workflow_orchestration/scripts/comprehensive_workflow_test.py",
                "description": "Pattern management, templates, and workflow analytics"
            },
            {
                "name": "Phase 3: Document Management",
                "script": "phase3_document_management/scripts/comprehensive_document_test.py",
                "description": "Document processing, analytics, and system integration"
            },
            {
                "name": "Phase 4: Context Engineering",
                "script": "phase4_context_engineering/scripts/comprehensive_context_test.py",
                "description": "RAG system performance, context retrieval, and vector embeddings"
            },
            {
                "name": "Phase 5: Performance Analytics",
                "script": "phase5_performance_analytics/scripts/comprehensive_performance_test.py",
                "description": "System metrics, performance monitoring, and optimization analytics"
            }
        ]
        
        self.results = {}
        self.master_log = []
        
    def run_all_phases(self):
        """
        Execute all testing phases sequentially
        """
        print("🚀 AUTOMOTAS AI COMPREHENSIVE TESTING - MASTER EXECUTION (5 PHASES)")
        print("=" * 80)
        print(f"⏰ Started at: {datetime.now().isoformat()}")
        print(f"📋 Phases to execute: {len(self.phases)}")
        print()
        
        start_time = time.time()
        overall_success = True
        
        for i, phase in enumerate(self.phases, 1):
            print(f"\n{'='*25} {phase['name'].upper()} {'='*25}")
            print(f"📋 Description: {phase['description']}")
            print(f"📄 Script: {phase['script']}")
            print(f"📊 Progress: {i}/{len(self.phases)} phases")
            print()
            
            # Log phase start
            phase_start = time.time()
            self.log_event("phase_start", phase['name'], {"script": phase['script']})
            
            # Execute phase
            success = self.run_phase(phase)
            phase_duration = time.time() - phase_start
            
            # Log phase completion
            self.log_event("phase_complete", phase['name'], {
                "success": success,
                "duration_seconds": round(phase_duration, 2)
            })
            
            # Store results
            self.results[f"phase_{i}"] = {
                "name": phase['name'],
                "success": success,
                "duration": phase_duration,
                "script": phase['script']
            }
            
            if not success:
                overall_success = False
                print(f"❌ {phase['name']} FAILED!")
                # Continue with other phases even if one fails
            else:
                print(f"✅ {phase['name']} COMPLETED SUCCESSFULLY!")
                
            # Brief pause between phases
            if i < len(self.phases):
                print("⏳ Brief pause before next phase...")
                time.sleep(2)
        
        # Generate master report
        total_duration = time.time() - start_time
        self.generate_master_report(overall_success, total_duration)
        
        print(f"\n{'='*80}")
        print(f"🏁 COMPREHENSIVE TESTING COMPLETED - ALL 5 PHASES")
        print(f"⏱️ Total Duration: {round(total_duration, 2)} seconds ({round(total_duration/60, 1)} minutes)")
        print(f"📊 Overall Success: {'✅ YES' if overall_success else '❌ NO'}")
        print(f"🎯 Successful Phases: {len([r for r in self.results.values() if r['success']])}/{len(self.phases)}")
        
        return overall_success
    
    def run_phase(self, phase):
        """
        Execute a single testing phase
        """
        script_path = self.test_dir / phase['script']
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        try:
            # Make script executable
            script_path.chmod(0o755)
            
            # Execute the test script
            print(f"🚀 Executing: {script_path}")
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(script_path.parent),
                capture_output=True,
                text=True,
                timeout=900  # 15 minute timeout per phase (increased for new phases)
            )
            
            # Log output
            self.log_event("phase_output", phase['name'], {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            })
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"❌ {phase['name']} timed out after 15 minutes")
            return False
        except Exception as e:
            print(f"❌ {phase['name']} failed with exception: {str(e)}")
            return False
    
    def log_event(self, event_type, phase_name, data):
        """
        Log an event to the master log
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "phase_name": phase_name,
            "data": data
        }
        self.master_log.append(log_entry)
    
    def generate_master_report(self, overall_success, total_duration):
        """
        Generate comprehensive master report
        """
        successful_phases = len([r for r in self.results.values() if r['success']])
        failed_phases = len([r for r in self.results.values() if not r['success']])
        
        report = {
            "test_execution": {
                "timestamp": datetime.now().isoformat(),
                "overall_success": overall_success,
                "total_duration_seconds": round(total_duration, 2),
                "total_duration_minutes": round(total_duration / 60, 2),
                "phases_executed": len(self.phases)
            },
            "phase_results": self.results,
            "summary": {
                "successful_phases": successful_phases,
                "failed_phases": failed_phases,
                "success_rate": round((successful_phases / len(self.phases)) * 100, 2),
                "total_phases": len(self.phases)
            },
            "performance_summary": {
                "fastest_phase": min(self.results.values(), key=lambda x: x['duration'])['name'] if self.results else None,
                "slowest_phase": max(self.results.values(), key=lambda x: x['duration'])['name'] if self.results else None,
                "average_phase_duration": round(sum(r['duration'] for r in self.results.values()) / len(self.results), 2) if self.results else 0
            },
            "detailed_log": self.master_log
        }
        
        # Save master report
        report_file = self.test_dir / f"MASTER_TEST_REPORT_5PHASES_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Create enhanced summary report
        summary_file = self.test_dir / f"MASTER_SUMMARY_5PHASES_{int(time.time())}.md"
        with open(summary_file, 'w') as f:
            f.write(f"# AUTOMOTAS AI COMPREHENSIVE TESTING - 5 PHASE MASTER REPORT\n\n")
            f.write(f"**Execution Time:** {datetime.now().isoformat()}\n")
            f.write(f"**Overall Success:** {'✅ YES' if overall_success else '❌ NO'}\n")
            f.write(f"**Total Duration:** {round(total_duration, 2)} seconds ({round(total_duration/60, 1)} minutes)\n")
            f.write(f"**Phases Executed:** {len(self.phases)}\n\n")
            
            f.write(f"## Phase Results\n\n")
            for phase_key, phase_result in self.results.items():
                status = "✅ SUCCESS" if phase_result['success'] else "❌ FAILED"
                f.write(f"### {phase_result['name']}\n")
                f.write(f"- **Status:** {status}\n")
                f.write(f"- **Duration:** {round(phase_result['duration'], 2)} seconds\n")
                f.write(f"- **Script:** `{phase_result['script']}`\n\n")
            
            f.write(f"## Summary Statistics\n\n")
            f.write(f"- **Successful Phases:** {successful_phases}/{len(self.phases)}\n")
            f.write(f"- **Success Rate:** {report['summary']['success_rate']}%\n")
            f.write(f"- **Failed Phases:** {failed_phases}\n")
            f.write(f"- **Average Phase Duration:** {report['performance_summary']['average_phase_duration']} seconds\n")
            f.write(f"- **Fastest Phase:** {report['performance_summary']['fastest_phase']}\n")
            f.write(f"- **Slowest Phase:** {report['performance_summary']['slowest_phase']}\n\n")
            
            f.write(f"## Testing Coverage\n\n")
            f.write(f"This comprehensive test suite covers:\n")
            f.write(f"1. **Agent Management** - Agent lifecycle, skills, execution\n")
            f.write(f"2. **Workflow Orchestration** - Patterns, templates, analytics\n")
            f.write(f"3. **Document Management** - Processing, uploads, analytics\n")
            f.write(f"4. **Context Engineering** - RAG system, embeddings, retrieval\n")
            f.write(f"5. **Performance Analytics** - Metrics, monitoring, optimization\n\n")
        
        print(f"\n📊 Master report saved to: {report_file}")
        print(f"📄 Summary report saved to: {summary_file}")
        
        return report

def main():
    """
    Main execution function
    """
    print("🚀 AUTOMOTAS AI COMPREHENSIVE TESTING SUITE - 5 PHASES")
    print("=====================================================")
    print("📋 Testing Coverage:")
    print("   1. Agent Management")
    print("   2. Workflow Orchestration") 
    print("   3. Document Management")
    print("   4. Context Engineering")
    print("   5. Performance Analytics")
    print()
    
    runner = MasterTestRunner()
    success = runner.run_all_phases()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Automotas AI Testing Framework Runner
====================================

Command-line interface for running the comprehensive testing framework.
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / "framework"))

from framework.test_runner import TestRunner
from framework.config import TestLevel, TestEnvironment

async def main():
    parser = argparse.ArgumentParser(
        description="Automotas AI Comprehensive Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                          # Run all tests
  python run_tests.py --filter agent          # Run only agent-related tests
  python run_tests.py --level integration     # Run only integration tests
  python run_tests.py --environment staging   # Run tests against staging
  python run_tests.py --parallel --reports    # Run tests in parallel with reports
        """
    )
    
    parser.add_argument(
        "--filter", "-f",
        help="Filter tests by name (substring match)"
    )
    
    parser.add_argument(
        "--level", "-l",
        choices=[level.value for level in TestLevel],
        help="Run tests of specific level"
    )
    
    parser.add_argument(
        "--environment", "-e",
        choices=[env.value for env in TestEnvironment],
        help="Target environment for testing"
    )
    
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run tests in parallel"
    )
    
    parser.add_argument(
        "--reports", "-r",
        action="store_true",
        help="Generate test reports"
    )
    
    parser.add_argument(
        "--api-url",
        help="Override API base URL"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Override configuration based on arguments
    if args.environment:
        import os
        os.environ["TEST_ENVIRONMENT"] = args.environment
        
    if args.api_url:
        import os
        os.environ["API_BASE_URL"] = args.api_url
        # Ensure OpenAPI discovery path alignment
        os.environ.setdefault("OPENAPI_PATH", "/openapi.json")
        
    if args.parallel:
        import os
        os.environ["PARALLEL_TESTS"] = "true"
        
    if args.reports:
        import os
        os.environ["GENERATE_REPORTS"] = "true"
        
    # Set logging level
    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run test runner
    runner = TestRunner()
    
    test_level = None
    if args.level:
        test_level = TestLevel(args.level)
    
    try:
        summary = await runner.run_tests(
            test_filter=args.filter,
            test_level=test_level
        )
        
        # Exit with error code if tests failed
        if summary["status"] == "failed":
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Testing framework error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

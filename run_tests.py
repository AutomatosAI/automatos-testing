
#!/usr/bin/env python3
"""
Automotas AI Testing Framework Runner
====================================

Command-line interface for running the comprehensive testing framework.
"""

import asyncio
import argparse
import sys
import json
import os
from pathlib import Path
try:
    from dotenv import load_dotenv, find_dotenv  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    load_dotenv = None  # type: ignore
    find_dotenv = None  # type: ignore

# Load .env BEFORE importing framework so config picks it up at import-time
if 'PYTEST_CURRENT_TEST' not in os.environ:  # avoid side-effects during pytest collection
    if load_dotenv is not None:
        try:
            # Local .env next to this script
            load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=False)
            # And search upward from CWD
            if find_dotenv is not None:
                env_path = find_dotenv(usecwd=True)
                if env_path:
                    load_dotenv(env_path, override=False)
        except Exception:
            pass

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / "framework"))

from framework.test_runner import TestRunner
from framework.config import TestLevel, TestEnvironment

async def main():
    # Load environment variables from a .env file if present (repo root or CWD)
    # Does not override existing environment variables
    # Load from .env if python-dotenv is available
    if load_dotenv is not None:
        try:
            # Explicit repo-local .env next to this file
            load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=False)
            # And a generic search starting from CWD upward
            if find_dotenv is not None:
                env_path = find_dotenv(usecwd=True)
                if env_path:
                    load_dotenv(env_path, override=False)
        except Exception:
            # Safe to ignore any load error
            pass
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
        "--json",
        help="Write summary JSON to this path"
    )
    parser.add_argument(
        "--module-sequence",
        action="store_true",
        help="Run modules in sequence and write per-module artifacts to reports/<module>.json"
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop sequence on first failure"
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
        os.environ["TEST_ENVIRONMENT"] = args.environment
        
    if args.api_url:
        os.environ["API_BASE_URL"] = args.api_url
        # Ensure OpenAPI discovery path alignment
        os.environ.setdefault("OPENAPI_PATH", "/openapi.json")
        
    if args.parallel:
        os.environ["PARALLEL_TESTS"] = "true"
        
    if args.reports:
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
    
    MODULES_ORDER = [
        "dashboard","agents","workflows","context","analytics","knowledge","playbooks","settings"
    ]

    try:
        if args.module_sequence:
            reports_dir = Path(os.environ.get("REPORTS_DIR", "reports"))
            reports_dir.mkdir(parents=True, exist_ok=True)

            combined = {"ok": True, "modules": {}}
            any_failed = False
            for module in MODULES_ORDER:
                summary = await runner.run_tests(test_filter=module, test_level=test_level)
                combined["modules"][module] = summary
                # Write per-module JSON
                with open(reports_dir / f"{module}.json", "w") as f:
                    json.dump(summary, f, indent=2)
                # Determine failure state
                if summary.get("status") == "failed":
                    any_failed = True
                    if args.fail_fast:
                        break
            overall = {
                "ok": not any_failed,
                "focus": "sequence",
                "modules": combined["modules"]
            }
            if args.json:
                with open(args.json, "w") as f:
                    json.dump(overall, f, indent=2)
            sys.exit(0 if overall["ok"] else 1)
        else:
            summary = await runner.run_tests(
                test_filter=args.filter,
                test_level=test_level
            )
            if args.json:
                with open(args.json, "w") as f:
                    json.dump(summary, f, indent=2)
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

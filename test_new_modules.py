#!/usr/bin/env python3
"""
Quick test runner for newly created test modules
"""

import asyncio
import sys
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / "framework"))

async def test_single_module(module_name):
    """Test a single module"""
    print(f"\n🧪 Testing {module_name} module...")
    
    try:
        # Import the test module
        if module_name == "documents":
            from tests.test_documents import TestDocuments
            test_class = TestDocuments()
        elif module_name == "field_theory":
            from tests.test_field_theory import TestFieldTheory
            test_class = TestFieldTheory()
        elif module_name == "evaluation":
            from tests.test_evaluation import TestEvaluation
            test_class = TestEvaluation()
        else:
            print(f"❌ Unknown module: {module_name}")
            return
            
        # Run a simple test method
        await test_class.setup()
        
        # Run health check or first test
        if module_name == "documents":
            print("  → Testing document upload...")
            doc_id = await test_class.test_upload_text_document()
            print(f"  ✅ Document uploaded successfully: {doc_id}")
        elif module_name == "field_theory":
            print("  → Testing field update...")
            session_id = await test_class.test_update_field_context()
            print(f"  ✅ Field updated successfully: {session_id}")
        elif module_name == "evaluation":
            print("  → Testing system evaluation...")
            eval_id = await test_class.test_evaluate_system()
            print(f"  ✅ Evaluation started successfully: {eval_id}")
            
        await test_class.cleanup()
        print(f"✅ {module_name} module tests are working!")
        
    except Exception as e:
        print(f"❌ Error testing {module_name}: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test runner"""
    print("🚀 Testing newly created test modules...")
    print("=" * 50)
    
    modules = ["documents", "field_theory", "evaluation"]
    
    for module in modules:
        await test_single_module(module)
        
    print("\n" + "=" * 50)
    print("✅ Test validation complete!")
    print("\nTo run full tests for each module:")
    print("  python run_tests.py --filter documents")
    print("  python run_tests.py --filter field")
    print("  python run_tests.py --filter evaluation")

if __name__ == "__main__":
    asyncio.run(main())


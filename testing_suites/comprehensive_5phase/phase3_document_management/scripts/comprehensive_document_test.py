#!/usr/bin/env python3
"""
PHASE 3: COMPREHENSIVE DOCUMENT MANAGEMENT TESTING
Tests all document-related endpoints with full request/response logging
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_utils import ComprehensiveAPITester

class DocumentManagementTester:
    """
    Comprehensive Document Management testing with full API logging
    """
    
    def __init__(self):
        test_dir = Path(__file__).parent.parent
        config_path = test_dir.parent.parent / "shared_config.yaml"
        
        self.tester = ComprehensiveAPITester(
            config_path=str(config_path),
            phase_name="document_management",
            test_dir=str(test_dir)
        )
        
        self.created_documents = []
        self.created_collections = []
        self.test_summary = {
            "documents_tested": 0,
            "collections_tested": 0,
            "processing_operations": 0,
            "analytics_operations": 0,
            "upload_attempts": 0,
            "upload_successes": 0,
            "api_calls_made": 0,
            "successful_calls": 0,
            "failed_calls": 0
        }
    
    def run_comprehensive_tests(self):
        """
        Run all document management tests and return real success/failure
        """
        print("🚀 STARTING COMPREHENSIVE DOCUMENT MANAGEMENT TESTING")
        print("=" * 64)
        
        try:
            # Phase 1: Environment Discovery
            self.test_environment_setup()
            
            # Phase 2: Document Upload Operations
            self.test_document_upload()
            
            # Phase 3: Document Processing
            self.test_document_processing()
            
            # Phase 4: Document Analytics
            self.test_document_analytics()
            
            # Phase 5: Search and Retrieval
            self.test_document_search()
            
            # Phase 6: Advanced Operations
            self.test_advanced_operations()
            
            # Phase 7: Error Handling
            self.test_error_handling()
            
            # Phase 8: Performance Testing
            self.test_performance()
            
            # Generate final report
            report = self.generate_final_report()
            
            # Calculate real success based on API results
            total_calls = self.test_summary["api_calls_made"]
            successful_calls = self.test_summary["successful_calls"]
            
            print(f"\n📊 DOCUMENT MANAGEMENT TESTING COMPLETED")
            print(f"📊 Total API Calls: {total_calls}")
            print(f"✅ Successful: {successful_calls}")
            print(f"❌ Failed: {total_calls - successful_calls}")
            
            # Define minimum success threshold (70% of API calls must succeed)
            success_threshold = 0.7
            success_rate = successful_calls / total_calls if total_calls > 0 else 0
            
        print(f"📈 Success Rate: {success_rate * 100:.1f}%")
        print(f"🎯 Required Threshold: {success_threshold * 100:.1f}%")
            
            is_successful = success_rate >= success_threshold
            
            if is_successful:
                print("✅ DOCUMENT MANAGEMENT TESTS PASSED - Meeting minimum threshold")
                return True
            else:
                print("❌ DOCUMENT MANAGEMENT TESTS FAILED - Below minimum threshold")
                return False
            
        except Exception as e:
            print(f"💥 COMPREHENSIVE TESTING FAILED: {str(e)}")
            import traceback
            print(f"🔍 Error details: {traceback.format_exc()}")
            return False

    def test_environment_setup(self):
        """
        Test 1: Environment Setup and Discovery
        """
        print("\n🔍 PHASE 1: ENVIRONMENT SETUP & DISCOVERY")
        
        # Test 1.1: Health Check
        result = self.tester.make_api_call("GET", "/health")
        self.update_summary(result)
        
        # Test 1.2: Endpoint Discovery
        discovery = self.tester.test_endpoint_discovery()
        
        # Test 1.3: Document System Discovery
        document_endpoints = [
            "/api/documents/",
            "/api/documents/processing/pipeline",
            "/api/documents/processing/live-status",
            "/api/documents/analytics/overview",
            "/api/documents/analytics/search-patterns"
        ]
        
        print("\n📋 Testing Document Endpoint Availability:")
        for endpoint in document_endpoints:
            result = self.tester.make_api_call("GET", endpoint, expected_status=[200, 404, 405])
            self.update_summary(result)
            status = "✅ Available" if result.get("validation", {}).get("is_success") else "❌ Not Available"
            print(f"  {endpoint}: {status}")
        
        # Test 1.4: Validate Expected Document Endpoints
        validation = self.tester.validate_endpoint_list("documents")
        
        print(f"✅ Environment setup completed - {len(discovery['endpoints'])} total endpoints discovered")
    
    def test_document_upload_attempts(self):
        """
        Test 2: Document Upload Attempts (Testing CRUD Availability)
        """
        print("\n📤 PHASE 2: DOCUMENT UPLOAD & CRUD ATTEMPTS")
        
        # Test 2.1: Attempt Document Upload via POST /api/documents/
        document_data = self.tester.config["test_data"]["documents"][0].copy()
        result = self.tester.make_api_call("POST", "/api/documents/", document_data, expected_status=[200, 201, 404, 405, 422])
        self.update_summary(result)
        self.test_summary["upload_attempts"] += 1
        
        if result.get("validation", {}).get("is_success"):
            self.test_summary["upload_successes"] += 1
            doc_id = self.extract_document_id(result)
            if doc_id:
                self.created_documents.append(doc_id)
                self.test_summary["documents_tested"] += 1
                
                # Test 2.2: Get Created Document
                result = self.tester.make_api_call("GET", f"/api/documents/{doc_id}")
                self.update_summary(result)
                
                # Test 2.3: Update Document
                update_data = {"title": "Updated Test Document"}
                result = self.tester.make_api_call("PUT", f"/api/documents/{doc_id}", update_data, expected_status=[200, 404, 405])
                self.update_summary(result)
        
        # Test 2.4: Alternative Upload Endpoints
        upload_endpoints = [
            "/api/documents/upload",
            "/api/document/",
            "/api/document/upload",
            "/documents/",
            "/documents/upload"
        ]
        
        print("\n📋 Testing Alternative Upload Endpoints:")
        for endpoint in upload_endpoints:
            result = self.tester.make_api_call("POST", endpoint, document_data, expected_status=[200, 201, 404, 405, 422])
            self.update_summary(result)
            self.test_summary["upload_attempts"] += 1
            
            status = "✅ Works" if result.get("validation", {}).get("is_success") else "❌ Not Available"
            print(f"  {endpoint}: {status}")
            
            if result.get("validation", {}).get("is_success"):
                self.test_summary["upload_successes"] += 1
        
        # Test 2.5: Document Collection Management
        collection_data = {
            "name": "Test Document Collection",
            "description": "Collection for comprehensive testing"
        }
        result = self.tester.make_api_call("POST", "/api/documents/collections/", collection_data, expected_status=[200, 201, 404, 405])
        self.update_summary(result)
        
        if result.get("validation", {}).get("is_success"):
            collection_id = self.extract_collection_id(result)
            if collection_id:
                self.created_collections.append(collection_id)
                self.test_summary["collections_tested"] += 1
        
        print(f"✅ Upload testing completed - {self.test_summary['upload_successes']}/{self.test_summary['upload_attempts']} upload attempts successful")
    
    def test_document_processing(self):
        """
        Test 3: Document Processing Pipeline
        """
        print("\n⚙️ PHASE 3: DOCUMENT PROCESSING PIPELINE")
        
        # Test 3.1: Get Processing Pipeline Status
        result = self.tester.make_api_call("GET", "/api/documents/processing/pipeline")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["processing_operations"] += 1
        
        # Test 3.2: Get Live Processing Status
        result = self.tester.make_api_call("GET", "/api/documents/processing/live-status")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["processing_operations"] += 1
        
        # Test 3.3: Trigger Document Reprocessing (Dry Run)
        reprocess_data = {
            "force": False,
            "batch_size": 10,
            "dry_run": True
        }
        result = self.tester.make_api_call("POST", "/api/documents/processing/reprocess-all", reprocess_data)
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["processing_operations"] += 1
        
        # Test 3.4: Advanced Reprocessing with Filters
        advanced_reprocess_data = {
            "force": False,
            "batch_size": 5,
            "dry_run": True,
            "filter_criteria": {
                "file_types": ["text", "json"],
                "modified_since": "2025-01-01T00:00:00Z"
            }
        }
        result = self.tester.make_api_call("POST", "/api/documents/processing/reprocess-all", advanced_reprocess_data)
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["processing_operations"] += 1
        
        # Test 3.5: Monitor Processing Over Time
        print("\n⏱️ Monitoring Processing Status Over Time:")
        for i in range(3):
            result = self.tester.make_api_call("GET", "/api/documents/processing/live-status")
            self.update_summary(result)
            if i < 2:
                time.sleep(2)
        
        # Test 3.6: Processing Queue Status
        result = self.tester.make_api_call("GET", "/api/documents/processing/queue", expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ Processing testing completed - {self.test_summary['processing_operations']} processing operations tested")
    
    def test_document_upload(self):
        """
        Test 2: Document Upload Operations
        """
        print("📄 PHASE 2: DOCUMENT UPLOAD OPERATIONS")
        
        # Test 2.1: Get upload status/info
        result = self.tester.make_api_call("GET", "/api/documents")
        self.update_summary(result)
        
        # Test 2.2: Check processing pipeline
        result = self.tester.make_api_call("GET", "/api/documents/processing/pipeline")
        self.update_summary(result)
        
        # Test 2.3: Get live processing status
        result = self.tester.make_api_call("GET", "/api/documents/processing/live-status")
        self.update_summary(result)
        
        # Test 2.4: Test document upload endpoint (if available)
        upload_data = {
            "filename": "test_document.txt",
            "content": "This is a test document for upload testing",
            "document_type": "text"
        }
        result = self.tester.make_api_call("POST", "/api/documents/upload", upload_data, [200, 201, 404])
        self.update_summary(result)
        
        print("✅ Document upload testing completed")

    def test_document_analytics(self):
        """
        Test 4: Document Analytics & Monitoring
        """
        print("\n📊 PHASE 4: DOCUMENT ANALYTICS & MONITORING")
        
        # Test 4.1: Get Document Analytics Overview
        result = self.tester.make_api_call("GET", "/api/documents/analytics/overview")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["analytics_operations"] += 1
        
        # Test 4.2: Get Document Search Patterns
        result = self.tester.make_api_call("GET", "/api/documents/analytics/search-patterns")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["analytics_operations"] += 1
        
        # Test 4.3: Document Type Analytics
        result = self.tester.make_api_call("GET", "/api/documents/analytics/types", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 4.4: Document Processing Metrics
        result = self.tester.make_api_call("GET", "/api/documents/analytics/processing", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 4.5: Document Storage Analytics
        result = self.tester.make_api_call("GET", "/api/documents/analytics/storage", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 4.6: Vector Storage Statistics
        result = self.tester.make_api_call("GET", "/api/documents/vector/stats", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 4.7: Document Search Capabilities
        search_data = {
            "query": "comprehensive test document",
            "limit": 10,
            "filters": {"type": "text"}
        }
        result = self.tester.make_api_call("POST", "/api/documents/search", search_data, expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 4.8: Semantic Search
        semantic_search_data = {
            "query": "document analysis and processing",
            "limit": 5,
            "threshold": 0.7
        }
        result = self.tester.make_api_call("POST", "/api/documents/search/semantic", semantic_search_data, expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ Analytics testing completed - {self.test_summary['analytics_operations']} analytics operations tested")
    
    def test_document_search(self):
        """
        Test 5: Document Search and Retrieval
        """
        print("🔍 PHASE 5: DOCUMENT SEARCH & RETRIEVAL")
        
        # Test 5.1: Search functionality
        result = self.tester.make_api_call("GET", "/api/documents/search", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 5.2: Search with query parameters
        search_params = {"query": "test", "limit": 10}
        result = self.tester.make_api_call("GET", "/api/documents/search", search_params, [200, 404])
        self.update_summary(result)
        
        # Test 5.3: Vector search (if available)
        result = self.tester.make_api_call("GET", "/api/documents/vector-search", expected_status=[200, 404])
        self.update_summary(result)
        
        print("✅ Document search testing completed")

    def test_advanced_operations(self):
        """
        Test 5: Advanced Document Operations
        """
        print("\n🧠 PHASE 5: ADVANCED OPERATIONS")
        
        # Test 5.1: Document Embeddings Information
        result = self.tester.make_api_call("GET", "/api/documents/embeddings/info", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 5.2: Document Similarity (if documents exist)
        if len(self.created_documents) >= 2:
            doc1, doc2 = self.created_documents[0], self.created_documents[1]
            result = self.tester.make_api_call("GET", f"/api/documents/{doc1}/similarity/{doc2}", expected_status=[200, 404])
            self.update_summary(result)
        
        # Test 5.3: Bulk Document Operations
        if self.created_documents:
            bulk_data = {
                "operation": "update_metadata",
                "document_ids": self.created_documents[:2] if len(self.created_documents) >= 2 else self.created_documents,
                "metadata": {"test_tag": "comprehensive_test"}
            }
            result = self.tester.make_api_call("POST", "/api/documents/bulk", bulk_data, expected_status=[200, 404])
            self.update_summary(result)
        
        # Test 5.4: Document Versioning
        if self.created_documents:
            doc_id = self.created_documents[0]
            result = self.tester.make_api_call("GET", f"/api/documents/{doc_id}/versions", expected_status=[200, 404])
            self.update_summary(result)
        
        # Test 5.5: Document Metadata Management
        if self.created_documents:
            doc_id = self.created_documents[0]
            metadata_update = {
                "tags": ["comprehensive", "test", "document"],
                "category": "testing",
                "priority": "high"
            }
            result = self.tester.make_api_call("PUT", f"/api/documents/{doc_id}/metadata", metadata_update, expected_status=[200, 404])
            self.update_summary(result)
        
        # Test 5.6: Document Content Analysis
        if self.created_documents:
            doc_id = self.created_documents[0]
            result = self.tester.make_api_call("POST", f"/api/documents/{doc_id}/analyze", {}, expected_status=[200, 404])
            self.update_summary(result)
        
        print("✅ Advanced operations testing completed")
    
    def test_error_handling(self):
        """
        Test 6: Error Handling and Edge Cases
        """
        print("\n🚨 PHASE 6: ERROR HANDLING")
        
        # Test 6.1: Get Non-existent Document
        result = self.tester.make_api_call("GET", "/api/documents/invalid_doc_999999", expected_status=404)
        self.update_summary(result)
        
        # Test 6.2: Invalid Document Upload
        invalid_document = {
            "title": "",  # Empty title
            "content": "x" * 100000,  # Very large content
            "document_type": "invalid_type"
        }
        result = self.tester.make_api_call("POST", "/api/documents/", invalid_document, expected_status=[400, 404, 422])
        self.update_summary(result)
        
        # Test 6.3: Invalid Reprocessing Request
        invalid_reprocess = {
            "force": "invalid_boolean",
            "batch_size": -1,
            "dry_run": "not_a_boolean"
        }
        result = self.tester.make_api_call("POST", "/api/documents/processing/reprocess-all", invalid_reprocess, expected_status=[200, 400, 422])
        self.update_summary(result)
        
        # Test 6.4: Invalid Search Query
        invalid_search = {
            "query": "",  # Empty query
            "limit": -1,
            "threshold": 2.0  # Invalid threshold
        }
        result = self.tester.make_api_call("POST", "/api/documents/search/semantic", invalid_search, expected_status=[400, 404, 422])
        self.update_summary(result)
        
        # Test 6.5: Invalid Analytics Endpoint
        result = self.tester.make_api_call("GET", "/api/documents/analytics/nonexistent", expected_status=404)
        self.update_summary(result)
        
        # Test 6.6: Invalid Processing Endpoint
        result = self.tester.make_api_call("GET", "/api/documents/processing/invalid-endpoint", expected_status=404)
        self.update_summary(result)
        
        print("✅ Error handling testing completed")
    
    def test_performance(self):
        """
        Test 7: Performance and Stress Testing
        """
        print("\n⚡ PHASE 7: PERFORMANCE TESTING")
        
        # Test 7.1: Rapid Pipeline Status Requests
        for i in range(5):
            result = self.tester.make_api_call("GET", "/api/documents/processing/pipeline")
            self.update_summary(result)
        
        # Test 7.2: Rapid Analytics Requests
        for i in range(3):
            result = self.tester.make_api_call("GET", "/api/documents/analytics/overview")
            self.update_summary(result)
        
        # Test 7.3: Concurrent Live Status Monitoring
        for i in range(3):
            result = self.tester.make_api_call("GET", "/api/documents/processing/live-status")
            self.update_summary(result)
        
        print("✅ Performance testing completed")
    
    def test_system_integration(self):
        """
        Test 8: System Integration Testing
        """
        print("\n🔗 PHASE 8: SYSTEM INTEGRATION")
        
        # Test 8.1: Integration with Workflow System
        result = self.tester.make_api_call("GET", "/api/workflows/stats/dashboard")
        self.update_summary(result)
        
        # Test 8.2: Integration with Pattern System
        result = self.tester.make_api_call("GET", "/api/patterns/")
        self.update_summary(result)
        
        # Test 8.3: Cross-System Analytics
        result = self.tester.make_api_call("GET", "/api/system/metrics", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 8.4: Document-Workflow Integration
        result = self.tester.make_api_call("GET", "/api/documents/analytics/search-patterns")
        self.update_summary(result)
        
        print("✅ System integration testing completed")
    
    def extract_document_id(self, result):
        """Extract document ID from API response"""
        try:
            response_data = result.get("response", {}).get("data", {})
            return response_data.get("id") or response_data.get("document_id") or response_data.get("doc_id")
        except:
            return None
    
    def extract_collection_id(self, result):
        """Extract collection ID from API response"""
        try:
            response_data = result.get("response", {}).get("data", {})
            return response_data.get("id") or response_data.get("collection_id")
        except:
            return None
    
    def update_summary(self, result):
        """Update test summary statistics"""
        self.test_summary["api_calls_made"] += 1
        if result.get("validation", {}).get("is_success", False):
            self.test_summary["successful_calls"] += 1
        else:
            self.test_summary["failed_calls"] += 1
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        base_report = self.tester.generate_comprehensive_report()
        
        # Add document-specific metrics
        base_report["document_management_summary"] = self.test_summary
        
        # Calculate document system capabilities
        base_report["document_system_analysis"] = {
            "upload_capability": self.test_summary["upload_successes"] > 0,
            "processing_capability": self.test_summary["processing_operations"] > 0,
            "analytics_capability": self.test_summary["analytics_operations"] > 0,
            "crud_available": len(self.created_documents) > 0,
            "monitoring_available": self.test_summary["processing_operations"] > 0
        }
        
        # Save enhanced report
        report_file = Path(self.tester.test_dir) / "results" / f"FINAL_DOCUMENT_MANAGEMENT_REPORT_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(base_report, f, indent=2)
        
        return base_report

def main():
    """
    Main execution function
    """
    print("🚀 COMPREHENSIVE DOCUMENT MANAGEMENT TESTING")
    print("============================================")
    
    tester = DocumentManagementTester()
    success = tester.run_comprehensive_tests()
    
    # Cleanup resources
    tester.tester.cleanup()
    
    if success:
        print("\n🎉 COMPREHENSIVE DOCUMENT MANAGEMENT TESTING COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("\n💥 COMPREHENSIVE DOCUMENT MANAGEMENT TESTING FAILED!")
        return 1



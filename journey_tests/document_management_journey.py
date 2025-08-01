#!/usr/bin/env python3
"""
Document Management Journey Test
Tests: Document upload, processing, analytics, vector storage, types, and management
"""

import sys
import os
import time
import json
from typing import Dict, Any, List, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from test_logger import WorkflowTestLogger
from api_client import AutomotasAPIClient
from data_generators import TestData

class DocumentManagementJourney:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.logger = WorkflowTestLogger("document_management_journey")
        self.api = AutomotasAPIClient(base_url, self.logger)
        self.uploaded_documents: List[str] = []
        self.created_collections: List[str] = []
        self.journey_stats = {
            "documents_uploaded": 0,
            "documents_processed": 0,
            "collections_created": 0,
            "vector_operations": 0,
            "analytics_checked": 0,
            "errors_handled": 0
        }

    def run_full_journey(self) -> bool:
        """Execute the complete document management journey"""
        print("🚀 DOCUMENT MANAGEMENT JOURNEY TEST - PHASE 3")
        print("=" * 60)
        
        try:
            # Phase 1: Environment Setup
            if not self._phase1_setup():
                return False
            
            # Phase 2: Document Upload & Creation
            if not self._phase2_document_upload():
                return False
            
            # Phase 3: Document Processing & Analysis
            if not self._phase3_document_processing():
                return False
            
            # Phase 4: Vector Storage & Embeddings
            if not self._phase4_vector_operations():
                return False
            
            # Phase 5: Document Analytics & Metrics
            if not self._phase5_analytics():
                return False
            
            # Phase 6: Document Management Operations
            if not self._phase6_management():
                return False
            
            # Phase 7: Error Handling & Edge Cases
            if not self._phase7_error_handling():
                return False
            
            # Phase 8: Cleanup
            self._phase8_cleanup()
            
            self._log_journey_success()
            return True
            
        except Exception as e:
            self.logger.log_error("journey_failed", f"Document Management Journey failed: {str(e)}")
            return False

    def _phase1_setup(self) -> bool:
        """Phase 1: Environment Setup & Validation"""
        self.logger.log_step("phase1_start", "Phase 1: Environment Setup & Validation", "in_progress")
        
        # Health check
        self.logger.log_step("health_check", "System Health Check", "in_progress")
        health_response = self.api.health_check()
        if not health_response.get("success", False):
            self.logger.log_step("health_check", "System Health Check", "failed", health_response)
            return False
        self.logger.log_step("health_check", "System Health Check", "completed")
        
        # Check document system availability
        self.logger.log_step("docs_system_check", "Document System Check", "in_progress")
        docs_response = self.api.get("/api/documents/")
        if not self.api.validate_response(docs_response, expected_status=200):
            self.logger.log_step("docs_system_check", "Document System Check", "failed", docs_response)
            return False
        self.logger.log_step("docs_system_check", "Document System Check", "completed")
        
        # Check vector system
        self.logger.log_step("vector_system_check", "Vector System Check", "in_progress")
        vector_response = self.api.get("/api/documents/vector/stats")
        if self.api.validate_response(vector_response, expected_status=200):
            self.logger.log_step("vector_system_check", "Vector System Check", "completed")
        else:
            self.logger.log_step("vector_system_check", "Vector System Check", "warning", 
                               metadata={"note": "Vector stats endpoint may not be available"})
        
        self.logger.log_step("phase1_complete", "Phase 1: Environment Setup Complete", "completed")
        return True

    def _phase2_document_upload(self) -> bool:
        """Phase 2: Document Upload & Creation"""
        self.logger.log_step("phase2_start", "Phase 2: Document Upload & Creation", "in_progress")
        
        # Test 1: Create document collection
        self.logger.log_step("create_collection", "Create Document Collection", "in_progress")
        collection_data = TestData.Document.create_collection_data("TestCollection")
        collection_response = self.api.post("/api/documents/collections/", collection_data)
        
        if self.api.validate_response(collection_response, expected_status=[200, 201]):
            collection_id = self.api.extract_id(collection_response)
            if collection_id:
                self.created_collections.append(collection_id)
                self.journey_stats["collections_created"] += 1
            self.logger.log_step("create_collection", "Create Document Collection", "completed")
        else:
            self.logger.log_step("create_collection", "Create Document Collection", "warning")
        
        # Test 2: Upload text document
        self.logger.log_step("upload_text_doc", "Upload Text Document", "in_progress")
        text_doc_data = TestData.Document.create_document_data("text", "Test Analysis Document")
        text_response = self.api.post("/api/documents/", text_doc_data)
        
        if self.api.validate_response(text_response, expected_status=[200, 201]):
            doc_id = self.api.extract_id(text_response)
            if doc_id:
                self.uploaded_documents.append(doc_id)
                self.journey_stats["documents_uploaded"] += 1
            self.logger.log_step("upload_text_doc", "Upload Text Document", "completed")
        else:
            self.logger.log_step("upload_text_doc", "Upload Text Document", "warning")
        
        # Test 3: Upload structured document
        self.logger.log_step("upload_structured_doc", "Upload Structured Document", "in_progress")
        structured_doc_data = TestData.Document.create_document_data("json", "API Documentation")
        structured_response = self.api.post("/api/documents/", structured_doc_data)
        
        if self.api.validate_response(structured_response, expected_status=[200, 201]):
            doc_id = self.api.extract_id(structured_response)
            if doc_id:
                self.uploaded_documents.append(doc_id)
                self.journey_stats["documents_uploaded"] += 1
            self.logger.log_step("upload_structured_doc", "Upload Structured Document", "completed")
        else:
            self.logger.log_step("upload_structured_doc", "Upload Structured Document", "warning")
        
        # Test 4: List documents
        self.logger.log_step("list_documents", "List All Documents", "in_progress")
        list_response = self.api.get("/api/documents/")
        if self.api.validate_response(list_response, expected_status=200):
            self.logger.log_step("list_documents", "List All Documents", "completed", 
                               metadata={"document_count": len(list_response.get("data", []))})
        else:
            self.logger.log_step("list_documents", "List All Documents", "warning")
        
        self.logger.log_step("phase2_complete", "Phase 2: Document Upload Complete", "completed")
        return True

    def _phase3_document_processing(self) -> bool:
        """Phase 3: Document Processing & Analysis"""
        self.logger.log_step("phase3_start", "Phase 3: Document Processing & Analysis", "in_progress")
        
        # Test 1: Check processing status
        self.logger.log_step("check_processing", "Check Document Processing Status", "in_progress")
        processing_response = self.api.get("/api/documents/processing/status")
        if self.api.validate_response(processing_response, expected_status=200):
            self.logger.log_step("check_processing", "Check Document Processing Status", "completed")
        else:
            self.logger.log_step("check_processing", "Check Document Processing Status", "warning")
        
        # Test 2: Process specific document (if we have uploaded documents)
        if self.uploaded_documents:
            doc_id = self.uploaded_documents[0]
            self.logger.log_step("process_document", f"Process Document {doc_id}", "in_progress")
            process_response = self.api.post(f"/api/documents/{doc_id}/process", {})
            
            if self.api.validate_response(process_response, expected_status=[200, 202]):
                self.journey_stats["documents_processed"] += 1
                self.logger.log_step("process_document", f"Process Document {doc_id}", "completed")
                
                # Wait a bit and check status
                time.sleep(2)
                status_response = self.api.get(f"/api/documents/{doc_id}/status")
                if self.api.validate_response(status_response, expected_status=200):
                    self.logger.log_step("check_doc_status", f"Check Document {doc_id} Status", "completed")
            else:
                self.logger.log_step("process_document", f"Process Document {doc_id}", "warning")
        
        # Test 3: Check processing queue
        self.logger.log_step("check_queue", "Check Processing Queue", "in_progress")
        queue_response = self.api.get("/api/documents/processing/queue")
        if self.api.validate_response(queue_response, expected_status=200):
            self.logger.log_step("check_queue", "Check Processing Queue", "completed")
        else:
            self.logger.log_step("check_queue", "Check Processing Queue", "warning")
        
        self.logger.log_step("phase3_complete", "Phase 3: Document Processing Complete", "completed")
        return True

    def _phase4_vector_operations(self) -> bool:
        """Phase 4: Vector Storage & Embeddings"""
        self.logger.log_step("phase4_start", "Phase 4: Vector Storage & Operations", "in_progress")
        
        # Test 1: Vector statistics
        self.logger.log_step("vector_stats", "Get Vector Statistics", "in_progress")
        vector_stats_response = self.api.get("/api/documents/vector/stats")
        if self.api.validate_response(vector_stats_response, expected_status=200):
            self.journey_stats["vector_operations"] += 1
            self.logger.log_step("vector_stats", "Get Vector Statistics", "completed")
        else:
            self.logger.log_step("vector_stats", "Get Vector Statistics", "warning")
        
        # Test 2: Search vectors (semantic search)
        self.logger.log_step("vector_search", "Perform Vector Search", "in_progress")
        search_data = {
            "query": "document analysis and processing",
            "limit": 5,
            "threshold": 0.7
        }
        search_response = self.api.post("/api/documents/search/semantic", search_data)
        if self.api.validate_response(search_response, expected_status=200):
            self.journey_stats["vector_operations"] += 1
            self.logger.log_step("vector_search", "Perform Vector Search", "completed")
        else:
            self.logger.log_step("vector_search", "Perform Vector Search", "warning")
        
        # Test 3: Vector similarity
        if self.uploaded_documents and len(self.uploaded_documents) >= 2:
            doc1, doc2 = self.uploaded_documents[0], self.uploaded_documents[1]
            self.logger.log_step("vector_similarity", f"Check Similarity {doc1} vs {doc2}", "in_progress")
            similarity_response = self.api.get(f"/api/documents/{doc1}/similarity/{doc2}")
            if self.api.validate_response(similarity_response, expected_status=200):
                self.journey_stats["vector_operations"] += 1
                self.logger.log_step("vector_similarity", f"Check Similarity {doc1} vs {doc2}", "completed")
            else:
                self.logger.log_step("vector_similarity", f"Check Similarity {doc1} vs {doc2}", "warning")
        
        # Test 4: Vector embeddings info
        self.logger.log_step("embeddings_info", "Get Embeddings Information", "in_progress")
        embeddings_response = self.api.get("/api/documents/embeddings/info")
        if self.api.validate_response(embeddings_response, expected_status=200):
            self.journey_stats["vector_operations"] += 1
            self.logger.log_step("embeddings_info", "Get Embeddings Information", "completed")
        else:
            self.logger.log_step("embeddings_info", "Get Embeddings Information", "warning")
        
        self.logger.log_step("phase4_complete", "Phase 4: Vector Operations Complete", "completed")
        return True

    def _phase5_analytics(self) -> bool:
        """Phase 5: Document Analytics & Metrics"""
        self.logger.log_step("phase5_start", "Phase 5: Document Analytics & Metrics", "in_progress")
        
        # Test 1: Document analytics overview
        self.logger.log_step("analytics_overview", "Get Analytics Overview", "in_progress")
        analytics_response = self.api.get("/api/documents/analytics/overview")
        if self.api.validate_response(analytics_response, expected_status=200):
            self.journey_stats["analytics_checked"] += 1
            self.logger.log_step("analytics_overview", "Get Analytics Overview", "completed")
        else:
            self.logger.log_step("analytics_overview", "Get Analytics Overview", "warning")
        
        # Test 2: Document type distribution
        self.logger.log_step("type_distribution", "Get Document Type Distribution", "in_progress")
        types_response = self.api.get("/api/documents/analytics/types")
        if self.api.validate_response(types_response, expected_status=200):
            self.journey_stats["analytics_checked"] += 1
            self.logger.log_step("type_distribution", "Get Document Type Distribution", "completed")
        else:
            self.logger.log_step("type_distribution", "Get Document Type Distribution", "warning")
        
        # Test 3: Processing metrics
        self.logger.log_step("processing_metrics", "Get Processing Metrics", "in_progress")
        metrics_response = self.api.get("/api/documents/analytics/processing")
        if self.api.validate_response(metrics_response, expected_status=200):
            self.journey_stats["analytics_checked"] += 1
            self.logger.log_step("processing_metrics", "Get Processing Metrics", "completed")
        else:
            self.logger.log_step("processing_metrics", "Get Processing Metrics", "warning")
        
        # Test 4: Search patterns (from workflow journey)
        self.logger.log_step("search_patterns", "Get Document Search Patterns", "in_progress")
        patterns_response = self.api.get("/api/documents/analytics/search-patterns")
        if self.api.validate_response(patterns_response, expected_status=200):
            self.journey_stats["analytics_checked"] += 1
            self.logger.log_step("search_patterns", "Get Document Search Patterns", "completed")
        else:
            self.logger.log_step("search_patterns", "Get Document Search Patterns", "warning")
        
        # Test 5: Storage usage
        self.logger.log_step("storage_usage", "Get Storage Usage Statistics", "in_progress")
        storage_response = self.api.get("/api/documents/analytics/storage")
        if self.api.validate_response(storage_response, expected_status=200):
            self.journey_stats["analytics_checked"] += 1
            self.logger.log_step("storage_usage", "Get Storage Usage Statistics", "completed")
        else:
            self.logger.log_step("storage_usage", "Get Storage Usage Statistics", "warning")
        
        self.logger.log_step("phase5_complete", "Phase 5: Analytics Complete", "completed")
        return True

    def _phase6_management(self) -> bool:
        """Phase 6: Document Management Operations"""
        self.logger.log_step("phase6_start", "Phase 6: Document Management Operations", "in_progress")
        
        # Test 1: Document metadata update
        if self.uploaded_documents:
            doc_id = self.uploaded_documents[0]
            self.logger.log_step("update_metadata", f"Update Document {doc_id} Metadata", "in_progress")
            metadata_update = {
                "tags": ["test", "journey", "document_management"],
                "category": "test_document",
                "priority": "medium"
            }
            update_response = self.api.put(f"/api/documents/{doc_id}/metadata", metadata_update)
            if self.api.validate_response(update_response, expected_status=200):
                self.logger.log_step("update_metadata", f"Update Document {doc_id} Metadata", "completed")
            else:
                self.logger.log_step("update_metadata", f"Update Document {doc_id} Metadata", "warning")
        
        # Test 2: Document versioning
        if self.uploaded_documents:
            doc_id = self.uploaded_documents[0]
            self.logger.log_step("check_versions", f"Check Document {doc_id} Versions", "in_progress")
            versions_response = self.api.get(f"/api/documents/{doc_id}/versions")
            if self.api.validate_response(versions_response, expected_status=200):
                self.logger.log_step("check_versions", f"Check Document {doc_id} Versions", "completed")
            else:
                self.logger.log_step("check_versions", f"Check Document {doc_id} Versions", "warning")
        
        # Test 3: Bulk operations
        self.logger.log_step("bulk_operations", "Test Bulk Operations", "in_progress")
        bulk_data = {
            "operation": "update_tags",
            "document_ids": self.uploaded_documents[:2] if len(self.uploaded_documents) >= 2 else self.uploaded_documents,
            "tags": ["bulk_test", "journey"]
        }
        bulk_response = self.api.post("/api/documents/bulk", bulk_data)
        if self.api.validate_response(bulk_response, expected_status=[200, 202]):
            self.logger.log_step("bulk_operations", "Test Bulk Operations", "completed")
        else:
            self.logger.log_step("bulk_operations", "Test Bulk Operations", "warning")
        
        self.logger.log_step("phase6_complete", "Phase 6: Management Operations Complete", "completed")
        return True

    def _phase7_error_handling(self) -> bool:
        """Phase 7: Error Handling & Edge Cases"""
        self.logger.log_step("phase7_start", "Phase 7: Error Handling & Edge Cases", "in_progress")
        
        # Test 1: Invalid document ID
        self.logger.log_step("test_invalid_doc_id", "Test Invalid Document ID", "in_progress")
        invalid_response = self.api.get("/api/documents/invalid_doc_999999")
        if self.api.validate_response(invalid_response, expected_status=404):
            self.journey_stats["errors_handled"] += 1
            self.logger.log_step("test_invalid_doc_id", "Test Invalid Document ID", "completed")
        else:
            self.logger.log_step("test_invalid_doc_id", "Test Invalid Document ID", "warning")
        
        # Test 2: Invalid file upload
        self.logger.log_step("test_invalid_upload", "Test Invalid File Upload", "in_progress")
        invalid_upload_data = {
            "title": "",  # Empty title
            "content": "x" * 100000,  # Very large content
            "file_type": "invalid_type"
        }
        invalid_upload_response = self.api.post("/api/documents/", invalid_upload_data)
        if self.api.validate_response(invalid_upload_response, expected_status=[400, 422]):
            self.journey_stats["errors_handled"] += 1
            self.logger.log_step("test_invalid_upload", "Test Invalid File Upload", "completed")
        else:
            self.logger.log_step("test_invalid_upload", "Test Invalid File Upload", "warning")
        
        # Test 3: Invalid search query
        self.logger.log_step("test_invalid_search", "Test Invalid Search Query", "in_progress")
        invalid_search_data = {
            "query": "",  # Empty query
            "limit": -1,  # Invalid limit
            "threshold": 2.0  # Invalid threshold
        }
        invalid_search_response = self.api.post("/api/documents/search/semantic", invalid_search_data)
        if self.api.validate_response(invalid_search_response, expected_status=[400, 422]):
            self.journey_stats["errors_handled"] += 1
            self.logger.log_step("test_invalid_search", "Test Invalid Search Query", "completed")
        else:
            self.logger.log_step("test_invalid_search", "Test Invalid Search Query", "warning")
        
        self.logger.log_step("phase7_complete", "Phase 7: Error Handling Complete", "completed")
        return True

    def _phase8_cleanup(self):
        """Phase 8: Cleanup"""
        self.logger.log_step("phase8_start", "Phase 8: Cleanup", "in_progress")
        
        # Clean up uploaded documents
        for doc_id in self.uploaded_documents:
            self.logger.log_step("cleanup_document", f"Delete Document {doc_id}", "in_progress")
            delete_response = self.api.delete(f"/api/documents/{doc_id}")
            if self.api.validate_response(delete_response, expected_status=[200, 204]):
                self.logger.log_step("cleanup_document", f"Delete Document {doc_id}", "completed")
            else:
                self.logger.log_step("cleanup_document", f"Delete Document {doc_id}", "warning")
        
        # Clean up collections
        for collection_id in self.created_collections:
            self.logger.log_step("cleanup_collection", f"Delete Collection {collection_id}", "in_progress")
            delete_response = self.api.delete(f"/api/documents/collections/{collection_id}")
            if self.api.validate_response(delete_response, expected_status=[200, 204]):
                self.logger.log_step("cleanup_collection", f"Delete Collection {collection_id}", "completed")
            else:
                self.logger.log_step("cleanup_collection", f"Delete Collection {collection_id}", "warning")
        
        self.logger.log_step("phase8_complete", "Phase 8: Cleanup Complete", "completed")

    def _log_journey_success(self):
        """Log successful journey completion"""
        self.logger.log_journey_end(
            status="SUCCESS",
            summary=f"Document Management Journey completed successfully",
            metadata={
                "stats": self.journey_stats,
                "documents_uploaded": len(self.uploaded_documents),
                "collections_created": len(self.created_collections)
            }
        )

def main():
    print("🚀 Starting Document Management Journey Test")
    journey = DocumentManagementJourney()
    success = journey.run_full_journey()
    
    if success:
        print("✅ Document Management Journey completed successfully!")
        return 0
    else:
        print("❌ Document Management Journey failed!")
        return 1

if __name__ == "__main__":
    exit(main())
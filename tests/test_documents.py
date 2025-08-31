"""
Document Management Testing Module
==================================

Comprehensive testing for document upload, processing, retrieval,
and analytics functionality.
"""

import asyncio
import json
import os
from typing import Dict, Any, List
from pathlib import Path
import base64
import io

from framework.base_test import APITest, TestLevel


class TestDocuments(APITest):
    """Test suite for document management functionality"""
    
    def __init__(self):
        super().__init__("Documents")
        self.test_level = TestLevel.FUNCTIONAL
        self.test_documents = []
        self.test_files_dir = Path(__file__).parent.parent / "test_data" / "documents"
        
    async def setup(self):
        """Setup test environment"""
        await self.setup_session()
        print("🔧 Setting up Document tests...")
        
        # Create test data directory if it doesn't exist
        self.test_files_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sample test files
        await self._create_test_files()
        
    async def cleanup(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up Document tests...")
        
        # Delete all test documents
        for doc_id in self.test_documents:
            try:
                await self.make_request("DELETE", f"/api/documents/{doc_id}")
            except:
                pass
                
        await self.cleanup_session()
        
    async def _create_test_files(self):
        """Create sample files for testing"""
        # Create a test text file
        test_txt = self.test_files_dir / "test_document.txt"
        test_txt.write_text("""This is a test document for the Automatos AI platform.
It contains multiple lines of text to test document processing.
The document should be properly chunked and indexed.
Keywords: AI, automation, testing, document processing.""")
        
        # Create a test JSON file
        test_json = self.test_files_dir / "test_config.json"
        test_json.write_text(json.dumps({
            "name": "Test Configuration",
            "version": "1.0",
            "settings": {
                "processing": "enabled",
                "chunking": True,
                "embedding_model": "sentence-transformers"
            }
        }, indent=2))
        
        # Create a test CSV file
        test_csv = self.test_files_dir / "test_data.csv"
        test_csv.write_text("""id,name,value,category
1,Item One,100,A
2,Item Two,200,B
3,Item Three,300,A
4,Item Four,400,C""")
        
    # Document Upload Tests
    async def test_upload_text_document(self):
        """Test uploading a text document"""
        test_file = self.test_files_dir / "test_document.txt"
        
        with open(test_file, 'rb') as f:
            file_content = f.read()
            
        files = {
            'file': ('test_document.txt', file_content, 'text/plain')
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={
                'title': 'Test Document',
                'description': 'A test document for automated testing',
                'tags': json.dumps(['test', 'automation'])
            }
        )
        
        assert response["status_code"] == 200, f"Document upload failed: {response}"
        result = response["json"]
        
        assert "document_id" in result
        assert result["status"] == "processing" or result["status"] == "completed"
        assert result["title"] == "Test Document"
        
        self.test_documents.append(result["document_id"])
        
        return result["document_id"]
        
    async def test_upload_json_document(self):
        """Test uploading a JSON document"""
        test_file = self.test_files_dir / "test_config.json"
        
        with open(test_file, 'rb') as f:
            file_content = f.read()
            
        files = {
            'file': ('test_config.json', file_content, 'application/json')
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={
                'title': 'Test Configuration',
                'description': 'JSON configuration file'
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        self.test_documents.append(result["document_id"])
        
    async def test_upload_csv_document(self):
        """Test uploading a CSV document"""
        test_file = self.test_files_dir / "test_data.csv"
        
        with open(test_file, 'rb') as f:
            file_content = f.read()
            
        files = {
            'file': ('test_data.csv', file_content, 'text/csv')
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={
                'title': 'Test Data',
                'description': 'CSV data file',
                'process_as_structured': 'true'
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        self.test_documents.append(result["document_id"])
        
    async def test_upload_large_document(self):
        """Test uploading a large document"""
        # Create a large text file (5MB)
        large_content = "This is a test line.\n" * 250000  # ~5MB
        
        files = {
            'file': ('large_document.txt', large_content.encode(), 'text/plain')
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={
                'title': 'Large Test Document',
                'description': 'Testing large file handling'
            }
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        self.test_documents.append(result["document_id"])
        
    async def test_upload_invalid_file_type(self):
        """Test uploading an unsupported file type"""
        files = {
            'file': ('test.exe', b'MZ\x90\x00', 'application/x-msdownload')
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={'title': 'Invalid File'}
        )
        
        assert response["status_code"] in [400, 415], "Should reject invalid file types"
        
    # Document Retrieval Tests
    async def test_list_documents(self):
        """Test listing documents with pagination"""
        # First upload a document
        doc_id = await self.test_upload_text_document()
        
        # List documents
        response = await self.make_request(
            "GET",
            "/api/documents/",
            params={
                'skip': 0,
                'limit': 10,
                'status': 'all'
            }
        )
        
        assert response["status_code"] == 200
        documents = response["json"]
        
        assert isinstance(documents, list)
        assert len(documents) > 0
        
        # Verify our document is in the list
        doc_ids = [doc["id"] for doc in documents]
        assert doc_id in doc_ids
        
    async def test_get_document_by_id(self):
        """Test retrieving a specific document"""
        # Upload a document first
        doc_id = await self.test_upload_text_document()
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Get document details
        response = await self.make_request(
            "GET",
            f"/api/documents/{doc_id}"
        )
        
        assert response["status_code"] == 200
        document = response["json"]
        
        assert document["id"] == doc_id
        assert document["title"] == "Test Document"
        assert "chunks" in document or "content" in document
        assert "metadata" in document
        
    async def test_get_document_content(self):
        """Test retrieving document content"""
        # Upload a document
        doc_id = await self.test_upload_text_document()
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Get document content
        response = await self.make_request(
            "GET",
            f"/api/documents/{doc_id}/content"
        )
        
        assert response["status_code"] == 200
        content = response["json"]
        
        assert "content" in content or "chunks" in content
        if "content" in content:
            assert "test document" in content["content"].lower()
            
    async def test_get_nonexistent_document(self):
        """Test retrieving a document that doesn't exist"""
        response = await self.make_request(
            "GET",
            "/api/documents/99999"
        )
        
        assert response["status_code"] == 404
        
    # Document Processing Tests
    async def test_reprocess_document(self):
        """Test reprocessing a document"""
        # Upload a document
        doc_id = await self.test_upload_text_document()
        
        # Wait for initial processing
        await asyncio.sleep(2)
        
        # Reprocess the document
        response = await self.make_request(
            "POST",
            f"/api/documents/{doc_id}/reprocess"
        )
        
        assert response["status_code"] == 200
        result = response["json"]
        
        assert result["status"] == "reprocessing"
        assert result["message"]
        
    async def test_document_processing_pipeline(self):
        """Test document processing pipeline status"""
        response = await self.make_request(
            "GET",
            "/api/documents/processing/pipeline"
        )
        
        if response["status_code"] == 200:
            pipeline = response["json"]
            assert "stages" in pipeline
            assert "chunking" in pipeline["stages"]
            assert "embedding" in pipeline["stages"]
            
    async def test_document_processing_live_status(self):
        """Test live processing status"""
        # Upload a document
        doc_id = await self.test_upload_text_document()
        
        # Check live status
        response = await self.make_request(
            "GET",
            "/api/documents/processing/live-status",
            params={'document_id': doc_id}
        )
        
        if response["status_code"] == 200:
            status = response["json"]
            assert "processing_stage" in status
            assert "progress" in status
            
    # Document Search and Analytics Tests
    async def test_document_search(self):
        """Test document search functionality"""
        # Upload documents first
        await self.test_upload_text_document()
        await asyncio.sleep(2)
        
        # Search documents
        response = await self.make_request(
            "GET",
            "/api/documents/",
            params={
                'search': 'test',
                'limit': 10
            }
        )
        
        assert response["status_code"] == 200
        results = response["json"]
        assert len(results) > 0
        
    async def test_document_analytics_overview(self):
        """Test document analytics overview"""
        response = await self.make_request(
            "GET",
            "/api/documents/analytics/overview"
        )
        
        if response["status_code"] == 200:
            analytics = response["json"]
            assert "total_documents" in analytics
            assert "documents_by_type" in analytics
            assert "processing_stats" in analytics
            assert "storage_usage" in analytics
            
    async def test_document_search_patterns(self):
        """Test search pattern analytics"""
        response = await self.make_request(
            "GET",
            "/api/documents/analytics/search-patterns"
        )
        
        if response["status_code"] == 200:
            patterns = response["json"]
            assert "popular_searches" in patterns
            assert "search_frequency" in patterns
            
    # Document Management Tests
    async def test_delete_document(self):
        """Test document deletion"""
        # Upload a document
        doc_id = await self.test_upload_text_document()
        
        # Delete the document
        response = await self.make_request(
            "DELETE",
            f"/api/documents/{doc_id}"
        )
        
        assert response["status_code"] in [200, 204]
        
        # Verify it's deleted
        response = await self.make_request(
            "GET",
            f"/api/documents/{doc_id}"
        )
        
        assert response["status_code"] == 404
        
    async def test_bulk_document_operations(self):
        """Test bulk document operations"""
        # Upload multiple documents
        doc_ids = []
        for i in range(3):
            files = {
                'file': (f'bulk_test_{i}.txt', f'Bulk test content {i}'.encode(), 'text/plain')
            }
            response = await self.make_request(
                "POST",
                "/api/documents/upload",
                files=files,
                data={'title': f'Bulk Test {i}'}
            )
            if response["status_code"] == 200:
                doc_ids.append(response["json"]["document_id"])
                self.test_documents.append(response["json"]["document_id"])
                
        # Test bulk reprocessing
        if doc_ids:
            response = await self.make_request(
                "POST",
                "/api/documents/processing/reprocess-all",
                json={'document_ids': doc_ids}
            )
            
            if response["status_code"] == 200:
                result = response["json"]
                assert "processed" in result
                assert result["processed"] == len(doc_ids)
                
    # Edge Cases and Error Handling
    async def test_concurrent_document_uploads(self):
        """Test handling concurrent document uploads"""
        upload_tasks = []
        
        for i in range(5):
            files = {
                'file': (f'concurrent_{i}.txt', f'Concurrent content {i}'.encode(), 'text/plain')
            }
            task = self.make_request(
                "POST",
                "/api/documents/upload",
                files=files,
                data={'title': f'Concurrent {i}'}
            )
            upload_tasks.append(task)
            
        # Execute all uploads concurrently
        responses = await asyncio.gather(*upload_tasks, return_exceptions=True)
        
        # Count successful uploads
        successful = 0
        for response in responses:
            if isinstance(response, dict) and response.get("status_code") == 200:
                successful += 1
                self.test_documents.append(response["json"]["document_id"])
                
        assert successful >= 3, "At least 3 concurrent uploads should succeed"
        
    async def test_document_with_special_characters(self):
        """Test handling documents with special characters"""
        special_content = """Special characters test:
        Unicode: 你好世界 🌍 
        Symbols: @#$%^&*()
        Quotes: "test" 'test'
        Math: ∑∏∫∂"""
        
        files = {
            'file': ('special_chars.txt', special_content.encode('utf-8'), 'text/plain')
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={'title': 'Special Characters Test'}
        )
        
        assert response["status_code"] == 200
        self.test_documents.append(response["json"]["document_id"])
        
    async def test_empty_document_handling(self):
        """Test handling empty documents"""
        files = {
            'file': ('empty.txt', b'', 'text/plain')
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={'title': 'Empty Document'}
        )
        
        # Should either accept with warning or reject
        assert response["status_code"] in [200, 400]
        
    async def test_document_metadata_handling(self):
        """Test document metadata storage and retrieval"""
        test_file = self.test_files_dir / "test_document.txt"
        
        with open(test_file, 'rb') as f:
            file_content = f.read()
            
        files = {
            'file': ('metadata_test.txt', file_content, 'text/plain')
        }
        
        metadata = {
            'author': 'Test Author',
            'department': 'Engineering',
            'project': 'Automatos AI',
            'version': '1.0',
            'custom_field': 'custom_value'
        }
        
        response = await self.make_request(
            "POST",
            "/api/documents/upload",
            files=files,
            data={
                'title': 'Metadata Test',
                'metadata': json.dumps(metadata)
            }
        )
        
        assert response["status_code"] == 200
        doc_id = response["json"]["document_id"]
        self.test_documents.append(doc_id)
        
        # Retrieve and verify metadata
        response = await self.make_request(
            "GET",
            f"/api/documents/{doc_id}"
        )
        
        assert response["status_code"] == 200
        document = response["json"]
        assert "metadata" in document
        
        doc_metadata = document["metadata"]
        assert doc_metadata.get("author") == "Test Author"
        assert doc_metadata.get("department") == "Engineering"


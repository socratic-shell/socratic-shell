"""Integration tests for the journal server."""

import tempfile
from pathlib import Path

import pytest

from journal_server.server import JournalServer


@pytest.mark.asyncio
async def test_basic_journal_workflow():
    """Test basic journal operations through the MCP server."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / "test.json"
        server = JournalServer(data_file)
        
        # Test journal_write
        write_result = await server._handle_write({
            "path": "test-project",
            "entry": "Started working on the test project. Set up basic structure.",
            "work_context": "project setup",
            "overview": "A test project for validating the journal server functionality."
        })
        
        assert len(write_result) == 1
        assert "Added entry to journal section 'test-project' and updated overview" in write_result[0].text
        
        # Test journal_read
        read_result = await server._handle_read({
            "path": "test-project",
            "include_entries": True,
            "max_entries": 5
        })
        
        assert len(read_result) == 1
        content = read_result[0].text
        assert "# Journal Section: test-project" in content
        assert "A test project for validating" in content
        assert "Started working on the test project" in content
        
        # Test journal_toc
        toc_result = await server._handle_toc({})
        
        assert len(toc_result) == 1
        toc_content = toc_result[0].text
        assert "# Journal Table of Contents" in toc_content
        assert "test-project" in toc_content
        
        # Test journal_list_entries
        list_result = await server._handle_list_entries({
            "path": "test-project",
            "limit": 10
        })
        
        assert len(list_result) == 1
        list_content = list_result[0].text
        assert "# Entries from test-project" in list_content
        assert "project setup" in list_content


@pytest.mark.asyncio
async def test_journal_search():
    """Test journal search functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / "test.json"
        server = JournalServer(data_file)
        
        # Add some entries
        await server._handle_write({
            "path": "project-alpha",
            "entry": "Implemented user authentication with JWT tokens.",
            "work_context": "authentication development"
        })
        
        await server._handle_write({
            "path": "project-alpha",
            "entry": "Set up database schema for user management.",
            "work_context": "database design"
        })
        
        await server._handle_write({
            "path": "project-beta",
            "entry": "Created API endpoints for user registration and login.",
            "work_context": "authentication development"
        })
        
        # Search for authentication-related entries
        search_result = await server._handle_search({
            "work_context": "authentication development",
            "content": "user authentication",
            "salience_threshold": 0.3,
            "max_results": 5
        })
        
        assert len(search_result) == 1
        search_content = search_result[0].text
        assert "Found" in search_content
        assert "authentication" in search_content

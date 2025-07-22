"""Tests for JSON storage backend."""

import json
import tempfile
from pathlib import Path

import pytest

from journal_server.storage import JsonStorage
from journal_server.types import Journal, JournalEntry, JournalSection


def test_empty_journal_creation():
    """Test creating an empty journal when file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / "test.json"
        storage = JsonStorage(data_file)
        
        journal = storage.load()
        assert isinstance(journal, Journal)
        assert len(journal.sections) == 0


def test_journal_persistence():
    """Test saving and loading journal data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / "test.json"
        storage = JsonStorage(data_file)
        
        # Create a journal with some data
        journal = Journal()
        section = JournalSection(path="test-section")
        section.overview = "Test overview"
        section.entries.append(JournalEntry(
            work_context="testing",
            content="This is a test entry"
        ))
        journal.sections["test-section"] = section
        
        # Save and reload
        storage.save(journal)
        reloaded_journal = storage.load()
        
        assert len(reloaded_journal.sections) == 1
        assert "test-section" in reloaded_journal.sections
        
        reloaded_section = reloaded_journal.sections["test-section"]
        assert reloaded_section.overview == "Test overview"
        assert len(reloaded_section.entries) == 1
        assert reloaded_section.entries[0].work_context == "testing"
        assert reloaded_section.entries[0].content == "This is a test entry"


def test_section_creation():
    """Test creating new sections."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / "test.json"
        storage = JsonStorage(data_file)
        
        # Create a root section
        section = storage.create_section("project-alpha")
        assert section.path == "project-alpha"
        
        # Create a nested section
        nested_section = storage.create_section("project-alpha/api-design")
        assert nested_section.path == "project-alpha/api-design"
        
        # Verify structure
        journal = storage.load()
        assert "project-alpha" in journal.sections
        assert "api-design" in journal.sections["project-alpha"].subsections


def test_section_retrieval():
    """Test getting existing sections."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / "test.json"
        storage = JsonStorage(data_file)
        
        # Create sections
        storage.create_section("project-alpha")
        storage.create_section("project-alpha/api-design")
        
        # Test retrieval
        root_section = storage.get_section("project-alpha")
        assert root_section is not None
        assert root_section.path == "project-alpha"
        
        nested_section = storage.get_section("project-alpha/api-design")
        assert nested_section is not None
        assert nested_section.path == "project-alpha/api-design"
        
        # Test non-existent section
        missing_section = storage.get_section("non-existent")
        assert missing_section is None

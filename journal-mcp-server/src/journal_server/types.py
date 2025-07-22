"""Type definitions for the journal server."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class JournalEntry(BaseModel):
    """A single journal entry with work context and content."""
    
    work_context: str = Field(description="The broader kind of work being done")
    content: str = Field(description="The specific content of the entry")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    

class JournalSection(BaseModel):
    """A journal section with overview and entries."""
    
    path: str = Field(description="Path identifier for this section")
    overview: str = Field(default="", description="Current synthesis/understanding")
    entries: List[JournalEntry] = Field(default_factory=list)
    subsections: Dict[str, "JournalSection"] = Field(default_factory=dict)
    

class Journal(BaseModel):
    """Root journal structure."""
    
    sections: Dict[str, JournalSection] = Field(default_factory=dict)
    

class SearchResult(BaseModel):
    """Search result with scoring information."""
    
    section_path: str
    entry_index: int
    entry: JournalEntry
    work_context_score: float
    content_score: float
    combined_score: float
    temporal_score: float


# Enable forward references
JournalSection.model_rebuild()

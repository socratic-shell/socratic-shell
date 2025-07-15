"""Pydantic models for socratic-shell MCP server."""

from typing import Optional
from pydantic import BaseModel


class WriteMemoryRequest(BaseModel):
    """Request to write memory to storage.
    
    Used for both creating new memories and updating existing ones.
    The presence of the 'id' field determines the operation type.
    
    Attributes:
        content: The main text content of the memory to store
        situation: Optional context phrases that help with future retrieval.
                  These are weighted 2x higher than content during search.
                  Example: ['debugging', 'frustrated', 'late evening']
        id: Memory ID for updates. If provided, must be a memory that was
           previously read via read_in. If omitted, creates a new memory
           with auto-generated UUID.
    """
    content: str
    situation: Optional[list[str]] = None
    id: Optional[str] = None


class ReadInRequest(BaseModel):
    """Request to read in relevant memories.
    
    Searches stored memories using keyword matching with stemming.
    Returns up to 5 most relevant memories based on content and situation.
    
    Attributes:
        query: What kind of information to retrieve. Natural language
              description of what you're looking for.
              Example: 'debugging race conditions in payment system'
        situation: Current situational context as separate phrases.
                  These help find memories from similar circumstances.
                  Example: ['debugging', 'feeling frustrated', 'after team meeting']
    """
    query: str
    situation: Optional[list[str]] = None




class Memory(BaseModel):
    """A memory object returned from the system.
    
    Represents a stored memory with its content and metadata.
    Used both for internal storage format and API responses.
    
    Attributes:
        id: Unique identifier for the memory (UUID format)
        content: The main text content of the memory
        situation: Context phrases associated with this memory for retrieval.
                  These are searched separately and weighted higher than content.
        relevance_score: Score indicating how well this memory matches a search query.
                        Higher scores indicate better matches. (Currently unused)
        last_accessed: ISO timestamp of when this memory was last retrieved.
                      Used for potential future aging/importance algorithms. (Currently unused)
    """
    id: str
    content: str
    situation: Optional[list[str]] = None
    relevance_score: Optional[float] = None
    last_accessed: Optional[str] = None
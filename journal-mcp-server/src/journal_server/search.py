"""Semantic search implementation for journal entries."""

import math
from datetime import datetime, timedelta
from typing import Any, List, Tuple, TYPE_CHECKING

from sentence_transformers import SentenceTransformer

from .types import Journal, JournalEntry, SearchResult

if TYPE_CHECKING:
    from .types import JournalSection


class JournalSearcher:
    """Semantic search for journal entries with dual-dimension matching."""
    
    def __init__(self) -> None:
        # Use a lightweight model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search(
        self,
        journal: Journal,
        work_context: str,
        content: str,
        salience_threshold: float = 0.5,
        max_results: int = 10,
    ) -> List[SearchResult]:
        """Search journal entries using dual-dimension matching."""
        
        # Generate embeddings for search queries
        work_context_embedding = self.model.encode([work_context])[0]
        content_embedding = self.model.encode([content])[0]
        
        results: List[SearchResult] = []
        
        # Search through all sections and entries
        for section_path, section in journal.sections.items():
            self._search_section(
                section, section_path, work_context_embedding, content_embedding,
                salience_threshold, results
            )
        
        # Sort by combined score (descending)
        results.sort(key=lambda r: r.combined_score, reverse=True)
        
        return results[:max_results]
    
    def _search_section(
        self,
        section: "JournalSection",
        section_path: str,
        work_context_embedding: Any,
        content_embedding: Any,
        salience_threshold: float,
        results: List[SearchResult],
    ) -> None:
        """Recursively search a section and its subsections."""
        
        # Search entries in this section
        for i, entry in enumerate(section.entries):
            result = self._score_entry(
                section_path, i, entry, work_context_embedding, content_embedding
            )
            
            if result.combined_score >= salience_threshold:
                results.append(result)
        
        # Search subsections
        for subsection_name, subsection in section.subsections.items():
            subsection_path = f"{section_path}/{subsection_name}"
            self._search_section(
                subsection, subsection_path, work_context_embedding, content_embedding,
                salience_threshold, results
            )
    
    def _score_entry(
        self,
        section_path: str,
        entry_index: int,
        entry: JournalEntry,
        work_context_embedding: Any,
        content_embedding: Any,
    ) -> SearchResult:
        """Score a single entry against the search criteria."""
        
        # Generate embeddings for the entry
        entry_work_embedding = self.model.encode([entry.work_context])[0]
        entry_content_embedding = self.model.encode([entry.content])[0]
        
        # Calculate cosine similarity scores
        work_context_score = self._cosine_similarity(work_context_embedding, entry_work_embedding)
        content_score = self._cosine_similarity(content_embedding, entry_content_embedding)
        
        # Calculate temporal salience (recent entries score higher)
        temporal_score = self._calculate_temporal_score(entry.timestamp)
        
        # Combine scores (equal weight for now, could be tunable)
        combined_score = (work_context_score + content_score) / 2 * temporal_score
        
        return SearchResult(
            section_path=section_path,
            entry_index=entry_index,
            entry=entry,
            work_context_score=work_context_score,
            content_score=content_score,
            combined_score=combined_score,
            temporal_score=temporal_score,
        )
    
    def _cosine_similarity(self, a: Any, b: Any) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return float(dot_product / (norm_a * norm_b))
    
    def _calculate_temporal_score(self, timestamp: datetime) -> float:
        """Calculate temporal salience score (recent entries score higher)."""
        now = datetime.utcnow()
        age = now - timestamp
        
        # Exponential decay with half-life of 30 days
        half_life_days = 30
        decay_factor = math.exp(-age.days * math.log(2) / half_life_days)
        
        # Ensure minimum score of 0.1 for very old entries
        return max(0.1, decay_factor)

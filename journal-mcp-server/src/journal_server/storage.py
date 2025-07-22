"""JSON storage backend for the journal server."""

import json
from pathlib import Path
from typing import Optional

from .types import Journal, JournalSection


class JsonStorage:
    """JSON file-based storage for journal data."""
    
    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        self._journal: Optional[Journal] = None
    
    def load(self) -> Journal:
        """Load journal from JSON file."""
        if self._journal is not None:
            return self._journal
            
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._journal = Journal.model_validate(data)
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Failed to load journal from {self.data_file}: {e}")
        else:
            self._journal = Journal()
            
        return self._journal
    
    def save(self, journal: Journal) -> None:
        """Save journal to JSON file."""
        self._journal = journal
        
        # Ensure parent directory exists
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to temporary file first, then rename for atomicity
        temp_file = self.data_file.with_suffix('.tmp')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(journal.model_dump(), f, indent=2, default=str)
            temp_file.replace(self.data_file)
        except Exception:
            # Clean up temp file if something went wrong
            if temp_file.exists():
                temp_file.unlink()
            raise
    
    def get_section(self, path: str) -> Optional[JournalSection]:
        """Get a specific journal section by path."""
        journal = self.load()
        
        # Handle root level sections
        if '/' not in path:
            return journal.sections.get(path)
        
        # Handle nested sections
        parts = path.split('/')
        current = journal.sections.get(parts[0])
        
        for part in parts[1:]:
            if current is None:
                return None
            current = current.subsections.get(part)
            
        return current
    
    def create_section(self, path: str) -> JournalSection:
        """Create a new journal section at the given path."""
        journal = self.load()
        
        # Handle root level sections
        if '/' not in path:
            if path not in journal.sections:
                journal.sections[path] = JournalSection(path=path)
            section = journal.sections[path]
        else:
            # Handle nested sections
            parts = path.split('/')
            
            # Ensure parent sections exist
            current_sections = journal.sections
            current_path = ""
            
            for i, part in enumerate(parts):
                if current_path:
                    current_path += f"/{part}"
                else:
                    current_path = part
                    
                if i == len(parts) - 1:
                    # This is the target section
                    if part not in current_sections:
                        current_sections[part] = JournalSection(path=current_path)
                    section = current_sections[part]
                else:
                    # This is a parent section
                    if part not in current_sections:
                        current_sections[part] = JournalSection(path=current_path)
                    current_sections = current_sections[part].subsections
        
        self.save(journal)
        return section

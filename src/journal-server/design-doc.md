# Implementation Notes

*Technical design for the git-centric journal server*

## Core Concept

The journal server uses git as both storage engine and identifier system. Each journal section is a single file containing the current overview/synthesis, with incremental journal entries stored as git commit messages. This creates an elegant inversion where:

- **File contents**: Always the current understanding (overview)
- **Commit messages**: The incremental journey (journal entries)
- **Git history**: The complete collaborative record
- **Git merges**: Natural collaboration mechanism

## File Structure

Each journal section is simply a markdown file:

```
journal-data/
├── project-alpha.md           # Current overview of project-alpha
├── project-beta/
│   ├── api-design.md         # Current overview of project-beta/api-design
│   └── error-handling.md     # Current overview of project-beta/error-handling
└── .git/                     # Git repository containing all history
```

## Identifier Scheme

Journal identifiers use the format `path#hash` where `#hash` is optional:

- **Current overview**: `project-alpha/api-design`
- **Specific journal entry**: `project-alpha/api-design#abc123def`

The hash refers to the git commit SHA that contains the journal entry in its commit message.

## MCP Server Tools

### journal_search

Search journal entries by work context and content across git commit history:

```python
Tool(
    name="journal_search",
    description="Search journal entries by work context and content",
    inputSchema={
        "type": "object",
        "properties": {
            "work_context": {"type": "string", "description": "The broader kind of work being done"},
            "content": {"type": "string", "description": "Specific content being sought"},
            "salience_threshold": {"type": "number", "default": 0.5}
        },
        "required": ["work_context", "content"]
    }
)
```

**Returns**: List of journal entries with scores and metadata:
```python
[
    {
        "id": "project-alpha/api-design#abc123def",
        "content": "work_context: debugging memory retrieval\n\n# Today's Session...",
        "work_context_score": 0.85,
        "content_score": 0.72,
        "combined_score": 0.785,
        "timestamp": "2024-07-21T18:00:00Z"
    }
]
```

### journal_read

Read a journal overview or specific entry:

```python
Tool(
    name="journal_read",
    description="Read a journal overview or specific entry",
    inputSchema={
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "Journal identifier (e.g., 'project-alpha/api-design' or 'project-alpha/api-design#abc123')"}
        },
        "required": ["id"]
    }
)
```

**Behavior**:
- `project-alpha/api-design` → Returns current file contents (overview)
- `project-alpha/api-design#abc123` → Returns commit message from that SHA (journal entry)
- Server remembers what was read for conflict detection

### journal_toc

Get the hierarchical structure of journal sections:

```python
Tool(
    name="journal_toc", 
    description="Get the table of contents showing journal sections and subsections",
    inputSchema={
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "Starting point for TOC query (empty string for root)", "default": ""},
            "depth": {"type": "number", "description": "How many levels deep to descend", "default": 1}
        }
    }
)
```

**Returns**: Hierarchical structure with basic metadata:
```python
{
    "id": "project-alpha",
    "type": "section",
    "last_updated": "2024-07-21T18:00:00Z",
    "entry_count": 47,  # git rev-list --count
    "subsections": [
        {
            "id": "project-alpha/api-design",
            "type": "section", 
            "last_updated": "2024-07-20T15:30:00Z",
            "entry_count": 12
        }
    ]  # if depth > 1
}
```

### journal_list_entries

List entries for a specific journal section with chronological paging:

```python
Tool(
    name="journal_list_entries",
    description="List entries for a specific journal section",
    inputSchema={
        "type": "object", 
        "properties": {
            "path": {"type": "string", "description": "Journal section path"},
            "start": {"type": "number", "description": "Starting index (0 = most recent)", "default": 0},
            "length": {"type": "number", "description": "Number of entries to return", "default": 10}
        },
        "required": ["path"]
    }
)
```

**Returns**: Chronological list of entries:
```python
[
    {"id": "project-alpha#abc123", "timestamp": "2024-07-21T18:00:00Z", "summary": "debugging session"},
    {"id": "project-alpha#def456", "timestamp": "2024-07-20T15:30:00Z", "summary": "api design work"}
]
```

### journal_write

Add a new journal entry and optionally update the overview synthesis:

```python
Tool(
    name="journal_write",
    description="Add a new journal entry and optionally update the overview synthesis",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Journal section path (no #hash)"},
            "entry": {"type": "string", "description": "Journal entry that covers what has changed, been learned, etc. (becomes commit message)"},
            "overview": {"type": "string", "description": "Optional updated overview content when the entry represents a shift in overall understanding or strategy"},
            "summary": {"type": "string", "description": "Optional brief summary for the commit"}
        },
        "required": ["path", "entry"]
    }
)
```

**Write Protection**: 
- Writing only permitted after reading the journal section
- Server tracks `{session_id: {path: last_read_commit_hash}}`
- If HEAD has moved since read, returns merge error
- Client must re-read and retry

## Git Workflow

### Adding Journal Entries

Each journal update creates a git commit with two distinct patterns:

**Entry-only commits** (most common):
1. **Read current state**: `journal_read("project-alpha/api-design")` (server remembers HEAD)
2. **Add journal entry**: Call `journal_write` with just `entry` parameter
3. **File modification**: System increments entry count comment based on current git history
4. **Git commit**: Full entry goes in commit message, minimal file change enables git tracking
5. **Conflict resolution**: If entry count conflicts, resolve by counting actual commits in git history for this path

**Entry + overview commits** (consolidation moments):
1. **Read current state**: Same as above
2. **Update understanding**: Call `journal_write` with both `entry` and `overview` parameters  
3. **File replacement**: New overview content replaces file, entry log section preserved
4. **Git commit**: Entry in commit message, substantial file change captures new synthesis

### File Structure with Entry Count

Journal files maintain a clean overview section plus an entry count for conflict avoidance:

```markdown
# Current Understanding of API Design

Our current approach focuses on REST endpoints with...

[Main overview content here]

<!-- entry count: 47 -->
```

When `journal_read` loads overview content, it strips the entry count comment before returning to the LLM. The count represents the number of journal entries (git commits) for this section and provides a meaningful way to create file changes that can be automatically merged.

### Commit Message Format

Commit messages contain the journal entry with structured metadata:

```
work_context: debugging memory retrieval issues

# Today's Debugging Session

We discovered that the async retrieval pattern was failing because...

Key insights:
- Pattern X works better than Y when dealing with temporal data  
- The salience threshold needs to be context-dependent

This led us to update our understanding of error handling patterns...
```

### Conflict Resolution

**For file conflicts**: Auto-rebase and merge - journal entries are typically independent

**For overview conflicts**: LLM synthesis tool merges conflicting understandings:
```python
Tool(
    name="journal_synthesize_conflict",
    description="Synthesize conflicting journal overviews using LLM",
    inputSchema={
        "section": "project-alpha",
        "version_a": "# Understanding from session 1...",
        "version_b": "# Understanding from session 2...", 
        "work_context": "what kind of work led to this conflict"
    }
)
```

## Search Implementation

### Dual-Dimension Matching

Search operates on git commit messages using semantic embeddings:

```python
class JournalSearch:
    def __init__(self, git_repo, embeddings_model):
        self.repo = git_repo
        self.embeddings = embeddings_model
    
    async def search(self, work_context: str, content: str, salience_threshold: float = 0.5):
        # Get all commits across all journal files
        commits = self.repo.iter_commits(all=True)
        
        # Extract commit messages and metadata
        candidates = []
        for commit in commits:
            if self.is_journal_commit(commit):
                candidates.append({
                    'id': f"{self.get_journal_path(commit)}#{commit.hexsha[:7]}",
                    'content': commit.message,
                    'timestamp': commit.committed_datetime,
                    'salience': self.calculate_temporal_salience(commit.committed_datetime)
                })
        
        # Filter by temporal salience
        candidates = [c for c in candidates if c['salience'] >= salience_threshold]
        
        # Score both dimensions
        results = []
        for candidate in candidates:
            work_context_score = await self.semantic_similarity(work_context, candidate['content'])
            content_score = await self.semantic_similarity(content, candidate['content'])
            combined_score = (work_context_score + content_score) / 2
            
            if combined_score > salience_threshold:
                results.append({
                    **candidate,
                    'work_context_score': work_context_score,
                    'content_score': content_score,
                    'combined_score': combined_score
                })
        
        return sorted(results, key=lambda x: x['combined_score'], reverse=True)
```

### Temporal Salience

Recent commits are more easily accessible, older commits require higher relevance:

```python
def calculate_temporal_salience(commit_timestamp: datetime) -> float:
    age_days = (datetime.now() - commit_timestamp).days
    half_life_days = 30  # Configurable
    decay_factor = 0.5 ** (age_days / half_life_days)
    return decay_factor
```

## Session Management

The server maintains session state for conflict detection:

```python
class SessionManager:
    def __init__(self):
        self.session_reads = {}  # {session_id: {path: commit_hash}}
    
    def record_read(self, session_id: str, path: str, commit_hash: str):
        if session_id not in self.session_reads:
            self.session_reads[session_id] = {}
        self.session_reads[session_id][path] = commit_hash
    
    def check_conflicts(self, session_id: str, path: str, current_head: str) -> bool:
        if session_id not in self.session_reads:
            return True  # No read recorded, conflict
        if path not in self.session_reads[session_id]:
            return True  # Path not read, conflict
        return self.session_reads[session_id][path] != current_head
```

## Configuration

```json
{
    "journal_data_path": "./journal-data",
    "git_config": {
        "auto_gc": true,
        "commit_author": "Journal Server <journal@localhost>"
    },
    "temporal_decay": {
        "half_life_days": 30,
        "minimum_salience": 0.1
    },
    "search": {
        "default_salience_threshold": 0.5,
        "max_results": 20,
        "context_weight": 0.5,
        "content_weight": 0.5
    },
    "embeddings": {
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        "cache_path": "./embeddings-cache"
    }
}
```

## Future Enhancements

- **Git synchronization**: Pull/push for multi-user collaboration
- **Branch support**: Explore different understanding paths
- **Merge strategies**: Advanced conflict resolution patterns
- **Performance optimization**: Incremental search indexing
- **Rich commit metadata**: Structured frontmatter in commit messages

## Why This Design Works

This git-centric approach elegantly solves several problems:

1. **Natural collaboration**: Git's merge machinery handles multiple sessions
2. **Simple storage**: Just markdown files + git, no complex databases
3. **Rich history**: Full journey preserved in commit messages
4. **Familiar tooling**: Standard git commands work for exploration
5. **Conflict resolution**: Leverages both git automation and LLM synthesis
6. **Temporal relevance**: Git timestamps provide natural salience decay

The journal becomes a living document where the current understanding is always visible in the file, while the collaborative journey lives in the git history.

---

*This design transforms git from a version control system into a collaborative memory engine.*

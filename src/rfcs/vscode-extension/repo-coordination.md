# RFC: Coordinating Repositories and Multi-Language Bundling

## Problem Statement

How should the Socratic Shell VSCode extension coordinate multiple components written in different languages (TypeScript dialectic, Python hippo, future Rust components) while maintaining:
- Independent development of each component
- Unified distribution and user experience
- Manageable build and sync processes
- Cross-component integration capabilities

## Architecture Overview

Use **git subtrees** to create a unified development environment while preserving component independence. Each component maintains its native tooling and build processes, with orchestration handled at the extension level.

## Repository Structure

### Source Repository Layout
```
socratic-shell-extension/
├── src/                     # Main extension (TypeScript)
│   ├── installation.ts      # Installation orchestration
│   ├── configuration.ts     # MCP server management
│   └── extension.ts         # Activation + delegation
├── dialectic/               # Git subtree from dialectic repo
│   ├── extension/src/       # Dialectic VSCode extension code
│   ├── mcp-server/         # Dialectic MCP server
│   ├── package.json
│   └── tsconfig.json
├── hippo/                   # Git subtree from hippo repo
│   ├── src/hippo/          # Python source
│   ├── pyproject.toml
│   └── requirements.txt
├── mcp-server/              # Future: Git subtree from Rust MCP server
│   ├── src/
│   ├── Cargo.toml
│   └── Cargo.lock
├── binaries/                # Build output directory
│   ├── windows-x64/
│   ├── darwin-x64/
│   ├── darwin-arm64/
│   └── linux-x64/
└── package.json             # Main extension manifest
```

### Component Independence
Each subtree maintains:
- **Own build system**: npm/cargo/pip/etc.
- **Own dependencies**: package.json/Cargo.toml/pyproject.toml
- **Own testing**: Component-specific test frameworks
- **Own CI/CD**: Can be developed and tested independently

## Git Subtree Management

### Initial Setup
```bash
# Add subtrees to socratic-shell-extension repo
git subtree add --prefix=dialectic \
  https://github.com/socratic-shell/dialectic.git main --squash

git subtree add --prefix=hippo \
  https://github.com/socratic-shell/hippo.git main --squash
```

### Sync Strategy
**Automated Daily Sync** via GitHub Actions:
- Pull changes from component repos into subtrees
- Detect and report sync failures (merge conflicts, network issues)
- Detect local changes that need to be pushed upstream
- Create issues for manual intervention when needed

### Cross-Component Development Workflow

**Normal Development** (Recommended):
1. Develop in source repos (dialectic, hippo)
2. Automated sync brings changes into socratic-shell-extension
3. Test integration in unified environment

**Integration Development** (When Needed):
1. Edit components directly in socratic-shell-extension subtrees
2. Test integration immediately
3. Push changes back to source repos:
   ```bash
   git subtree push --prefix=dialectic origin integration-feature
   ```
4. Create PR in source repo to merge integration changes

## Build Orchestration

### Multi-Language Build Pipeline

**Phase 1: Component Builds**
```bash
# Python components (hippo)
cd hippo/
pip install -r requirements.txt
pyinstaller --onefile src/hippo/main.py -n hippo-standalone
cp dist/hippo-standalone ../binaries/linux-x64/

# TypeScript components (dialectic MCP server)
cd dialectic/mcp-server/
npm install
npm run build
npm run package  # Creates standalone executable
cp dist/dialectic-server ../binaries/linux-x64/

# Rust components (future MCP server)
cd mcp-server/
cargo build --release --target x86_64-unknown-linux-gnu
cp target/x86_64-unknown-linux-gnu/release/socratic-shell ../binaries/linux-x64/
```

**Phase 2: Extension Build**
```bash
# Main extension
npm install
npm run compile  # TypeScript compilation
npm run webpack  # Bundle with binaries
```

### Cross-Platform Build Matrix
Use GitHub Actions matrix strategy:
```yaml
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        target: linux-x64
      - os: macos-latest  
        target: darwin-x64
      - os: macos-latest
        target: darwin-arm64
      - os: windows-latest
        target: windows-x64
```

Each job builds all components for its target platform and uploads artifacts.

## Automated Synchronization

### GitHub Actions Sync Workflow
```yaml
name: Sync Subtrees
on:
  schedule:
    - cron: '0 6 * * *'  # Daily sync
  workflow_dispatch:     # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Check for local changes
        # Detect if subtrees have local modifications
        
      - name: Sync each subtree
        # Pull from source repos with conflict detection
        
      - name: File issues on failure
        # Create GitHub issues for sync problems
        
      - name: Create PR if successful
        # Auto-PR for successful syncs with changes
```

### Conflict Resolution Strategy
When sync fails due to conflicts:
1. **Automated issue creation** with conflict details
2. **Manual resolution** by maintainer
3. **Documentation** of common conflict patterns
4. **Process refinement** based on conflict frequency

## Integration Points

### VSCode Extension Integration
The main extension acts as a **thin delegation layer**:
```typescript
// Main extension delegates to dialectic
import { activateDialectic } from './dialectic/extension/src/extension';

export function activate(context: vscode.ExtensionContext) {
    // Socratic Shell setup
    await setupInstallation(context);
    await startMCPServer(context);
    
    // Delegate to dialectic
    const dialecticChannel = vscode.window.createOutputChannel('Socratic Shell - Dialectic');
    activateDialectic(context, dialecticChannel);
}
```

### MCP Server Coordination
The Rust MCP server orchestrates backend components:
- Routes requests to appropriate language-specific servers
- Manages process lifecycle for Python/TypeScript backends
- Handles cross-component communication

## Benefits of This Approach

### For Development
- **Language-native tooling**: Each component uses its optimal build system
- **Independent evolution**: Components can be developed separately
- **Unified testing**: Integration testing in single environment
- **Cross-component editing**: Can make coordinated changes when needed

### For Distribution
- **Single extension**: Users install one VSCode extension
- **All platforms supported**: Multi-language builds handled automatically
- **Consistent versioning**: Extension version coordinates all components
- **Simplified updates**: Single extension update brings all components

### For Maintenance
- **Automated syncing**: Reduces manual coordination overhead
- **Conflict visibility**: Issues filed automatically for problems
- **Proven approach**: Based on successful Rust project experience
- **Extensible**: Easy to add new language components

## Challenges and Mitigations

### Challenge: Build Complexity
**Mitigation**: Comprehensive CI/CD pipeline with clear documentation and automated testing

### Challenge: Sync Conflicts
**Mitigation**: Automated issue filing, clear conflict resolution procedures, and preference for upstream development

### Challenge: Version Coordination
**Mitigation**: Extension version acts as coordination point, with component versions tracked in build metadata

### Challenge: Cross-Language Dependencies
**Mitigation**: MCP protocol provides clean boundaries between components, minimizing tight coupling

## Success Criteria

- New components can be added with minimal changes to build system
- Sync failures are rare and quickly resolved when they occur
- Developers can work productively in either source repos or unified repo
- Build times remain reasonable despite multi-language complexity
- Users experience seamless installation regardless of underlying complexity

## Future Considerations

- **Workspace management**: Tools for managing multiple subtrees efficiently
- **Dependency coordination**: Handling shared dependencies across languages
- **Performance optimization**: Caching strategies for multi-language builds
- **Component discovery**: Automatic detection of new components to include

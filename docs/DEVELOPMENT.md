# DevPulse - Development Documentation

## Overview

DevPulse is a CLI tool designed for the GitHub Copilot CLI Challenge. It demonstrates how Copilot CLI can help rapidly build professional developer tools.

## Design Decisions

### 1. Python Standard Library Only

**Decision**: Use only Python's standard library (no external dependencies)

**Rationale**:
- Shows real engineering without relying on heavy frameworks
- Faster to install and run
- Easier for judges/users to evaluate
- Demonstrates Copilot CLI's ability to work with standard libraries

**Trade-off**: No fancy colored output (could add `rich` library later)

### 2. Local-First Architecture

**Decision**: All scanning happens locally, no network calls

**Rationale**:
- Privacy: No code leaves the developer's machine
- Speed: No network latency
- Reliability: Works offline
- Trust: Users can inspect everything

### 3. Read-Only by Default

**Decision**: Scanner never modifies files; fixes require explicit command

**Rationale**:
- Safety: Users maintain full control
- Predictability: No surprises
- Trust: Clear separation between analysis and modification

### 4. Composable Check System

**Decision**: Each check is independent and returns standardized results

**Rationale**:
- Maintainability: Easy to add new checks
- Testability: Each check can be tested in isolation
- Performance: Checks can potentially run in parallel (future enhancement)
- Clarity: Clear separation of concerns

## Architecture

### Data Flow

```
User Command
    ↓
CLI Parser (devpulse.py)
    ↓
Scanner (core/scanner.py)
    ↓
Metadata Collection (utils/fs.py)
    ↓
Independent Checks (checks/*.py)
    ↓
Result Aggregation
    ↓
Reporter (core/reporter.py)
    ↓
Output (Terminal or JSON)
```

### Result Format

Each check returns results in this format:

```python
{
    'name': 'Check Name',           # Human-readable name
    'status': 'ok|info|warning|critical',  # Severity
    'details': 'Description...',    # Human-readable details
    'fixable': True|False,          # Can be auto-fixed?
    'data': {...}                   # Optional: structured data
}
```

## Implementation Details

### Scanner (core/scanner.py)

The scanner orchestrates the entire analysis:

1. Collects metadata once (file list, sizes, extensions)
2. Passes metadata to all checks
3. Aggregates results
4. Returns to reporter

**Key insight**: Metadata is collected once and reused by all checks, making the tool fast.

### Checks

#### Stack Check (checks/stack.py)
- Looks for indicator files (package.json, requirements.txt, etc.)
- Returns detected technologies
- Status: `info` (informational only)

#### Hygiene Check (checks/hygiene.py)
- Checks for README, LICENSE, .gitignore
- Looks for test directories
- Counts TODO/FIXME comments
- Status: `warning` for missing files

#### Security Check (checks/security.py)
- Scans for .env files not in .gitignore
- Regex patterns for API keys, secrets, tokens
- Status: `critical` for .env exposure, `warning` for potential secrets

**Note**: This is intentionally basic. We warn users not to rely on this for production security.

#### Size Check (checks/size.py)
- Finds files > 10MB
- Reports total project size
- Status: `warning` for large files, `info` for size summary

### Fixer (core/fixer.py)

Applies only safe, non-destructive fixes:

- ✅ Create missing README (from template)
- ✅ Create missing LICENSE (MIT, from template)
- ✅ Create missing .gitignore (comprehensive template)

**Never does**:
- ❌ Delete files
- ❌ Modify existing code
- ❌ Auto-commit to git

### Reporter (core/reporter.py)

Two output modes:

1. **Terminal**: Human-readable with emojis and grouping
2. **JSON**: Machine-readable for automation/CI

## Future Enhancements

### Could Add:
- Parallel check execution
- Plugin system for custom checks
- Configuration file support (.devpulse.yml)
- CI/CD integration helpers
- Colored terminal output (using `rich`)
- More tech stack detections
- Dependency vulnerability checks
- Code complexity metrics

### Intentionally Excluded:
- Deep security scanning (use Snyk, GitGuardian)
- Code quality analysis (use linters)
- Build/test execution (use CI/CD)
- Git operations (use git CLI)

## Testing Strategy

### Manual Testing

```bash
# Test scanning
python devpulse.py scan
python devpulse.py scan --json
python devpulse.py scan --path /other/project

# Test fixing
python devpulse.py fix --safe
python devpulse.py fix --interactive

# Test error handling
python devpulse.py scan --path /nonexistent
python devpulse.py scan --path README.md  # not a directory
```

### Test Cases Covered

1. ✅ Scan current directory
2. ✅ Scan specific path
3. ✅ JSON output format
4. ✅ Fix generation (README, LICENSE, .gitignore)
5. ✅ Interactive fix mode
6. ✅ Invalid path handling
7. ✅ Empty directory handling

## Built with GitHub Copilot CLI

This entire project was built using GitHub Copilot CLI, demonstrating:

- Rapid prototyping from concept to working tool
- Professional code structure and documentation
- Best practices (error handling, argument parsing, modularity)
- Comprehensive functionality in minimal time

**Development time**: ~1-2 hours with Copilot CLI assistance

## License

MIT License - See LICENSE file for details

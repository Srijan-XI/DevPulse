# DevPulse - Usage Examples

## Basic Usage

### Scan Current Directory

```bash
python devpulse.py scan
```

This will scan the current directory and output a human-readable report.

### Scan Specific Project

```bash
python devpulse.py scan --path /path/to/my/project
python devpulse.py scan --path ~/projects/my-app
python devpulse.py scan --path "C:\Users\Dev\Projects\MyApp"
```

### JSON Output for Automation

```bash
# Output as JSON
python devpulse.py scan --json

# Save to file
python devpulse.py scan --json > report.json

# Use in CI/CD
python devpulse.py scan --json | jq '.summary.critical'
```

## Fixing Issues

### Safe Auto-Fix

```bash
# Automatically fix all safe issues (README, LICENSE, .gitignore)
python devpulse.py fix --safe
```

This will create:
- `README.md` (if missing)
- `LICENSE` (if missing)
- `.gitignore` (if missing)

### Interactive Fix

```bash
# Ask before each fix
python devpulse.py fix --interactive
```

You'll be prompted:
```
Fix 'Missing README'? [y/N]: y
Fix 'Missing LICENSE'? [y/N]: n
Fix 'Missing .gitignore'? [y/N]: y
```

## Common Scenarios

### New Project Setup

```bash
# Create a new project directory
mkdir my-new-project
cd my-new-project

# Initialize with git
git init

# Use DevPulse to bootstrap essential files
python /path/to/devpulse.py fix --safe

# You now have README.md, LICENSE, and .gitignore
```

### Pre-Commit Check

```bash
# Check for issues before committing
python devpulse.py scan

# If critical issues found (exit code 1), fix them
# If warnings only (exit code 0), you're good
```

### CI/CD Integration

**GitHub Actions Example:**

```yaml
name: DevPulse Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Run DevPulse
        run: |
          python devpulse.py scan --json > report.json
          
      - name: Check for critical issues
        run: |
          CRITICAL=$(jq '.summary.critical' report.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "Critical issues found!"
            exit 1
          fi
```

### Team Onboarding

Add to your project's documentation:

```markdown
## Project Health Check

Before starting development, run DevPulse to understand the project:

```bash
python devpulse.py scan
```

This will show you:
- What technologies we use
- Common issues to watch for
- Project size and structure
```

## Exit Codes

DevPulse uses standard exit codes:

- `0`: Success (no critical issues)
- `1`: Critical issues found
- `130`: Interrupted by user (Ctrl+C)

Use in scripts:

```bash
#!/bin/bash

python devpulse.py scan

if [ $? -eq 0 ]; then
    echo "✓ Project health check passed"
else
    echo "✗ Critical issues found"
    exit 1
fi
```

## Understanding the Report

### Status Levels

- **✓ OK**: Everything is fine
- **ℹ Info**: Informational only (tech stack detected, file counts)
- **⚠ Warning**: Should be addressed but not blocking
- **🚨 Critical**: Must be fixed (security issues, etc.)

### Tech Stack Detection

DevPulse automatically detects:

- **Python**: requirements.txt, pyproject.toml, setup.py
- **Node.js**: package.json, yarn.lock, pnpm-lock.yaml
- **Java**: pom.xml, build.gradle, gradlew
- **Docker**: Dockerfile, docker-compose.yml
- **GitHub Actions**: .github/workflows/
- And more...

### Security Checks

DevPulse performs **basic** local security scanning:

1. **Environment Files**: Checks if .env is tracked by git
2. **Secret Patterns**: Scans for API_KEY, SECRET, TOKEN, PASSWORD patterns

⚠️ **Important**: This is NOT a comprehensive security tool. Use dedicated tools like:
- Snyk
- GitGuardian
- Trivy
- npm audit / pip audit

## Advanced Usage

### Scan Multiple Projects

```bash
#!/bin/bash
for dir in ~/projects/*/; do
    echo "Scanning $dir"
    python devpulse.py scan --path "$dir" --json > "$(basename $dir)-report.json"
done
```

### Generate Summary Report

```bash
# Scan all projects and create a summary
python devpulse.py scan --path ~/projects/project1 --json > p1.json
python devpulse.py scan --path ~/projects/project2 --json > p2.json

# Use jq to summarize
jq -s 'map({project: .project, critical: .summary.critical, warnings: .summary.warnings})' *.json
```

### Filter Specific Issues

```bash
# Show only critical issues
python devpulse.py scan --json | jq '.results[] | select(.status == "critical")'

# Show only fixable issues
python devpulse.py scan --json | jq '.results[] | select(.fixable == true)'

# Count TODO comments
python devpulse.py scan --json | jq '.results[] | select(.name == "TODO/FIXME Comments") | .data'
```

## Troubleshooting

### "No such file or directory"

Make sure you're providing a valid path:

```bash
# Check if path exists
ls /path/to/project

# Use absolute path if relative path fails
python devpulse.py scan --path /absolute/path/to/project
```

### "Path is not a directory"

DevPulse only scans directories, not individual files:

```bash
# Wrong
python devpulse.py scan --path README.md

# Correct
python devpulse.py scan --path .
```

### Large Projects Taking Too Long

DevPulse automatically ignores common directories:
- `.git`
- `node_modules`
- `venv`, `.venv`, `env`
- `__pycache__`
- `dist`, `build`, `target`

If still slow, the project might be very large. Consider scanning subdirectories separately.

## Tips & Best Practices

1. **Run regularly**: Make DevPulse part of your workflow
2. **CI/CD integration**: Catch issues early in PRs
3. **Team standards**: Use as a baseline for project quality
4. **Not a replacement**: Complement with proper testing, linting, security tools
5. **Trust but verify**: Review auto-fixes before committing

## Examples from Real Projects

### Scan Result: Well-Maintained Project

```
Tech Stack & Info:
  ✓ Python
  ✓ Docker
  ✓ GitHub Actions
  ℹ Total size: 12.45 MB (456 files)

Summary:
  Total checks: 5
  Critical: 0
  Warnings: 0
```

### Scan Result: Needs Attention

```
Warnings:
  ⚠ Missing README.md
  ⚠ Missing LICENSE
  ⚠ Found 127 TODO/FIXME comments
  ⚠ Large Files: 3 file(s) larger than 10.00 MB

Critical Issues:
  🚨 .env file exists but may not be in .gitignore

💡 2 issue(s) can be auto-fixed with: devpulse fix --safe
```

## Getting Help

```bash
# Show help
python devpulse.py --help

# Show command-specific help
python devpulse.py scan --help
python devpulse.py fix --help
```

## Next Steps

1. Try scanning your current project
2. Review the output and understand the issues
3. Use `fix --safe` to address simple issues
4. Integrate into your workflow
5. Share with your team!

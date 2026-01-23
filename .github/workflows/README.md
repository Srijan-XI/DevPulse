# DevPulse GitHub Workflows

This directory contains automated workflows to maintain code quality and streamline development.

## 🔄 Workflows (6 Total)

### 1. **CI - Continuous Integration** (`ci.yml`)
**Triggers:** Push to main/develop, Pull Requests, Manual

**Jobs:**
- **Test** - Runs DevPulse on multiple OS (Ubuntu, Windows, macOS) and Python versions (3.10, 3.11, 3.12)
  - Tests CLI scanning on self and examples
  - Verifies JSON output
  - Tests all module imports
  - Tests GUI imports (Linux/macOS only)

- **Lint** - Code quality checks
  - Black (formatting)
  - isort (import sorting)
  - flake8 (linting)

- **Security** - Security analysis
  - Bandit (security linter)
  - Safety (dependency vulnerabilities)

- **Dogfooding** - DevPulse scans itself
  - Runs health check on codebase
  - Fails if critical issues found
  - Uploads JSON report as artifact

- **Docs** - Documentation validation
  - Verifies all required docs exist
  - Checks documentation structure

**Usage:**
```yaml
# Automatically runs on:
- Push to main/develop
- Pull requests
- Manual trigger via Actions tab
```

---

### 2. **Release** (`release.yml`)
**Triggers:** Tag push (v*.*.*), Manual with version input

**Jobs:**
- **Create Release**
  - Runs self-check before release
  - Generates changelog from git commits
  - Creates distribution packages (.tar.gz, .zip)
  - Generates checksums
  - Creates GitHub Release with assets

- **Test Release**
  - Downloads release package
  - Tests on Ubuntu, Windows, macOS
  - Verifies package works correctly

**Usage:**
```bash
# Create a new release
git tag v1.0.0
git push origin v1.0.0

# Or manually via Actions tab with version input
```

---

### 3. **CodeQL Security Analysis** (`codeql.yml`)
**Triggers:** Push to main, Pull Requests, Weekly schedule, Manual

**Jobs:**
- Initializes CodeQL for Python
- Analyzes code for security vulnerabilities
- Reports findings to GitHub Security tab

**Usage:**
- Automatically runs weekly on Mondays
- Check results in Security → Code scanning alerts

---

### 4. **Auto Label PRs** (`label-pr.yml`)
**Triggers:** PR opened/updated

**Jobs:**
- Automatically labels PRs based on modified files
- Adds size labels (xs, s, m, l, xl)
- Uses `.github/labeler.yml` for configuration

**Labels:**
- `type/*` - Based on file paths (docs, core, checks, etc.)
- `size/*` - Based on number of changed lines

---

### 5. **Mark Stale Issues and PRs** (`stale.yml`)
**Triggers:** Daily schedule, Manual

**Jobs:**
- Marks issues stale after 30 days of inactivity
- Marks PRs stale after 14 days of inactivity
- Closes stale items after 7 days
- Exempts pinned/in-progress items

---

### 6. **Greetings** (`greetings.yml`)
**Triggers:** First issue/PR from new contributors

**Jobs:**
- Welcomes first-time issue creators
- Celebrates first-time PR contributors
- Provides helpful links and next steps
- Encourages community participation

---

## 📋 Issue Templates

### Bug Report (`bug_report.yml`)
Structured form for reporting bugs with fields for:
- Bug description
- Reproduction steps
- Expected vs actual behavior
- Python version, OS, interface (CLI/GUI)

### Feature Request (`feature_request.yml`)
Structured form for suggesting features with fields for:
- Problem statement
- Proposed solution
- Feature area (detection, scanning, UI, etc.)
- Priority level

## 🔧 Configuration Files

### `labeler.yml`
Maps file paths to PR labels:
```yaml
'type/documentation': ['docs/**/*', '**/*.md']
'type/core': ['core/**/*']
'type/checks': ['checks/**/*']
# ... etc
```

### `dependabot.yml`
Monitors GitHub Actions versions for updates:
- Weekly checks on Mondays
- Auto-creates PRs for updates

### `PULL_REQUEST_TEMPLATE.md`
Standard PR template with:
- Description and change type
- Testing checklist
- DevPulse self-check section

## 🚀 Quick Reference

### Running Workflows Manually

1. Go to **Actions** tab on GitHub
2. Select workflow from left sidebar
3. Click **Run workflow** button
4. Fill in inputs (if required)
5. Click **Run workflow**

### Viewing Workflow Results

- **Actions tab**: See all workflow runs
- **Pull Requests**: CI status checks on PRs
- **Releases**: Release artifacts and notes
- **Security tab**: CodeQL findings

### Adding New Workflows

1. Create `.github/workflows/your-workflow.yml`
2. Define triggers, jobs, and steps
3. Test with `workflow_dispatch` trigger
4. Commit and push

## 📊 Workflow Status Badges

Add to README.md:

```markdown
[![CI](https://github.com/YOUR_USERNAME/devpulse/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/devpulse/actions/workflows/ci.yml)
[![CodeQL](https://github.com/YOUR_USERNAME/devpulse/actions/workflows/codeql.yml/badge.svg)](https://github.com/YOUR_USERNAME/devpulse/actions/workflows/codeql.yml)
```

## 🔐 Secrets Required

None currently required. All workflows use `GITHUB_TOKEN` which is automatically provided.

## ⚙️ Maintenance

- Review and update Python versions in CI when new versions release
- Update actions (checkout, setup-python, etc.) when new versions available
- Adjust stale timeouts based on project activity
- Update labeler.yml when adding new directories

## 💡 Best Practices

1. **Test locally first**: Run `python devpulse.py scan --path .` before pushing
2. **Small PRs**: Smaller PRs get labeled as `size/xs` or `size/s` and are easier to review
3. **Descriptive commits**: Help generate better changelogs for releases
4. **Link issues**: Use "Fixes #123" in PR descriptions to auto-close issues

---

**Need help?** Check [GitHub Actions Documentation](https://docs.github.com/en/actions) or open an issue.

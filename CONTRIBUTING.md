# Contributing to DevPulse

Thank you for considering contributing to DevPulse! 🩺

## 🎯 Project Philosophy

DevPulse is designed to be:
- **Local-first**: All analysis on the user's machine
- **Zero-config**: No setup required
- **Dependency-free**: Python stdlib only
- **Fast and simple**: Scan in seconds

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- A text editor or IDE

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/devpulse.git
cd devpulse

# Test the CLI
python devpulse.py scan --path .

# Test the GUI (optional)
python devpulse_gui.py
```

## 🔧 Development Workflow

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/devpulse.git
cd devpulse
git remote add upstream https://github.com/ORIGINAL_OWNER/devpulse.git
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Make Changes

- Keep commits focused and atomic
- Write clear commit messages
- Follow existing code style
- Test your changes thoroughly

### 4. Test Locally

```bash
# Test on yourself
python devpulse.py scan --path .

# Test on examples
python devpulse.py scan --path examples/python-app
python devpulse.py scan --path examples/web-app

# Test JSON output
python devpulse.py scan --path . --json

# Test auto-fix (on a test directory)
python devpulse.py fix --safe --path test-directory
```

### 5. Run DevPulse on Your Changes

```bash
# Dogfooding - always scan your own changes
python devpulse.py scan --path .
```

### 6. Commit and Push

```bash
git add .
git commit -m "feat: add new tech stack detection for Ruby"
git push origin feature/your-feature-name
```

### 7. Create Pull Request

- Use the PR template
- Fill in all sections
- Link related issues
- Include DevPulse scan results

## 📝 Commit Message Convention

We use conventional commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no functional change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Examples:**
```
feat(checks): add Ruby on Rails detection
fix(scanner): handle permission errors gracefully
docs(readme): update installation instructions
refactor(reporter): simplify JSON formatting
```

## 🏗️ Project Structure

Understanding the codebase:

```
cli/
├── devpulse.py          # CLI entry - start here for CLI changes
├── devpulse_gui.py      # GUI app - start here for GUI changes
├── core/                # Core logic
│   ├── scanner.py       # Orchestration - add new check types here
│   ├── reporter.py      # Output formatting
│   └── fixer.py         # Auto-fix logic
├── checks/              # Check modules - extend these
│   ├── stack.py         # Tech detection - add new tech here
│   ├── hygiene.py       # Repo quality checks
│   ├── security.py      # Security scanning
│   └── size.py          # File size analysis
├── utils/               # Utilities
│   ├── fs.py            # Filesystem operations
│   └── patterns.py      # Tech patterns - add detection patterns
└── templates/           # Templates for auto-fix
```

## 🎨 Code Style

- **Python 3.10+**: Use modern Python features
- **Type hints**: Encouraged but not required
- **Docstrings**: For public functions and classes
- **Comments**: Explain "why", not "what"
- **Line length**: ~100 characters (flexible)
- **Imports**: Stdlib only (core requirement)

**Example:**

```python
def check_tech_stack(project_meta: dict) -> dict:
    """
    Detect technologies used in a project.
    
    Args:
        project_meta: Dictionary with project metadata
        
    Returns:
        Dictionary with detected technologies
    """
    detected = []
    
    # Check for package managers first (most reliable)
    if 'package.json' in project_meta['files']:
        detected.append('Node.js')
    
    return {'technologies': detected}
```

## 🧪 Testing Your Changes

### Manual Testing Checklist

- [ ] CLI works on multiple project types
- [ ] GUI launches without errors
- [ ] New features work on examples/
- [ ] No new critical issues in self-scan
- [ ] Works on Windows/Linux/macOS (if possible)
- [ ] JSON output is valid
- [ ] Auto-fix doesn't break existing files

### Example Projects

Use `examples/` for testing:

```bash
# Python project with security issue
python devpulse.py scan --path examples/python-app

# Web project with HTML/CSS/JS
python devpulse.py scan --path examples/web-app
```

## 🎯 Areas for Contribution

### 🔍 Tech Stack Detection

Add support for new languages/frameworks in `utils/patterns.py`:

```python
STACK_PATTERNS = {
    'Languages': {
        'Ruby': ['Gemfile', '*.rb'],
        # Add more...
    }
}
```

### 🔐 Security Checks

Enhance security scanning in `checks/security.py`:
- New secret patterns
- File permission checks
- Dependency vulnerability detection

### 📋 Hygiene Checks

Add new quality checks in `checks/hygiene.py`:
- Code coverage requirements
- Documentation completeness
- Branch protection rules

### 🎨 GUI Improvements

Enhance the GUI in `devpulse_gui.py`:
- Better visualizations
- Export formats (PDF, HTML)
- Dark mode
- Settings persistence

### 📚 Documentation

- Improve existing docs
- Add tutorials
- Create video guides
- Translate to other languages

## 🐛 Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml):

1. Clear description
2. Steps to reproduce
3. Expected vs actual behavior
4. Python version & OS
5. DevPulse version

## ✨ Requesting Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml):

1. Problem statement
2. Proposed solution
3. Use cases
4. Alternative approaches

## 📋 Pull Request Process

1. **Fill out the PR template** completely
2. **Link related issues** (Fixes #123)
3. **Pass CI checks** (all workflows must pass)
4. **Include test results** (DevPulse scan output)
5. **Respond to feedback** within 7 days
6. **Update documentation** if needed

### PR Review Criteria

✅ **Must Have:**
- Clear description
- Working functionality
- No breaking changes (unless discussed)
- DevPulse self-check passes

✨ **Nice to Have:**
- Tests or test results
- Documentation updates
- Examples for new features

## 🔄 CI/CD Workflows

All PRs trigger:
- Multi-OS testing (Ubuntu, Windows, macOS)
- Python 3.10, 3.11, 3.12 compatibility
- Linting (flake8, black, isort)
- Security scanning (bandit, CodeQL)
- Dogfooding (DevPulse scans itself)

See [.github/workflows/README.md](.github/workflows/README.md) for details.

## 🤝 Code Review

We value:
- **Respectful feedback**
- **Constructive suggestions**
- **Learning opportunities**
- **Collaborative problem-solving**

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

- **Open an issue** for questions
- **Start a discussion** for ideas
- **Check existing issues** first

## 🙏 Thank You!

Every contribution helps make DevPulse better for everyone. Whether it's code, documentation, bug reports, or feature ideas - all contributions are valued and appreciated!

---

**Happy coding! 🚀**

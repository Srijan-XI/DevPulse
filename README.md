# DevPulse 🩺

**A local-first development project health checker built with GitHub Copilot CLI**

DevPulse is a zero-configuration CLI tool that scans your codebase to detect tech stack, check repository hygiene, find potential security issues, and suggest improvements—all in seconds.

## 🎯 Philosophy

- **Local-first**: All analysis happens on your machine, no data leaves
- **Read-only by default**: Safe scanning with no modifications unless explicitly requested
- **Zero configuration**: Just point and scan
- **Fast**: Analysis completes in seconds, not minutes

## ✨ Features

- �️ **Dual Interface**: Modern GUI and powerful CLI
- 🔍 **Tech Stack Detection**: Automatically identifies your project's technologies (Node.js, Python, Java, Docker, etc.)
- 📋 **Repository Hygiene**: Checks for README, LICENSE, .gitignore, and tests
- 🔐 **Security Scanning**: Detects potential secrets and exposed credentials (basic local scanning)
- 📊 **File Size Analysis**: Identifies large files that might need attention
- 🔧 **Safe Auto-fixes**: Automatically generates missing README, LICENSE, and .gitignore files
- 📤 **Multiple Output Formats**: Human-readable terminal output or JSON for automation
- 📊 **Visual Statistics**: GUI shows summary cards with critical issues, warnings, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd cli

# No external dependencies needed! Uses only Python standard library
```

### Usage

**GUI Version (Recommended for beginners):**
```bash
python devpulse_gui.py
```
- Visual interface with summary cards
- One-click scanning and fixing
- Export results to JSON
- Copy reports to clipboard

**CLI Version (For automation & CI/CD):**

**Scan a project:**
```bash
python devpulse.py scan                    # Scan current directory
python devpulse.py scan --path /my/project # Scan specific directory
python devpulse.py scan --json             # Output as JSON
```

**Apply safe fixes:**
```bash
python devpulse.py fix --safe              # Apply all safe fixes automatically
python devpulse.py fix --interactive       # Ask before each fix
```

## 📖 Example Output

```
============================================================
DevPulse Report — /my/awesome-project
============================================================

Tech Stack & Info:
  ✓ Node.js
  ✓ Docker
  ✓ GitHub Actions
  ℹ Total size: 45.67 MB (234 files)

Warnings:
  ⚠ Missing LICENSE file
  ⚠ Found 15 TODO/FIXME comments
  ⚠ Large Files: 2 file(s) larger than 10.00 MB

Critical Issues:
  🚨 .env file exists but may not be in .gitignore

Summary:
  Total checks: 8
  Critical: 1
  Warnings: 3

💡 1 issue(s) can be auto-fixed with: devpulse fix --safe
============================================================
```

## 🏗️ Project Structure

```
cli/
├── devpulse.py          # CLI entry point
├── devpulse_gui.py      # GUI application (tkinter)
├── core/                # Core functionality
│   ├── scanner.py       # Orchestrates all checks
│   ├── reporter.py      # Formats output
│   └── fixer.py         # Applies fixes
├── checks/              # Health check modules
│   ├── stack.py         # Tech stack detection
│   ├── hygiene.py       # Repo hygiene checks
│   ├── security.py      # Local secret scanning
│   └── size.py          # Large file detection
├── utils/               # Utility functions
│   ├── fs.py            # Filesystem operations
│   └── patterns.py      # Pattern matching & detection
├── templates/           # File templates for fixes
│   ├── README.md        # README template
│   ├── gitignore.txt    # .gitignore template
│   └── LICENSE.txt      # MIT license template
├── docs/                # Documentation
│   ├── QUICKSTART.md    # Quick start guide
│   ├── USAGE.md         # Comprehensive CLI usage
│   ├── GUI-GUIDE.md     # GUI user guide
│   ├── DEVELOPMENT.md   # Technical docs
│   ├── ARCHITECTURE.md  # Architecture diagrams
│   └── ...              # More documentation
└── examples/            # Example projects
    ├── python-app/      # Python/Flask example
    └── web-app/         # HTML/CSS/JS example
```

## 🎯 What DevPulse Is (and Isn't)

### DevPulse IS:
- A quick health check for local projects
- A repository hygiene auditor
- A basic local secret detector
- A project initialization helper

### DevPulse IS NOT:
- A replacement for CI/CD pipelines (GitHub Actions, etc.)
- A deep security scanner (use dedicated tools like Snyk, GitGuardian)
- A code quality analyzer (use linters, formatters)
- A build tool

## 🛡️ Security Note

DevPulse performs **basic local scanning** for common secret patterns. It's designed to catch obvious mistakes (like committed `.env` files), not to provide comprehensive security analysis. Always use dedicated security tools for production environments.

## 📖 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) folder:

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 2 minutes
- **[CLI Usage](docs/USAGE.md)** - Comprehensive command-line examples
- **[GUI Guide](docs/GUI-GUIDE.md)** - Complete GUI user manual
- **[Development Docs](docs/DEVELOPMENT.md)** - Technical architecture
- **[Architecture Diagrams](docs/ARCHITECTURE.md)** - Visual system design
- **[Challenge Submission](docs/CHALLENGE.md)** - GitHub Copilot CLI Challenge
- **[Project Summary](docs/PROJECT-SUMMARY.md)** - Overview and statistics
- **[File Index](docs/INDEX.md)** - Complete file reference

## 🧪 Example Projects

Test DevPulse on the example projects in [`examples/`](examples/):

```bash
# Python Flask app with security issues
python devpulse.py scan --path examples/python-app

# HTML/CSS/JS web application
python devpulse.py scan --path examples/web-app
```

See [examples/README.md](examples/README.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built entirely with **GitHub Copilot CLI**
- Designed to showcase Copilot CLI's ability to rapidly build useful developer tools
- Inspired by the need for quick, local project health checks
# DevPulse

# DevPulse - File Index

## 📋 Documentation Files

| File | Description | Read Time |
|------|-------------|-----------|
| [README.md](../README.md) | Main project documentation, features, quick start | 5 min |
| [QUICKSTART.md](QUICKSTART.md) | Get started in 2 minutes (GUI + CLI) | 2 min |
| [GUI-GUIDE.md](GUI-GUIDE.md) | Complete GUI user guide with workflows | 10 min |
| [GUI-SCREENSHOTS.md](GUI-SCREENSHOTS.md) | Visual GUI documentation and features | 5 min |
| [USAGE.md](USAGE.md) | Comprehensive CLI usage examples | 10 min |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Technical architecture and design decisions | 8 min |
| [CHALLENGE.md](CHALLENGE.md) | GitHub Copilot CLI Challenge submission | 7 min |
| [PROJECT-SUMMARY.md](PROJECT-SUMMARY.md) | High-level overview and statistics | 5 min |

## 🔧 Core Application Files

| File | Purpose | Lines |
|------|---------|-------|
| [devpulse.py](../devpulse.py) | CLI entry point, argument parsing | ~150 |
| [devpulse_gui.py](../devpulse_gui.py) | GUI application (tkinter) | ~450 |
| [core/scanner.py](../core/scanner.py) | Orchestrates all checks | ~60 |
| [core/reporter.py](../core/reporter.py) | Formats terminal and JSON output | ~135 |
| [core/fixer.py](../core/fixer.py) | Applies safe auto-fixes | ~115 |

## ✅ Check Modules

| File | Purpose | Lines |
|------|---------|-------|
| [checks/stack.py](../checks/stack.py) | Tech stack detection | ~40 |
| [checks/hygiene.py](../checks/hygiene.py) | Repository hygiene checks | ~70 |
| [checks/security.py](../checks/security.py) | Basic security scanning | ~90 |
| [checks/size.py](../checks/size.py) | File size analysis | ~60 |

## 🛠️ Utility Modules

| File | Purpose | Lines |
|------|---------|-------|
| [utils/fs.py](../utils/fs.py) | Filesystem operations and project walking | ~110 |
| [utils/patterns.py](../utils/patterns.py) | Pattern matching and detection logic | ~165 |

## 📝 Template Files

| File | Purpose |
|------|---------|
| [templates/README.md](../templates/README.md) | README template for new projects |
| [templates/LICENSE.txt](../templates/LICENSE.txt) | MIT License template |
| [templates/gitignore.txt](../templates/gitignore.txt) | Comprehensive .gitignore template |

## 🧪 Example Projects

| File | Purpose |
|------|---------|
| [examples/python-app/](../examples/python-app/) | Sample Python/Flask project for testing |
| [examples/python-app/app.py](../examples/python-app/app.py) | Simple Flask app with TODO comments |
| [examples/python-app/requirements.txt](../examples/python-app/requirements.txt) | Python dependencies |
| [examples/python-app/.env](../examples/python-app/.env) | Environment file (for security testing) |
| [examples/web-app/](../examples/web-app/) | Sample HTML/CSS/JS web application |
| [examples/web-app/index.html](../examples/web-app/index.html) | HTML landing page |
| [examples/web-app/styles.css](../examples/web-app/styles.css) | CSS styling |
| [examples/web-app/app.js](../examples/web-app/app.js) | JavaScript functionality |
| [examples/README.md](../examples/README.md) | Examples documentation |

## 📦 Project Files

| File | Purpose |
|------|---------|
| [.gitignore](../.gitignore) | Git ignore rules (auto-generated) |
| [LICENSE](../LICENSE) | MIT License (auto-generated) |
| [challenge.txt](../challenge.txt) | Original challenge prompt |
| [draft.md](../draft.md) | Initial planning and framework |

## 🎯 Quick Navigation

### For First-Time Users
1. Start with [QUICKSTART.md](QUICKSTART.md)
2. Launch GUI: `python devpulse_gui.py`
3. Browse to a project and scan
4. Review [GUI-GUIDE.md](GUI-GUIDE.md) for details

### For Detailed Usage
1. Read [USAGE.md](USAGE.md)
2. Explore examples
3. Try different commands

### For Technical Understanding
1. Read [DEVELOPMENT.md](DEVELOPMENT.md)
2. Explore [core/](core/) directory
3. Review [checks/](checks/) modules

### For Challenge Judges
1. Read [CHALLENGE.md](CHALLENGE.md)
2. Review [PROJECT-SUMMARY.md](PROJECT-SUMMARY.md)
3. Try the tool: `python devpulse.py scan`

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| **Total Files** | 30 |
| **Python Modules** | 13 |
| **Documentation Pages** | 6 |
| **Template Files** | 3 |
| **Test Examples** | 4 |
| **Total Size** | ~74 KB |
| **Lines of Code** | ~1,200 |

## 🚀 Essential Commands
**GUI Version:**
```bash
# Launch GUI
python devpulse_gui.py

# Then use visual interface:
# 1. Browse to project
# 2. Click "Scan Project"
# 3. Click "Fix Issues"
# 4. Export or copy results
```

**CLI Version:**

```bash
# Scan current directory
python devpulse.py scan

# Scan specific project
python devpulse.py scan --path /path/to/project

# Get JSON output
python devpulse.py scan --json

# Auto-fix issues
python devpulse.py fix --safe

# Interactive fixing
python devpulse.py fix --interactive

# Get help
python devpulse.py --help
```

## 🏗️ Directory Structure

```
cli/
├── 📄 devpulse.py              # Main entry point
├── 📁 core/                    # Core functionality
│   ├── scanner.py
│   ├── reporter.py
│   └── fixer.py
├── 📁 checks/                  # Check modules
│   ├── stack.py
│   ├── hygiene.py
│   ├── security.py
│   └── size.py
├── 📁 utils/                   # Utility functions
│   ├── fs.py
│   └── patterns.py
├── 📁 templates/               # Fix templates
│   ├── README.md
│   ├── LICENSE.txt
│   └── gitignore.txt
├── 📁 test-examples/           # Test projects
│   └── python-app/
├── 📁 docs/                    # Documentation
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── USAGE.md
│   ├── DEVELOPMENT.md
│   ├── CHALLENGE.md
│   └── PROJECT-SUMMARY.md
└── 📄 .gitignore              # Git ignore file
```

## 🔍 Code Overview

### Module Dependencies

```
devpulse.py
    ├── core/scanner.py
    │   ├── utils/fs.py
    │   ├── checks/stack.py
    │   │   └── utils/patterns.py
    │   ├── checks/hygiene.py
    │   │   └── utils/patterns.py
    │   ├── checks/security.py
    │   │   └── utils/patterns.py
    │   └── checks/size.py
    │       └── utils/fs.py
    ├── core/reporter.py
    └── core/fixer.py
```

### Key Design Patterns

1. **Composable Checks**: Each check is independent
2. **Single Metadata Collection**: Scanned once, used by all checks
3. **Standardized Results**: All checks return same format
4. **Safe by Default**: Read-only unless explicitly fixing
5. **Dual Output**: Terminal + JSON formats

## 💡 Tips

- **New to DevPulse?** → Start with [QUICKSTART.md](QUICKSTART.md)
- **Want examples?** → Read [USAGE.md](USAGE.md)
- **Technical details?** → See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Evaluating for challenge?** → Check [CHALLENGE.md](CHALLENGE.md)

---

**Built with GitHub Copilot CLI in ~80 minutes** 🚀

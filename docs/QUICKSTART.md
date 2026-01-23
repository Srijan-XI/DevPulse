# DevPulse - Quick Start Guide

## 1. Installation (30 seconds)

No installation needed! Just Python 3.10+

```bash
# Verify Python version
python --version  # Should be 3.10 or higher

# Navigate to DevPulse directory
cd /path/to/devpulse
```

## 2. Choose Your Interface

### Option A: GUI (Recommended for Beginners)

```bash
# Launch GUI
python devpulse_gui.py
```

**The GUI window opens with:**
- Visual summary cards
- One-click scanning
- Interactive fix buttons
- Export and copy features

**Usage:**
1. Click "Browse..." to select your project
2. Click "🔍 Scan Project"
3. View results in Summary tab
4. Click "🔧 Fix Issues" to auto-fix
5. Done! ✅

### Option B: CLI (For Automation)

```bash
# Scan current directory
python devpulse.py scan
```

**You'll see:**
- Tech stack detected
- Missing files (README, LICENSE, .gitignore)
- Potential security issues
- File size analysis

## 3. Fix Issues (30 seconds)

```bash
# Auto-fix safe issues
python devpulse.py fix --safe
```

**This creates:**
- ✓ README.md
- ✓ LICENSE
- ✓ .gitignore

## 4. Verify (15 seconds)

```bash
# Scan again to verify fixes
python devpulse.py scan
```

You should see fewer warnings!

## That's It! 🎉

In under 2 minutes, you've:
1. Scanned your project for issues
2. Auto-fixed common problems
3. Improved your project health

## Next Steps

### Scan Other Projects

```bash
python devpulse.py scan --path ~/projects/my-app
```

### Get JSON Output

```bash
python devpulse.py scan --json > report.json
```

### Interactive Fixing

```bash
python devpulse.py fix --interactive
```

## Common Use Cases

### New Project Setup
```bash
mkdir my-new-project
cd my-new-project
git init
python /path/to/devpulse.py fix --safe
# You now have README, LICENSE, .gitignore!
```

### Pre-Commit Check
```bash
python devpulse.py scan
# Exit code 0 = good, 1 = critical issues
```

### Team Onboarding
```bash
# New team member checks project health
python devpulse.py scan
# Instantly see tech stack and issues
```

## Understanding the Output

### Status Icons
- ✓ = OK
- ℹ = Info
- ⚠ = Warning
- 🚨 = Critical

### Example Output
```
Tech Stack & Info:
  ✓ Python          # Detected from requirements.txt
  ✓ Docker          # Detected from Dockerfile
  
Warnings:
  ⚠ Missing LICENSE  # Should add one
  
Critical:
  🚨 .env not in .gitignore  # Security risk!
```

## Tips

1. **Run regularly** - Make it part of your workflow
2. **Before committing** - Catch issues early
3. **CI/CD integration** - Use JSON output
4. **Share with team** - Everyone benefits

## Need Help?

```bash
python devpulse.py --help
python devpulse.py scan --help
python devpulse.py fix --help
```

## Full Documentation

- [README.md](README.md) - Full feature list
- [USAGE.md](USAGE.md) - Comprehensive examples
- [DEVELOPMENT.md](DEVELOPMENT.md) - How it works

---

**Start scanning in 30 seconds! 🚀**

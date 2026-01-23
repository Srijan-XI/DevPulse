# Example Projects

This directory contains sample projects for testing DevPulse's capabilities.

## Available Examples

### 1. Python App (`python-app/`)
A simple Flask application demonstrating:
- Python tech stack detection
- Security issue detection (.env file)
- TODO/FIXME comment tracking

### 2. Web App (`web-app/`)
A static website demonstrating:
- HTML, CSS, JavaScript detection
- Frontend project structure
- Basic web development patterns

## Usage

Test DevPulse on these examples:

```bash
# Scan Python app
python devpulse.py scan --path examples/python-app

# Scan Web app
python devpulse.py scan --path examples/web-app

# Or use the GUI
python devpulse_gui.py
# Then browse to examples/python-app or examples/web-app
```

## What DevPulse Detects

### Python App
- ✓ Python
- ✓ Flask
- ✓ pip
- 🚨 .env file not in .gitignore (critical)
- ⚠ Missing README, LICENSE, .gitignore

### Web App
- ✓ HTML
- ✓ CSS  
- ✓ JavaScript
- ⚠ Missing README, LICENSE, .gitignore

## Adding Your Own Examples

Feel free to add more example projects here to test DevPulse's detection capabilities!

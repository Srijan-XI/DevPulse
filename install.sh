#!/bin/bash
# ============================================================
# DevPulse Installation Script
# ============================================================
# This script checks Python installation and optionally
# installs documentation requirements.
# ============================================================

echo ""
echo "============================================================"
echo "DevPulse Installation"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora/RHEL:   sudo dnf install python3 python3-pip"
    echo "  macOS:         brew install python3"
    echo ""
    exit 1
fi

# Get Python version
echo "[INFO] Checking Python version..."
python3 --version
echo ""

# Check Python version (requires 3.10+)
python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] Python 3.10 or higher is recommended"
    echo "Current version may not be compatible"
    echo ""
fi

echo "[SUCCESS] Python is installed and ready!"
echo ""

# Main application has no dependencies
echo "============================================================"
echo "DevPulse Core Application"
echo "============================================================"
echo ""
echo "The core DevPulse application requires NO external dependencies!"
echo "It uses only Python standard library."
echo ""
echo "You can start using DevPulse right away with:"
echo "  - ./start.sh (interactive launcher)"
echo "  - python3 devpulse.py scan"
echo "  - python3 devpulse_gui.py"
echo ""

# Ask about documentation requirements
echo "============================================================"
echo "Optional: Documentation Requirements"
echo "============================================================"
echo ""
read -p "Do you want to install documentation tools (MkDocs)? (y/N): " INSTALL_DOCS

if [[ "$INSTALL_DOCS" =~ ^[Yy]$ ]]; then
    echo ""
    echo "[INFO] Installing documentation requirements..."
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null; then
        echo "[ERROR] pip3 is not installed"
        echo "Please install pip3 and try again"
        exit 1
    fi
    
    pip3 install -r requirements-docs.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install documentation requirements"
        echo ""
        exit 1
    fi
    echo ""
    echo "[SUCCESS] Documentation tools installed!"
    echo "You can now build docs with: mkdocs serve"
    echo ""
else
    echo ""
    echo "[INFO] Skipping documentation tools installation"
    echo ""
fi

echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Quick Start:"
echo "  1. Run \"./start.sh\" for interactive launcher"
echo "  2. OR run \"python3 devpulse.py scan\" for CLI"
echo "  3. OR run \"python3 devpulse_gui.py\" for GUI"
echo ""
echo "For more information, see README.md"
echo ""

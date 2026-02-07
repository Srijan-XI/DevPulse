#!/bin/bash
# ============================================================
# DevPulse Launcher
# ============================================================
# Interactive launcher for DevPulse CLI and GUI
# ============================================================

show_menu() {
    clear
    echo ""
    echo "============================================================"
    echo "DevPulse - Project Health Checker"
    echo "============================================================"
    echo ""
    echo "Please select an option:"
    echo ""
    echo "  1. Launch GUI (Graphical Interface)"
    echo "  2. Scan Current Directory (CLI)"
    echo "  3. Scan Specific Directory (CLI)"
    echo "  4. Fix Issues in Current Directory (CLI)"
    echo "  5. Show Help"
    echo "  6. Exit"
    echo ""
    echo "============================================================"
    echo ""
}

launch_gui() {
    clear
    echo ""
    echo "============================================================"
    echo "Launching DevPulse GUI..."
    echo "============================================================"
    echo ""
    python3 devpulse_gui.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] Failed to launch GUI"
        echo "Make sure Python 3 and tkinter are installed"
        echo ""
        read -p "Press Enter to continue..."
    fi
}

scan_current() {
    clear
    echo ""
    echo "============================================================"
    echo "Scanning Current Directory..."
    echo "============================================================"
    echo ""
    python3 devpulse.py scan
    echo ""
    echo "============================================================"
    echo "Scan Complete!"
    echo "============================================================"
    echo ""
    read -p "Press Enter to continue..."
}

scan_custom() {
    clear
    echo ""
    echo "============================================================"
    echo "Scan Specific Directory"
    echo "============================================================"
    echo ""
    read -p "Enter the path to scan (or press Enter to cancel): " SCAN_PATH
    
    if [ -z "$SCAN_PATH" ]; then
        echo "[INFO] Cancelled"
        read -p "Press Enter to continue..."
        return
    fi
    
    echo ""
    echo "[INFO] Scanning: $SCAN_PATH"
    echo ""
    python3 devpulse.py scan --path "$SCAN_PATH"
    echo ""
    echo "============================================================"
    echo "Scan Complete!"
    echo "============================================================"
    echo ""
    read -p "Press Enter to continue..."
}

fix_issues() {
    clear
    echo ""
    echo "============================================================"
    echo "Fix Issues in Current Directory"
    echo "============================================================"
    echo ""
    echo "This will apply safe fixes (generate missing README, LICENSE, .gitignore)"
    echo ""
    read -p "Continue? (y/N): " CONFIRM
    
    if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
        echo "[INFO] Cancelled"
        read -p "Press Enter to continue..."
        return
    fi
    
    echo ""
    echo "[INFO] Applying safe fixes..."
    echo ""
    python3 devpulse.py fix --safe
    echo ""
    echo "============================================================"
    echo "Fix Complete!"
    echo "============================================================"
    echo ""
    read -p "Press Enter to continue..."
}

show_help() {
    clear
    echo ""
    echo "============================================================"
    echo "DevPulse Help"
    echo "============================================================"
    echo ""
    echo "DevPulse is a local-first development project health checker"
    echo "that scans your codebase to detect tech stack, check hygiene,"
    echo "find security issues, and suggest improvements."
    echo ""
    echo "============================================================"
    echo "Features:"
    echo "============================================================"
    echo "  - Tech Stack Detection (Node.js, Python, Docker, etc.)"
    echo "  - Repository Hygiene Checks (README, LICENSE, .gitignore)"
    echo "  - Security Scanning (potential secrets, .env files)"
    echo "  - File Size Analysis (large files detection)"
    echo "  - Auto-Fix Capabilities (safe, non-destructive)"
    echo ""
    echo "============================================================"
    echo "Command-Line Usage:"
    echo "============================================================"
    echo "  Scan current directory:"
    echo "    python3 devpulse.py scan"
    echo ""
    echo "  Scan specific directory:"
    echo "    python3 devpulse.py scan --path /my/project"
    echo ""
    echo "  Output as JSON:"
    echo "    python3 devpulse.py scan --json"
    echo ""
    echo "  Apply safe fixes:"
    echo "    python3 devpulse.py fix --safe"
    echo ""
    echo "  Interactive fixes:"
    echo "    python3 devpulse.py fix --interactive"
    echo ""
    echo "============================================================"
    echo "For more information, see README.md"
    echo "============================================================"
    echo ""
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-6): " CHOICE
    
    case $CHOICE in
        1)
            launch_gui
            ;;
        2)
            scan_current
            ;;
        3)
            scan_custom
            ;;
        4)
            fix_issues
            ;;
        5)
            show_help
            ;;
        6)
            clear
            echo ""
            echo "Thank you for using DevPulse!"
            echo ""
            exit 0
            ;;
        *)
            echo ""
            echo "[ERROR] Invalid choice. Please enter a number between 1 and 6."
            echo ""
            read -p "Press Enter to continue..."
            ;;
    esac
done

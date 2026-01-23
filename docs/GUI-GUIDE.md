# DevPulse GUI - User Guide

## Overview

DevPulse GUI provides a visual, user-friendly interface to scan projects, view results, and fix issues with just a few clicks.

## Launching the GUI

```bash
python devpulse_gui.py
```

The GUI window will open automatically.

## Interface Overview

### 1. Project Selection (Top Bar)

```
┌─────────────────────────────────────────────────────────┐
│ Project Path: [/path/to/project]  [Browse...]           │
└─────────────────────────────────────────────────────────┘
```

- **Path Field**: Shows the current project path
- **Browse Button**: Opens a folder browser to select a different project

### 2. Action Buttons

```
┌──────────────────────────────────────────────────────────┐
│ [🔍 Scan Project] [🔧 Fix Issues] [💾 Export JSON] [📋 Copy Report] │
└──────────────────────────────────────────────────────────┘
```

- **🔍 Scan Project**: Analyzes the selected project
- **🔧 Fix Issues**: Automatically fixes detected issues (enabled after scan)
- **💾 Export JSON**: Saves results as JSON file
- **📋 Copy Report**: Copies terminal-style report to clipboard

### 3. Tabs

#### **Summary Tab**

Displays statistics in visual cards:

```
┌─────────────────┬─────────────────┬─────────────────┐
│ Critical Issues │    Warnings     │   Info Items    │
│       0         │       3         │       2         │
└─────────────────┴─────────────────┴─────────────────┘
┌─────────────────┬─────────────────┬─────────────────┐
│ Fixable Issues  │  Total Files    │  Project Size   │
│       3         │      150        │    12.45 MB     │
└─────────────────┴─────────────────┴─────────────────┘
```

**Color-coded cards:**
- 🔴 Critical Issues (Red)
- 🟡 Warnings (Yellow)
- 🔵 Info Items (Blue)
- 🟢 Fixable Issues (Green)
- ⚫ File Stats (Gray)

#### **Detailed Results Tab**

Shows all check results in a table:

```
┌──────┬──────────┬─────────────────┬──────────────────┬──────────┐
│      │ Status   │ Check Name      │ Details          │ Fixable  │
├──────┼──────────┼─────────────────┼──────────────────┼──────────┤
│ ⚠    │ WARNING  │ Missing README  │ README.md not... │ ✓        │
│ ⚠    │ WARNING  │ Missing LICENSE │ LICENSE file ... │ ✓        │
│ 🚨   │ CRITICAL │ .env exposed    │ .env exists b... │          │
└──────┴──────────┴─────────────────┴──────────────────┴──────────┘
```

**Features:**
- Sortable columns
- Color-coded status
- Scrollable view
- Full details visible

#### **Tech Stack Tab**

Displays detected technologies and project information:

```
Detected Technologies:

  ✓ Python
  ✓ Docker
  ✓ GitHub Actions

Project Information:

  Files: 150
  Size: 12.45 MB

File Types:

  .py: 45 file(s)
  .js: 32 file(s)
  .json: 12 file(s)
```

## Step-by-Step Guide

### Scanning a Project

1. **Select Project**
   - Click **Browse...** to choose a project folder
   - Or manually edit the path field

2. **Run Scan**
   - Click **🔍 Scan Project**
   - Progress bar shows scanning activity
   - Status bar shows "Scanning project..."

3. **View Results**
   - Summary cards update automatically
   - Switch between tabs to see different views
   - Detailed results show in table format

### Fixing Issues

1. **After Scanning**
   - If fixable issues exist, **🔧 Fix Issues** button becomes enabled

2. **Review Fixes**
   - Click **🔧 Fix Issues**
   - Dialog shows what will be fixed:
     ```
     DevPulse will fix 3 issue(s):
     
       • Missing README
       • Missing LICENSE
       • Missing .gitignore
     
     Proceed?
     ```

3. **Apply Fixes**
   - Click **Yes** to apply fixes
   - Success message shows what was created
   - Project automatically rescans to update results

### Exporting Results

#### Export as JSON

1. Click **💾 Export JSON**
2. Choose save location and filename
3. JSON file contains complete scan results

**Use cases:**
- Share with team members
- Import into other tools
- Archive historical scans
- CI/CD integration

#### Copy to Clipboard

1. Click **📋 Copy Report**
2. Terminal-style report copied to clipboard
3. Paste into emails, chat, documentation

**Example output:**
```
============================================================
DevPulse Report — /my/project
============================================================

Tech Stack & Info:
  ✓ Python
  ✓ Docker

Warnings:
  ⚠ Missing LICENSE

Summary:
  Total checks: 5
  Critical: 0
  Warnings: 1
============================================================
```

## Understanding the Interface

### Status Colors

| Color  | Meaning | Example |
|--------|---------|---------|
| 🔴 Red | Critical issue requiring immediate attention | `.env` file exposed |
| 🟡 Yellow | Warning that should be addressed | Missing README |
| 🔵 Blue | Informational (not an issue) | Tech stack detected |
| 🟢 Green | Positive/fixable | Can auto-fix this issue |

### Status Bar Messages

| Message | Meaning |
|---------|---------|
| "Ready..." | Application ready, no scan performed |
| "Scanning project..." | Scan in progress |
| "Scan complete: X warning(s) found." | Scan finished successfully |
| "Scan failed." | Error occurred during scan |

### Button States

- **Enabled** (normal color): Ready to click
- **Disabled** (grayed out): Action not available yet
  - Fix button disabled until scan finds fixable issues
  - Export/Copy disabled until scan completes

## Common Workflows

### Workflow 1: Quick Health Check

```
1. Launch GUI → python devpulse_gui.py
2. Browse to project folder
3. Click "Scan Project"
4. Review Summary tab
5. Done!
```

**Time: 30 seconds**

### Workflow 2: New Project Setup

```
1. Create new project folder
2. Open DevPulse GUI
3. Browse to new folder
4. Click "Scan Project" (will show missing files)
5. Click "Fix Issues"
6. Essential files created automatically
```

**Time: 1 minute**

### Workflow 3: Team Review

```
1. Scan project
2. Export JSON
3. Share JSON with team
4. Discuss critical issues in meeting
5. Fix issues collaboratively
6. Rescan to verify
```

### Workflow 4: Documentation

```
1. Scan project
2. Switch to Tech Stack tab
3. Copy report to clipboard
4. Paste into project documentation
5. Shows clear tech overview for new developers
```

## Tips & Tricks

### Keyboard Shortcuts

While the GUI doesn't have custom keyboard shortcuts, you can use:
- `Alt+F4` - Close window
- `Tab` - Navigate between controls
- `Enter` - Activate focused button
- `Ctrl+Tab` - Switch between tabs

### Performance

**For large projects (10,000+ files):**
- Scan may take 5-15 seconds
- GUI remains responsive during scan
- Progress bar shows activity
- Can be interrupted with window close

**For small projects (<100 files):**
- Scan completes in < 1 second
- Instant results

### Best Practices

1. **Regular Scans**
   - Scan before commits
   - Weekly health checks
   - After major changes

2. **Fix Incrementally**
   - Don't ignore warnings
   - Fix critical issues first
   - Address warnings over time

3. **Share Results**
   - Export JSON for team discussions
   - Copy reports for documentation
   - Track improvements over time

4. **Verify Fixes**
   - Always rescan after fixing
   - Check that issues are resolved
   - Review what was changed

## Troubleshooting

### "Path does not exist"

**Problem**: Selected path is invalid

**Solution**:
- Use Browse button to select valid folder
- Check for typos in manual path entry
- Ensure folder exists and is accessible

### "Scan failed"

**Problem**: Error during scanning

**Solution**:
- Check folder permissions
- Ensure Python has read access
- Try a different project
- Check error message details

### "No fixable issues"

**Problem**: Fix button enabled but nothing to fix

**Solution**:
- This is normal if issues aren't auto-fixable
- Some issues require manual intervention
- See Detailed Results for specifics

### GUI Freezes During Scan

**Problem**: Window appears unresponsive

**Solution**:
- Wait a few seconds - large projects take time
- Progress bar should be animated
- If truly frozen, close and restart
- Report bug with project details

## Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| **Visual Summary** | ✓ Cards and colors | Basic text |
| **Ease of Use** | ✓ Point and click | Command typing |
| **Automation** | Limited | ✓ Scriptable |
| **CI/CD Integration** | ❌ | ✓ Perfect |
| **Export Options** | JSON + Copy | JSON only |
| **Interactive Fixes** | ✓ One-click | Flag required |
| **Tech Stack View** | ✓ Formatted | Plain text |
| **Learning Curve** | Easy | Medium |

**When to use GUI:**
- Quick visual overview
- First-time users
- Manual reviews
- Demonstrating to stakeholders

**When to use CLI:**
- CI/CD pipelines
- Automation scripts
- Remote servers
- Batch processing

## Advanced Features

### Rescan Automation

After fixing issues, GUI automatically rescans to show updated results.

### Thread-Safe Scanning

Scan runs in background thread, keeping GUI responsive.

### Smart Button Management

Buttons enable/disable based on current state, preventing errors.

### Multi-Tab Organization

Separate views for different types of information:
- Summary: Quick overview
- Details: All findings
- Tech Stack: Technology info

## Accessibility

- Clear status messages for screen readers
- High-contrast color scheme
- Keyboard navigation support
- Progress indicators for operations

## Getting Help

1. Hover over buttons for tooltips (future enhancement)
2. Check status bar for current operation
3. Error dialogs provide specific messages
4. See main [README.md](README.md) for general help

---

**Enjoy the DevPulse GUI! 🎉**

Fast, visual project health checking in a user-friendly interface.

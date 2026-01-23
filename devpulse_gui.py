#!/usr/bin/env python3
"""
DevPulse GUI - Graphical interface for DevPulse project health checker.
"""

import sys
from tkinter import (Tk, StringVar, ttk, filedialog, messagebox, scrolledtext,
                     X, Y, LEFT, RIGHT, BOTTOM, BOTH, END, WORD, SUNKEN, DISABLED, NORMAL)
from pathlib import Path
import json
import threading

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.scanner import Scanner
from core.reporter import Reporter
from core.fixer import Fixer


class DevPulseGUI:
    """Main GUI application for DevPulse."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("DevPulse - Project Health Checker")
        self.root.geometry("900x700")
        
        # Current project path
        self.project_path = str(Path.cwd())
        
        # Scan results
        self.scanner = None
        self.results = []
        self.metadata = {}
        
        # Status symbols
        self.status_symbols = {
            'ok': '✓',
            'info': 'ℹ',
            'warning': '⚠',
            'critical': '🚨'
        }
        
        # Status colors
        self.status_colors = {
            'ok': '#28a745',
            'info': '#17a2b8',
            'warning': '#ffc107',
            'critical': '#dc3545'
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Top frame - Project selection
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=X)
        
        ttk.Label(top_frame, text="Project Path:").pack(side=LEFT, padx=(0, 5))
        
        self.path_var = StringVar(value=self.project_path)
        path_entry = ttk.Entry(top_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        ttk.Button(top_frame, text="Browse...", command=self.browse_folder).pack(side=LEFT, padx=5)
        
        # Action buttons frame
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=X)
        
        self.scan_button = ttk.Button(button_frame, text="🔍 Scan Project", command=self.scan_project)
        self.scan_button.pack(side=LEFT, padx=5)
        
        self.fix_button = ttk.Button(button_frame, text="🔧 Fix Issues", command=self.fix_issues, state=DISABLED)
        self.fix_button.pack(side=LEFT, padx=5)
        
        ttk.Button(button_frame, text="💾 Export JSON", command=self.export_json).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Copy Report", command=self.copy_report).pack(side=LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill=X, padx=10)
        
        # Status label
        self.status_var = StringVar(value="Ready. Select a project and click 'Scan Project'.")
        status_label = ttk.Label(self.root, textvariable=self.status_var, relief=SUNKEN)
        status_label.pack(fill=X, padx=10, pady=5)
        
        # Notebook for results
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Summary tab
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Summary")
        self.create_summary_tab()
        
        # Details tab
        self.details_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.details_frame, text="Detailed Results")
        self.create_details_tab()
        
        # Tech Stack tab
        self.tech_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tech_frame, text="Tech Stack")
        self.create_tech_tab()
    
    def create_summary_tab(self):
        """Create summary statistics tab."""
        # Summary cards frame
        cards_frame = ttk.Frame(self.summary_frame, padding="10")
        cards_frame.pack(fill=BOTH, expand=True)
        
        # Create summary cards
        self.critical_label = self.create_stat_card(cards_frame, "Critical Issues", "0", "#dc3545", 0, 0)
        self.warning_label = self.create_stat_card(cards_frame, "Warnings", "0", "#ffc107", 0, 1)
        self.info_label = self.create_stat_card(cards_frame, "Info Items", "0", "#17a2b8", 0, 2)
        self.fixable_label = self.create_stat_card(cards_frame, "Fixable Issues", "0", "#28a745", 1, 0)
        self.files_label = self.create_stat_card(cards_frame, "Total Files", "0", "#6c757d", 1, 1)
        self.size_label = self.create_stat_card(cards_frame, "Project Size", "0 B", "#6c757d", 1, 2)
        
        # Configure grid weights
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
    
    def create_stat_card(self, parent, title, value, color, row, col):
        """Create a statistics card."""
        frame = ttk.LabelFrame(parent, text=title, padding="10")
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        label = ttk.Label(frame, text=value, font=("Arial", 24, "bold"), foreground=color)
        label.pack()
        
        return label
    
    def create_details_tab(self):
        """Create detailed results tab."""
        # Create treeview for results
        tree_frame = ttk.Frame(self.details_frame)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=RIGHT, fill=Y)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=BOTTOM, fill=X)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("Status", "Name", "Details", "Fixable"), 
                                 yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill=BOTH, expand=True)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("#0", text="")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Name", text="Check Name")
        self.tree.heading("Details", text="Details")
        self.tree.heading("Fixable", text="Fixable")
        
        self.tree.column("#0", width=30, stretch=False)
        self.tree.column("Status", width=80, stretch=False)
        self.tree.column("Name", width=150)
        self.tree.column("Details", width=400)
        self.tree.column("Fixable", width=80, stretch=False)
        
        # Tags for colors
        for status, color in self.status_colors.items():
            self.tree.tag_configure(status, foreground=color)
    
    def create_tech_tab(self):
        """Create tech stack visualization tab."""
        self.tech_text = scrolledtext.ScrolledText(self.tech_frame, wrap=WORD, 
                                                    font=("Consolas", 10), height=20)
        self.tech_text.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.tech_text.insert(1.0, "No scan performed yet. Click 'Scan Project' to detect tech stack.")
        self.tech_text.config(state=DISABLED)
    
    def browse_folder(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(initialdir=self.project_path, title="Select Project Folder")
        if folder:
            self.project_path = folder
            self.path_var.set(folder)
    
    def scan_project(self):
        """Scan the selected project."""
        path = self.path_var.get()
        
        # Validate path
        if not Path(path).exists():
            messagebox.showerror("Error", f"Path does not exist: {path}")
            return
        
        if not Path(path).is_dir():
            messagebox.showerror("Error", f"Path is not a directory: {path}")
            return
        
        # Disable scan button and show progress
        self.scan_button.config(state=DISABLED)
        self.fix_button.config(state=DISABLED)
        self.progress.start()
        self.status_var.set("Scanning project...")
        
        # Run scan in background thread
        def run_scan():
            try:
                self.scanner = Scanner(path)
                self.results = self.scanner.scan()
                self.metadata = self.scanner.get_metadata()
                
                # Update UI in main thread
                self.root.after(0, self.update_results)
            except Exception as e:
                self.root.after(0, lambda: self.scan_error(str(e)))
        
        thread = threading.Thread(target=run_scan, daemon=True)
        thread.start()
    
    def scan_error(self, error_msg):
        """Handle scan error."""
        self.progress.stop()
        self.scan_button.config(state=NORMAL)
        self.status_var.set("Scan failed.")
        messagebox.showerror("Scan Error", f"Failed to scan project:\n{error_msg}")
    
    def update_results(self):
        """Update UI with scan results."""
        self.progress.stop()
        self.scan_button.config(state=NORMAL)
        
        # Check if there are fixable issues
        fixable_count = len([r for r in self.results if r.get('fixable')])
        if fixable_count > 0:
            self.fix_button.config(state=NORMAL)
        
        # Update summary statistics
        critical_count = len([r for r in self.results if r.get('status') == 'critical'])
        warning_count = len([r for r in self.results if r.get('status') == 'warning'])
        info_count = len([r for r in self.results if r.get('status') == 'info'])
        
        self.critical_label.config(text=str(critical_count))
        self.warning_label.config(text=str(warning_count))
        self.info_label.config(text=str(info_count))
        self.fixable_label.config(text=str(fixable_count))
        self.files_label.config(text=str(self.metadata.get('file_count', 0)))
        
        # Format size
        size_bytes = self.metadata.get('total_size', 0)
        size_str = self.format_size(size_bytes)
        self.size_label.config(text=size_str)
        
        # Update details treeview
        self.tree.delete(*self.tree.get_children())
        
        for result in self.results:
            status = result.get('status', 'info')
            symbol = self.status_symbols.get(status, '')
            name = result.get('name', 'Unknown')
            details = result.get('details', '')
            fixable = '✓' if result.get('fixable') else ''
            
            self.tree.insert('', END, text=symbol, 
                           values=(status.upper(), name, details, fixable),
                           tags=(status,))
        
        # Update tech stack tab
        self.update_tech_stack()
        
        # Update status
        if critical_count > 0:
            self.status_var.set(f"Scan complete: {critical_count} critical issue(s) found!")
        elif warning_count > 0:
            self.status_var.set(f"Scan complete: {warning_count} warning(s) found.")
        else:
            self.status_var.set("Scan complete: No issues found!")
    
    def update_tech_stack(self):
        """Update tech stack visualization."""
        self.tech_text.config(state=NORMAL)
        self.tech_text.delete(1.0, END)
        
        # Get tech stack info
        tech_result = next((r for r in self.results if r.get('name') == 'Tech Stack'), None)
        
        if tech_result and tech_result.get('data'):
            tech_stack = tech_result['data']
            
            self.tech_text.insert(END, "Detected Technologies:\n\n", "header")
            for tech in tech_stack:
                self.tech_text.insert(END, f"  ✓ {tech}\n", "tech")
            
            self.tech_text.insert(END, f"\n\nProject Information:\n\n", "header")
            self.tech_text.insert(END, f"  Files: {self.metadata.get('file_count', 0)}\n")
            self.tech_text.insert(END, f"  Size: {self.format_size(self.metadata.get('total_size', 0))}\n")
            
            # Show file extensions
            extensions = self.metadata.get('extensions', {})
            if extensions:
                self.tech_text.insert(END, f"\n\nFile Types:\n\n", "header")
                sorted_ext = sorted(extensions.items(), key=lambda x: x[1], reverse=True)
                for ext, count in sorted_ext[:10]:
                    self.tech_text.insert(END, f"  {ext}: {count} file(s)\n")
        else:
            self.tech_text.insert(END, "No technology stack detected.\n\n")
            self.tech_text.insert(END, "This might be a general-purpose project or using ")
            self.tech_text.insert(END, "technologies not yet recognized by DevPulse.")
        
        # Configure tags
        self.tech_text.tag_config("header", font=("Arial", 12, "bold"))
        self.tech_text.tag_config("tech", foreground="#28a745", font=("Consolas", 10))
        
        self.tech_text.config(state=DISABLED)
    
    def fix_issues(self):
        """Fix issues interactively."""
        if not self.results:
            messagebox.showwarning("No Results", "Please scan a project first.")
            return
        
        fixable = [r for r in self.results if r.get('fixable')]
        
        if not fixable:
            messagebox.showinfo("No Fixable Issues", "No issues can be automatically fixed.")
            return
        
        # Ask for confirmation
        msg = f"DevPulse will fix {len(fixable)} issue(s):\n\n"
        for result in fixable:
            msg += f"  • {result.get('name')}\n"
        msg += "\nProceed?"
        
        if messagebox.askyesno("Fix Issues", msg):
            try:
                fixer = Fixer(self.path_var.get(), interactive=False)
                fixes_applied = fixer.fix(self.results)
                
                if fixes_applied:
                    msg = "✓ Fixes applied:\n\n"
                    for fix in fixes_applied:
                        msg += f"  • {fix}\n"
                    messagebox.showinfo("Success", msg)
                    
                    # Rescan to update results
                    self.scan_project()
                else:
                    messagebox.showinfo("Info", "No fixes were applied.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply fixes:\n{e}")
    
    def export_json(self):
        """Export results as JSON."""
        if not self.results:
            messagebox.showwarning("No Results", "Please scan a project first.")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="devpulse-report.json"
        )
        
        if filename:
            try:
                reporter = Reporter(self.results, self.metadata)
                json_output = reporter.report_json()
                
                with open(filename, 'w') as f:
                    f.write(json_output)
                
                messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{e}")
    
    def copy_report(self):
        """Copy terminal report to clipboard."""
        if not self.results:
            messagebox.showwarning("No Results", "Please scan a project first.")
            return
        
        try:
            reporter = Reporter(self.results, self.metadata)
            terminal_output = reporter.report_terminal()
            
            self.root.clipboard_clear()
            self.root.clipboard_append(terminal_output)
            
            messagebox.showinfo("Success", "Report copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy:\n{e}")
    
    def format_size(self, size_bytes):
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


def main():
    """Main entry point for GUI."""
    root = Tk()
    DevPulseGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

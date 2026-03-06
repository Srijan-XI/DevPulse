"""Code cohesion and coupling checks."""

from typing import List, Dict, Any
import re
from pathlib import Path

def run_cohesion_check(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check for code cohesion and coupling issues.
    
    Args:
        metadata: Project metadata from scanner
        
    Returns:
        List of check results
    """
    results = []
    files = metadata.get('files', [])
    
    high_coupling_files = []
    low_cohesion_files = []
    
    for file_path in files:
        target_exts = {'.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.java', '.cs', '.cpp', '.h', '.rb', '.php'}
        if file_path.suffix not in target_exts:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            lines = content.split('\n')
            
            # Simple coupling check: count imports
            import_count = 0
            if file_path.suffix == '.py':
                import_count = sum(1 for line in lines if line.strip().startswith('import ') or line.strip().startswith('from '))
            elif file_path.suffix in {'.js', '.ts', '.jsx', '.tsx'}:
                import_count = sum(1 for line in lines if line.strip().startswith('import ') or 'require(' in line)
            elif file_path.suffix == '.go':
                import_count = sum(1 for line in lines if line.strip().startswith('import ') or line.strip().startswith('"'))
            else:
                # Basic fallback for other C-like languages
                import_count = sum(1 for line in lines if line.strip().startswith('import ') or line.strip().startswith('#include') or line.strip().startswith('using '))
                
            if import_count > 15:
                high_coupling_files.append((file_path.name, import_count))
                
            # Simple cohesion check: file size in lines
            if len(lines) > 500:
                low_cohesion_files.append((file_path.name, len(lines)))
                
        except Exception:
            pass
            
    # Sort files by the severity
    high_coupling_files.sort(key=lambda x: x[1], reverse=True)
    low_cohesion_files.sort(key=lambda x: x[1], reverse=True)
            
    if high_coupling_files:
        details = ", ".join([f"{name} ({count} imports)" for name, count in high_coupling_files[:5]])
        if len(high_coupling_files) > 5:
            details += f" and {len(high_coupling_files) - 5} more files"
            
        results.append({
            'name': 'High Coupling Detected',
            'status': 'warning',
            'details': f"Files with too many dependencies: {details}",
            'fixable': False
        })
        
    if low_cohesion_files:
        details = ", ".join([f"{name} ({lines} lines)" for name, lines in low_cohesion_files[:5]])
        if len(low_cohesion_files) > 5:
            details += f" and {len(low_cohesion_files) - 5} more files"
            
        results.append({
            'name': 'Low Cohesion Detected',
            'status': 'warning',
            'details': f"Files that are too large (possibly doing too much): {details}",
            'fixable': False
        })
        
    # If no issues found but we checked some files, we can return an info to show it ran
    if not high_coupling_files and not low_cohesion_files:
        results.append({
            'name': 'Cohesiveness and Coupling',
            'status': 'info',
            'details': 'Code appears to have good cohesion and low coupling',
            'fixable': False
        })
        
    return results

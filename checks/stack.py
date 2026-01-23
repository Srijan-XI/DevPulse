"""Tech stack detection check."""

from typing import List, Dict, Any
from pathlib import Path
from utils.patterns import detect_tech_stack


def run_stack_check(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect technology stack from project files.
    
    Args:
        metadata: Project metadata from scanner
        
    Returns:
        List of check results
    """
    results = []
    
    files = metadata.get('files', [])
    detected_stack = detect_tech_stack(files)
    
    if detected_stack:
        results.append({
            'name': 'Tech Stack',
            'status': 'info',
            'details': f"Detected: {', '.join(detected_stack)}",
            'data': detected_stack
        })
    else:
        results.append({
            'name': 'Tech Stack',
            'status': 'warning',
            'details': 'No common technology stack detected',
            'data': []
        })
    
    return results

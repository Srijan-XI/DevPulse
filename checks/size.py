"""File size and large file detection checks."""

from typing import List, Dict, Any
from pathlib import Path
from utils.fs import get_file_size, format_size


# 10MB threshold
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024


def run_size_check(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check for large files that might be problematic.
    
    Args:
        metadata: Project metadata from scanner
        
    Returns:
        List of check results
    """
    results = []
    root = metadata.get('root')
    files = metadata.get('files', [])
    total_size = metadata.get('total_size', 0)
    
    # Find large files
    large_files = []
    for file_path in files:
        size = get_file_size(file_path)
        if size > LARGE_FILE_THRESHOLD:
            large_files.append({
                'path': str(file_path.relative_to(root)),
                'size': size,
                'size_formatted': format_size(size)
            })
    
    if large_files:
        # Sort by size descending
        large_files.sort(key=lambda x: x['size'], reverse=True)
        
        details = f"Found {len(large_files)} file(s) larger than {format_size(LARGE_FILE_THRESHOLD)}"
        
        results.append({
            'name': 'Large Files',
            'status': 'warning',
            'details': details,
            'data': large_files[:10],  # Limit to 10 largest
            'fixable': False
        })
    
    # Report total project size
    results.append({
        'name': 'Project Size',
        'status': 'info',
        'details': f"Total size: {format_size(total_size)} ({metadata.get('file_count', 0)} files)",
        'data': {
            'size': total_size,
            'file_count': metadata.get('file_count', 0)
        }
    })
    
    return results

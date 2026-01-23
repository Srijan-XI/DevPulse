"""Repository hygiene checks."""

from typing import List, Dict, Any
from utils.patterns import check_hygiene_files, count_todos


def run_hygiene_check(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check for repository hygiene files and issues.
    
    Args:
        metadata: Project metadata from scanner
        
    Returns:
        List of check results
    """
    results = []
    root = metadata.get('root')
    files = metadata.get('files', [])
    
    # Check for essential files
    hygiene_status = check_hygiene_files(root)
    
    if not hygiene_status['README']:
        results.append({
            'name': 'Missing README',
            'status': 'warning',
            'details': 'README.md not found in project root',
            'fixable': True
        })
    
    if not hygiene_status['LICENSE']:
        results.append({
            'name': 'Missing LICENSE',
            'status': 'warning',
            'details': 'LICENSE file not found in project root',
            'fixable': True
        })
    
    if not hygiene_status['.gitignore']:
        results.append({
            'name': 'Missing .gitignore',
            'status': 'warning',
            'details': '.gitignore file not found in project root',
            'fixable': True
        })
    
    # Check for tests directory
    has_tests = any('test' in str(f).lower() for f in files)
    if not has_tests:
        results.append({
            'name': 'No Tests Detected',
            'status': 'warning',
            'details': 'No test files or directories found',
            'fixable': False
        })
    
    # Count TODO/FIXME comments
    total_todos = sum(count_todos(f) for f in files)
    if total_todos > 0:
        results.append({
            'name': 'TODO/FIXME Comments',
            'status': 'info',
            'details': f"Found {total_todos} TODO/FIXME comments",
            'data': total_todos
        })
    
    return results

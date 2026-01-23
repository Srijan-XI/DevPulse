"""Security-related checks (basic local scanning)."""

from typing import List, Dict, Any
from utils.patterns import scan_for_secrets


def run_security_check(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Run basic security checks on project files.
    
    Args:
        metadata: Project metadata from scanner
        
    Returns:
        List of check results
    """
    results = []
    root = metadata.get('root')
    files = metadata.get('files', [])
    
    # Check if .env file is tracked
    env_files = ['.env', '.env.local', '.env.production', '.env.development']
    for env_file in env_files:
        if (root / env_file).exists():
            # Check if it might be tracked (not in .gitignore)
            gitignore_path = root / '.gitignore'
            is_ignored = False
            
            if gitignore_path.exists():
                try:
                    with open(gitignore_path, 'r') as f:
                        gitignore_content = f.read()
                        if env_file in gitignore_content or '.env' in gitignore_content:
                            is_ignored = True
                except (OSError, UnicodeDecodeError):
                    pass
            
            if not is_ignored:
                results.append({
                    'name': 'Environment File Not Ignored',
                    'status': 'critical',
                    'details': f'{env_file} exists but may not be in .gitignore',
                    'fixable': False
                })
    
    # Scan for potential secrets in files
    secret_findings = []
    for file_path in files:
        # Only scan specific file types
        if file_path.suffix in ['.py', '.js', '.ts', '.env', '.yml', '.yaml', '.json', '.xml', '.properties']:
            findings = scan_for_secrets(file_path)
            for secret_type, line_num, matched_text in findings:
                secret_findings.append({
                    'file': str(file_path.relative_to(root)),
                    'line': line_num,
                    'type': secret_type,
                    'preview': matched_text
                })
    
    if secret_findings:
        # Limit to first 5 findings to avoid overwhelming output
        limited_findings = secret_findings[:5]
        more = len(secret_findings) - 5
        
        details = f"Found {len(secret_findings)} potential secrets"
        if more > 0:
            details += f" (showing first 5)"
        
        results.append({
            'name': 'Potential Secrets Detected',
            'status': 'warning',
            'details': details,
            'data': limited_findings,
            'fixable': False
        })
    
    return results

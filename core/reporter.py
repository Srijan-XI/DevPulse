"""Reporter formats and outputs scan results."""

import json
from typing import List, Dict, Any


# Status symbols
STATUS_SYMBOLS = {
    'ok': '✓',
    'info': 'ℹ',
    'warning': '⚠',
    'critical': '🚨'
}


class Reporter:
    """Formats and outputs scan results."""
    
    def __init__(self, results: List[Dict[str, Any]], metadata: Dict[str, Any] = None):
        """
        Initialize reporter with scan results.
        
        Args:
            results: List of check results
            metadata: Optional project metadata
        """
        self.results = results
        self.metadata = metadata or {}
    
    def report_terminal(self) -> str:
        """
        Generate human-readable terminal output.
        
        Returns:
            Formatted report string
        """
        lines = []
        
        # Header
        project_path = self.metadata.get('root', '.')
        lines.append("=" * 60)
        lines.append(f"DevPulse Report — {project_path}")
        lines.append("=" * 60)
        lines.append("")
        
        # Group results by status
        grouped = self._group_by_status()
        
        # Tech Stack (info items)
        if grouped.get('info'):
            lines.append("Tech Stack & Info:")
            for result in grouped['info']:
                if result['name'] == 'Tech Stack' and result.get('data'):
                    for tech in result['data']:
                        lines.append(f"  {STATUS_SYMBOLS['ok']} {tech}")
                elif result['name'] not in ['Tech Stack']:
                    lines.append(f"  {STATUS_SYMBOLS['info']} {result['details']}")
            lines.append("")
        
        # Warnings
        if grouped.get('warning'):
            lines.append("Warnings:")
            for result in grouped['warning']:
                lines.append(f"  {STATUS_SYMBOLS['warning']} {result['details']}")
                
                # Show additional data if present
                if result.get('data') and isinstance(result['data'], list):
                    for item in result['data'][:3]:  # Limit to 3 items
                        if isinstance(item, dict):
                            if 'path' in item and 'size_formatted' in item:
                                lines.append(f"      - {item['path']} ({item['size_formatted']})")
                            elif 'file' in item and 'type' in item:
                                lines.append(f"      - {item['file']}:{item.get('line', '?')} ({item['type']})")
            lines.append("")
        
        # Critical issues
        if grouped.get('critical'):
            lines.append("Critical Issues:")
            for result in grouped['critical']:
                lines.append(f"  {STATUS_SYMBOLS['critical']} {result['details']}")
            lines.append("")
        
        # Summary
        total = len(self.results)
        critical_count = len(grouped.get('critical', []))
        warning_count = len(grouped.get('warning', []))
        
        lines.append("Summary:")
        lines.append(f"  Total checks: {total}")
        lines.append(f"  Critical: {critical_count}")
        lines.append(f"  Warnings: {warning_count}")
        
        # Suggest fixes if available
        fixable = [r for r in self.results if r.get('fixable')]
        if fixable:
            lines.append("")
            lines.append(f"💡 {len(fixable)} issue(s) can be auto-fixed with: devpulse fix --safe")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def report_json(self) -> str:
        """
        Generate JSON output for machine consumption.
        
        Returns:
            JSON string
        """
        output = {
            'project': str(self.metadata.get('root', '.')),
            'total_files': self.metadata.get('file_count', 0),
            'total_size': self.metadata.get('total_size', 0),
            'results': self.results,
            'summary': {
                'total': len(self.results),
                'critical': len([r for r in self.results if r.get('status') == 'critical']),
                'warnings': len([r for r in self.results if r.get('status') == 'warning']),
                'info': len([r for r in self.results if r.get('status') == 'info']),
                'fixable': len([r for r in self.results if r.get('fixable')])
            }
        }
        
        return json.dumps(output, indent=2, default=str)
    
    def _group_by_status(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group results by status."""
        grouped = {}
        for result in self.results:
            status = result.get('status', 'info')
            if status not in grouped:
                grouped[status] = []
            grouped[status].append(result)
        return grouped

"""Scanner orchestrates all checks on the project."""

from pathlib import Path
from typing import List, Dict, Any
from utils.fs import get_project_metadata
from checks.stack import run_stack_check
from checks.hygiene import run_hygiene_check
from checks.security import run_security_check
from checks.size import run_size_check


class Scanner:
    """Main scanner that orchestrates all project checks."""
    
    def __init__(self, root_path: str):
        """
        Initialize scanner with project path.
        
        Args:
            root_path: Root directory of project to scan
        """
        self.root_path = Path(root_path).resolve()
        self.metadata = None
        self.results = []
    
    def scan(self) -> List[Dict[str, Any]]:
        """
        Run all checks on the project.
        
        Returns:
            List of check results
        """
        # Collect project metadata once
        self.metadata = get_project_metadata(str(self.root_path))
        
        # Run all checks independently
        self.results = []
        
        # Tech stack detection
        stack_results = run_stack_check(self.metadata)
        self.results.extend(stack_results)
        
        # Hygiene checks
        hygiene_results = run_hygiene_check(self.metadata)
        self.results.extend(hygiene_results)
        
        # Security checks
        security_results = run_security_check(self.metadata)
        self.results.extend(security_results)
        
        # File size checks
        size_results = run_size_check(self.metadata)
        self.results.extend(size_results)
        
        return self.results
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get scan results."""
        return self.results
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get project metadata."""
        return self.metadata

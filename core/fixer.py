"""Fixer applies safe automatic fixes to project issues."""

import os
from pathlib import Path
from typing import List, Dict, Any


class Fixer:
    """Applies safe automatic fixes to project issues."""
    
    def __init__(self, root_path: str, interactive: bool = False):
        """
        Initialize fixer with project path.
        
        Args:
            root_path: Root directory of project
            interactive: Whether to ask before each fix
        """
        self.root_path = Path(root_path).resolve()
        self.interactive = interactive
        self.fixes_applied = []
    
    def fix(self, results: List[Dict[str, Any]]) -> List[str]:
        """
        Apply safe fixes based on scan results.
        
        Args:
            results: Scan results from scanner
            
        Returns:
            List of fixes applied
        """
        # Find fixable issues
        fixable = [r for r in results if r.get('fixable')]
        
        for result in fixable:
            name = result.get('name', '')
            
            if self.interactive:
                response = input(f"Fix '{name}'? [y/N]: ").strip().lower()
                if response not in ['y', 'yes']:
                    continue
            
            # Apply appropriate fix
            if name == 'Missing README':
                self._fix_readme()
            elif name == 'Missing LICENSE':
                self._fix_license()
            elif name == 'Missing .gitignore':
                self._fix_gitignore()
        
        return self.fixes_applied
    
    def _fix_readme(self):
        """Generate README.md from template."""
        readme_path = self.root_path / 'README.md'
        
        if readme_path.exists():
            return
        
        # Load template
        template_path = Path(__file__).parent.parent / 'templates' / 'README.md'
        
        try:
            with open(template_path, 'r') as f:
                template = f.read()
            
            # Simple substitution
            project_name = self.root_path.name
            content = template.replace('{project_name}', project_name)
            
            # Write README
            with open(readme_path, 'w') as f:
                f.write(content)
            
            self.fixes_applied.append('Created README.md')
        except Exception as e:
            print(f"Failed to create README.md: {e}")
    
    def _fix_license(self):
        """Generate LICENSE from template."""
        license_path = self.root_path / 'LICENSE'
        
        if license_path.exists():
            return
        
        # Load template
        template_path = Path(__file__).parent.parent / 'templates' / 'LICENSE.txt'
        
        try:
            with open(template_path, 'r') as f:
                template = f.read()
            
            # Simple substitution (could be enhanced to ask for author name)
            content = template.replace('{project_author}', 'Project Author')
            
            # Write LICENSE
            with open(license_path, 'w') as f:
                f.write(content)
            
            self.fixes_applied.append('Created LICENSE')
        except Exception as e:
            print(f"Failed to create LICENSE: {e}")
    
    def _fix_gitignore(self):
        """Generate .gitignore from template."""
        gitignore_path = self.root_path / '.gitignore'
        
        if gitignore_path.exists():
            return
        
        # Load template
        template_path = Path(__file__).parent.parent / 'templates' / 'gitignore.txt'
        
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Write .gitignore
            with open(gitignore_path, 'w') as f:
                f.write(content)
            
            self.fixes_applied.append('Created .gitignore')
        except Exception as e:
            print(f"Failed to create .gitignore: {e}")

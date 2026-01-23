"""Filesystem utilities for DevPulse."""

from pathlib import Path
from typing import List, Set


# Directories to ignore during scanning
IGNORED_DIRS = {
    '.git', 'node_modules', 'venv', '__pycache__', 
    '.venv', 'env', 'dist', 'build', '.pytest_cache',
    '.mypy_cache', 'target', 'out', '.next', '.nuxt'
}

# File extensions to ignore
IGNORED_EXTENSIONS = {
    '.pyc', '.pyo', '.so', '.dll', '.dylib', '.exe',
    '.class', '.jar', '.war', '.ear'
}


def should_ignore_dir(dir_name: str) -> bool:
    """Check if directory should be ignored during scan."""
    return dir_name in IGNORED_DIRS or dir_name.startswith('.')


def should_ignore_file(file_name: str) -> bool:
    """Check if file should be ignored during scan."""
    path = Path(file_name)
    return path.suffix in IGNORED_EXTENSIONS


def walk_project(root_path: str) -> List[Path]:
    """
    Walk project directory and collect all relevant files.
    
    Args:
        root_path: Root directory to scan
        
    Returns:
        List of Path objects for all non-ignored files
    """
    files = []
    root = Path(root_path).resolve()
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out ignored directories
        dirnames[:] = [d for d in dirnames if not should_ignore_dir(d)]
        
        # Collect non-ignored files
        for filename in filenames:
            if not should_ignore_file(filename):
                file_path = Path(dirpath) / filename
                files.append(file_path)
    
    return files


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    try:
        return file_path.stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def get_project_metadata(root_path: str) -> dict:
    """
    Collect project metadata for analysis.
    
    Args:
        root_path: Root directory to scan
        
    Returns:
        Dictionary with project metadata
    """
    files = walk_project(root_path)
    
    # Collect extensions
    extensions = {}
    for file_path in files:
        ext = file_path.suffix or 'no-extension'
        extensions[ext] = extensions.get(ext, 0) + 1
    
    # Calculate total size
    total_size = sum(get_file_size(f) for f in files)
    
    return {
        'root': Path(root_path).resolve(),
        'files': files,
        'file_count': len(files),
        'extensions': extensions,
        'total_size': total_size
    }


def file_exists(root_path: str, filename: str) -> bool:
    """Check if a file exists in the root directory."""
    return (Path(root_path) / filename).exists()


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

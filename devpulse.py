#!/usr/bin/env python3
"""
DevPulse - A local-first development project health checker.

DevPulse scans your codebase to detect tech stack, check hygiene,
find potential security issues, and suggest improvements.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.scanner import Scanner
from core.reporter import Reporter
from core.fixer import Fixer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='DevPulse - Local-first development project health checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  devpulse scan                    # Scan current directory
  devpulse scan --path /my/project # Scan specific directory
  devpulse scan --json             # Output JSON format
  devpulse fix --safe              # Apply safe automatic fixes
  devpulse fix --interactive       # Ask before each fix
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan project for issues')
    scan_parser.add_argument(
        '--path',
        default='.',
        help='Project directory to scan (default: current directory)'
    )
    scan_parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    # Fix command
    fix_parser = subparsers.add_parser('fix', help='Apply automatic fixes')
    fix_parser.add_argument(
        '--path',
        default='.',
        help='Project directory to fix (default: current directory)'
    )
    fix_parser.add_argument(
        '--safe',
        action='store_true',
        help='Apply only safe, non-destructive fixes'
    )
    fix_parser.add_argument(
        '--interactive',
        action='store_true',
        help='Ask before applying each fix'
    )
    
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'scan':
            return cmd_scan(args)
        elif args.command == 'fix':
            return cmd_fix(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_scan(args):
    """Execute scan command."""
    # Validate path
    path = Path(args.path).resolve()
    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        return 1
    
    if not path.is_dir():
        print(f"Error: Path is not a directory: {path}", file=sys.stderr)
        return 1
    
    # Run scanner
    scanner = Scanner(str(path))
    results = scanner.scan()
    metadata = scanner.get_metadata()
    
    # Generate report
    reporter = Reporter(results, metadata)
    
    if args.json:
        print(reporter.report_json())
    else:
        print(reporter.report_terminal())
    
    # Exit with non-zero if critical issues found
    critical_count = len([r for r in results if r.get('status') == 'critical'])
    return 1 if critical_count > 0 else 0


def cmd_fix(args):
    """Execute fix command."""
    # Validate path
    path = Path(args.path).resolve()
    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        return 1
    
    if not path.is_dir():
        print(f"Error: Path is not a directory: {path}", file=sys.stderr)
        return 1
    
    # First, scan to find issues
    scanner = Scanner(str(path))
    results = scanner.scan()
    
    # Apply fixes
    interactive = args.interactive or not args.safe
    fixer = Fixer(str(path), interactive=interactive)
    fixes_applied = fixer.fix(results)
    
    # Report results
    if fixes_applied:
        print("✓ Fixes applied:")
        for fix in fixes_applied:
            print(f"  - {fix}")
    else:
        print("No fixes needed or applied.")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

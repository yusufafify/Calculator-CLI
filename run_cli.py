#!/usr/bin/env python
"""
Calculator CLI - Command line interface to the calculator

This is a simple entry point script that allows running the calculator
directly from the command line after installing the package.
"""

import sys
from python.cli import main

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

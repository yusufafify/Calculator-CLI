from setuptools import setup
from setuptools.command.install import install
import os
import subprocess

class MakefileCommand(install):
    """Custom install command that runs make commands and generates run_cli.py."""
    
    def run(self):
        # Run Makefile commands
        print("Running Makefile to build the C library...")
        try:
            # Clean first
            subprocess.check_call(['make', 'clean'])
            # Build the shared library
            subprocess.check_call(['make'])
            # Install to site-packages
            subprocess.check_call(['make', 'python-install'])
            print("DLL installed to site-packages via Makefile")
        except subprocess.CalledProcessError as e:
            print(f"Error running make: {e}")
            raise
        
        # Create run_cli.py if it doesn't exist
        if not os.path.exists('run_cli.py'):
            print("Creating run_cli.py...")
            with open('run_cli.py', 'w') as f:
                f.write('#!/usr/bin/env python\n')
                f.write('"""\n')
                f.write('Calculator CLI - Command line interface to the calculator\n')
                f.write('\n')
                f.write('This is a simple entry point script that allows running the calculator\n')
                f.write('directly from the command line.\n')
                f.write('"""\n')
                f.write('\n')
                f.write('import sys\n')
                f.write('from python.cli import main\n')
                f.write('\n')
                f.write('if __name__ == "__main__":\n')
                f.write('    try:\n')
                f.write('        sys.exit(main())\n')
                f.write('    except Exception as e:\n')
                f.write('        print(f"Error: {e}", file=sys.stderr)\n')
                f.write('        sys.exit(1)\n')
            
        # Run standard install
        install.run(self)

# Minimal setup configuration
setup(
    name="calculator-cli",
    version="1.0.0",
    description="A CLI calculator with C backend for fast arithmetic operations",
    packages=['python'],
    entry_points={
        "console_scripts": [
            "calculator-cli=python.cli:main",
        ],
    },
    cmdclass={
        'install': MakefileCommand,
    },
)
# filepath: d:\Gam3a\GP\assessment\calculator_cli\setup.py.new
"""
Setup script for calculator-cli package with C backend.

This script ensures the C library is built and installed when used with pip.
"""
from setuptools import setup, Command
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py
import os
import subprocess
import sys


class BuildCLibrary(Command):
    """Custom command to build the C library."""
    description = "Build the C library using make commands"
    user_options = []
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        pass
        
    def run(self):
        print("Building C library with make...")
        try:
            # Clean first
            print("Running: make clean")
            subprocess.check_call(['make', 'clean'], shell=True)
            
            # Build the shared library
            print("Running: make")
            subprocess.check_call(['make'], shell=True)
            
            # Install to site-packages
            print("Running: make python-install")
            subprocess.check_call(['make', 'python-install'], shell=True)
            
            print("DLL installed to site-packages via Makefile")
            
            # Verify that calculator_c module was installed correctly
            import os
            import sys
            import site
            
            # Check if the module exists in site-packages
            site_packages = site.getsitepackages()
            module_found = False
            
            for sp in site_packages:
                module_path = os.path.join(sp, 'calculator_c')
                if os.path.exists(module_path):
                    module_found = True
                    print(f"Found calculator_c module at: {module_path}")
                    # Make sure it's in the Python path
                    if sp not in sys.path:
                        sys.path.insert(0, sp)
                    break
            
            if not module_found:
                print("WARNING: calculator_c module not found in site-packages!")
                # Try to add the current module path to Python's path
                venv_path = os.environ.get('VIRTUAL_ENV')
                if venv_path:
                    venv_site_packages = os.path.join(venv_path, 'Lib', 'site-packages')
                    module_path = os.path.join(venv_site_packages, 'calculator_c')
                    if os.path.exists(module_path):
                        print(f"Found calculator_c in virtual env: {module_path}")
                        if venv_site_packages not in sys.path:
                            sys.path.insert(0, venv_site_packages)
                        module_found = True
            
            # Test import
            try:
                import calculator_c
                print(f"Successfully imported calculator_c: {calculator_c.add(1, 1)} == 2.0")
            except ImportError as e:
                print(f"WARNING: Could not import calculator_c: {e}")
                print(f"Current sys.path: {sys.path}")
                # Try to manually copy the module if needed
                if not module_found and venv_path:
                    print("Trying to manually fix module installation...")
                    subprocess.check_call(['make', 'python-install'], shell=True)
            
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
            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Command failed with exit code {e.returncode}")
            sys.exit(1)


class CustomInstall(install):
    """Custom install command that runs build_c first."""
    def run(self):
        self.run_command('build_c')
        install.run(self)


class CustomDevelop(develop):
    """Custom develop command that runs build_c first."""
    def run(self):
        self.run_command('build_c')
        develop.run(self)


class CustomBuildPy(build_py):
    """Custom build_py command that runs build_c first."""
    def run(self):
        self.run_command('build_c')
        build_py.run(self)


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
    # Command classes
    cmdclass={
        'build_c': BuildCLibrary,
        'build_py': CustomBuildPy,
        'install': CustomInstall,
        'develop': CustomDevelop,
    },
)

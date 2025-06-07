from setuptools import setup, Extension, find_packages, Command
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py
import os
import subprocess
import sys
import site

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

class BuildCLibrary(Command):
    """Custom command to build the C library using make."""
    description = "Build the C library with make commands"
    user_options = []
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        pass
        
    def run(self):
        """Run the make commands to build and install the C library."""
        print("Building C library with make...")
        try:
            # Clean first
            print("Running make clean...")
            subprocess.check_call(['make', 'clean'], shell=True)
            
            # Build the shared library
            print("Running make...")
            subprocess.check_call(['make'], shell=True)
            
            # Install to site-packages
            print("Running make python-install...")
            subprocess.check_call(['make', 'python-install'], shell=True)
            
            print("C library successfully built and installed via Makefile")
            
            # Verify installation
            try:
                import calculator_c
                print(f"Successfully imported calculator_c module")
                print(f"Test: calculator_c.add(1, 1) = {calculator_c.add(1, 1)}")
            except ImportError as e:
                print(f"WARNING: Could not import calculator_c module: {e}")
                print("This may cause issues when running the calculator")
                
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
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI calculator with C backend for fast arithmetic operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yusufafify/Calculator-CLI",
    packages=find_packages(),
    # We're not using ext_modules as we build the C extension with Makefile
    # ext_modules=[calculator_c],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: C",    ],    
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "calculator-cli=python.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    # Register custom command classes
    cmdclass={
        'build_c': BuildCLibrary,
        'build_py': CustomBuildPy,
        'install': CustomInstall,
        'develop': CustomDevelop,
    },
)
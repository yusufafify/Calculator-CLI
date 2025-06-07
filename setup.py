from setuptools import setup, Extension, find_packages
import os

# C extension module
calculator_c = Extension(
    'calculator_c',
    sources=['c_src/calculate.c'],
    include_dirs=['c_src'],
)

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="calculator-cli",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI calculator with C backend for fast arithmetic operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/calculator-cli",
    packages=find_packages(),
    ext_modules=[calculator_c],
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
        "Programming Language :: C",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "calculator-cli=python.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
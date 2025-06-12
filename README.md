# Calculator CLI

A cross-platform command-line calculator project.

## Project Scope

Candidates are required to implement a command-line calculator that performs: addition, subtraction, multiplication, and division with the following architecture:

- **Backend Logic in C**
- **Python Interface**
- **Usable as a Python API** (to be able to import it and use it in a Python environment)
- **Also usable as a CLI tool**

This project includes unit tests, code formatting, and automated linting. The C code provides the core calculation logic, which is accessible both as a Python API and as a standalone CLI tool. Code quality is enforced with pre-commit hooks and GitHub Actions.

## Getting Started for New Developers

Follow these steps to set up your development environment and ensure code quality from your first commit.

### 1. Create a New Python Virtual Environment

```sh
python -m venv .venv
```

### 2. Activate the Virtual Environment

- **On Windows (Python 3.11+):**
  ```powershell
  .venv\Scripts\activate
  ```
- **On Windows (Python <3.11):**
  ```powershell
  .venv\Scripts\activate.bat
  ```
- **On macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Install Packages**
  ```bash
  pip install -r requirements.txt
  ```

### 3. Install Build Tools (Make, CMake, Ninja)
To use different build systems like make, cmake, or ninja, you must install them and add them to your system's PATH.

**Windows**
**Make**
-Download from [Link Text](GnuWin32).

-Add the directory containing make.exe to your System or User PATH.

**CMake**
-Download the installer from [Link Text](cmake.org).

-During installation, select the option to add CMake to system PATH or manually add the bin folder to your PATH.

**Ninja**
-Download ninja.exe from the [Link Text](Ninja GitHub releases).

-Create a folder (e.g., C:\Program Files\Ninja) and place ninja.exe inside.

-Add that folder to your System or User PATH.

⚠️ After updating your PATH, restart the terminal or your IDE for the changes to take effect.

### 4. Install the Calculator Package

```powershell
pip install -e .
```

This will:
- Build By default by makefile
- to build with CMake and Ninja `$env:BUILD_SYSTEM = "cmake"; pip install -e .`
- This will:
- Run the Makefile or Cmake/ Ninja according to choice to build the C shared library
- Install the package in development mode
- Make the `calculator-cli` command available
- Create `calculator_cli.egg-info` metadata

### 5. Starting Sphinx docs

```powershell
sphinx-quickstart docs
````
To build the docs or make changes
navigate to docs dir
```
make html
```
To run the Docs:
  go live with index.html in your browser
```
cd docs\build\html
```


### 6. Using the Calculator

After installation, you can use the calculator in two ways:

#### As a Python API:
```python
from python import Calculator

calc = Calculator()
result = calc.add(2, 3)  # Returns 5.0
```

#### As a CLI Tool:
```powershell
# run CLI'
calculator-cli "2 + 3"

# or calculate from python command
python run_cli.py "2 + 3"

# Or run the interactive mode:
python run_cli.py -i
```

### 7. Development Tools

```powershell
# Install pre-commit
pre-commit install

# Test linting
pre-commit run --all-files --show-diff-on-failure
```

---


### 7. Deploy Commands

```powershell
# Deploy Commands

  python deploy.py                    # Interactive mode (choose build system)
  python deploy.py --build-system make    # Use Make
  python deploy.py --build-system cmake   # Use CMake
  python deploy.py --no-interactive       # Auto-select build system
```
#### create the .exe file and can run as a standalone cli and added to the environment variables and run in any terminal on the device
---

For more details on building and testing the C and Python code, see the Makefile and workflow files in `.github/workflows/`.

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

### 3. Install the Calculator Package

```powershell
pip install -e .
```

This will:
- Run the Makefile to build the C shared library
- Install the package in development mode
- Make the `calculator-cli` command available
- Create `calculator_cli.egg-info` metadata



### 4. Using the Calculator

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

### 5. Development Tools

```powershell
# Install pre-commit
pre-commit install

# Test linting
pre-commit run --all-files --show-diff-on-failure
```

---

For more details on building and testing the C and Python code, see the Makefile and workflow files in `.github/workflows/`.

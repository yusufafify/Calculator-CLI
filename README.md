# Calculator CLI

A cross-platform command-line calculator project.

## Project Description

A command-line calculator that performs: addition, subtraction, multiplication, and division with the following architecture:

- **Backend Logic in C**
- **Python Interface**
- **Usable as a Python API**
- **Also usable as a CLI tool**

This project includes unit tests, code formatting, and automated linting. The C code provides the core calculation logic, which is accessible both as a Python API and as a standalone CLI tool. Code quality is enforced with pre-commit hooks and GitHub Actions.

## Getting Started

Follow these steps to set up your development environment and ensure code quality from your first commit.

### 1. Create a New Python Virtual Environment

```sh
python -m venv .venv
```

### 2. Activate the Virtual Environment

- **On Windows (Python 3.11+):**
  ```sh
  .venv\Scripts\activate
  ```
- **On Windows (Python <3.11):**
  ```sh
  .venv\Scripts\activate.bat
  ```
- **On macOS/Linux:**
  ```sh
  source .venv/bin/activate
  ```

### 3. Install Pre-commit

After activating your virtual environment, run:

```sh
pip install pre-commit
```

### 4. Install the Pre-commit Hook (One Time Only)

```sh
pre-commit install
```

### 5. Test Linting and Code Format

To check all files for linting and formatting issues, run:

```sh
pre-commit run --all-files --show-diff-on-failure
```

This will show any issues and auto-fix code format where possible. Fix any remaining issues before committing.

---

For more details on building and testing the C and Python code, see the Makefile and workflow files in `.github/workflows/`.

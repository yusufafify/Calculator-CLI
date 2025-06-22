import sys
import os
import site

# Try to import calculator_c, if it fails, try to find and add it to the path
try:
    import calculator_c
except ImportError:
    # Look for calculator_c in all site-packages directories
    calculator_c_found = False

    # Check virtual environment first
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path:
        venv_site_packages = os.path.join(venv_path, "Lib", "site-packages")
        calculator_c_path = os.path.join(venv_site_packages, "calculator_c")

        if os.path.exists(calculator_c_path):
            if venv_site_packages not in sys.path:
                sys.path.insert(0, venv_site_packages)
            calculator_c_found = True

    # Check all site-packages directories
    if not calculator_c_found:
        for site_package in site.getsitepackages():
            calculator_c_path = os.path.join(site_package, "calculator_c")
            if os.path.exists(calculator_c_path):
                if site_package not in sys.path:
                    sys.path.insert(0, site_package)
                calculator_c_found = True
                break

    # Try import again
    import calculator_c


class Calculator:
    """A calculator class that uses C backend for operations."""

    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return calculator_c.add(a, b)

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract two numbers."""
        return calculator_c.subtract(a, b)

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return calculator_c.multiply(a, b)

    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return calculator_c.divide(a, b)

    @staticmethod
    def power(a: float, b: float) -> float:
        """power function"""
        return calculator_c.power(a, b)

    def calculate(self, expression: str) -> float:
        """Parse and calculate a simple expression."""
        expression = expression.replace(" ", "")

        for op in ["+", "-", "*", "/", "^"]:
            if op in expression:
                parts = expression.split(op)
                if len(parts) == 2:
                    try:
                        a, b = float(parts[0]), float(parts[1])
                        if op == "+":
                            return self.add(a, b)
                        elif op == "-":
                            return self.subtract(a, b)
                        elif op == "*":
                            return self.multiply(a, b)
                        elif op == "/":
                            return self.divide(a, b)
                        elif op == "^":
                            return self.power(a, b)
                    except ValueError:
                        raise ValueError("Invalid numbers in expression")

        raise ValueError("Invalid expression format")


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
        return calculator_c.divide(a, b)
    
    def calculate(self, expression: str) -> float:
        """Parse and calculate a simple expression."""
        expression = expression.replace(" ", "")
        
        for op in ['+', '-', '*', '/']:
            if op in expression:
                parts = expression.split(op)
                if len(parts) == 2:
                    try:
                        a, b = float(parts[0]), float(parts[1])
                        if op == '+':
                            return self.add(a, b)
                        elif op == '-':
                            return self.subtract(a, b)
                        elif op == '*':
                            return self.multiply(a, b)
                        elif op == '/':
                            return self.divide(a, b)
                    except ValueError:
                        raise ValueError("Invalid numbers in expression")
        
        raise ValueError("Invalid expression format")
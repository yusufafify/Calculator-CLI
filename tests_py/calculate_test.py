import pytest
import calculator_c


class TestCBackend:
    """Test the C backend functions directly."""

    def test_add(self):
        """Test addition function."""
        assert calculator_c.add(2.0, 3.0) == 5.0
        assert calculator_c.add(-1.0, 1.0) == 0.0
        assert calculator_c.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract(self):
        """Test subtraction function."""
        assert calculator_c.subtract(5.0, 3.0) == 2.0
        assert calculator_c.subtract(1.0, 1.0) == 0.0
        assert calculator_c.subtract(-1.0, -1.0) == 0.0

    def test_multiply(self):
        """Test multiplication function."""
        assert calculator_c.multiply(2.0, 3.0) == 6.0
        assert calculator_c.multiply(-2.0, 3.0) == -6.0
        assert calculator_c.multiply(0.0, 5.0) == 0.0

    def test_divide(self):
        """Test division function."""
        assert calculator_c.divide(6.0, 2.0) == 3.0
        assert calculator_c.divide(-6.0, 2.0) == -3.0
        assert calculator_c.divide(1.0, 3.0) == pytest.approx(0.333333, rel=1e-5)

    def test_divide_by_zero(self):
        """Test division by zero raises exception."""
        with pytest.raises(ZeroDivisionError):
            calculator_c.divide(5.0, 0.0)

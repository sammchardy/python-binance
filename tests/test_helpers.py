import pytest
from decimal import Decimal, InvalidOperation
from binance.helpers import round_step_size


@pytest.mark.parametrize(
    "quantity,step_size,expected",
    [
        # Basic cases
        (1.23456, 0.1, 1.2),
        (1.23456, 0.01, 1.23),
        (1.23456, 1, 1),
        # Edge cases
        (0.0, 0.1, 0.0),
        (0.1, 0.1, 0.1),
        (1.0, 1, 1.0),
        # Large numbers
        (100.123456, 0.1, 100.1),
        (1000.123456, 1, 1000),
        # Small step sizes
        (1.123456, 0.0001, 1.1234),
        (1.123456, 0.00001, 1.12345),
        # Decimal inputs
        (Decimal("1.23456"), Decimal("0.1"), 1.2),
        (Decimal("1.23456"), 0.01, 1.23),
        # String conversion edge cases
        (1.23456, Decimal("0.01"), 1.23),
        ("1.23456", "0.01", 1.23),
    ],
)
def test_round_step_size(quantity, step_size, expected):
    """Test round_step_size with various inputs"""
    result = round_step_size(quantity, step_size)
    assert result == expected
    assert isinstance(result, float)


def test_round_step_size_precision():
    """Test that rounding maintains proper precision"""
    # Should maintain step size precision
    assert round_step_size(1.123456, 0.0001) == 1.1234
    assert round_step_size(1.123456, 0.001) == 1.123
    assert round_step_size(1.123456, 0.01) == 1.12
    assert round_step_size(1.123456, 0.1) == 1.1


def test_round_step_size_always_rounds_down():
    """Test that values are always rounded down"""
    assert round_step_size(1.19, 0.1) == 1.1
    assert round_step_size(1.99, 1.0) == 1.0
    assert round_step_size(0.99999, 0.1) == 0.9


def test_round_step_size_invalid_inputs():
    """Test error handling for invalid inputs"""
    with pytest.raises(TypeError):
        round_step_size(None, 0.1)  # type: ignore

    with pytest.raises((ValueError, InvalidOperation)):
        round_step_size("invalid", 0.1)  # type: ignore

    with pytest.raises((ValueError, InvalidOperation)):
        round_step_size(1.23, "invalid")  # type: ignore


import pytest

from app.operations.factory import CalculationFactory


@pytest.mark.parametrize(
    "calculation_type, a, b, expected",
    [
        ("Add", 10, 5, 15),
        ("Sub", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
    ],
)
def test_factory_operations(calculation_type, a, b, expected):
    operation = CalculationFactory.create(calculation_type)
    assert operation(a, b) == expected


def test_factory_invalid_type():
    with pytest.raises(ValueError, match="Invalid calculation type"):
        CalculationFactory.create("Invalid")


def test_factory_division_by_zero():
    operation = CalculationFactory.create("Divide")

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        operation(10, 0)

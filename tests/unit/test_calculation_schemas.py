
import pytest
from pydantic import ValidationError

from app.models import Calculation
from app.schemas import CalculationCreate, CalculationRead


@pytest.mark.parametrize(
    "operation", ["Add", "Sub", "Multiply", "Divide"]
)
def test_valid_calculation_types(operation):
    calculation = CalculationCreate(
        a=10, b=5, type=operation, user_id=1
    )
    assert calculation.type == operation


@pytest.mark.parametrize(
    "operation", ["Invalid", "Power", "add", ""]
)
def test_invalid_calculation_types(operation):
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10, b=5, type=operation, user_id=1
        )


def test_division_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10, b=0, type="Divide", user_id=1
        )


@pytest.mark.parametrize(
    "operation", ["Add", "Sub", "Multiply"]
)
def test_zero_allowed_for_other_operations(operation):
    calculation = CalculationCreate(
        a=10, b=0, type=operation, user_id=1
    )
    assert calculation.b == 0


@pytest.mark.parametrize("user_id", [0, -1])
def test_invalid_user_id(user_id):
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10, b=5, type="Add", user_id=user_id
        )


@pytest.mark.parametrize(
    "invalid_number",
    [float("nan"), float("inf"), float("-inf")],
)
def test_invalid_numbers(invalid_number):
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=invalid_number, b=5, type="Add", user_id=1
        )


def test_calculation_read_from_model():
    calculation = Calculation(
        id=1,
        a=10,
        b=5,
        type="Add",
        result=15,
        user_id=2,
    )

    response = CalculationRead.model_validate(calculation)

    assert response.id == 1
    assert response.result == 15
    assert response.user_id == 2
    assert response.type == "Add"

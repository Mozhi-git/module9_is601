
from app.operations import add, subtract, multiply, divide


class CalculationFactory:
    OPERATIONS = {
        "Add": add,
        "Sub": subtract,
        "Multiply": multiply,
        "Divide": divide,
    }

    @classmethod
    def create(cls, calculation_type: str):
        operation = cls.OPERATIONS.get(calculation_type)

        if operation is None:
            raise ValueError(
                f"Invalid calculation type: {calculation_type}"
            )

        return operation


import pytest
from sqlalchemy import func, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_engine
from app.models import Calculation, User
from app.operations.factory import CalculationFactory
from app.schemas import CalculationCreate, CalculationRead


@pytest.fixture(scope="module")
def db_engine():
    engine = get_engine()

    try:
        with engine.connect() as connection:
            database = connection.scalar(
                select(func.current_database())
            )

        if database != "module10_test_db":
            raise RuntimeError("Not connected to test database")

        if not inspect(engine).has_table("users"):
            raise RuntimeError("Users table is missing")

        # Create only the new table if it does not exist.
        Calculation.__table__.create(
            bind=engine,
            checkfirst=True,
        )

        yield engine

    finally:
        engine.dispose()


@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    try:
        with Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        ) as session:
            yield session

    finally:
        transaction.rollback()
        connection.close()


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        ("Add", 10, 5, 15),
        ("Sub", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
    ],
)
def test_save_calculation(
    db_session, operation, a, b, expected
):
    user = User(
        username="module11user",
        email="module11@example.com",
        password_hash="test-only-hash",
    )

    db_session.add(user)
    db_session.flush()

    data = CalculationCreate(
        a=a,
        b=b,
        type=operation,
        user_id=user.id,
    )

    operation_function = CalculationFactory.create(
        data.type
    )

    result = operation_function(data.a, data.b)

    calculation = Calculation(
        **data.model_dump(),
        result=result,
    )

    db_session.add(calculation)
    db_session.flush()

    calculation_id = calculation.id
    assert calculation_id is not None

    db_session.expire_all()

    saved = db_session.get(
        Calculation, calculation_id
    )

    assert saved is not None
    assert saved.result == pytest.approx(expected)
    assert saved.user_id == user.id

    response = CalculationRead.model_validate(saved)

    assert response.id == calculation_id
    assert response.type == operation


def test_invalid_user_foreign_key(db_session):
    calculation = Calculation(
        a=10,
        b=5,
        type="Add",
        result=15,
        user_id=-1,
    )

    db_session.add(calculation)

    with pytest.raises(IntegrityError):
        db_session.flush()

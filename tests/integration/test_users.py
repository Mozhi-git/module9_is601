
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_engine
from app.models import User
from app.security import hash_password, verify_password


@pytest.fixture
def db_session():
    engine = get_engine()
    connection = engine.connect()
    transaction = connection.begin()

    try:
        database = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        if database != "module10_test_db":
            raise RuntimeError("Not connected to test database")

        with Session(
            bind=connection,
            join_transaction_mode="create_savepoint"
        ) as session:
            yield session

    finally:
        transaction.rollback()
        connection.close()
        engine.dispose()


def test_create_user(db_session):
    user = User(
        username="newuser",
        email="new@example.com",
        password_hash=hash_password("Password123")
    )

    db_session.add(user)
    db_session.flush()

    assert user.id is not None
    assert user.created_at is not None
    assert verify_password(
        "Password123", user.password_hash
    )


def test_duplicate_username(db_session):
    first = User(
        username="duplicate",
        email="first@example.com",
        password_hash=hash_password("Password123")
    )

    db_session.add(first)
    db_session.flush()

    second = User(
        username="duplicate",
        email="second@example.com",
        password_hash=hash_password("Password456")
    )

    db_session.add(second)

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_duplicate_email(db_session):
    first = User(
        username="userone",
        email="duplicate@example.com",
        password_hash=hash_password("Password123")
    )

    db_session.add(first)
    db_session.flush()

    second = User(
        username="usertwo",
        email="duplicate@example.com",
        password_hash=hash_password("Password456")
    )

    db_session.add(second)

    with pytest.raises(IntegrityError):
        db_session.flush()

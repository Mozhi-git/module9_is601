
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas import UserCreate, UserRead


def test_valid_user():
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="Password123"
    )
    assert user.username == "testuser"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="invalid-email",
            password="Password123"
        )


def test_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            password="123"
        )


def test_short_username():
    with pytest.raises(ValidationError):
        UserCreate(
            username="ab",
            email="test@example.com",
            password="Password123"
        )


def test_user_read_hides_password():
    user = UserRead(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at=datetime.now(),
    )

    result = user.model_dump()

    assert "password" not in result
    assert "password_hash" not in result

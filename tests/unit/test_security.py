
from app.security import hash_password, verify_password


def test_password_is_hashed():
    password = "TestPassword123"
    hashed = hash_password(password)

    assert hashed != password


def test_correct_password():
    password = "TestPassword123"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_wrong_password():
    hashed = hash_password("TestPassword123")

    assert verify_password("WrongPassword", hashed) is False


def test_invalid_hash():
    assert verify_password("TestPassword123", "invalid_hash") is False

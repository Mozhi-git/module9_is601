import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_engine
from app.dependencies import get_db
from app.models import Base, Calculation, User
from main import app


@pytest.fixture
def api_client():
    engine = get_engine()

    database_name = None
    with engine.connect() as check_connection:
        database_name = check_connection.scalar(
            select(func.current_database())
        )

    if database_name != "module10_test_db":
        engine.dispose()
        raise RuntimeError("Not connected to test database")

    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client, session
    finally:
        app.dependency_overrides.clear()
        session.close()
        transaction.rollback()
        connection.close()
        engine.dispose()


def test_register_and_login(api_client):
    client, db = api_client

    register_response = client.post(
        "/users/register",
        json={
            "username": "module12test",
            "email": "module12test@example.com",
            "password": "TestPass123!",
        },
    )

    assert register_response.status_code == 201
    assert register_response.json()["username"] == "module12test"
    assert "password" not in register_response.json()
    assert "password_hash" not in register_response.json()

    user = db.scalar(
        select(User).where(User.username == "module12test")
    )

    assert user is not None
    assert user.password_hash != "TestPass123!"

    login_response = client.post(
        "/users/login",
        json={
            "username": "module12test",
            "password": "TestPass123!",
        },
    )

    assert login_response.status_code == 200
    assert login_response.json()["message"] == "Login successful"

    wrong_password = client.post(
        "/users/login",
        json={
            "username": "module12test",
            "password": "WrongPassword123!",
        },
    )

    assert wrong_password.status_code == 401


def test_calculation_bread_flow(api_client):
    client, db = api_client

    register_response = client.post(
        "/users/register",
        json={
            "username": "calcuser",
            "email": "calcuser@example.com",
            "password": "TestPass123!",
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    create_response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
            "user_id": user_id,
        },
    )

    assert create_response.status_code == 201
    calculation_id = create_response.json()["id"]
    assert create_response.json()["result"] == 15

    saved = db.get(Calculation, calculation_id)
    assert saved is not None
    assert saved.result == 15

    browse_response = client.get("/calculations")
    assert browse_response.status_code == 200
    assert any(
        item["id"] == calculation_id
        for item in browse_response.json()
    )

    read_response = client.get(
        f"/calculations/{calculation_id}"
    )

    assert read_response.status_code == 200
    assert read_response.json()["id"] == calculation_id

    update_response = client.put(
        f"/calculations/{calculation_id}",
        json={
            "a": 20,
            "b": 4,
            "type": "Sub",
            "user_id": user_id,
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["result"] == 16

    delete_response = client.delete(
        f"/calculations/{calculation_id}"
    )

    assert delete_response.status_code == 204

    missing_response = client.get(
        f"/calculations/{calculation_id}"
    )

    assert missing_response.status_code == 404


def test_invalid_calculation_data(api_client):
    client, _ = api_client

    register_response = client.post(
        "/users/register",
        json={
            "username": "invalidtest",
            "email": "invalidtest@example.com",
            "password": "TestPass123!",
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 0,
            "type": "Divide",
            "user_id": user_id,
        },
    )

    assert response.status_code == 400
    assert "error" in response.json()

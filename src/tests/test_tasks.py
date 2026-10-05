import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


os.environ.setdefault("DATABASE_URL", "sqlite://")

from test_api.database.connection import Base, get_db
from test_api.main import app
from test_api.models.task import TaskModel


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks() -> Generator[None, None, None]:
    with TestingSessionLocal() as db:
        db.execute(delete(TaskModel))
        db.commit()

    yield

    with TestingSessionLocal() as db:
        db.execute(delete(TaskModel))
        db.commit()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task() -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "SQLAlchemy",
            "description": "Persistir datos en PostgreSQL",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["title"] == "SQLAlchemy"
    assert data["completed"] is False


def test_get_tasks() -> None:
    client.post(
        "/tasks",
        json={"title": "Tarea 2"},
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_task() -> None:
    created_response = client.post(
        "/tasks",
        json={"title": "Tarea 2"},
    )

    task_id = created_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Tarea 2"


def test_get_nonexistent_task() -> None:
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_create_task_without_title() -> None:
    response = client.post(
        "/tasks",
        json={"description": "Falta title"},
    )

    assert response.status_code == 422
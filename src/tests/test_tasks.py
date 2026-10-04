from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from test_api.main import app
from test_api.routes.tasks import tasks

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_tasks() -> Generator[None, None, None]:
    tasks.clear()
    yield
    tasks.clear()

def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task() -> None:
    payload = {
        "title": "Ejecutar prueba",
        "description": "Probar la API con pytest",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Ejecutar prueba"
    assert data["completed"] is False

def test_get_tasks() -> None:
    client.post(
        "/tasks",
        json={"title": "miniproyecto FastAPI"},
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_nonexistent_task() -> None:
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarea no encontrada"}


def test_create_task_without_title() -> None:
    response = client.post(
        "/tasks",
        json={"description": "Falta title"},
    )

    assert response.status_code == 422
# Task API

API REST para gestión de tareas desarrollada como miniproyecto de práctica backend con **Python**, **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **pytest**, **uv** y **Docker Compose**.

El objetivo del proyecto es practicar un flujo de desarrollo backend completo: creación de endpoints, validación de datos, persistencia en base de datos, migrations, testing, manejo de dependencias, containerización y control de versiones con Git.

## Tecnologías

- Python 3.14+
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Psycopg
- Alembic
- pytest
- HTTPX
- uv
- Docker
- Docker Compose
- Git / GitHub

## Funcionalidades

La API permite actualmente:

- Crear tareas.
- Listar todas las tareas.
- Obtener una tarea por ID.
- Validar automáticamente los payloads mediante Pydantic.
- Retornar errores HTTP controlados.
- Persistir información en PostgreSQL.
- Gestionar el schema de la base de datos mediante Alembic.
- Ejecutar tests automatizados.
- Levantar API y base de datos mediante Docker Compose.

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/` | Verifica que la API está disponible |
| `GET` | `/health` | Health check de la aplicación |
| `POST` | `/tasks` | Crea una nueva tarea |
| `GET` | `/tasks` | Lista todas las tareas |
| `GET` | `/tasks/{task_id}` | Obtiene una tarea por ID |

La documentación interactiva de la API está disponible en:

```text
http://localhost:8000/docs
```

## Ejemplo de creación de una tarea

Request:

```json
{
  "title": "Aprender FastAPI",
  "description": "Completar el miniproyecto Task API"
}
```

Response:

```json
{
  "title": "Aprender FastAPI",
  "description": "Completar el miniproyecto Task API",
  "id": 1,
  "completed": false
}
```

## Estructura del proyecto

```text
test-api/
├── alembic/
│   └── versions/
├── src/
│   └── test_api/
│       ├── database/
│       │   └── connection.py
│       ├── models/
│       │   └── task.py
│       ├── routes/
│       │   └── tasks.py
│       ├── schemas/
│       │   └── task.py
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_tasks.py
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

## Arquitectura

El flujo principal de la aplicación es:

```text
Cliente / Swagger
        |
        v
     FastAPI
        |
        v
     Pydantic
        |
        v
      Routes
        |
        v
 SQLAlchemy ORM
        |
        v
     Psycopg
        |
        v
   PostgreSQL
```

La aplicación separa responsabilidades en:

- `routes/`: endpoints y lógica HTTP.
- `schemas/`: validación y serialización con Pydantic.
- `models/`: modelos ORM de SQLAlchemy.
- `database/`: configuración de conexión y sesiones.
- `tests/`: pruebas automatizadas de la API.

## Configuración del entorno

Crea un archivo `.env` tomando como referencia `.env.example`.

Ejemplo:

```env
POSTGRES_USER=test_api_user
POSTGRES_PASSWORD=change_me
POSTGRES_DB=test_api_db

DATABASE_URL=postgresql+psycopg://test_api_user:change_me@localhost:5432/test_api_db
```

> El archivo `.env` contiene credenciales locales y no debe versionarse en Git.

## Ejecución local

Instala las dependencias:

```bash
uv sync
```

Aplica las migrations:

```bash
uv run alembic upgrade head
```

Levanta la API:

```bash
uv run fastapi dev src/test_api/main.py
```

Luego abre:

```text
http://127.0.0.1:8000/docs
```

## Migrations con Alembic

Para crear una nueva migration después de modificar los modelos:

```bash
uv run alembic revision --autogenerate -m "descripcion del cambio"
```

Para aplicar todas las migrations pendientes:

```bash
uv run alembic upgrade head
```

Para consultar la migration actual:

```bash
uv run alembic current
```

## Testing

Los tests utilizan una base SQLite en memoria para mantenerse aislados de la base PostgreSQL utilizada por la aplicación.

Ejecuta:

```bash
uv run pytest -v
```

Los tests cubren actualmente:

- Health check.
- Creación de tareas.
- Listado de tareas.
- Obtención de una tarea por ID.
- Respuesta `404` para tareas inexistentes.
- Validación `422` para payloads inválidos.

## Ejecución con Docker Compose

La forma más sencilla de levantar el proyecto completo es:

```bash
docker compose up --build
```

Docker Compose levanta:

```text
Docker Compose
├── api
│   └── FastAPI
└── db
    └── PostgreSQL
```

La API queda disponible en:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

El PostgreSQL del Compose se expone al host mediante el puerto configurado en `compose.yaml`.

Para detener los containers:

```bash
docker compose down
```

Los datos de PostgreSQL se mantienen mediante un Docker volume.

Para eliminar también los datos persistidos:

```bash
docker compose down -v
```

## Conceptos practicados

Este proyecto fue desarrollado para reforzar:

- Diseño básico de APIs REST.
- HTTP methods y status codes.
- Request body y path parameters.
- Validación con Pydantic.
- Dependency Injection en FastAPI.
- ORM con SQLAlchemy.
- Sesiones y transacciones.
- Persistencia con PostgreSQL.
- Migrations con Alembic.
- Testing de endpoints con pytest.
- Gestión moderna de dependencias con uv.
- Variables de entorno.
- Docker images y containers.
- Docker Compose.
- Docker volumes.
- Git y control de versiones.

## Estado del proyecto

Miniproyecto completado como ejercicio práctico de backend.

Posibles mejoras futuras:

- `PUT` / `PATCH` para actualizar tareas.
- `DELETE` para eliminar tareas.
- Autenticación con JWT/OAuth2.
- Logging estructurado.
- CI/CD.
- Deploy en cloud.

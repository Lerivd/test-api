from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI(title="Task API")

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class Task(TaskCreate):
    id: int
    completed: bool = False

tasks: list[Task] = []
@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Task API running"}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

# CREATE
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    new_task = Task(
        id=len(tasks) + 1,
        title=task.title,
        description=task.description,
    )

    tasks.append(new_task)

    return new_task

# READ TASKS
@app.get("/tasks", response_model=list[Task])
def get_tasks() -> list[Task]:
    return tasks

# READ TASK BY ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail="Tarea no encontrada"
    )
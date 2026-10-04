from fastapi import APIRouter, HTTPException, status

from test_api.schemas.task import Task, TaskCreate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

tasks: list[Task] = []

# CREATE
@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    new_task = Task(
        id=len(tasks) + 1,
        title=task.title,
        description=task.description,
    )

    tasks.append(new_task)

    return new_task

# READ TASKS
@router.get("", response_model=list[Task])
def get_tasks() -> list[Task]:
    return tasks

# READ TASK BY ID
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tarea no encontrada"
    )
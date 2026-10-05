from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from test_api.database.connection import get_db
from test_api.models.task import TaskModel
from test_api.schemas.task import Task, TaskCreate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

# CREATE
@router.post(
        "", 
        response_model=Task, 
        status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate, db: Session = Depends(get_db),) -> TaskModel:
    
    new_task = TaskModel(
        title=task.title,
        description=task.description,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# READ TASKS
@router.get("", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db),) -> list[TaskModel]:
    statement = select(TaskModel)

    return list(db.scalars(statement).all())

# READ TASK BY ID
@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskModel:
    task = db.get(TaskModel, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task
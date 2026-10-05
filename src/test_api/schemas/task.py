from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class Task(TaskCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed: bool = False
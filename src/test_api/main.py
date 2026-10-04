from fastapi import FastAPI

from test_api.routes.tasks import router as task_router
app = FastAPI(title="Task API")

app.include_router(task_router)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Task API running"}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
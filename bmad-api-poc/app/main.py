"""Application factory. Run with: uvicorn app.main:app --reload"""

from fastapi import FastAPI

from app.errors import register_error_handlers
from app.repository import InMemoryTaskRepository, TaskRepository
from app.routers import tasks


def create_app(repository: TaskRepository | None = None) -> FastAPI:
    app = FastAPI(
        title="Task Management API (BMAD POC)",
        version="0.1.0",
        description="Sample API built by following the BMAD Method workflow.",
    )
    app.state.repository = repository or InMemoryTaskRepository()
    register_error_handlers(app)
    app.include_router(tasks.router)

    @app.get("/health", tags=["ops"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

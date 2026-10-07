"""Uniform error envelope {"code", "message"} for every error (AD-4)."""

from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


class TaskNotFound(Exception):
    def __init__(self, task_id: UUID) -> None:
        self.task_id = task_id


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(TaskNotFound)
    async def _not_found(_: Request, exc: TaskNotFound) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"code": "TASK_NOT_FOUND", "message": f"Task {exc.task_id} not found"},
        )

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0]
        field = ".".join(str(p) for p in first["loc"] if p != "body")
        return JSONResponse(
            status_code=422,
            content={"code": "VALIDATION_ERROR", "message": f"{field}: {first['msg']}"},
        )

    @app.exception_handler(HTTPException)
    async def _http(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": "HTTP_ERROR", "message": str(exc.detail)},
        )

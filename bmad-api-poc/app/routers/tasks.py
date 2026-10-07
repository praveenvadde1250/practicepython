"""Task endpoints (Epic 1, stories 1.1-1.4)."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response, status

from app.errors import TaskNotFound
from app.models import ErrorResponse, Task, TaskCreate, TaskPage, TaskStatus, TaskUpdate
from app.repository import TaskRepository

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

NOT_FOUND = {404: {"model": ErrorResponse}}


def get_repository(request: Request) -> TaskRepository:
    return request.app.state.repository


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskCreate, response: Response, repo: TaskRepository = Depends(get_repository)
) -> Task:
    task = repo.create(body)
    response.headers["Location"] = f"{router.prefix}/{task.id}"
    return task


@router.get("", response_model=TaskPage)
def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    repo: TaskRepository = Depends(get_repository),
) -> TaskPage:
    items, total = repo.list(status_filter, limit, offset)
    return TaskPage(items=items, total=total, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=Task, responses=NOT_FOUND)
def get_task(task_id: UUID, repo: TaskRepository = Depends(get_repository)) -> Task:
    task = repo.get(task_id)
    if task is None:
        raise TaskNotFound(task_id)
    return task


@router.patch("/{task_id}", response_model=Task, responses=NOT_FOUND)
def update_task(
    task_id: UUID, body: TaskUpdate, repo: TaskRepository = Depends(get_repository)
) -> Task:
    task = repo.update(task_id, body)
    if task is None:
        raise TaskNotFound(task_id)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND)
def delete_task(task_id: UUID, repo: TaskRepository = Depends(get_repository)) -> Response:
    if not repo.delete(task_id):
        raise TaskNotFound(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

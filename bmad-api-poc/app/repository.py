"""Storage layer (AD-2: repository interface, in-memory for the POC)."""

from datetime import datetime, timezone
from threading import Lock
from typing import Protocol
from uuid import UUID, uuid4

from app.models import Task, TaskCreate, TaskStatus, TaskUpdate


class TaskRepository(Protocol):
    def create(self, data: TaskCreate) -> Task: ...
    def get(self, task_id: UUID) -> Task | None: ...
    def list(
        self, status: TaskStatus | None, limit: int, offset: int
    ) -> tuple[list[Task], int]: ...
    def update(self, task_id: UUID, data: TaskUpdate) -> Task | None: ...
    def delete(self, task_id: UUID) -> bool: ...


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}
        self._lock = Lock()

    def create(self, data: TaskCreate) -> Task:
        now = datetime.now(timezone.utc)
        task = Task(
            id=uuid4(),
            title=data.title,
            description=data.description,
            priority=data.priority,
            status=TaskStatus.todo,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._tasks[task.id] = task
        return task

    def get(self, task_id: UUID) -> Task | None:
        return self._tasks.get(task_id)

    def list(
        self, status: TaskStatus | None, limit: int, offset: int
    ) -> tuple[list[Task], int]:
        tasks = sorted(self._tasks.values(), key=lambda t: t.created_at)
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        return tasks[offset : offset + limit], len(tasks)

    def update(self, task_id: UUID, data: TaskUpdate) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None
            changes = data.model_dump(exclude_unset=True)
            changes["updated_at"] = datetime.now(timezone.utc)
            updated = task.model_copy(update=changes)
            self._tasks[task_id] = updated
            return updated

    def delete(self, task_id: UUID) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None

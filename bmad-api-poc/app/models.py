"""API schemas (architecture decision AD-3: Pydantic models are the API contract)."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: TaskPriority = TaskPriority.medium


class TaskUpdate(BaseModel):
    """Partial update: only the fields sent are changed."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: TaskPriority | None = None
    status: TaskStatus | None = None


class Task(BaseModel):
    id: UUID
    title: str
    description: str | None
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class TaskPage(BaseModel):
    items: list[Task]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    """Uniform error envelope (AD-4)."""

    code: str
    message: str

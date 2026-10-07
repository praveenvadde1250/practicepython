# Story 1.1: Create a task

Status: done

## Story
As an integrating developer, I want to `POST /api/v1/tasks` so that I can record new work.

## Acceptance criteria
1. Valid body → `201`, `status=todo`, default `priority=medium`, `Location` header.
2. Empty `title` → `422`, `code=VALIDATION_ERROR`, message names the field.
3. Unknown field → `422`.

## Dev notes (context the Dev agent needs — from architecture.md)
- AD-3: input model `TaskCreate` with `extra="forbid"`; constraints via `Field(...)`.
- AD-4: validation errors go through the `RequestValidationError` handler in `app/errors.py`.
- AD-5: set `Location` to `/api/v1/tasks/{id}`.

## Tasks
- [x] Add `TaskCreate`, `Task`, `TaskPriority`, `TaskStatus` to `app/models.py`
- [x] Implement `InMemoryTaskRepository.create`
- [x] Add `POST /api/v1/tasks` in `app/routers/tasks.py`
- [x] Add error envelope handlers
- [x] Tests: `test_create_task_*` in `tests/test_tasks.py`

## Dev agent record
- Files changed: `app/models.py`, `app/repository.py`, `app/routers/tasks.py`, `app/errors.py`,
  `tests/test_tasks.py`
- Tests: 3 new, all passing.

## Review
`bmad-code-review` run in a fresh chat. No blocking findings.

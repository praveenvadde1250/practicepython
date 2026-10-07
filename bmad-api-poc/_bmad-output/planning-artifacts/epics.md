# Epics and Stories: Task Management API

> Produced with `bmad-create-epics-and-stories` from `prd.md` + `architecture.md`.

## Epic 1: Task CRUD API
Deliver FR1–FR6 with the decisions in `architecture.md`.

### Story 1.1: Create a task
As an integrating developer, I want to `POST /api/v1/tasks` so that I can record new work.

**Acceptance criteria**
1. Given a valid body with `title`, when I POST, then I get `201`, the task with `status=todo`,
   default `priority=medium`, and a `Location` header pointing to the task.
2. Given an empty `title`, then I get `422` with `code=VALIDATION_ERROR` naming the field.
3. Given an unknown field, then I get `422`.

### Story 1.2: Read tasks
As an integrating developer, I want to fetch one task or a filtered, paginated list.

**Acceptance criteria**
1. `GET /api/v1/tasks/{id}` returns the task, or `404` with `code=TASK_NOT_FOUND`.
2. `GET /api/v1/tasks` returns `{items,total,limit,offset}`, oldest first.
3. `?status=` filters; `limit` must be 1–100 (else `422`).

### Story 1.3: Update a task
As an automation owner, I want to `PATCH` a task so that I can move it through statuses.

**Acceptance criteria**
1. Only fields present in the body change; `updated_at` is refreshed.
2. Unknown task ID returns `404` envelope.

### Story 1.4: Delete a task
As an integrating developer, I want to `DELETE` a task.

**Acceptance criteria**
1. Returns `204`; subsequent GET returns `404`.
2. Deleting a missing task returns `404`.

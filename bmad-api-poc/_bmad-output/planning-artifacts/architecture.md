# Architecture: Task Management API

> Phase 3 (Solutioning). Produced with `bmad-architecture` (Winston, `bmad-agent-architect`)
> from `prd.md`. These decisions are what keep separately built stories consistent.

## Stack
Python 3.11+, FastAPI, Pydantic v2, Uvicorn, pytest + FastAPI `TestClient`.

## Decisions

| ID | Decision | Why |
|----|----------|-----|
| AD-1 | Layered layout: `routers/` (HTTP) → `repository.py` (storage) ; `models.py` holds schemas. Routers never touch storage directly except through the repository. | Lets us swap storage without touching endpoints. |
| AD-2 | Storage behind a `TaskRepository` protocol. POC ships `InMemoryTaskRepository`; the repository is injected through `app.state` and a FastAPI dependency. | Satisfies "no DB in POC" and makes tests isolated (fresh repo per test). |
| AD-3 | Pydantic models are the API contract. Separate `TaskCreate`, `TaskUpdate`, `Task` models; `extra="forbid"` on inputs (NFR4). | One source of truth for validation and OpenAPI (NFR3). |
| AD-4 | One error envelope `{"code","message"}` (NFR2), produced only by handlers in `app/errors.py`. Domain errors are exceptions (e.g. `TaskNotFound`), not inline `HTTPException`s. | Consistent client experience; easy to extend. |
| AD-5 | URL prefix `/api/v1` (NFR1). `POST` returns `201` + `Location`; `DELETE` returns `204`; `PATCH` for partial updates. | Standard REST semantics. |
| AD-6 | App factory `create_app(repository=None)`. | Tests and future deployments can inject their own repository. |

## Source tree
```
app/
  main.py          # create_app(), /health
  models.py        # Pydantic schemas (AD-3)
  repository.py    # TaskRepository protocol + in-memory impl (AD-2)
  errors.py        # error envelope handlers (AD-4)
  routers/tasks.py # /api/v1/tasks endpoints (AD-5)
tests/
  conftest.py      # fresh app per test
  test_tasks.py    # one test group per story
```

## Path to production (after POC)
Replace `InMemoryTaskRepository` with a SQL-backed repository implementing the same protocol;
add auth as a FastAPI dependency on the router; containerize.

# PRD: Task Management API

> Phase 2 (Planning). Produced with `bmad-prd` (John, `bmad-agent-pm`) from `product-brief.md`.

## 1. Overview
REST API (JSON over HTTP) for managing tasks. See `product-brief.md` for problem and goals.

## 2. Functional requirements

| ID | Requirement |
|----|-------------|
| FR1 | A client can create a task with a `title` (required, 1–200 chars), optional `description` (≤2000 chars) and `priority` (`low`/`medium`/`high`, default `medium`). New tasks start in status `todo`. |
| FR2 | A client can fetch a single task by its ID. |
| FR3 | A client can list tasks, filter by `status`, and paginate with `limit` (1–100, default 20) and `offset`. |
| FR4 | A client can partially update a task's title, description, priority, or status. |
| FR5 | A client can delete a task. |
| FR6 | The service exposes a `/health` endpoint for liveness checks. |

## 3. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR1 | All endpoints are versioned under `/api/v1`. |
| NFR2 | Every error response uses the same JSON shape: `{"code": "...", "message": "..."}`. |
| NFR3 | The OpenAPI document is generated from code and served at `/openapi.json` and `/docs`. |
| NFR4 | Unknown request fields are rejected (422) rather than silently ignored. |
| NFR5 | Automated tests cover every acceptance criterion; the suite runs in < 10 s. |

## 4. Out of scope (POC)
Authentication/authorization, durable storage, rate limiting, deployment pipeline.

## 5. Open questions
- Which database will replace the in-memory store after the POC? (Owner: Architect)
- Which auth provider (OIDC/SSO) will the real service use? (Owner: PM)

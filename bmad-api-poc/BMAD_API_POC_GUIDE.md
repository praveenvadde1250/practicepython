# BMAD Method for API Development: Step-by-Step POC Guide (AIDLC Team)

This guide shows the AIDLC team how to use the **BMAD Method** ("Agile AI-Driven Development")
to plan and build REST APIs with an AI coding assistant. Every step has a worked example in
this folder: a small **Task Management API** (FastAPI) and the planning documents BMAD produced
for it.

> Written against `bmad-method` **v6.12.1** (npm `latest`, Oct 2026). BMAD changes quickly.
> If a skill name below doesn't exist in your install, run `bmad-help`; it lists what you have.

---

## 0. What BMAD is

BMAD gives your AI assistant a set of **agents** (personas) and **skills** (structured workflows).
Each skill produces a **document** that the next skill reads. Because decisions are written down,
you don't have to re-explain context in every chat, and the code stays consistent across stories.

| Phase | Purpose | Agent (persona) | Key skills | Output (this POC) |
|---|---|---|---|---|
| 1. Analysis (optional) | Understand the problem | Mary – Analyst (`bmad-agent-analyst`) | `bmad-brainstorming`, `bmad-deep-recon`, `bmad-product-brief` | `planning-artifacts/product-brief.md` |
| 2. Planning | Define *what* to build | John – PM (`bmad-agent-pm`) | `bmad-prd` (or `bmad-spec` for small work) | `planning-artifacts/prd.md` |
| 3. Solutioning | Define *how* it hangs together | Winston – Architect (`bmad-agent-architect`) | `bmad-architecture`, `bmad-create-epics-and-stories` | `architecture.md`, `epics.md` |
| 4. Implementation | Build, review, verify | Amelia – Dev (`bmad-agent-dev`) | `bmad-sprint-planning`, `bmad-create-story`, `bmad-build`, `bmad-code-review`, `bmad-qa-generate-e2e-tests`, `bmad-retrospective` | `sprint-status.yaml`, story files, code + tests |

**Choose your depth.** BMAD sizes the process to the work:
- **Small, clear change** (add one endpoint): skip to `bmad-build` directly.
- **New API / service** (this POC): do the full flow, Steps 3–10.
- **Unsure?** Run `bmad-help` and describe what you want to do.

---

## 1. Prerequisites

| Tool | Version | Check |
|---|---|---|
| Node.js | 20.12+ | `node --version` |
| Python | 3.10+ | `python3 --version` |
| uv (BMAD's helper scripts run through it) | latest | `uv --version` (install: `curl -LsSf https://astral.sh/uv/install.sh \| sh`) |
| An AI coding tool | Claude Code, Cursor, GitHub Copilot, Windsurf, … | |
| Git | any | |

---

## 2. Install BMAD into your API project

```bash
mkdir task-api && cd task-api && git init
npx bmad-method@latest install
```

The interactive installer asks for your name, languages, output folder (default `_bmad-output`),
modules (keep **BMad Method / `bmm`** selected), and which AI tools to set up.

**Non-interactive (good for a team template / CI):**

```bash
npx bmad-method@latest install --yes \
  --modules bmm \
  --tools claude-code \
  --user-name "AIDLC Team" \
  --output-folder _bmad-output
```

Use `--list-tools` to see tool IDs (`claude-code`, `cursor`, `github-copilot`, …) and
`--list-options bmm` to see config keys you can set with `--set bmm.<key>=<value>`.

**What gets created**

```
_bmad/                       # BMAD config + module files (commit this)
.claude/skills/bmad-*/       # skills for Claude Code (Cursor/Copilot use .agents/skills/)
_bmad-output/                # created lazily when skills write documents
  planning-artifacts/        # brief, PRD, architecture, epics
  implementation-artifacts/  # sprint-status.yaml, story files, reviews
```

Commit `_bmad/`, the skills folder, and `_bmad-output/` so the whole team shares the same
agents and the same planning context.

**How to call a skill:** in your AI tool, name it — e.g. type `/bmad-prd` in Claude Code, or
just say *"create the PRD"*. Agents are called the same way (`/bmad-agent-architect` or
*"talk to Winston"*).

> **Rule of thumb:** start a **fresh chat for each skill**. The documents carry the context;
> long chats just add noise.

---

## 3. Phase 1 – Product brief (Analyst)

**Run:** `bmad-product-brief` (optionally after `bmad-brainstorming` or `bmad-deep-recon`).

**Prompt example:**
> Create a product brief. We need a REST API for internal teams to create, read, update and
> delete tasks so dashboards and bots can integrate. POC only: no auth, no database yet.

The analyst will interview you (problem, users, goals, out-of-scope, success measures).
Answer honestly — short answers are fine.

**Output:** [`_bmad-output/planning-artifacts/product-brief.md`](./_bmad-output/planning-artifacts/product-brief.md)

**Check before moving on:** problem, users, scope and *out-of-scope* are explicit.

---

## 4. Phase 2 – PRD (Product Manager)

**Run:** `bmad-prd` in a new chat. It reads the brief automatically.

**Prompt example:**
> Create the PRD from the product brief. Focus on API behaviour: endpoints, validation rules,
> pagination, error format, and versioning.

**API-specific things to make the PM pin down** (these prevent most rework):
- Field rules (required, lengths, enums, defaults)
- Pagination & filtering contract (`limit`/`offset` bounds)
- Error response shape (one shape for all errors)
- Versioning (`/api/v1`)
- What happens with unknown fields, missing IDs, empty lists

**Output:** [`prd.md`](./_bmad-output/planning-artifacts/prd.md) — FR1–FR6 and NFR1–NFR5.

**Validate:** run `bmad-prd` again and ask it to *"validate the PRD"*.

---

## 5. Phase 3a – Architecture (Architect)

**Run:** `bmad-architecture` in a new chat.

**Prompt example:**
> Create the architecture from the PRD. Stack: Python, FastAPI, Pydantic v2, pytest. Storage
> must be swappable; in-memory for the POC. Keep it short — decisions only.

The output is a short list of **decisions** (AD-1 … AD-6 in our example) that every story must
follow: layering, repository pattern, contract-first models, error envelope, REST conventions,
app factory. This is what stops five stories from producing five different coding styles.

**Output:** [`architecture.md`](./_bmad-output/planning-artifacts/architecture.md)

**Tip for API teams:** ask Winston to include the **source tree** and the **error format**
explicitly. Those two save the most time later.

---

## 6. Phase 3b – Epics & stories

**Run:** `bmad-create-epics-and-stories`.

**Prompt example:**
> Create the epics and stories list from the PRD and architecture. One story per endpoint
> group, each with Given/When/Then acceptance criteria.

**Output:** [`epics.md`](./_bmad-output/planning-artifacts/epics.md) — Epic 1 with stories
1.1 Create, 1.2 Read, 1.3 Update, 1.4 Delete.

**Good API stories are:** one endpoint (or a tight group), testable ACs that name status codes
and error codes, small enough to finish in one dev session.

---

## 7. Phase 4a – Sprint planning (readiness gate)

**Run:** `bmad-sprint-planning` → *"run sprint planning"*.

It first checks that PRD, architecture and epics are complete enough to build ("implementation
readiness"), then generates `sprint-status.yaml`, which tracks every story through:

```
backlog → ready-for-dev → in-progress → review → done
```

**Output:** [`sprint-status.yaml`](./_bmad-output/implementation-artifacts/sprint-status.yaml)

Ask *"show sprint status"* at any time to see progress and the recommended next story.

---

## 8. Phase 4b – Build each story (Dev)

Repeat for every story, **each in a fresh chat**:

1. **Prepare the story** – `bmad-create-story` → *"create the next story"*. It writes a story
   file with ACs, tasks, and *dev notes* pulled from the architecture.
   Example: [`1-1-create-a-task.md`](./_bmad-output/implementation-artifacts/1-1-create-a-task.md)
2. **Implement** – `bmad-build` → *"build story 1.1"* (or give it the story file path).
   It writes code + tests, runs them, and records what changed in the story file.
3. **Review** – `bmad-code-review` → *"run code review"*. Use a **fresh chat** (ideally a
   different model) so the reviewer isn't biased by the author's reasoning. Fix findings, rerun.
4. **Mark done** – the story moves to `done` in `sprint-status.yaml`.

For the POC, the result of Epic 1 is the code in [`app/`](./app) and tests in [`tests/`](./tests).

**Optional:**
- `bmad-qa-generate-e2e-tests` → *"create qa automated tests for the tasks API"* to add API
  tests beyond the story-level ones.
- `bmad-walkthrough` → a guided human review of a change before merge.
- `bmad-correct-course` → if requirements change mid-sprint; it updates PRD/epics/architecture
  consistently instead of letting docs drift.

---

## 9. Run and verify the sample API

```bash
cd bmad-api-poc
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pytest -q                         # 11 tests, one group per story AC
uvicorn app.main:app --reload     # http://127.0.0.1:8000/docs  (Swagger UI)
```

Try it:

```bash
curl -s -X POST localhost:8000/api/v1/tasks -H 'content-type: application/json' \
     -d '{"title":"Write PRD","priority":"high"}'
curl -s 'localhost:8000/api/v1/tasks?status=todo&limit=10'
curl -s -X PATCH localhost:8000/api/v1/tasks/<id> -H 'content-type: application/json' \
     -d '{"status":"done"}'
curl -s -X DELETE -i localhost:8000/api/v1/tasks/<id>
```

| Method | Path | Success | Errors |
|---|---|---|---|
| GET | `/health` | 200 | – |
| POST | `/api/v1/tasks` | 201 + `Location` | 422 `VALIDATION_ERROR` |
| GET | `/api/v1/tasks?status=&limit=&offset=` | 200 `{items,total,limit,offset}` | 422 |
| GET | `/api/v1/tasks/{id}` | 200 | 404 `TASK_NOT_FOUND` |
| PATCH | `/api/v1/tasks/{id}` | 200 | 404, 422 |
| DELETE | `/api/v1/tasks/{id}` | 204 | 404 |

---

## 10. Retrospective & POC evaluation

**Run:** `bmad-retrospective` → *"lets retro epic 1"*. It reviews the stories, diffs and sprint
status and produces findings + action items.

Use this scorecard to report the POC outcome to the team:

| Criterion | How to measure | Result |
|---|---|---|
| Time from idea to working API | Wall-clock per phase | |
| Rework | # of stories that needed a second build/review round | |
| Consistency | Do all endpoints follow AD-1…AD-6 without reminders? | |
| Test coverage of ACs | Every AC has a test? | |
| Onboarding | Can a new dev run it from this guide in < 10 min? | |
| Doc quality | Are PRD/architecture usable as real design docs? | |

---

## 11. Rolling BMAD out to the AIDLC team

1. **Team template repo** – install BMAD once with the non-interactive command, commit `_bmad/`
   and skills, and use it as the starting point for new API services.
2. **Customize, don't fork** – use `bmad-customize` to bake in team standards (e.g. "always use
   our error envelope", "OpenAPI first", "pytest + 90% coverage") so every agent follows them.
3. **Project context** – run `bmad-project-context` to write an `AGENTS.md` block with repo
   conventions and recurring AI mistakes ("pitfalls").
4. **Existing services** – BMAD works on brownfield code too: start with `bmad-help` and
   *"I want to add an endpoint to this existing service"*.
5. **Definition of done per story** – ACs tested, `bmad-code-review` clean, sprint status
   updated, docs (OpenAPI) regenerated.
6. **Keep humans on decisions** – agents draft; people approve the brief, PRD, architecture and
   every merge.

---

## Common pitfalls

| Pitfall | Fix |
|---|---|
| One giant chat for all phases | New chat per skill; the documents carry context. |
| Skipping architecture for an API | Endpoints drift in error format, naming, layering. Always do Step 5 for new services. |
| Vague ACs ("handles errors") | Name status codes and error codes in every AC. |
| Self-review by the same chat | Run `bmad-code-review` in a fresh chat / different model. |
| Docs drift after a change | Use `bmad-correct-course`, not ad-hoc edits. |
| Not sure what's next | `bmad-help` or *"show sprint status"*. |

## References
- BMAD Method repo: https://github.com/bmad-code-org/BMAD-METHOD
- Docs: https://docs.bmad-method.org (start with *Build Your First Change* and *Choose a Planning Path*)
- npm: https://www.npmjs.com/package/bmad-method

"""Acceptance-criteria tests for Epic 1 (one test group per story AC)."""

from uuid import uuid4

BASE = "/api/v1/tasks"


def make(client, **overrides):
    body = {"title": "Write PRD", **overrides}
    resp = client.post(BASE, json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


# Story 1.1 - Create a task
def test_create_task_returns_201_with_defaults_and_location(client):
    resp = client.post(BASE, json={"title": "Write PRD"})
    assert resp.status_code == 201
    task = resp.json()
    assert task["status"] == "todo"
    assert task["priority"] == "medium"
    assert resp.headers["Location"] == f"{BASE}/{task['id']}"


def test_create_task_rejects_empty_title(client):
    resp = client.post(BASE, json={"title": ""})
    assert resp.status_code == 422
    assert resp.json()["code"] == "VALIDATION_ERROR"
    assert resp.json()["message"].startswith("title:")


def test_create_task_rejects_unknown_fields(client):
    resp = client.post(BASE, json={"title": "x", "owner": "bob"})
    assert resp.status_code == 422


# Story 1.2 - Read tasks
def test_get_task_by_id(client):
    task = make(client)
    assert client.get(f"{BASE}/{task['id']}").json() == task


def test_get_missing_task_returns_404_envelope(client):
    resp = client.get(f"{BASE}/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["code"] == "TASK_NOT_FOUND"


def test_list_tasks_paginates_and_filters(client):
    for i in range(5):
        make(client, title=f"t{i}")
    first = make(client, title="finished")
    client.patch(f"{BASE}/{first['id']}", json={"status": "done"})

    page = client.get(BASE, params={"limit": 2, "offset": 1}).json()
    assert page["total"] == 6
    assert [t["title"] for t in page["items"]] == ["t1", "t2"]

    done = client.get(BASE, params={"status": "done"}).json()
    assert done["total"] == 1
    assert done["items"][0]["title"] == "finished"


def test_list_rejects_limit_over_100(client):
    assert client.get(BASE, params={"limit": 101}).status_code == 422


# Story 1.3 - Update a task
def test_patch_changes_only_sent_fields(client):
    task = make(client, description="draft")
    resp = client.patch(f"{BASE}/{task['id']}", json={"status": "in_progress"})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["status"] == "in_progress"
    assert updated["description"] == "draft"
    assert updated["updated_at"] >= task["updated_at"]


def test_patch_missing_task_returns_404(client):
    assert client.patch(f"{BASE}/{uuid4()}", json={"status": "done"}).status_code == 404


# Story 1.4 - Delete a task
def test_delete_task(client):
    task = make(client)
    assert client.delete(f"{BASE}/{task['id']}").status_code == 204
    assert client.get(f"{BASE}/{task['id']}").status_code == 404
    assert client.delete(f"{BASE}/{task['id']}").status_code == 404

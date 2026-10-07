# practicepython

## BMAD API POC

[`bmad-api-poc/`](./bmad-api-poc) is a proof of concept for using the **BMAD Method** to build
APIs in the AIDLC team.

- **Start here:** [`bmad-api-poc/BMAD_API_POC_GUIDE.md`](./bmad-api-poc/BMAD_API_POC_GUIDE.md), a step-by-step guide
- **BMAD documents:** [`bmad-api-poc/_bmad-output/`](./bmad-api-poc/_bmad-output) (brief, PRD, architecture, epics, sprint status, story)
- **Working API:** [`bmad-api-poc/app/`](./bmad-api-poc/app) (FastAPI) with tests in [`bmad-api-poc/tests/`](./bmad-api-poc/tests)

```bash
cd bmad-api-poc
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload   # open http://127.0.0.1:8000/docs
```

# Najm Transfers: the sample system under test

A small, fictional banking back end that the *Software Testing: Zero to Hero in the AI Era* course tests, lesson after lesson. Everything in it — the bank, the limits, the fees, the rules — is made up.

| Part | What it is | Used in |
|---|---|---|
| `najm/transfers.py` | Business rules: money rounding, fees, limits, cut-off times, idempotent transfers | Unit and integration tests, test design, property-based tests, mutation testing |
| `najm/api.py` | A FastAPI REST API: `POST /transfers`, `GET /transfers/{id}`, `GET /accounts/{id}/balance`, `GET /health` | API testing, security testing, performance testing |
| `static/transfer.html` | A small web page served at `/app` (English, and Arabic right-to-left with `?lang=ar`) | End-to-end, accessibility and localisation testing |
| `najm/assist.py` | **Najm Assist**: a deterministic stand-in for an LLM assistant — retrieval over policy documents, a fake model, and tools | Evals, RAG tests, agent tests, red-teaming |
| `tests/` | A deliberately incomplete starter test suite | Test quality, mutation testing |
| `e2e/` | A Playwright starter that starts the API and drives the page | End-to-end testing |

## Run it

```bash
cd testing/sample
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                                                # the starter suite
uvicorn najm.api:app --port 8000                      # the API; open http://127.0.0.1:8000/app
```

End-to-end tests (Node 20+):

```bash
npm install
npx playwright install chromium
PYTHON=.venv/bin/python npx playwright test --config e2e/playwright.config.ts
```

Fake tokens for the API: `Authorization: Bearer token-alice` (owns `acc-1` and `acc-3`) and `Bearer token-bob` (owns `acc-2`). `POST /transfers` also needs an `Idempotency-Key` header.

## Seeded bugs

Set an environment variable and the system misbehaves in one specific, realistic way. Your job is to write tests that notice.

| Variable | Bug name | What goes wrong |
|---|---|---|
| `NAJM_BUGS` | `limit_off_by_one` | The daily limit is checked with `>=` instead of `>` |
| `NAJM_BUGS` | `float_fee` | The international fee is computed with binary floats and `round()` |
| `NAJM_BUGS` | `tz_cutoff` | The 15:00 cut-off is read in UTC instead of Qatar time |
| `NAJM_BUGS` | `no_idempotency` | Repeating a request with the same key creates a second transfer |
| `NAJM_BUGS` | `bola` | Any signed-in user can read any transfer |
| `NAJM_AI_BUGS` | `hallucinate` | With no policy found, the assistant invents an answer |
| `NAJM_AI_BUGS` | `obey_injection` | The assistant follows instructions hidden inside a policy document |
| `NAJM_AI_BUGS` | `skip_confirm` | A card is frozen without the customer's confirmation |
| `NAJM_AI_BUGS` | `wrong_account` | The assistant reads a balance from the wrong account |

Combine them with commas: `NAJM_BUGS=float_fee,bola pytest`. A good suite passes with no bug switched on and fails for every bug. How many does the starter suite catch?

> The pytest run may print a deprecation notice about Starlette's test client and `httpx`. It is harmless.

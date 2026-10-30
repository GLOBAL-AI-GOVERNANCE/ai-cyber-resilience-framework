# AGENTS.md

Instructions for coding agents working in this repository.

## Setup and checks

```bash
python3 -m venv .venv && . .venv/bin/activate
python3 -m pip install --require-hashes --no-deps -r requirements-schema.lock
python3 -B tools/check_history_privacy.py
python3 -B tools/validate_schemas_standard.py
python3 -B tools/validate_framework.py
python3 -B tools/validate_assurance.py examples/secure-inference-cell/reference-bundle.json
ACRF_REQUIRE_STANDARD_SCHEMA=1 python3 -m unittest discover -s tests -v
```

## Rules

- This is a defensive reference framework, not executable security software, certification, or proof that a control works.
- Every public result keeps `authority_effect: "NONE"`. Do not add a path that approves, certifies, or authorizes.
- Prefer squash-merge through green CI. Do not force-push `main`.

## Setup guide

End-to-end local setup for the toolkit and MCP: [AGENT_SETUP](https://ai-governance.solutions/AGENT_SETUP.html).

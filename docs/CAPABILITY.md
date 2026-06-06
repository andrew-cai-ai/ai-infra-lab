# Agent Reliability Platform Capability

## CAPABILITY

The Agent Reliability Platform lets AI engineers, founders, and internal platform teams run offline, versioned evals against an AI agent before they have production traffic. In v1, the platform is CLI-first: it validates eval cases and suites, runs one sample agent end to end, applies deterministic graders, writes observable run artifacts, promotes baselines, compares later runs against those baselines, validates local trace artifacts, inspects trace summaries, and emits human-readable failure reports with concrete evidence.

## CONSTRAINTS

- v1 is CLI-first and does not include FastAPI, a web UI, hosted dashboards, or production trace ingestion.
- v1 supports local trace artifact validation and inspection, but does not yet persist imported traces under `artifacts/traces/`.
- v1 must work in a blank repo without observability infrastructure.
- Eval cases are versioned files committed with the repo.
- Deterministic checks are the only v1 grading path.
- LLM judges cannot be added until deterministic grading, artifacts, and regression comparison are stable.
- External actions are not executed in v1; fake/sample agents may only emit local artifacts.
- Failures must include expected value, actual value, and evidence.

## DAILY ECC SURFACE

- `product-capability`: this file is the durable implementation contract.
- `agent-sort`: only the vertical-slice surfaces are active by default.
- `eval-harness`: eval cases, deterministic graders, pass/fail run artifacts, and regression comparison.
- `trace-contract`: local trace artifacts with spans, parent references, model calls, tool calls, external actions, errors, tokens, cost, and inspection summaries.
- `verification-loop`: schema tests, runner tests, baseline tests, CLI tests, and command-level verification.

## LIBRARY / PHASE 2

- Memory Store and memory behavior checks.
- LLM judge graders and judge calibration.
- Production trace ingestion.
- Trace-to-eval conversion.
- Hosted dashboard or FastAPI service.
- Multi-agent orchestration.
- Real external action execution with human approval workflows.

## IMPLEMENTATION CONTRACT

### Actors

- AI engineer: authors eval cases and runs suites locally.
- Founder/operator: checks whether a candidate agent regressed before release.
- Internal platform team: standardizes deterministic quality gates.
- Sample agent: deterministic fake agent used to prove the harness works end to end.

### Surfaces

- CLI commands:
  - `case validate`
  - `trace validate`
  - `trace inspect`
  - `run`
  - `baseline promote`
  - `compare`
  - `report`
- JSON eval case files under `evals/cases/`.
- JSON suite files under `evals/suites/`.
- Run artifacts under `artifacts/runs/`.
- Baseline artifacts under `artifacts/baselines/`.
- Trace examples under `examples/traces/`.

### States

- Eval case: `draft -> valid -> active`.
- Run: `running -> passed|failed|errored`.
- Baseline: `none -> promoted -> superseded`.
- Regression comparison: `not_compared -> passed|regressed`.

### Interfaces

- Eval case input: JSON file using `arp.eval.case.v1`.
- Suite input: JSON file using `arp.eval.suite.v1`.
- Trace input: JSON file using `arp.trace.v1`.
- Agent output: JSON object with `output`, `transcript`, `tool_calls`, and `external_actions`.
- Run output: `run.json`, per-case attempt artifacts, timing metadata, and `report.txt`.
- Errored run output: `run.json`, per-case attempt artifacts, timing metadata, captured error type/message, and `report.txt`.
- Baseline output: one promoted JSON baseline per suite and agent.
- Trace inspection output: span count, model call count, tool call count, external action count, error count, token totals, and cost total.

## QUALITY GATES

- Case schema gate: every case has id, version, task prompt, and deterministic checks.
- Deterministic grader gate: every active case has at least one deterministic check.
- Artifact gate: every run writes machine-readable JSON and a human-readable report.
- Observability gate: every run and per-case attempt records start time, completion time, and duration.
- Trace schema gate: every local trace has trace id, agent id, lifecycle timing, status, and at least one validated span.
- Trace parent gate: every non-root span parent reference must point to an existing span.
- Error artifact gate: agent or grader exceptions are captured as `errored` case/run artifacts with type and message.
- Regression gate: a run fails comparison if any case that passed in the baseline fails now.
- Explainability gate: every failed check records expected value, actual value, and evidence.

## NON-GOALS

- Hosted SaaS.
- Production observability.
- Full approval workflow for real external actions.
- General-purpose agent runtime.
- LLM-as-judge scoring in v1.

## HANDOFF

Ready for implementation as a Python standard-library CLI vertical slice.

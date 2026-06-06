# AI Infra Lab Architecture

## Consolidation Summary

AI Infra Lab is the single unified project for the AI infrastructure portfolio.

The workspace review found:

| Project Name | Workspace Evidence | Keep As | Decision |
| --- | --- | --- | --- |
| `agent-reliability-platform` | Root `pyproject.toml`, `arp/`, `evals/`, `tests/`, `docs/CAPABILITY.md` | Current implementation slice | Keep in root as the active platform core |
| `llm-evaluation-platform` | Evaluation behavior inside `arp`: cases, suites, graders, baselines, reports | Evaluation module | Merge into AI Infra Lab |
| `agent-observability-platform` | Timing metadata, run artifacts, attempt artifacts, error capture, and first-class trace artifact validation/inspection | Observability module | Merge into AI Infra Lab as trace/run observability |
| `unify-ai-infrastructure` | Prior portfolio strategy doc | Architecture and roadmap docs | Replace with unified docs |
| `course-planner-agent` | `apps/course-planner-agent` | Reference agent only | Archive as non-core standalone app |

## Overlap Analysis

| Overlap Area | Duplicate Concern | Unified Decision |
| --- | --- | --- |
| Eval cases and suites | LLM evaluation and agent reliability both need versioned cases, suites, graders, and pass/fail evidence | One Evaluation module owns cases, suites, graders, dataset runs, and comparisons |
| Baselines and regressions | Evaluation and reliability both compare current behavior against expected behavior | Reliability uses Evaluation baselines as release gates |
| Run artifacts | Observability, evaluation, and reliability all need run status, timing, errors, and evidence | One Run Artifact schema feeds all modules |
| Traces | Observability traces and eval attempts both represent agent execution | One Trace schema with spans, tool calls, model calls, external actions, errors, cost, and latency |
| Reports | Evaluation reports, reliability reports, and incident reports can diverge | Reports are generated from shared artifacts instead of separate ad hoc formats |
| Governance | Policy enforcement can be duplicated across agents, evals, and runtime tooling | Governance owns policy decisions and approval artifacts |
| Correction loops | Eval failures, trace failures, incidents, and feedback can create separate TODO lists | Correction owns trace-to-eval, incident-to-eval, and feedback-to-eval workflows |

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Agents["Agent Workloads"]
        A1["Reference Agents"]
        A2["Production Agent Adapters"]
        A3["Tool Calls"]
        A4["Model Calls"]
        A5["External Actions"]
    end

    subgraph Ingestion["Ingestion Layer"]
        I1["Eval Runner"]
        I2["Trace Import"]
        I3["Policy Event Import"]
        I4["Feedback Import"]
        I5["Schema Validation"]
    end

    subgraph Artifacts["Artifact Stores"]
        S1["Run Artifacts"]
        S2["Trace Artifacts"]
        S3["Eval Cases and Suites"]
        S4["Baselines"]
        S5["Policy Decisions"]
        S6["Approvals"]
        S7["Incidents"]
        S8["Registries"]
    end

    subgraph Platform["AI Infra Lab Modules"]
        M1["Evaluation"]
        M2["Observability"]
        M3["Reliability"]
        M4["Governance"]
        M5["Operations"]
        M6["Correction"]
    end

    subgraph Interfaces["Operator Interfaces"]
        U1["CLI"]
        U2["CI/CD Gates"]
        U3["API"]
        U4["Dashboard"]
        U5["Interview Case Study Docs"]
    end

    A1 --> I1
    A2 --> I1
    A2 --> I2
    A3 --> I2
    A4 --> I2
    A5 --> I3

    I1 --> I5
    I2 --> I5
    I3 --> I5
    I4 --> I5

    I5 --> S1
    I5 --> S2
    I5 --> S3
    I5 --> S5
    I5 --> S6

    S1 --> M1
    S1 --> M2
    S2 --> M2
    S2 --> M6
    S3 --> M1
    S4 --> M1
    S4 --> M3
    S5 --> M4
    S6 --> M4
    S7 --> M3
    S7 --> M6
    S8 --> M5

    M1 --> U1
    M1 --> U2
    M2 --> U1
    M2 --> U4
    M3 --> U2
    M3 --> U4
    M4 --> U3
    M4 --> U4
    M5 --> U3
    M5 --> U4
    M6 --> M1
    M6 --> U5
```

## Module Responsibilities

### Evaluation

Owns quality measurement:

- eval case schemas
- eval suite schemas
- deterministic graders
- LLM judge integration later
- baseline promotion
- regression comparison
- prompt and model comparison
- evaluation reports

Current code: `arp/schema.py`, `arp/graders.py`, `arp/runner.py`, `arp/baseline.py`, `arp/report.py`.

### Observability

Owns understanding what agents did:

- trace schema
- span and event import
- model call telemetry
- tool call telemetry
- latency and cost metadata
- run inspection
- OpenTelemetry-shaped identifiers

Current coverage: run and attempt artifacts with timing and errors, plus `arp.trace.v1` trace artifacts with spans, model calls, tool calls, external actions, errors, tokens, cost, parent span references, validation, and CLI inspection.

Missing: persisted trace import into `artifacts/traces/`, OpenTelemetry ingestion, and trace-to-eval conversion.

### Reliability

Owns dependable production behavior:

- release gates
- SLO evaluation
- retry and fallback policy modeling
- incident artifacts
- regression blocking
- failure trend reporting

Current coverage: baseline comparison, errored run capture, CLI exit codes.

### Governance

Owns risk control:

- policy schemas
- policy decisions
- approval requests
- risk scores
- external action controls
- audit records

Current coverage: none in root implementation. This is a priority gap.

### Operations

Owns lifecycle management:

- agent registry
- prompt registry
- model/provider metadata
- usage analytics
- cost tracking
- version promotion
- owner and environment metadata

Current coverage: minimal agent ID in run artifacts.

### Correction

Owns continuous improvement:

- failed-run-to-eval workflows
- trace-to-eval workflows
- incident-to-eval workflows
- feedback capture
- correction report artifacts

Current coverage: reports expose evidence, but there is no correction workflow yet.

## Single Architecture Principle

All modules should read and write shared artifacts. Avoid separate formats for evaluation, observability, governance, and reliability.

The core artifact chain should be:

```text
agent execution -> trace artifact -> run artifact -> eval result -> baseline comparison -> release gate -> incident/correction if needed
```

This is the main reason the projects should be merged.

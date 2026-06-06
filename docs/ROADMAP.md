# AI Infra Lab Unified Roadmap

## Roadmap Objective

Move from a CLI-first reliability harness to a unified AI infrastructure control plane.

The roadmap optimizes for Staff AI Infrastructure interview signal:

- platform contracts
- schema evolution
- observability
- reliability controls
- governance
- operational lifecycle management
- correction loops

## Phase 0: Consolidation

Status: in progress.

Deliverables:

- Single root project name: `AI Infra Lab`.
- Root README for unified positioning.
- Unified architecture doc.
- Unified roadmap.
- Module structure doc.
- 30-day execution plan.
- Archive standalone app/demo material.

## Phase 1: Shared Run And Trace Foundation

Target: first 30 days.

Deliverables:

- `RunArtifact` schema that contains suite, agent, prompt, model, timing, cost, status, errors, and case results.
- `TraceArtifact` schema with spans, model calls, tool calls, external actions, parent-child relationships, and OpenTelemetry-shaped IDs. Initial local schema and CLI inspection are implemented with `arp.trace.v1`.
- Agent adapter interface so the platform can run more than the built-in sample agent.
- CLI commands:
  - `trace validate` implemented
  - `trace inspect` implemented
  - `trace import`
  - `eval from-trace`
- Examples that show trace-to-eval conversion.

Staff signal:

- Evaluation and observability use the same evidence model.
- The platform can explain agent behavior before and after failures.

## Phase 2: Registry And Release Gates

Target: days 31-60.

Deliverables:

- Agent registry.
- Prompt registry.
- Baseline history.
- Release gate command.
- SLO definitions for eval pass rate, latency, error rate, and cost.
- CI example that blocks on regressions.

Staff signal:

- The project becomes operational infrastructure, not a local test harness.

## Phase 3: Governance

Target: days 61-90.

Deliverables:

- Policy schema.
- Policy evaluator.
- Policy decision artifacts.
- Risk scoring for tools and external actions.
- Approval request and approval decision artifacts.
- Governance report.

Staff signal:

- The platform controls agent risk, not only measures quality.

## Phase 4: Correction Loops

Target: months 4-6.

Deliverables:

- Incident schema.
- Failed run to eval case workflow.
- Trace to eval case workflow.
- Feedback artifact schema.
- Correction reports.
- Dataset curation workflow.

Staff signal:

- Production failures become durable test coverage.

## Phase 5: API And Dashboard

Target: months 6-12.

Deliverables:

- Query API for runs, traces, baselines, policies, incidents, and registries.
- Operator dashboard for traces, eval results, release gates, and incidents.
- OpenTelemetry collector integration.
- Cost and usage analytics.
- Multi-agent and multi-environment support.

Staff signal:

- The portfolio demonstrates end-to-end AI platform architecture.

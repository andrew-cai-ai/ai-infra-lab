# AI Infra Lab Module Structure

## Current Structure

```text
AI Infra Lab/
  README.md
  pyproject.toml
  arp/
    cli.py
    schema.py
    runner.py
    graders.py
    baseline.py
    report.py
    sample_agent.py
  evals/
    cases/
    suites/
  examples/
    traces/
  tests/
  docs/
  archive/
```

The `arp` package is the active implementation. It should be treated as the first vertical slice of AI Infra Lab, not as a separate final product.

Current trace support lives in:

```text
arp/schema.py              # arp.trace.v1 validation
arp/traces.py              # trace summaries and inspection formatting
examples/traces/           # passing and errored trace fixtures
tests/test_traces.py       # trace schema and CLI coverage
```

## Target Structure

The target module structure should be introduced incrementally. Do not rename everything at once unless the tests and CLI migration are handled in the same change.

```text
AI Infra Lab/
  README.md
  pyproject.toml
  ai_infra_lab/
    __init__.py
    cli.py
    schemas/
      eval_case.py
      eval_suite.py
      run_artifact.py
      trace_artifact.py
      agent_registry.py
      prompt_registry.py
      policy.py
      approval.py
      incident.py
      slo.py
    evaluation/
      runner.py
      graders.py
      baselines.py
      reports.py
      datasets.py
      comparisons.py
    observability/
      traces.py
      spans.py
      importers.py
      metrics.py
      otel.py
    reliability/
      release_gate.py
      slo.py
      incidents.py
      fallback.py
      retry.py
    governance/
      policies.py
      decisions.py
      approvals.py
      risk.py
    operations/
      agents.py
      prompts.py
      models.py
      cost.py
      usage.py
    correction/
      feedback.py
      trace_to_eval.py
      incident_to_eval.py
      failure_to_eval.py
  evals/
    cases/
    suites/
    datasets/
  examples/
    traces/
    runs/
    policies/
    incidents/
  tests/
    evaluation/
    observability/
    reliability/
    governance/
    operations/
    correction/
  docs/
  archive/
```

## Migration Order

1. Keep `arp` stable while adding new schemas.
2. Add `ai_infra_lab/schemas` and keep existing tests passing.
3. Move schema validation from `arp/schema.py` into `ai_infra_lab/schemas`.
4. Add compatibility imports from `arp` while tests migrate.
5. Move runner, graders, baselines, and reports into `ai_infra_lab/evaluation`.
6. Add observability trace import and inspect commands.
7. Replace the `arp` CLI name only after the unified CLI is stable.

## Mapping From Old Projects To Modules

| Old Project | Unified Module |
| --- | --- |
| `llm-evaluation-platform` | `ai_infra_lab/evaluation` |
| `agent-reliability-platform` | `ai_infra_lab/reliability` plus `ai_infra_lab/evaluation` |
| `agent-observability-platform` | `ai_infra_lab/observability` |
| `unify-ai-infrastructure` | `docs/`, `README.md`, and architecture artifacts |

## What Should Not Be Mainline

Standalone domain apps should not live as primary projects in this repo. They can be archived as reference agents or examples.

The archived course planner is useful as a future source of sample traces, but it should not define the portfolio.

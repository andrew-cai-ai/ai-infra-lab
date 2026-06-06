# AI Infra Lab

AI Infra Lab is a unified AI infrastructure portfolio for operating AI agents in production-oriented environments.

The project consolidates four previously separate ideas:

- `llm-evaluation-platform`
- `agent-reliability-platform`
- `agent-observability-platform`
- `unify-ai-infrastructure`

The goal is not to build another chatbot, RAG demo, or standalone AI app. The goal is to demonstrate platform engineering for AI systems: evaluation, observability, reliability, governance, operations, and correction loops.

## Current Implementation

The current working implementation is the `arp` package. It provides a CLI-first agent reliability and evaluation harness:

- versioned eval cases and suites
- deterministic graders
- run artifacts
- per-case attempt artifacts
- baseline promotion
- regression comparison
- explainable failure reports
- timing and error capture
- CLI exit codes suitable for CI gates
- trace artifact validation
- trace inspection summaries for spans, model calls, tool calls, errors, tokens, and cost

## Unified Architecture

The long-term platform architecture is documented in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Core modules:

- Evaluation
- Observability
- Reliability
- Governance
- Operations
- Correction

## Project Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Unified Roadmap](docs/ROADMAP.md)
- [Module Structure](docs/MODULE_STRUCTURE.md)
- [Next 30-Day Plan](docs/NEXT_30_DAYS.md)
- [Current Capability Contract](docs/CAPABILITY.md)
- [Archive Notes](archive/README.md)

## Run The Current Reliability Gate

Validate the sample suite:

```bash
python3 -m arp suite validate evals/suites/sample.json
```

Run the suite:

```bash
python3 -m arp run --suite evals/suites/sample.json --agent sample
```

Promote a baseline:

```bash
python3 -m arp baseline promote artifacts/runs/<run_id>/run.json
```

Compare against the baseline:

```bash
python3 -m arp compare artifacts/runs/<run_id>/run.json
```

Print the report:

```bash
python3 -m arp report artifacts/runs/<run_id>/run.json
```

Validate a trace artifact:

```bash
python3 -m arp trace validate examples/traces/sample_success.json
```

Inspect a trace artifact:

```bash
python3 -m arp trace inspect examples/traces/sample_success.json
```

## Consolidation Decision

The root project is now `AI Infra Lab`. Standalone app material is archived as reference material. Platform capability work should happen in the root project and should map to one or more of:

- Evaluate
- Control
- Correct

# AI Infra Lab Next 30-Day Plan

## Outcome

By the end of 30 days, AI Infra Lab should have a credible unified platform foundation:

- one root project identity
- shared run and trace schemas
- trace import and inspection
- trace-to-eval conversion
- agent registry v1
- CI-ready release gate story
- updated docs and interview walkthrough

## Week 1: Consolidate And Stabilize

Deliverables:

- Keep root project as `AI Infra Lab`.
- Archive standalone app/demo material.
- Keep `arp` tests passing.
- Add a first version of `RunArtifact` and `TraceArtifact` schemas.
- Add fixture examples for a passing trace and failing trace.
- Update README and architecture docs.

Status:

- Completed: first-class `TraceArtifact` schema under `arp.trace.v1`.
- Completed: passing and errored trace fixtures under `examples/traces/`.
- Completed: `trace validate` and `trace inspect` CLI commands.
- Remaining: explicit `RunArtifact` schema beyond current generated `run.json`.

Acceptance criteria:

- Root tests pass.
- The docs clearly explain how evaluation, observability, reliability, governance, operations, and correction fit together.
- No standalone app is presented as the main project.

## Week 2: Observability Foundation

Deliverables:

- Add `trace import` command.
- Add `trace inspect` command. Completed for local trace files.
- Store traces under `artifacts/traces/`.
- Include span IDs, parent span IDs, tool calls, model calls, external actions, status, errors, latency, tokens, and cost fields.

Acceptance criteria:

- A trace fixture can be imported.
- A trace can be inspected from the CLI.
- Invalid trace payloads fail schema validation.

## Week 3: Trace-To-Eval Loop

Deliverables:

- Add `eval from-trace` command.
- Generate eval cases from failed traces.
- Link generated eval cases back to source trace IDs.
- Add tests for trace-to-eval conversion.

Acceptance criteria:

- A failed trace becomes a versioned eval case.
- The generated case can be added to a suite.
- The suite can run through the existing reliability gate.

## Week 4: Registry And Release Gate

Deliverables:

- Add agent registry v1.
- Add prompt registry v1.
- Add release gate command that combines eval result, baseline comparison, and basic latency/error thresholds.
- Add CI example.
- Add interview walkthrough doc.

Acceptance criteria:

- A registered agent can be associated with an eval suite.
- A release gate can pass or fail from CLI output.
- The project has a clear Staff AI Infrastructure narrative.

## Weekly Working Cadence

Use two to four focused implementation sessions per week.

Each session should produce:

- one merged capability slice
- tests for the slice
- a short doc update explaining the platform reason
- a brief interview note explaining how to discuss it

Do not optimize for daily code churn. Optimize for defensible platform milestones.

## 2026-06-07 - GitHub portfolio update

Updated the AI Career Director backend with infrastructure-oriented features: job scoring, career profile, approval workflows, content drafts, and daily brief generation.

Strategic angle: Repo: AI Infra Lab. Daily career execution for Andrew Cai. Positioning: Senior software engineer in Toronto with 7+ years building secure, scalable cloud platforms and APIs in high-uptime, regulated environments across Disney Streaming, Binance, and TikTok. Targeting AI infrastructure, LLM evaluation, agent observability, tool-integrated AI workflows, and platform systems with enterprise controls such as RBAC, audit logs, rate limiting, and production reliability. Career signal to show: one unified Staff-level AI Infrastructure portfolio. Update only AI Infra Lab: README.md, docs/ARCHITECTURE.md, docs/ROADMAP.md, docs/MODULE_STRUCTURE.md, docs/NEXT_30_DAYS.md, arp/, evals/, or tests/. Do not create or update standalone demo repos. Top roles reviewed: Senior Software Engineer, Data Platform at Gusto.

## 2026-06-08 - GitHub portfolio update

Updated the AI Career Director backend with infrastructure-oriented features: job scoring, career profile, approval workflows, content drafts, and daily brief generation.

Strategic angle: Repo: AI Infra Lab. Daily career execution for Andrew Cai. Positioning: Senior software engineer in Toronto with 7+ years building secure, scalable cloud platforms and APIs in high-uptime, regulated environments across Disney Streaming, Binance, and TikTok. Targeting AI infrastructure, LLM evaluation, agent observability, tool-integrated AI workflows, and platform systems with enterprise controls such as RBAC, audit logs, rate limiting, and production reliability. Career signal to show: one unified Staff-level AI Infrastructure portfolio. Update only AI Infra Lab: README.md, docs/ARCHITECTURE.md, docs/ROADMAP.md, docs/MODULE_STRUCTURE.md, docs/NEXT_30_DAYS.md, arp/, evals/, or tests/. Do not create or update standalone demo repos. Top roles reviewed: Senior Software Engineer, Data Platform at Gusto.

## 2026-06-09 - GitHub portfolio update

Updated the AI Career Director backend with infrastructure-oriented features: job scoring, career profile, approval workflows, content drafts, and daily brief generation.

Strategic angle: Repo: AI Infra Lab. Daily career execution for Andrew Cai. Positioning: Senior software engineer in Toronto with 7+ years building secure, scalable cloud platforms and APIs in high-uptime, regulated environments across Disney Streaming, Binance, and TikTok. Targeting AI infrastructure, LLM evaluation, agent observability, tool-integrated AI workflows, and platform systems with enterprise controls such as RBAC, audit logs, rate limiting, and production reliability. Career signal to show: one unified Staff-level AI Infrastructure portfolio. Update only AI Infra Lab: README.md, docs/ARCHITECTURE.md, docs/ROADMAP.md, docs/MODULE_STRUCTURE.md, docs/NEXT_30_DAYS.md, arp/, evals/, or tests/. Do not create or update standalone demo repos. Top roles reviewed: Senior Software Engineer, Data Platform at Gusto.

## 2026-06-10 - GitHub portfolio update

Updated the AI Career Director backend with infrastructure-oriented features: job scoring, career profile, approval workflows, content drafts, and daily brief generation.

Strategic angle: Repo: AI Infra Lab. Daily career execution for Andrew Cai. Positioning: Senior software engineer in Toronto with 7+ years building secure, scalable cloud platforms and APIs in high-uptime, regulated environments across Disney Streaming, Binance, and TikTok. Targeting AI infrastructure, LLM evaluation, agent observability, tool-integrated AI workflows, and platform systems with enterprise controls such as RBAC, audit logs, rate limiting, and production reliability. Career signal to show: one unified Staff-level AI Infrastructure portfolio. Update only AI Infra Lab: README.md, docs/ARCHITECTURE.md, docs/ROADMAP.md, docs/MODULE_STRUCTURE.md, docs/NEXT_30_DAYS.md, arp/, evals/, or tests/. Do not create or update standalone demo repos. Top roles reviewed: Senior Software Engineer, Data Platform at Gusto.

## 2026-06-11 - GitHub portfolio update

Updated the AI Career Director backend with infrastructure-oriented features: job scoring, career profile, approval workflows, content drafts, and daily brief generation.

Strategic angle: Repo: AI Infra Lab. Daily career execution for Andrew Cai. Positioning: Senior software engineer in Toronto with 7+ years building secure, scalable cloud platforms and APIs in high-uptime, regulated environments across Disney Streaming, Binance, and TikTok. Targeting AI infrastructure, LLM evaluation, agent observability, tool-integrated AI workflows, and platform systems with enterprise controls such as RBAC, audit logs, rate limiting, and production reliability. Career signal to show: one unified Staff-level AI Infrastructure portfolio. Update only AI Infra Lab: README.md, docs/ARCHITECTURE.md, docs/ROADMAP.md, docs/MODULE_STRUCTURE.md, docs/NEXT_30_DAYS.md, arp/, evals/, or tests/. Do not create or update standalone demo repos. Top roles reviewed: Senior Software Engineer, Data Platform at Gusto.

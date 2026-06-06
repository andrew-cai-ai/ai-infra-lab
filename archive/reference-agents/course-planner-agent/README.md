# AI Course Planning Assistant

An MVP agentic course planning API that recommends university course schedules from mock York University program data.

The first version is intentionally local and deterministic. It uses mock course and professor data, then applies prerequisite checks, schedule conflict detection, workload estimation, and ranking policies to return three plans: Easy, Balanced, and Hard.

The root route includes a simple browser UI for York students. The API remains available for testing and future integrations.

Current mock programs:

- Kinesiology and Health Science
- Psychology
- Commerce
- Biology
- Computer Science

## What It Does

- Accepts a student profile with university, program, completed courses, required courses, preferred days/times, and target mode.
- Uses synthetic York University program catalog data and professor ratings.
- Checks prerequisite eligibility using AND-of-OR prerequisite groups.
- Filters sections that do not fit preferred availability.
- Avoids overlapping class times while constructing each plan.
- Estimates weekly workload and workload risk.
- Ranks recommendations by graduation progress, professor rating, difficulty fit, and workload fit.
- Returns Easy, Balanced, and Hard plans with transparent score breakdowns.

## Project Layout

```text
apps/course-planner-agent/
  examples/
    sample_request.json
    sample_response.json
  src/course_planner_agent/
    api.py                 # FastAPI routes
    ui.py                  # Single-page browser UI served from /
    models.py              # Request models and adapter into engine dataclasses
    engine.py              # Constraints, ranking, workload, and plan generation
    data/york_catalog.py   # Mock York program catalogs and default course sets
    data/york_cs.py        # Mock York CS courses reused by the catalog registry
  tests/
    test_engine.py         # Prerequisite, time conflict, availability, and ranking tests
```

## Run Locally

```bash
cd apps/course-planner-agent
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
python3 -m uvicorn course_planner_agent.api:app --reload --port 8000
```

Then open:

- `GET http://127.0.0.1:8000/` for the York planner UI
- `GET http://127.0.0.1:8000/api` for API metadata
- `GET http://127.0.0.1:8000/health`
- `GET http://127.0.0.1:8000/mock-data/programs`
- `GET http://127.0.0.1:8000/mock-data/courses`
- `POST http://127.0.0.1:8000/plans`

Example request:

```bash
curl -X POST http://127.0.0.1:8000/plans \
  -H "Content-Type: application/json" \
  --data @examples/sample_request.json
```

## Test

```bash
cd apps/course-planner-agent
python3 -m unittest discover -s tests
```

From the repository root:

```bash
python3 -m unittest discover -s apps/course-planner-agent/tests
```

## Agent Workflow

The API response includes a lightweight `agentWorkflow` trace to show the intended tool-calling style:

1. `profile_parser`: normalize profile input and course codes.
2. `mock_course_catalog`: load candidate York courses and sections for the selected program.
3. `prerequisite_checker`: exclude completed courses and courses with missing prerequisite groups.
4. `schedule_solver`: remove unavailable sections and greedily avoid section time conflicts.
5. `ranking_engine`: score eligible course-section pairs for easy, balanced, and hard modes.

In a later agent implementation, each step can become a real tool call with inputs, outputs, confidence, and audit logs.

## Planning Logic

Prerequisites are represented as AND-of-OR groups. For example:

```python
(("PSYC 1010",), ("PSYC 2020", "PSYC 2030"))
```

This means the student needs `PSYC 1010`, and also needs either `PSYC 2020` or `PSYC 2030`.

Schedule conflicts use interval overlap on shared days. Back-to-back sections are allowed because one section ending at `10:30` and another starting at `10:30` do not overlap.

Ranking is deterministic. Each candidate receives points for:

- graduation progress: declared required courses score higher
- professor rating: higher mock rating scores higher
- difficulty fit: easy favors lower difficulty, balanced favors moderate difficulty, hard favors harder courses
- workload fit: easy prefers lower estimated workload, balanced prefers moderate workload, hard tolerates heavier work

Plan construction is a simple greedy solver for the MVP. It selects ranked candidates while respecting duplicate-course, workload-cap, and time-conflict constraints.

## API Shape

Main endpoint:

```http
POST /plans
```

Input fields:

- `university`
- `program`
- `completed_courses`
- `required_courses`
- `preferred_schedule.days`
- `preferred_schedule.earliest_start`
- `preferred_schedule.latest_end`
- `target_mode`: `easy`, `balanced`, or `hard`

Output fields:

- `recommendedPlan`
- `plans`: Easy, Balanced, and Hard plans
- `agentWorkflow`
- `excludedCourses`

See `examples/sample_request.json` and `examples/sample_response.json`.

## Future API Integrations

- University catalog and timetable APIs for live course offerings, sections, seats, and prerequisites.
- Degree audit or calendar requirement APIs for official graduation progress.
- Student calendar integrations to read unavailable time blocks.
- Professor rating sources, with freshness and provenance metadata.
- Historical enrollment and drop-rate data to improve workload risk.
- LLM tool orchestration so the agent can explain tradeoffs, ask clarifying questions, and repair invalid plans.

## Evaluation And Reliability Strategy

Near-term checks:

- Unit tests for prerequisite evaluation, time conflict detection, availability filtering, and mode-sensitive ranking.
- Golden input/output fixtures for stable API behavior.
- Constraint invariants: no selected completed courses, no missing prerequisites, no time conflicts, and workload under each mode cap.
- Regression cases for edge schedules, unavailable days, unknown professors, and no-valid-plan scenarios.

Agent reliability checks:

- Record every planning step in a structured trace.
- Compare ranked outputs against hand-labeled advisor scenarios.
- Add metamorphic tests, such as adding a completed prerequisite should not reduce eligibility.
- Add adversarial tests for malformed course codes, impossible schedules, and contradictory requirements.
- Track precision of exclusion reasons and recommendation rationales.

## Limitations

- All course and professor data is synthetic.
- The solver is greedy, not an exhaustive optimizer.
- The MVP does not validate official York University requirements.
- Workload estimates are heuristic and should not be treated as advising facts.

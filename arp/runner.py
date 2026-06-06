from __future__ import annotations

import json
from time import perf_counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .graders import grade_case
from .report import build_report
from .sample_agent import run_case as run_sample_agent
from .schema import load_suite_cases


def run_suite(suite_path: str | Path, agent_id: str, artifacts_dir: str | Path = "artifacts") -> dict[str, Any]:
    if agent_id != "sample":
        raise ValueError("v1 only supports the built-in 'sample' agent")
    suite, cases = load_suite_cases(suite_path)
    started_at = datetime.now(timezone.utc)
    run_started = perf_counter()
    run_id = f"{started_at.strftime('%Y%m%dT%H%M%SZ')}-{suite['id']}-{uuid4().hex[:8]}"
    run_dir = Path(artifacts_dir) / "runs" / run_id
    attempts_dir = run_dir / "attempts"
    attempts_dir.mkdir(parents=True, exist_ok=False)

    case_results = []
    for case in cases:
        attempt_started_at = datetime.now(timezone.utc)
        attempt_started = perf_counter()
        try:
            agent_result = run_sample_agent(case)
            checks = [result.to_dict() for result in grade_case(case, agent_result)]
            error = None
        except Exception as exc:  # noqa: BLE001 - run artifacts must capture agent/grader failures.
            agent_result = None
            checks = []
            error = {"type": type(exc).__name__, "message": str(exc)}
        attempt_completed_at = datetime.now(timezone.utc)
        attempt_duration_ms = _duration_ms(attempt_started)
        case_passed = error is None and all(check["passed"] for check in checks)
        case_status = "errored" if error else "passed" if case_passed else "failed"
        attempt = {
            "case_id": case["id"],
            "case_version": case["version"],
            "started_at": attempt_started_at.isoformat(),
            "completed_at": attempt_completed_at.isoformat(),
            "duration_ms": attempt_duration_ms,
            "agent_result": agent_result,
            "checks": checks,
            "status": case_status,
        }
        if error:
            attempt["error"] = error
        attempt_path = attempts_dir / f"{_safe_id(case['id'])}.json"
        _write_json(attempt_path, attempt)
        case_result = {
            "case_id": case["id"],
            "case_version": case["version"],
            "status": case_status,
            "duration_ms": attempt_duration_ms,
            "checks": checks,
            "attempt_artifact": str(attempt_path),
        }
        if error:
            case_result["error"] = error
        case_results.append(case_result)

    summary = _summary(case_results)
    completed_at = datetime.now(timezone.utc)
    run = {
        "schema_version": "arp.run.v1",
        "run_id": run_id,
        "created_at": started_at.isoformat(),
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "duration_ms": _duration_ms(run_started),
        "suite": {"id": suite["id"], "name": suite["name"], "path": str(Path(suite_path))},
        "agent": {"id": agent_id},
        "status": _run_status(summary),
        "summary": summary,
        "case_results": case_results,
    }
    _write_json(run_dir / "run.json", run)
    (run_dir / "report.txt").write_text(build_report(run), encoding="utf-8")
    return run


def load_run(path: str | Path) -> dict[str, Any]:
    run_path = Path(path)
    return json.loads(run_path.read_text(encoding="utf-8"))


def run_json_path(run: dict[str, Any], artifacts_dir: str | Path = "artifacts") -> Path:
    return Path(artifacts_dir) / "runs" / run["run_id"] / "run.json"


def _summary(case_results: list[dict[str, Any]]) -> dict[str, int]:
    checks_total = sum(len(case["checks"]) for case in case_results)
    checks_passed = sum(1 for case in case_results for check in case["checks"] if check["passed"])
    cases_passed = sum(1 for case in case_results if case["status"] == "passed")
    cases_errored = sum(1 for case in case_results if case["status"] == "errored")
    return {
        "cases_total": len(case_results),
        "cases_passed": cases_passed,
        "cases_failed": len(case_results) - cases_passed - cases_errored,
        "cases_errored": cases_errored,
        "checks_total": checks_total,
        "checks_passed": checks_passed,
        "checks_failed": checks_total - checks_passed,
    }


def _run_status(summary: dict[str, int]) -> str:
    if summary["cases_errored"]:
        return "errored"
    if summary["cases_passed"] == summary["cases_total"]:
        return "passed"
    return "failed"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _safe_id(value: str) -> str:
    return "".join(char if char.isalnum() or char in "._-" else "_" for char in value)


def _duration_ms(started: float) -> int:
    return max(0, round((perf_counter() - started) * 1000))

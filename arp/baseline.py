from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def promote_baseline(run: dict[str, Any], artifacts_dir: str | Path = "artifacts") -> dict[str, Any]:
    suite_id = run["suite"]["id"]
    agent_id = run["agent"]["id"]
    baseline = {
        "schema_version": "arp.baseline.v1",
        "suite_id": suite_id,
        "agent_id": agent_id,
        "run_id": run["run_id"],
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "status": run["status"],
        "summary": run["summary"],
        "case_results": _case_index(run),
    }
    path = baseline_path(suite_id, agent_id, artifacts_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return baseline


def compare_to_baseline(
    run: dict[str, Any],
    baseline: dict[str, Any] | None = None,
    artifacts_dir: str | Path = "artifacts",
) -> dict[str, Any]:
    if baseline is None:
        baseline = load_baseline(run["suite"]["id"], run["agent"]["id"], artifacts_dir)
    current_cases = _case_index(run)
    baseline_cases = baseline["case_results"]
    regressions = []
    improvements = []
    unchanged = []
    new_cases = []

    for case_id, current in current_cases.items():
        previous = baseline_cases.get(case_id)
        if previous is None:
            new_cases.append(case_id)
        elif previous["status"] == "passed" and current["status"] != "passed":
            regressions.append(_change(case_id, previous, current))
        elif previous["status"] != "passed" and current["status"] == "passed":
            improvements.append(_change(case_id, previous, current))
        else:
            unchanged.append(case_id)

    removed_cases = sorted(set(baseline_cases) - set(current_cases))
    comparison = {
        "schema_version": "arp.comparison.v1",
        "run_id": run["run_id"],
        "baseline_run_id": baseline["run_id"],
        "suite_id": run["suite"]["id"],
        "agent_id": run["agent"]["id"],
        "verdict": "regressed" if regressions else "passed",
        "regressions": regressions,
        "improvements": improvements,
        "unchanged": unchanged,
        "new_cases": new_cases,
        "removed_cases": removed_cases,
    }
    _write_comparison(run, comparison, artifacts_dir)
    return comparison


def baseline_path(suite_id: str, agent_id: str, artifacts_dir: str | Path = "artifacts") -> Path:
    return Path(artifacts_dir) / "baselines" / suite_id / f"{agent_id}.json"


def load_baseline(suite_id: str, agent_id: str, artifacts_dir: str | Path = "artifacts") -> dict[str, Any]:
    path = baseline_path(suite_id, agent_id, artifacts_dir)
    return json.loads(path.read_text(encoding="utf-8"))


def _case_index(run: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        case["case_id"]: {
            "status": case["status"],
            "failed_checks": [check["id"] for check in case["checks"] if not check["passed"]],
            "checks_total": len(case["checks"]),
            "checks_passed": sum(1 for check in case["checks"] if check["passed"]),
        }
        for case in run["case_results"]
    }


def _change(case_id: str, previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "baseline_status": previous["status"],
        "current_status": current["status"],
        "baseline_failed_checks": previous["failed_checks"],
        "current_failed_checks": current["failed_checks"],
    }


def _write_comparison(run: dict[str, Any], comparison: dict[str, Any], artifacts_dir: str | Path) -> None:
    path = Path(artifacts_dir) / "runs" / run["run_id"] / "comparison.json"
    if path.parent.exists():
        path.write_text(json.dumps(comparison, indent=2, sort_keys=True) + "\n", encoding="utf-8")

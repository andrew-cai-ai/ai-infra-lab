from __future__ import annotations

from typing import Any


def build_report(run: dict[str, Any], comparison: dict[str, Any] | None = None) -> str:
    summary = run["summary"]
    lines = [
        "Agent Reliability Run Report",
        "============================",
        f"Run ID: {run['run_id']}",
        f"Suite: {run['suite']['id']} ({run['suite']['name']})",
        f"Agent: {run['agent']['id']}",
        f"Status: {run['status']}",
        f"Cases: {summary['cases_passed']}/{summary['cases_total']} passed",
        f"Checks: {summary['checks_passed']}/{summary['checks_total']} passed",
        f"Duration: {run.get('duration_ms', 0)} ms",
    ]
    if summary.get("cases_errored", 0):
        lines.append(f"Errors: {summary['cases_errored']} case(s)")
    if comparison:
        lines.extend([
            "",
            "Regression Comparison",
            "---------------------",
            f"Verdict: {comparison['verdict']}",
            f"Baseline Run: {comparison['baseline_run_id']}",
            f"Regressions: {len(comparison['regressions'])}",
            f"Improvements: {len(comparison['improvements'])}",
        ])
    errors = _errors(run)
    if errors:
        lines.extend(["", "Errors", "------"])
        for error in errors:
            lines.extend([
                f"- Case: {error['case_id']}",
                f"  Type: {error['type']}",
                f"  Message: {error['message']}",
                f"  Attempt: {error['attempt_artifact']}",
            ])
    failures = _failures(run)
    if not failures:
        lines.extend(["", "Failures", "--------", "None"])
    else:
        lines.extend(["", "Failures", "--------"])
        for failure in failures:
            lines.extend([
                f"- Case: {failure['case_id']}",
                f"  Check: {failure['check_id']} ({failure['check_type']})",
                f"  Expected: {failure['expected']!r}",
                f"  Actual: {failure['actual']!r}",
                f"  Evidence: {failure['evidence']}",
            ])
    return "\n".join(lines) + "\n"


def _failures(run: dict[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for case_result in run["case_results"]:
        for check in case_result["checks"]:
            if not check["passed"]:
                failures.append({
                    "case_id": case_result["case_id"],
                    "check_id": check["id"],
                    "check_type": check["type"],
                    "expected": check["expected"],
                    "actual": check["actual"],
                    "evidence": check["evidence"],
                })
    return failures


def _errors(run: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for case_result in run["case_results"]:
        error = case_result.get("error")
        if error:
            errors.append({
                "case_id": case_result["case_id"],
                "type": error.get("type", "Error"),
                "message": error.get("message", ""),
                "attempt_artifact": case_result.get("attempt_artifact", ""),
            })
    return errors

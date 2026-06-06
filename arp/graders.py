from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    id: str
    type: str
    passed: bool
    expected: Any
    actual: Any
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def grade_case(case: dict[str, Any], agent_result: dict[str, Any]) -> list[CheckResult]:
    return [_grade_check(check, agent_result) for check in case["checks"]]


def _grade_check(check: dict[str, Any], agent_result: dict[str, Any]) -> CheckResult:
    check_type = check["type"]
    output = str(agent_result.get("output", ""))
    if check_type == "output_exact":
        expected = check["expected"]
        return CheckResult(
            id=check["id"],
            type=check_type,
            passed=output == expected,
            expected=expected,
            actual=output,
            evidence=f"assistant output was {output!r}",
        )
    if check_type == "output_contains":
        expected = check["text"]
        return CheckResult(
            id=check["id"],
            type=check_type,
            passed=expected in output,
            expected=f"output contains {expected!r}",
            actual=output,
            evidence=f"assistant output was {output!r}",
        )
    if check_type == "output_regex":
        pattern = check["pattern"]
        matched = re.search(pattern, output) is not None
        return CheckResult(
            id=check["id"],
            type=check_type,
            passed=matched,
            expected=f"output matches /{pattern}/",
            actual=output,
            evidence=f"assistant output was {output!r}",
        )
    if check_type == "tool_sequence":
        expected = check["expected"]
        actual = [str(call.get("name", "")) for call in agent_result.get("tool_calls", [])]
        return CheckResult(
            id=check["id"],
            type=check_type,
            passed=actual == expected,
            expected=expected,
            actual=actual,
            evidence=f"tool call sequence was {actual!r}",
        )
    if check_type == "no_external_actions":
        actual = agent_result.get("external_actions", [])
        return CheckResult(
            id=check["id"],
            type=check_type,
            passed=actual == [],
            expected=[],
            actual=actual,
            evidence=f"external actions were {actual!r}",
        )
    raise ValueError(f"unsupported check type: {check_type}")

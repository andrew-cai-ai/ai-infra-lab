from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


CASE_SCHEMA_VERSION = "arp.eval.case.v1"
SUITE_SCHEMA_VERSION = "arp.eval.suite.v1"
TRACE_SCHEMA_VERSION = "arp.trace.v1"

CHECK_TYPES = {
    "output_exact": {"expected"},
    "output_contains": {"text"},
    "output_regex": {"pattern"},
    "tool_sequence": {"expected"},
    "no_external_actions": set(),
}

TRACE_STATUSES = {"passed", "failed", "errored"}
TRACE_SPAN_TYPES = {"agent", "model_call", "tool_call", "external_action"}


class SchemaError(ValueError):
    """Raised when an eval case or suite does not satisfy the v1 contract."""


def load_json(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SchemaError(f"{file_path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise SchemaError(f"{file_path}: top-level value must be an object")
    return payload


def validate_case(case: dict[str, Any]) -> None:
    required = ["schema_version", "id", "version", "name", "task", "checks"]
    _require_keys(case, required, "case")
    if case["schema_version"] != CASE_SCHEMA_VERSION:
        raise SchemaError(f"case.schema_version must be {CASE_SCHEMA_VERSION!r}")
    for key in ["id", "version", "name"]:
        _require_string(case, key, "case")
    task = case["task"]
    if not isinstance(task, dict):
        raise SchemaError("case.task must be an object")
    _require_string(task, "prompt", "case.task")
    _require_string(task, "sample_agent_output", "case.task")
    checks = case["checks"]
    if not isinstance(checks, list) or not checks:
        raise SchemaError("case.checks must be a non-empty list")
    seen_ids: set[str] = set()
    for index, check in enumerate(checks):
        _validate_check(check, index, seen_ids)


def validate_suite(suite: dict[str, Any]) -> None:
    required = ["schema_version", "id", "name", "cases"]
    _require_keys(suite, required, "suite")
    if suite["schema_version"] != SUITE_SCHEMA_VERSION:
        raise SchemaError(f"suite.schema_version must be {SUITE_SCHEMA_VERSION!r}")
    for key in ["id", "name"]:
        _require_string(suite, key, "suite")
    cases = suite["cases"]
    if not isinstance(cases, list) or not cases:
        raise SchemaError("suite.cases must be a non-empty list")
    for index, case_path in enumerate(cases):
        if not isinstance(case_path, str) or not case_path.strip():
            raise SchemaError(f"suite.cases[{index}] must be a non-empty string")


def validate_trace(trace: dict[str, Any]) -> None:
    required = ["schema_version", "trace_id", "agent", "started_at", "completed_at", "duration_ms", "status", "spans"]
    _require_keys(trace, required, "trace")
    if trace["schema_version"] != TRACE_SCHEMA_VERSION:
        raise SchemaError(f"trace.schema_version must be {TRACE_SCHEMA_VERSION!r}")
    _require_string(trace, "trace_id", "trace")
    _require_string(trace, "started_at", "trace")
    _require_string(trace, "completed_at", "trace")
    _require_duration(trace, "duration_ms", "trace")
    _require_status(trace, "status", "trace")
    _validate_agent(trace["agent"])
    spans = trace["spans"]
    if not isinstance(spans, list) or not spans:
        raise SchemaError("trace.spans must be a non-empty list")
    span_ids: set[str] = set()
    for index, span in enumerate(spans):
        _validate_trace_span(span, index, span_ids)
    for index, span in enumerate(spans):
        parent_span_id = span.get("parent_span_id")
        if parent_span_id is not None:
            if not isinstance(parent_span_id, str) or not parent_span_id.strip():
                raise SchemaError(f"trace.spans[{index}].parent_span_id must be null or a non-empty string")
            if parent_span_id == span["span_id"]:
                raise SchemaError(f"trace.spans[{index}].parent_span_id cannot reference itself")
            if parent_span_id not in span_ids:
                raise SchemaError(f"trace.spans[{index}].parent_span_id references unknown span {parent_span_id!r}")
    _validate_optional_object(trace, "metadata", "trace")


def load_case(path: str | Path) -> dict[str, Any]:
    case = load_json(path)
    validate_case(case)
    return case


def load_suite(path: str | Path) -> dict[str, Any]:
    suite = load_json(path)
    validate_suite(suite)
    return suite


def load_trace(path: str | Path) -> dict[str, Any]:
    trace = load_json(path)
    validate_trace(trace)
    return trace


def load_suite_cases(suite_path: str | Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    suite_file = Path(suite_path)
    suite = load_suite(suite_file)
    cases = []
    for case_ref in suite["cases"]:
        case_path = (suite_file.parent / case_ref).resolve()
        cases.append(load_case(case_path))
    return suite, cases


def _validate_check(check: Any, index: int, seen_ids: set[str]) -> None:
    if not isinstance(check, dict):
        raise SchemaError(f"case.checks[{index}] must be an object")
    _require_keys(check, ["id", "type"], f"case.checks[{index}]")
    _require_string(check, "id", f"case.checks[{index}]")
    _require_string(check, "type", f"case.checks[{index}]")
    check_id = check["id"]
    if check_id in seen_ids:
        raise SchemaError(f"duplicate check id {check_id!r}")
    seen_ids.add(check_id)
    check_type = check["type"]
    if check_type not in CHECK_TYPES:
        allowed = ", ".join(sorted(CHECK_TYPES))
        raise SchemaError(f"case.checks[{index}].type must be one of: {allowed}")
    for key in CHECK_TYPES[check_type]:
        if key not in check:
            raise SchemaError(f"case.checks[{index}] missing required key {key!r}")
    if check_type in {"output_exact", "output_contains", "output_regex"}:
        payload_key = "expected" if check_type == "output_exact" else "text" if check_type == "output_contains" else "pattern"
        _require_string(check, payload_key, f"case.checks[{index}]")
        if check_type == "output_regex":
            try:
                re.compile(check[payload_key])
            except re.error as exc:
                raise SchemaError(f"case.checks[{index}].pattern must be a valid regex: {exc}") from exc
    if check_type == "tool_sequence":
        expected = check["expected"]
        if not isinstance(expected, list) or not all(isinstance(item, str) and item for item in expected):
            raise SchemaError(f"case.checks[{index}].expected must be a non-empty string list")


def _validate_agent(agent: Any) -> None:
    if not isinstance(agent, dict):
        raise SchemaError("trace.agent must be an object")
    _require_string(agent, "id", "trace.agent")
    if "version" in agent:
        _require_string(agent, "version", "trace.agent")
    if "environment" in agent:
        _require_string(agent, "environment", "trace.agent")


def _validate_trace_span(span: Any, index: int, span_ids: set[str]) -> None:
    label = f"trace.spans[{index}]"
    if not isinstance(span, dict):
        raise SchemaError(f"{label} must be an object")
    required = ["span_id", "name", "type", "started_at", "completed_at", "duration_ms", "status"]
    _require_keys(span, required, label)
    for key in ["span_id", "name", "type", "started_at", "completed_at"]:
        _require_string(span, key, label)
    span_id = span["span_id"]
    if span_id in span_ids:
        raise SchemaError(f"duplicate span id {span_id!r}")
    span_ids.add(span_id)
    span_type = span["type"]
    if span_type not in TRACE_SPAN_TYPES:
        allowed = ", ".join(sorted(TRACE_SPAN_TYPES))
        raise SchemaError(f"{label}.type must be one of: {allowed}")
    _require_duration(span, "duration_ms", label)
    _require_status(span, "status", label)
    if span_type == "model_call":
        _require_string(span, "model", label)
    if span_type == "tool_call":
        _require_string(span, "tool_name", label)
    if span_type == "external_action":
        _require_string(span, "action_name", label)
    if span["status"] == "errored":
        _validate_error(span.get("error"), label)
    if "error" in span and span["status"] != "errored":
        _validate_error(span["error"], label)
    _validate_optional_object(span, "attributes", label)
    _validate_optional_object(span, "input", label)
    _validate_optional_object(span, "output", label)
    _validate_optional_tokens(span, label)
    _validate_optional_cost(span, label)


def _validate_error(error: Any, label: str) -> None:
    if not isinstance(error, dict):
        raise SchemaError(f"{label}.error must be an object")
    _require_string(error, "type", f"{label}.error")
    _require_string(error, "message", f"{label}.error")


def _validate_optional_tokens(span: dict[str, Any], label: str) -> None:
    if "tokens" not in span:
        return
    tokens = span["tokens"]
    if not isinstance(tokens, dict):
        raise SchemaError(f"{label}.tokens must be an object")
    for key in ["input", "output", "total"]:
        value = tokens.get(key, 0)
        if not isinstance(value, int) or value < 0:
            raise SchemaError(f"{label}.tokens.{key} must be a non-negative integer")


def _validate_optional_cost(span: dict[str, Any], label: str) -> None:
    if "cost" not in span:
        return
    cost = span["cost"]
    if not isinstance(cost, dict):
        raise SchemaError(f"{label}.cost must be an object")
    amount = cost.get("amount_usd", 0)
    if not isinstance(amount, int | float) or amount < 0:
        raise SchemaError(f"{label}.cost.amount_usd must be a non-negative number")


def _validate_optional_object(payload: dict[str, Any], key: str, label: str) -> None:
    if key in payload and not isinstance(payload[key], dict):
        raise SchemaError(f"{label}.{key} must be an object")


def _require_keys(payload: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise SchemaError(f"{label} missing required keys: {', '.join(missing)}")


def _require_string(payload: dict[str, Any], key: str, label: str) -> None:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SchemaError(f"{label}.{key} must be a non-empty string")


def _require_duration(payload: dict[str, Any], key: str, label: str) -> None:
    value = payload.get(key)
    if not isinstance(value, int) or value < 0:
        raise SchemaError(f"{label}.{key} must be a non-negative integer")


def _require_status(payload: dict[str, Any], key: str, label: str) -> None:
    value = payload.get(key)
    if value not in TRACE_STATUSES:
        allowed = ", ".join(sorted(TRACE_STATUSES))
        raise SchemaError(f"{label}.{key} must be one of: {allowed}")

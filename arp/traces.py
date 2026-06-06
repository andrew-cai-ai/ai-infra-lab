from __future__ import annotations

from typing import Any


def trace_summary(trace: dict[str, Any]) -> dict[str, Any]:
    spans = trace["spans"]
    model_calls = [span for span in spans if span["type"] == "model_call"]
    tool_calls = [span for span in spans if span["type"] == "tool_call"]
    external_actions = [span for span in spans if span["type"] == "external_action"]
    errors = [span for span in spans if span["status"] == "errored" or "error" in span]
    token_totals = _token_totals(spans)
    cost_usd = sum(float(span.get("cost", {}).get("amount_usd", 0)) for span in spans)
    return {
        "trace_id": trace["trace_id"],
        "agent_id": trace["agent"]["id"],
        "agent_version": trace["agent"].get("version", ""),
        "status": trace["status"],
        "duration_ms": trace["duration_ms"],
        "span_count": len(spans),
        "model_call_count": len(model_calls),
        "tool_call_count": len(tool_calls),
        "external_action_count": len(external_actions),
        "error_count": len(errors),
        "tokens": token_totals,
        "cost_usd": cost_usd,
    }


def format_trace_inspection(trace: dict[str, Any]) -> str:
    summary = trace_summary(trace)
    agent = summary["agent_id"]
    if summary["agent_version"]:
        agent = f"{agent}@{summary['agent_version']}"
    tokens = summary["tokens"]
    lines = [
        "Trace Inspection",
        "================",
        f"Trace ID: {summary['trace_id']}",
        f"Agent: {agent}",
        f"Status: {summary['status']}",
        f"Duration: {summary['duration_ms']} ms",
        f"Spans: {summary['span_count']}",
        f"Model Calls: {summary['model_call_count']}",
        f"Tool Calls: {summary['tool_call_count']}",
        f"External Actions: {summary['external_action_count']}",
        f"Errors: {summary['error_count']}",
        f"Tokens: input={tokens['input']} output={tokens['output']} total={tokens['total']}",
        f"Cost: ${summary['cost_usd']:.6f}",
    ]
    return "\n".join(lines) + "\n"


def _token_totals(spans: list[dict[str, Any]]) -> dict[str, int]:
    totals = {"input": 0, "output": 0, "total": 0}
    for span in spans:
        tokens = span.get("tokens", {})
        totals["input"] += int(tokens.get("input", 0))
        totals["output"] += int(tokens.get("output", 0))
        totals["total"] += int(tokens.get("total", 0))
    return totals

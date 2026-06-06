from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .baseline import compare_to_baseline, promote_baseline
from .report import build_report
from .runner import load_run, run_json_path, run_suite
from .schema import SchemaError, load_case, load_suite_cases, load_trace
from .traces import format_trace_inspection


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (SchemaError, FileNotFoundError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arp", description="Agent Reliability Platform CLI")
    subcommands = parser.add_subparsers(dest="command", required=True)

    case_parser = subcommands.add_parser("case", help="work with eval cases")
    case_subcommands = case_parser.add_subparsers(dest="case_command", required=True)
    validate_parser = case_subcommands.add_parser("validate", help="validate an eval case")
    validate_parser.add_argument("path")
    validate_parser.set_defaults(func=_case_validate)

    run_parser = subcommands.add_parser("run", help="run a suite")
    run_parser.add_argument("--suite", required=True)
    run_parser.add_argument("--agent", default="sample")
    run_parser.add_argument("--artifacts-dir", default="artifacts")
    run_parser.set_defaults(func=_run)

    baseline_parser = subcommands.add_parser("baseline", help="work with baselines")
    baseline_subcommands = baseline_parser.add_subparsers(dest="baseline_command", required=True)
    promote_parser = baseline_subcommands.add_parser("promote", help="promote a run to baseline")
    promote_parser.add_argument("run_json")
    promote_parser.add_argument("--artifacts-dir", default="artifacts")
    promote_parser.set_defaults(func=_baseline_promote)

    compare_parser = subcommands.add_parser("compare", help="compare a run to its baseline")
    compare_parser.add_argument("run_json")
    compare_parser.add_argument("--artifacts-dir", default="artifacts")
    compare_parser.set_defaults(func=_compare)

    report_parser = subcommands.add_parser("report", help="print a human-readable run report")
    report_parser.add_argument("run_json")
    report_parser.set_defaults(func=_report)

    suite_parser = subcommands.add_parser("suite", help="work with eval suites")
    suite_subcommands = suite_parser.add_subparsers(dest="suite_command", required=True)
    suite_validate_parser = suite_subcommands.add_parser("validate", help="validate an eval suite")
    suite_validate_parser.add_argument("path")
    suite_validate_parser.set_defaults(func=_suite_validate)

    trace_parser = subcommands.add_parser("trace", help="work with trace artifacts")
    trace_subcommands = trace_parser.add_subparsers(dest="trace_command", required=True)
    trace_validate_parser = trace_subcommands.add_parser("validate", help="validate a trace artifact")
    trace_validate_parser.add_argument("path")
    trace_validate_parser.set_defaults(func=_trace_validate)
    trace_inspect_parser = trace_subcommands.add_parser("inspect", help="print a trace summary")
    trace_inspect_parser.add_argument("path")
    trace_inspect_parser.set_defaults(func=_trace_inspect)
    return parser


def _case_validate(args: argparse.Namespace) -> int:
    case = load_case(args.path)
    print(f"valid case: {case['id']}@{case['version']}")
    return 0


def _suite_validate(args: argparse.Namespace) -> int:
    suite, cases = load_suite_cases(args.path)
    print(f"valid suite: {suite['id']} ({len(cases)} cases)")
    return 0


def _trace_validate(args: argparse.Namespace) -> int:
    trace = load_trace(args.path)
    print(f"valid trace: {trace['trace_id']} ({len(trace['spans'])} spans)")
    return 0


def _trace_inspect(args: argparse.Namespace) -> int:
    trace = load_trace(args.path)
    print(format_trace_inspection(trace), end="")
    return 0 if trace["status"] == "passed" else 2


def _run(args: argparse.Namespace) -> int:
    run = run_suite(args.suite, args.agent, args.artifacts_dir)
    print(f"run: {run['run_id']}")
    print(f"status: {run['status']}")
    print(f"artifact: {run_json_path(run, args.artifacts_dir)}")
    return 0 if run["status"] == "passed" else 2


def _baseline_promote(args: argparse.Namespace) -> int:
    run = load_run(args.run_json)
    baseline = promote_baseline(run, args.artifacts_dir)
    print(f"promoted baseline: {baseline['suite_id']}/{baseline['agent_id']} -> {baseline['run_id']}")
    return 0


def _compare(args: argparse.Namespace) -> int:
    run = load_run(args.run_json)
    comparison = compare_to_baseline(run, artifacts_dir=args.artifacts_dir)
    print(json.dumps(comparison, indent=2, sort_keys=True))
    return 0 if comparison["verdict"] == "passed" else 2


def _report(args: argparse.Namespace) -> int:
    run = load_run(args.run_json)
    comparison_path = Path(args.run_json).with_name("comparison.json")
    comparison = None
    if comparison_path.exists():
        comparison = json.loads(comparison_path.read_text(encoding="utf-8"))
    print(build_report(run, comparison), end="")
    return 0 if run["status"] == "passed" else 2

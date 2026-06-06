import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from arp.schema import SchemaError, load_trace, validate_trace
from arp.traces import trace_summary


class TraceTests(unittest.TestCase):
    def test_sample_trace_is_valid_and_summarized(self) -> None:
        trace = load_trace("examples/traces/sample_success.json")
        summary = trace_summary(trace)

        self.assertEqual(trace["trace_id"], "trace.sample_success")
        self.assertEqual(summary["span_count"], 4)
        self.assertEqual(summary["model_call_count"], 1)
        self.assertEqual(summary["tool_call_count"], 2)
        self.assertEqual(summary["external_action_count"], 0)
        self.assertEqual(summary["tokens"]["total"], 15)
        self.assertEqual(summary["error_count"], 0)

    def test_trace_rejects_unknown_parent_span(self) -> None:
        trace = load_trace("examples/traces/sample_success.json")
        trace = json.loads(json.dumps(trace))
        trace["spans"][1]["parent_span_id"] = "span.missing"

        with self.assertRaisesRegex(SchemaError, "references unknown span"):
            validate_trace(trace)

    def test_trace_rejects_duplicate_span_ids(self) -> None:
        trace = load_trace("examples/traces/sample_success.json")
        trace = json.loads(json.dumps(trace))
        trace["spans"][1]["span_id"] = "span.root"

        with self.assertRaisesRegex(SchemaError, "duplicate span id"):
            validate_trace(trace)

    def test_trace_cli_validate_and_inspect(self) -> None:
        validate = subprocess.run(
            [sys.executable, "-m", "arp", "trace", "validate", "examples/traces/sample_success.json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(validate.returncode, 0, validate.stderr)
        self.assertIn("valid trace: trace.sample_success (4 spans)", validate.stdout)

        inspect = subprocess.run(
            [sys.executable, "-m", "arp", "trace", "inspect", "examples/traces/sample_success.json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(inspect.returncode, 0, inspect.stderr)
        self.assertIn("Trace Inspection", inspect.stdout)
        self.assertIn("Model Calls: 1", inspect.stdout)
        self.assertIn("Tool Calls: 2", inspect.stdout)
        self.assertIn("Tokens: input=14 output=1 total=15", inspect.stdout)

    def test_trace_cli_rejects_invalid_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.json"
            path.write_text(
                """{
  "schema_version": "arp.trace.v1",
  "trace_id": "bad.trace",
  "agent": {"id": "sample"},
  "started_at": "2026-06-06T10:00:00Z",
  "completed_at": "2026-06-06T10:00:01Z",
  "duration_ms": 1,
  "status": "passed",
  "spans": []
}
""",
                encoding="utf-8",
            )

            validate = subprocess.run(
                [sys.executable, "-m", "arp", "trace", "validate", str(path)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(validate.returncode, 1)
            self.assertIn("trace.spans must be a non-empty list", validate.stderr)


if __name__ == "__main__":
    unittest.main()

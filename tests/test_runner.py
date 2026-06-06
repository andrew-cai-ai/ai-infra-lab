import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from arp.runner import run_suite


class RunnerTests(unittest.TestCase):
    def test_run_suite_writes_artifacts_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = run_suite("evals/suites/sample.json", "sample", tmp)

            run_dir = Path(tmp) / "runs" / run["run_id"]
            run_json = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            report = (run_dir / "report.txt").read_text(encoding="utf-8")

            self.assertEqual(run["status"], "passed")
            self.assertGreaterEqual(run["duration_ms"], 0)
            self.assertEqual(run_json["summary"]["cases_failed"], 0)
            self.assertEqual(run_json["summary"]["checks_failed"], 0)
            self.assertEqual(run_json["summary"]["checks_passed"], 4)
            self.assertGreaterEqual(run_json["case_results"][0]["duration_ms"], 0)
            self.assertIn("Agent Reliability Run Report", report)
            self.assertIn("Duration: ", report)
            self.assertIn("Failures\n--------\nNone", report)
            attempt_path = run_dir / "attempts" / "sample.task_success.json"
            self.assertTrue(attempt_path.exists())
            attempt = json.loads(attempt_path.read_text(encoding="utf-8"))
            self.assertIn("started_at", attempt)
            self.assertIn("completed_at", attempt)
            self.assertGreaterEqual(attempt["duration_ms"], 0)

    def test_failed_run_report_includes_explainable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case_path = root / "case.json"
            suite_path = root / "suite.json"
            case_path.write_text(json.dumps({
                "schema_version": "arp.eval.case.v1",
                "id": "sample.failure",
                "version": "1.0.0",
                "name": "Sample Failure",
                "task": {
                    "prompt": "Return exactly ready.",
                    "sample_agent_output": "not-ready",
                },
                "checks": [
                    {"id": "output_is_ready", "type": "output_exact", "expected": "ready"},
                ],
            }), encoding="utf-8")
            suite_path.write_text(json.dumps({
                "schema_version": "arp.eval.suite.v1",
                "id": "failure-suite",
                "name": "Failure Suite",
                "cases": ["case.json"],
            }), encoding="utf-8")

            run = run_suite(suite_path, "sample", root / "artifacts")
            report = (root / "artifacts" / "runs" / run["run_id"] / "report.txt").read_text(encoding="utf-8")

            self.assertEqual(run["status"], "failed")
            self.assertIn("Expected: 'ready'", report)
            self.assertIn("Actual: 'not-ready'", report)
            self.assertIn("Evidence: assistant output was 'not-ready'", report)

    def test_errored_run_writes_artifacts_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case_path = root / "case.json"
            suite_path = root / "suite.json"
            case_path.write_text(json.dumps({
                "schema_version": "arp.eval.case.v1",
                "id": "sample.agent_error",
                "version": "1.0.0",
                "name": "Sample Agent Error",
                "task": {
                    "prompt": "Trigger an agent error.",
                    "sample_agent_output": "ready",
                },
                "checks": [
                    {"id": "output_is_ready", "type": "output_exact", "expected": "ready"},
                ],
            }), encoding="utf-8")
            suite_path.write_text(json.dumps({
                "schema_version": "arp.eval.suite.v1",
                "id": "error-suite",
                "name": "Error Suite",
                "cases": ["case.json"],
            }), encoding="utf-8")

            with patch("arp.runner.run_sample_agent", side_effect=RuntimeError("agent exploded")):
                run = run_suite(suite_path, "sample", root / "artifacts")

            run_dir = root / "artifacts" / "runs" / run["run_id"]
            attempt_path = run_dir / "attempts" / "sample.agent_error.json"
            attempt = json.loads(attempt_path.read_text(encoding="utf-8"))
            report = (run_dir / "report.txt").read_text(encoding="utf-8")

            self.assertEqual(run["status"], "errored")
            self.assertEqual(run["summary"]["cases_errored"], 1)
            self.assertEqual(run["summary"]["cases_failed"], 0)
            self.assertEqual(attempt["status"], "errored")
            self.assertEqual(attempt["agent_result"], None)
            self.assertEqual(attempt["error"]["type"], "RuntimeError")
            self.assertEqual(attempt["error"]["message"], "agent exploded")
            self.assertIn("Errors: 1 case(s)", report)
            self.assertIn("Type: RuntimeError", report)
            self.assertIn("Message: agent exploded", report)


if __name__ == "__main__":
    unittest.main()

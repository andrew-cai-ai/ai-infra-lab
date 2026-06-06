import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_cli_vertical_slice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            validate = subprocess.run(
                [sys.executable, "-m", "arp", "case", "validate", "evals/cases/sample_task_success.json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(validate.returncode, 0, validate.stderr)
            self.assertIn("valid case: sample.task_success@1.0.0", validate.stdout)

            run = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "arp",
                    "run",
                    "--suite",
                    "evals/suites/sample.json",
                    "--agent",
                    "sample",
                    "--artifacts-dir",
                    tmp,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            artifact_line = next(line for line in run.stdout.splitlines() if line.startswith("artifact: "))
            run_json = artifact_line.removeprefix("artifact: ")
            self.assertTrue(Path(run_json).exists())

            promote = subprocess.run(
                [sys.executable, "-m", "arp", "baseline", "promote", run_json, "--artifacts-dir", tmp],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(promote.returncode, 0, promote.stderr)

            compare = subprocess.run(
                [sys.executable, "-m", "arp", "compare", run_json, "--artifacts-dir", tmp],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compare.returncode, 0, compare.stderr)
            self.assertIn('"verdict": "passed"', compare.stdout)

            report = subprocess.run(
                [sys.executable, "-m", "arp", "report", run_json],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(report.returncode, 0, report.stderr)
            self.assertIn("Agent Reliability Run Report", report.stdout)

    def test_suite_validate_rejects_invalid_referenced_case(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case_path = root / "case.json"
            suite_path = root / "suite.json"
            case_path.write_text(
                """{
  "schema_version": "arp.eval.case.v1",
  "id": "bad",
  "version": "1.0.0",
  "name": "Bad",
  "task": {"prompt": "do it", "sample_agent_output": "done"},
  "checks": []
}
""",
                encoding="utf-8",
            )
            suite_path.write_text(
                """{
  "schema_version": "arp.eval.suite.v1",
  "id": "bad-suite",
  "name": "Bad Suite",
  "cases": ["case.json"]
}
""",
                encoding="utf-8",
            )

            validate = subprocess.run(
                [sys.executable, "-m", "arp", "suite", "validate", str(suite_path)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(validate.returncode, 1)
            self.assertIn("case.checks must be a non-empty list", validate.stderr)


if __name__ == "__main__":
    unittest.main()

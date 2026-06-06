import json
import tempfile
import unittest
from pathlib import Path

from arp.baseline import baseline_path, compare_to_baseline, promote_baseline
from arp.runner import run_suite


class BaselineTests(unittest.TestCase):
    def test_promote_and_compare_passing_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = run_suite("evals/suites/sample.json", "sample", tmp)
            baseline = promote_baseline(run, tmp)
            comparison = compare_to_baseline(run, baseline, tmp)

            self.assertEqual(baseline["run_id"], run["run_id"])
            self.assertEqual(comparison["verdict"], "passed")
            self.assertEqual(comparison["regressions"], [])
            self.assertTrue(baseline_path("sample", "sample", tmp).exists())

    def test_compare_detects_regression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = run_suite("evals/suites/sample.json", "sample", tmp)
            baseline = promote_baseline(run, tmp)
            regressed = json.loads(json.dumps(run))
            regressed["run_id"] = "regressed-run"
            regressed["status"] = "failed"
            regressed["case_results"][0]["status"] = "failed"
            regressed["case_results"][0]["checks"][0]["passed"] = False
            run_dir = Path(tmp) / "runs" / "regressed-run"
            run_dir.mkdir(parents=True)

            comparison = compare_to_baseline(regressed, baseline, tmp)

            self.assertEqual(comparison["verdict"], "regressed")
            self.assertEqual(comparison["regressions"][0]["case_id"], "sample.task_success")
            self.assertTrue((run_dir / "comparison.json").exists())


if __name__ == "__main__":
    unittest.main()

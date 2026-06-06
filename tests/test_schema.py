import unittest

from arp.schema import SchemaError, load_case, load_suite, validate_case


class SchemaTests(unittest.TestCase):
    def test_sample_case_is_valid(self) -> None:
        case = load_case("evals/cases/sample_task_success.json")

        self.assertEqual(case["id"], "sample.task_success")

    def test_sample_suite_is_valid(self) -> None:
        suite = load_suite("evals/suites/sample.json")

        self.assertEqual(suite["id"], "sample")

    def test_case_requires_deterministic_checks(self) -> None:
        with self.assertRaisesRegex(SchemaError, "case.checks must be a non-empty list"):
            validate_case({
                "schema_version": "arp.eval.case.v1",
                "id": "bad",
                "version": "1.0.0",
                "name": "Bad",
                "task": {"prompt": "do it", "sample_agent_output": "done"},
                "checks": [],
            })

    def test_case_rejects_invalid_regex_check(self) -> None:
        with self.assertRaisesRegex(SchemaError, "must be a valid regex"):
            validate_case({
                "schema_version": "arp.eval.case.v1",
                "id": "bad.regex",
                "version": "1.0.0",
                "name": "Bad Regex",
                "task": {"prompt": "match it", "sample_agent_output": "done"},
                "checks": [
                    {"id": "bad_pattern", "type": "output_regex", "pattern": "["},
                ],
            })


if __name__ == "__main__":
    unittest.main()

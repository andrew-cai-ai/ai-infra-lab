import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from course_planner_agent.data.york_catalog import get_program_catalog  # noqa: E402


class CatalogTests(unittest.TestCase):
    def test_kinesiology_aliases_resolve_to_program_catalog(self) -> None:
        for program_name in ("Kinesiology", "kinesiology", "kinensilogy", "kine"):
            catalog = get_program_catalog(program_name)

            self.assertEqual(catalog.name, "Kinesiology and Health Science")
            self.assertTrue(any(course.code == "KINE 1000" for course in catalog.courses))


if __name__ == "__main__":
    unittest.main()

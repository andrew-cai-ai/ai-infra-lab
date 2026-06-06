import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from course_planner_agent.engine import (  # noqa: E402
    Course,
    PreferredSchedule,
    ProfessorRating,
    Section,
    check_prerequisites,
    has_time_conflict,
    rank_courses,
    section_matches_availability,
)


class PlanningEngineTests(unittest.TestCase):
    def test_prerequisite_groups_allow_or_options_and_require_all_groups(self) -> None:
        course = Course(
            code="EECS 2011",
            title="Fundamentals of Data Structures",
            credits=3,
            prerequisites=(("EECS 1022", "EECS 1021"), ("MATH 1019",)),
            difficulty=4,
            workload_hours=9,
            requirement_tags=("core",),
            sections=(),
        )

        self.assertFalse(check_prerequisites(course, ["EECS 1022"]))
        self.assertTrue(check_prerequisites(course, ["eecs 1021", "math 1019"]))

    def test_time_conflicts_detect_overlap_only_on_shared_days(self) -> None:
        first = Section("A", ("Mon", "Wed"), "09:00", "10:30", "Dr. A")
        overlapping = Section("B", ("Wed",), "10:00", "11:00", "Dr. B")
        back_to_back = Section("C", ("Mon",), "10:30", "12:00", "Dr. C")
        different_day = Section("D", ("Tue",), "09:30", "10:15", "Dr. D")

        self.assertTrue(has_time_conflict(first, overlapping))
        self.assertFalse(has_time_conflict(first, back_to_back))
        self.assertFalse(has_time_conflict(first, different_day))

    def test_section_availability_respects_preferred_days_and_times(self) -> None:
        preference = PreferredSchedule(days=("Mon", "Wed"), earliest_start="09:00", latest_end="17:00")

        self.assertTrue(
            section_matches_availability(
                Section("A", ("Mon", "Wed"), "10:30", "12:00", "Dr. A"),
                preference,
            )
        )
        self.assertFalse(
            section_matches_availability(
                Section("B", ("Tue",), "10:30", "12:00", "Dr. A"),
                preference,
            )
        )
        self.assertFalse(
            section_matches_availability(
                Section("C", ("Mon",), "16:30", "18:00", "Dr. A"),
                preference,
            )
        )

    def test_ranking_changes_with_target_mode(self) -> None:
        easy_course = Course(
            code="EECS 3482",
            title="Computer Security",
            credits=3,
            prerequisites=(),
            difficulty=2,
            workload_hours=5,
            requirement_tags=("elective",),
            sections=(),
        )
        hard_course = Course(
            code="EECS 3101",
            title="Design and Analysis of Algorithms",
            credits=3,
            prerequisites=(),
            difficulty=5,
            workload_hours=11,
            requirement_tags=("core",),
            sections=(),
        )
        professor = ProfessorRating("Dr. Test", rating=4.0, workload_reputation=3, would_take_again=75)
        ratings = {"Dr. Test": professor}
        sections = [
            (easy_course, Section("A", ("Mon",), "09:00", "10:00", "Dr. Test")),
            (hard_course, Section("A", ("Tue",), "09:00", "10:00", "Dr. Test")),
        ]
        required_courses = ["EECS 3482", "EECS 3101"]

        easy_ranked = rank_courses(sections, required_courses, ratings, "easy")
        hard_ranked = rank_courses(sections, required_courses, ratings, "hard")

        self.assertEqual(easy_ranked[0].course.code, "EECS 3482")
        self.assertEqual(hard_ranked[0].course.code, "EECS 3101")


if __name__ == "__main__":
    unittest.main()

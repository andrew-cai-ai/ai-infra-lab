"""Constraint and ranking engine for the AI Course Planning Assistant MVP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Sequence

Mode = Literal["easy", "balanced", "hard"]
MODES: tuple[Mode, ...] = ("easy", "balanced", "hard")


@dataclass(frozen=True)
class Section:
    id: str
    days: tuple[str, ...]
    start: str
    end: str
    professor: str


@dataclass(frozen=True)
class Course:
    code: str
    title: str
    credits: int
    prerequisites: tuple[tuple[str, ...], ...]
    difficulty: int
    workload_hours: int
    requirement_tags: tuple[str, ...]
    sections: tuple[Section, ...]


@dataclass(frozen=True)
class ProfessorRating:
    name: str
    rating: float
    workload_reputation: int
    would_take_again: int


@dataclass(frozen=True)
class PreferredSchedule:
    days: tuple[str, ...] = ()
    earliest_start: str = "08:00"
    latest_end: str = "21:30"


@dataclass(frozen=True)
class StudentProfile:
    university: str
    program: str
    completed_courses: tuple[str, ...]
    required_courses: tuple[str, ...]
    preferred_schedule: PreferredSchedule
    target_mode: Mode = "balanced"


@dataclass(frozen=True)
class CourseCandidate:
    course: Course
    section: Section
    professor_rating: ProfessorRating
    estimated_workload_hours: int
    workload_risk: str
    score: float
    score_breakdown: dict[str, float]
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ExcludedCourse:
    code: str
    title: str
    reason: str


@dataclass(frozen=True)
class PlanPolicy:
    max_courses: int
    max_weekly_workload: int


PLAN_POLICIES: dict[Mode, PlanPolicy] = {
    "easy": PlanPolicy(max_courses=3, max_weekly_workload=22),
    "balanced": PlanPolicy(max_courses=4, max_weekly_workload=34),
    "hard": PlanPolicy(max_courses=5, max_weekly_workload=48),
}

NEUTRAL_PROFESSOR_RATING = ProfessorRating(
    name="Unknown Instructor",
    rating=3.0,
    workload_reputation=3,
    would_take_again=50,
)


def normalize_course_code(code: str) -> str:
    return " ".join(code.upper().strip().split())


def _minutes(value: str) -> int:
    hour_text, minute_text = value.split(":", maxsplit=1)
    return int(hour_text) * 60 + int(minute_text)


def check_prerequisites(course: Course, completed_courses: Sequence[str]) -> bool:
    """Return true when every prerequisite group has at least one completed option."""

    completed = {normalize_course_code(code) for code in completed_courses}
    return all(
        any(normalize_course_code(option) in completed for option in group)
        for group in course.prerequisites
    )


def missing_prerequisites(course: Course, completed_courses: Sequence[str]) -> list[str]:
    completed = {normalize_course_code(code) for code in completed_courses}
    missing = []
    for group in course.prerequisites:
        normalized_group = tuple(normalize_course_code(option) for option in group)
        if not any(option in completed for option in normalized_group):
            missing.append(" or ".join(normalized_group))
    return missing


def has_time_conflict(first: Section, second: Section) -> bool:
    if not set(first.days).intersection(second.days):
        return False
    return _minutes(first.start) < _minutes(second.end) and _minutes(second.start) < _minutes(first.end)


def section_matches_availability(section: Section, preference: PreferredSchedule) -> bool:
    preferred_days = set(preference.days)
    if preferred_days and not set(section.days).issubset(preferred_days):
        return False
    return _minutes(preference.earliest_start) <= _minutes(section.start) and _minutes(section.end) <= _minutes(preference.latest_end)


def estimate_workload_hours(course: Course, professor: ProfessorRating) -> int:
    professor_load_penalty = max(0, professor.workload_reputation - 3) * 1.5
    difficulty_penalty = max(0, course.difficulty - 3) * 0.75
    return round(course.workload_hours + professor_load_penalty + difficulty_penalty)


def workload_risk(course: Course, professor: ProfessorRating, estimated_hours: int) -> str:
    if estimated_hours <= 6 and course.difficulty <= 2 and professor.workload_reputation <= 3:
        return "low"
    if estimated_hours >= 10 or course.difficulty >= 4 or professor.workload_reputation >= 4:
        return "high"
    return "medium"


def score_candidate(
    course: Course,
    section: Section,
    professor: ProfessorRating,
    required_courses: Sequence[str],
    mode: Mode,
) -> CourseCandidate:
    required = normalize_course_code(course.code) in {
        normalize_course_code(code) for code in required_courses
    }
    estimated_hours = estimate_workload_hours(course, professor)

    progress_points = 45.0 if required else 10.0
    professor_points = professor.rating * 8.0

    if mode == "easy":
        difficulty_points = (6 - course.difficulty) * 8.0
        workload_points = max(0.0, 14.0 - estimated_hours) * 1.5
        mode_reason = "low workload and lower difficulty"
    elif mode == "balanced":
        difficulty_points = max(0.0, 6.0 - abs(3.0 - course.difficulty)) * 5.0
        workload_points = max(0.0, 12.0 - abs(8.0 - estimated_hours))
        mode_reason = "moderate workload with steady requirement progress"
    else:
        difficulty_points = course.difficulty * 8.0
        workload_points = min(float(estimated_hours), 12.0) * 0.7
        mode_reason = "ambitious course load and stronger technical stretch"

    score_breakdown = {
        "graduation_progress": progress_points,
        "professor_rating": professor_points,
        "difficulty_fit": difficulty_points,
        "workload_fit": workload_points,
    }
    score = sum(score_breakdown.values())

    reasons = [
        "counts toward declared requirements" if required else "useful elective or supporting course",
        f"{professor.name} mock rating {professor.rating:.1f}/5",
        mode_reason,
    ]

    return CourseCandidate(
        course=course,
        section=section,
        professor_rating=professor,
        estimated_workload_hours=estimated_hours,
        workload_risk=workload_risk(course, professor, estimated_hours),
        score=score,
        score_breakdown=score_breakdown,
        reasons=tuple(reasons),
    )


def rank_courses(
    course_sections: Sequence[tuple[Course, Section]],
    required_courses: Sequence[str],
    professor_ratings: dict[str, ProfessorRating],
    mode: Mode,
) -> list[CourseCandidate]:
    candidates = [
        score_candidate(
            course=course,
            section=section,
            professor=professor_ratings.get(section.professor, NEUTRAL_PROFESSOR_RATING),
            required_courses=required_courses,
            mode=mode,
        )
        for course, section in course_sections
    ]
    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.score,
            candidate.professor_rating.rating,
            -_minutes(candidate.section.start),
            candidate.course.code,
        ),
        reverse=True,
    )


def _eligible_course_sections(
    profile: StudentProfile,
    courses: Sequence[Course],
) -> tuple[list[tuple[Course, Section]], list[ExcludedCourse]]:
    completed = {normalize_course_code(code) for code in profile.completed_courses}
    eligible_sections: list[tuple[Course, Section]] = []
    excluded: list[ExcludedCourse] = []

    for course in courses:
        normalized_code = normalize_course_code(course.code)
        if normalized_code in completed:
            excluded.append(ExcludedCourse(course.code, course.title, "already completed"))
            continue

        missing = missing_prerequisites(course, profile.completed_courses)
        if missing:
            excluded.append(
                ExcludedCourse(
                    course.code,
                    course.title,
                    f"missing prerequisite group(s): {', '.join(missing)}",
                )
            )
            continue

        matching_sections = [
            section
            for section in course.sections
            if section_matches_availability(section, profile.preferred_schedule)
        ]
        if not matching_sections:
            excluded.append(
                ExcludedCourse(
                    course.code,
                    course.title,
                    "no offered section fits preferred days/times",
                )
            )
            continue

        eligible_sections.extend((course, section) for section in matching_sections)

    return eligible_sections, excluded


def build_mode_plan(
    mode: Mode,
    profile: StudentProfile,
    course_sections: Sequence[tuple[Course, Section]],
    professor_ratings: dict[str, ProfessorRating],
) -> dict[str, Any]:
    policy = PLAN_POLICIES[mode]
    ranked = rank_courses(course_sections, profile.required_courses, professor_ratings, mode)
    selected: list[CourseCandidate] = []
    selected_codes: set[str] = set()
    total_workload = 0

    for candidate in ranked:
        course_code = normalize_course_code(candidate.course.code)
        if course_code in selected_codes:
            continue
        if total_workload + candidate.estimated_workload_hours > policy.max_weekly_workload:
            continue
        if any(has_time_conflict(candidate.section, chosen.section) for chosen in selected):
            continue

        selected.append(candidate)
        selected_codes.add(course_code)
        total_workload += candidate.estimated_workload_hours

        if len(selected) >= policy.max_courses:
            break

    total_credits = sum(candidate.course.credits for candidate in selected)
    average_rating = (
        round(sum(candidate.professor_rating.rating for candidate in selected) / len(selected), 2)
        if selected
        else 0.0
    )

    return {
        "mode": mode,
        "title": f"{mode.title()} Plan",
        "courses": [_serialize_candidate(candidate, profile.required_courses) for candidate in selected],
        "totalCredits": total_credits,
        "weeklyWorkloadHours": total_workload,
        "averageProfessorRating": average_rating,
        "workloadRisk": _aggregate_workload_risk(total_workload),
        "rationale": _plan_rationale(mode, selected, policy),
        "constraints": {
            "maxCourses": policy.max_courses,
            "maxWeeklyWorkloadHours": policy.max_weekly_workload,
        },
    }


def build_plans(
    profile: StudentProfile,
    courses: Sequence[Course],
    professor_ratings: dict[str, ProfessorRating],
) -> dict[str, Any]:
    if profile.target_mode not in MODES:
        raise ValueError(f"target_mode must be one of: {', '.join(MODES)}")

    course_sections, excluded_courses = _eligible_course_sections(profile, courses)
    plans = [
        build_mode_plan(mode, profile, course_sections, professor_ratings)
        for mode in MODES
    ]

    return {
        "project": "AI Course Planning Assistant",
        "student": {
            "university": profile.university,
            "program": profile.program,
            "targetMode": profile.target_mode,
        },
        "recommendedPlan": f"{profile.target_mode.title()} Plan",
        "plans": plans,
        "agentWorkflow": [
            {"tool": "profile_parser", "result": "normalized student input"},
            {"tool": "mock_course_catalog", "result": f"loaded {len(courses)} York {profile.program} courses"},
            {"tool": "prerequisite_checker", "result": "filtered courses missing prerequisites"},
            {"tool": "schedule_solver", "result": "removed sections outside availability and with conflicts"},
            {"tool": "ranking_engine", "result": "scored plans for easy, balanced, and hard modes"},
        ],
        "excludedCourses": [
            {"code": course.code, "title": course.title, "reason": course.reason}
            for course in excluded_courses
        ],
    }


def _serialize_candidate(candidate: CourseCandidate, required_courses: Sequence[str]) -> dict[str, Any]:
    required = normalize_course_code(candidate.course.code) in {
        normalize_course_code(code) for code in required_courses
    }
    return {
        "code": candidate.course.code,
        "title": candidate.course.title,
        "credits": candidate.course.credits,
        "section": candidate.section.id,
        "days": list(candidate.section.days),
        "start": candidate.section.start,
        "end": candidate.section.end,
        "professor": candidate.section.professor,
        "professorRating": candidate.professor_rating.rating,
        "difficulty": candidate.course.difficulty,
        "estimatedWorkloadHours": candidate.estimated_workload_hours,
        "workloadRisk": candidate.workload_risk,
        "graduationRequirement": required,
        "score": round(candidate.score, 2),
        "scoreBreakdown": {
            key: round(value, 2) for key, value in candidate.score_breakdown.items()
        },
        "reasons": list(candidate.reasons),
    }


def _aggregate_workload_risk(total_workload: int) -> str:
    if total_workload <= 20:
        return "low"
    if total_workload <= 34:
        return "medium"
    return "high"


def _plan_rationale(mode: Mode, selected: Sequence[CourseCandidate], policy: PlanPolicy) -> str:
    if not selected:
        return "No valid courses fit the current prerequisite and schedule constraints."

    requirement_count = sum(
        1 for candidate in selected if "counts toward declared requirements" in candidate.reasons
    )
    return (
        f"Selected {len(selected)} course(s) within the {policy.max_weekly_workload}-hour "
        f"{mode} workload cap, including {requirement_count} declared requirement course(s)."
    )

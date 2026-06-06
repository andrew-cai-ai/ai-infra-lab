"""Mock York University Computer Science course and professor data.

The data is synthetic and intended for local MVP testing only.
"""

from __future__ import annotations

from course_planner_agent.engine import Course, ProfessorRating, Section

YORK_CS_PROFESSOR_RATINGS: dict[str, ProfessorRating] = {
    "Dr. Maya Chen": ProfessorRating("Dr. Maya Chen", rating=4.7, workload_reputation=2, would_take_again=92),
    "Dr. Lena Ortiz": ProfessorRating("Dr. Lena Ortiz", rating=4.4, workload_reputation=3, would_take_again=86),
    "Dr. Omar Saleh": ProfessorRating("Dr. Omar Saleh", rating=4.1, workload_reputation=3, would_take_again=80),
    "Dr. Noor Hassan": ProfessorRating("Dr. Noor Hassan", rating=4.6, workload_reputation=4, would_take_again=88),
    "Dr. Victor Huang": ProfessorRating("Dr. Victor Huang", rating=3.5, workload_reputation=5, would_take_again=61),
    "Dr. Samir Patel": ProfessorRating("Dr. Samir Patel", rating=3.8, workload_reputation=4, would_take_again=69),
    "Dr. Priya Nair": ProfessorRating("Dr. Priya Nair", rating=4.8, workload_reputation=2, would_take_again=94),
    "Dr. Claire Brooks": ProfessorRating("Dr. Claire Brooks", rating=4.2, workload_reputation=2, would_take_again=83),
}

YORK_CS_COURSES: tuple[Course, ...] = (
    Course(
        code="EECS 1012",
        title="Net-centric Introduction to Computing",
        credits=3,
        prerequisites=(),
        difficulty=2,
        workload_hours=5,
        requirement_tags=("programming", "first-year"),
        sections=(
            Section("A", ("Tue", "Thu"), "09:00", "10:30", "Dr. Maya Chen"),
            Section("B", ("Mon", "Wed"), "14:30", "16:00", "Dr. Omar Saleh"),
        ),
    ),
    Course(
        code="EECS 1022",
        title="Programming for Mobile Computing",
        credits=3,
        prerequisites=(("EECS 1012", "EECS 1015"),),
        difficulty=3,
        workload_hours=7,
        requirement_tags=("programming", "software"),
        sections=(
            Section("A", ("Mon", "Wed"), "10:30", "12:00", "Dr. Maya Chen"),
            Section("B", ("Tue", "Thu"), "13:00", "14:30", "Dr. Lena Ortiz"),
        ),
    ),
    Course(
        code="MATH 1019",
        title="Discrete Mathematics for Computer Science",
        credits=3,
        prerequisites=(),
        difficulty=3,
        workload_hours=7,
        requirement_tags=("math", "foundations"),
        sections=(
            Section("A", ("Mon", "Wed"), "12:00", "13:30", "Dr. Claire Brooks"),
            Section("B", ("Tue", "Thu"), "16:00", "17:30", "Dr. Samir Patel"),
        ),
    ),
    Course(
        code="MATH 1300",
        title="Differential Calculus with Applications",
        credits=3,
        prerequisites=(),
        difficulty=3,
        workload_hours=7,
        requirement_tags=("math", "calculus"),
        sections=(
            Section("A", ("Tue", "Thu"), "10:30", "12:00", "Dr. Claire Brooks"),
            Section("B", ("Fri",), "09:00", "12:00", "Dr. Samir Patel"),
        ),
    ),
    Course(
        code="EECS 2030",
        title="Advanced Object Oriented Programming",
        credits=3,
        prerequisites=(("EECS 1022", "EECS 1021"),),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("programming", "software"),
        sections=(
            Section("A", ("Mon", "Wed"), "13:00", "14:30", "Dr. Lena Ortiz"),
            Section("B", ("Tue", "Thu"), "10:30", "12:00", "Dr. Omar Saleh"),
        ),
    ),
    Course(
        code="EECS 2011",
        title="Fundamentals of Data Structures",
        credits=3,
        prerequisites=(("EECS 1022", "EECS 1021"), ("MATH 1019",)),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("algorithms", "core"),
        sections=(
            Section("A", ("Mon", "Wed"), "09:00", "10:30", "Dr. Noor Hassan"),
            Section("B", ("Tue", "Thu"), "14:30", "16:00", "Dr. Victor Huang"),
        ),
    ),
    Course(
        code="EECS 2021",
        title="Computer Organization",
        credits=3,
        prerequisites=(("EECS 2030",), ("MATH 1019",)),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("systems", "core"),
        sections=(
            Section("A", ("Tue", "Thu"), "09:00", "10:30", "Dr. Victor Huang"),
            Section("B", ("Fri",), "10:00", "13:00", "Dr. Samir Patel"),
        ),
    ),
    Course(
        code="EECS 2031",
        title="Software Tools",
        credits=3,
        prerequisites=(("EECS 2030",),),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("systems", "software"),
        sections=(
            Section("A", ("Mon", "Wed"), "16:00", "17:30", "Dr. Priya Nair"),
            Section("B", ("Fri",), "13:00", "16:00", "Dr. Omar Saleh"),
        ),
    ),
    Course(
        code="EECS 3101",
        title="Design and Analysis of Algorithms",
        credits=3,
        prerequisites=(("EECS 2011",),),
        difficulty=5,
        workload_hours=11,
        requirement_tags=("algorithms", "upper-year"),
        sections=(
            Section("A", ("Tue", "Thu"), "16:00", "17:30", "Dr. Noor Hassan"),
            Section("B", ("Mon", "Wed"), "10:30", "12:00", "Dr. Victor Huang"),
        ),
    ),
    Course(
        code="EECS 3311",
        title="Software Design",
        credits=3,
        prerequisites=(("EECS 2030",),),
        difficulty=3,
        workload_hours=7,
        requirement_tags=("software", "upper-year"),
        sections=(
            Section("A", ("Mon", "Wed"), "14:30", "16:00", "Dr. Maya Chen"),
            Section("B", ("Tue", "Thu"), "12:00", "13:30", "Dr. Priya Nair"),
        ),
    ),
    Course(
        code="EECS 3421",
        title="Introduction to Database Systems",
        credits=3,
        prerequisites=(("EECS 2011",), ("EECS 2031",)),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("data", "upper-year"),
        sections=(
            Section("A", ("Tue", "Thu"), "10:30", "12:00", "Dr. Lena Ortiz"),
            Section("B", ("Mon", "Wed"), "17:30", "19:00", "Dr. Samir Patel"),
        ),
    ),
    Course(
        code="EECS 3482",
        title="Computer Security",
        credits=3,
        prerequisites=(("EECS 2030",),),
        difficulty=2,
        workload_hours=5,
        requirement_tags=("security", "elective"),
        sections=(
            Section("A", ("Fri",), "09:00", "12:00", "Dr. Claire Brooks"),
            Section("B", ("Mon",), "18:00", "21:00", "Dr. Priya Nair"),
        ),
    ),
    Course(
        code="EECS 3221",
        title="Operating System Fundamentals",
        credits=3,
        prerequisites=(("EECS 2021",),),
        difficulty=5,
        workload_hours=12,
        requirement_tags=("systems", "upper-year"),
        sections=(
            Section("A", ("Mon", "Wed"), "12:00", "13:30", "Dr. Victor Huang"),
            Section("B", ("Tue", "Thu"), "18:00", "19:30", "Dr. Noor Hassan"),
        ),
    ),
)

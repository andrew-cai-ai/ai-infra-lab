"""Mock York University catalog registry for multiple programs.

The data is synthetic and intended for local MVP testing only. It gives the
planner a program-aware shape before real York catalog/timetable integrations
are added.
"""

from __future__ import annotations

from dataclasses import dataclass

from course_planner_agent.data.york_cs import YORK_CS_COURSES, YORK_CS_PROFESSOR_RATINGS
from course_planner_agent.engine import Course, ProfessorRating, Section


@dataclass(frozen=True)
class ProgramCatalog:
    slug: str
    name: str
    courses: tuple[Course, ...]
    professor_ratings: dict[str, ProfessorRating]
    default_completed_courses: tuple[str, ...]
    default_required_courses: tuple[str, ...]


YORK_SOCIAL_SCIENCE_RATINGS: dict[str, ProfessorRating] = {
    "Dr. Elaine Moretti": ProfessorRating("Dr. Elaine Moretti", rating=4.7, workload_reputation=2, would_take_again=91),
    "Dr. Jonah Reed": ProfessorRating("Dr. Jonah Reed", rating=4.2, workload_reputation=3, would_take_again=82),
    "Dr. Sofia Martins": ProfessorRating("Dr. Sofia Martins", rating=4.5, workload_reputation=3, would_take_again=88),
    "Dr. Rachel Kim": ProfessorRating("Dr. Rachel Kim", rating=3.9, workload_reputation=4, would_take_again=73),
    "Dr. Patrick Lewis": ProfessorRating("Dr. Patrick Lewis", rating=4.1, workload_reputation=4, would_take_again=76),
    "Dr. Aisha Grant": ProfessorRating("Dr. Aisha Grant", rating=4.8, workload_reputation=2, would_take_again=95),
}

YORK_BUSINESS_RATINGS: dict[str, ProfessorRating] = {
    "Prof. Daniel Rossi": ProfessorRating("Prof. Daniel Rossi", rating=4.6, workload_reputation=3, would_take_again=89),
    "Prof. Meera Shah": ProfessorRating("Prof. Meera Shah", rating=4.4, workload_reputation=2, would_take_again=87),
    "Prof. Nathan White": ProfessorRating("Prof. Nathan White", rating=3.7, workload_reputation=4, would_take_again=68),
    "Prof. Hannah Yu": ProfessorRating("Prof. Hannah Yu", rating=4.9, workload_reputation=3, would_take_again=96),
    "Prof. Lucas Martin": ProfessorRating("Prof. Lucas Martin", rating=4.0, workload_reputation=4, would_take_again=74),
    "Prof. Amira Khan": ProfessorRating("Prof. Amira Khan", rating=4.3, workload_reputation=3, would_take_again=84),
}

YORK_SCIENCE_RATINGS: dict[str, ProfessorRating] = {
    "Dr. Naomi Fischer": ProfessorRating("Dr. Naomi Fischer", rating=4.6, workload_reputation=3, would_take_again=88),
    "Dr. Mateo Alvarez": ProfessorRating("Dr. Mateo Alvarez", rating=4.1, workload_reputation=4, would_take_again=78),
    "Dr. Vivian Lau": ProfessorRating("Dr. Vivian Lau", rating=4.5, workload_reputation=3, would_take_again=86),
    "Dr. Ibrahim Okafor": ProfessorRating("Dr. Ibrahim Okafor", rating=3.8, workload_reputation=5, would_take_again=66),
    "Dr. Emily Carter": ProfessorRating("Dr. Emily Carter", rating=4.7, workload_reputation=2, would_take_again=92),
    "Dr. Ryan Singh": ProfessorRating("Dr. Ryan Singh", rating=4.0, workload_reputation=4, would_take_again=75),
}

YORK_KINESIOLOGY_RATINGS: dict[str, ProfessorRating] = {
    "Dr. Avery Riddell": ProfessorRating("Dr. Avery Riddell", rating=4.6, workload_reputation=3, would_take_again=89),
    "Dr. Celeste Morgan": ProfessorRating("Dr. Celeste Morgan", rating=4.4, workload_reputation=2, would_take_again=86),
    "Dr. Jordan Sato": ProfessorRating("Dr. Jordan Sato", rating=4.2, workload_reputation=4, would_take_again=79),
    "Dr. Mina Kapoor": ProfessorRating("Dr. Mina Kapoor", rating=4.8, workload_reputation=3, would_take_again=94),
    "Dr. Gabriel Stone": ProfessorRating("Dr. Gabriel Stone", rating=3.9, workload_reputation=5, would_take_again=70),
    "Dr. Nadia Brooks": ProfessorRating("Dr. Nadia Brooks", rating=4.5, workload_reputation=3, would_take_again=87),
    "Dr. Theo Campbell": ProfessorRating("Dr. Theo Campbell", rating=4.1, workload_reputation=4, would_take_again=76),
}

YORK_KINESIOLOGY_COURSES: tuple[Course, ...] = (
    Course(
        code="KINE 1000",
        title="Sociocultural Perspectives in Kinesiology",
        credits=6,
        prerequisites=(),
        difficulty=2,
        workload_hours=7,
        requirement_tags=("major-core", "first-year"),
        sections=(
            Section("A", ("Mon", "Wed"), "10:30", "12:00", "Dr. Celeste Morgan"),
            Section("B", ("Tue", "Thu"), "14:30", "16:00", "Dr. Jordan Sato"),
        ),
    ),
    Course(
        code="KINE 1020",
        title="Fitness and Health",
        credits=6,
        prerequisites=(),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("major-core", "first-year"),
        sections=(
            Section("A", ("Tue", "Thu"), "09:00", "10:30", "Dr. Avery Riddell"),
            Section("B", ("Mon", "Wed"), "13:00", "14:30", "Dr. Nadia Brooks"),
        ),
    ),
    Course(
        code="KINE 1900",
        title="Integrated Physical Activity for Life I",
        credits=3,
        prerequisites=(),
        difficulty=2,
        workload_hours=5,
        requirement_tags=("activity", "first-year"),
        sections=(
            Section("A", ("Fri",), "09:00", "12:00", "Dr. Mina Kapoor"),
            Section("B", ("Mon", "Wed"), "16:00", "17:30", "Dr. Theo Campbell"),
        ),
    ),
    Course(
        code="KINE 2011",
        title="Human Physiology I",
        credits=3,
        prerequisites=(("KINE 1020",),),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("science-core", "physiology"),
        sections=(
            Section("A", ("Mon", "Wed"), "09:00", "10:30", "Dr. Avery Riddell"),
            Section("B", ("Tue", "Thu"), "12:00", "13:30", "Dr. Gabriel Stone"),
        ),
    ),
    Course(
        code="KINE 2031",
        title="Human Anatomy",
        credits=3,
        prerequisites=(("KINE 1020",),),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("science-core", "anatomy"),
        sections=(
            Section("A", ("Tue", "Thu"), "10:30", "12:00", "Dr. Nadia Brooks"),
            Section("B", ("Fri",), "10:00", "13:00", "Dr. Jordan Sato"),
        ),
    ),
    Course(
        code="KINE 2049",
        title="Research Methods in Kinesiology",
        credits=3,
        prerequisites=(("KINE 1000",),),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("methods", "major-core"),
        sections=(
            Section("A", ("Mon", "Wed"), "14:30", "16:00", "Dr. Celeste Morgan"),
            Section("B", ("Tue", "Thu"), "16:00", "17:30", "Dr. Theo Campbell"),
        ),
    ),
    Course(
        code="KINE 2050",
        title="Analysis of Data in Kinesiology",
        credits=3,
        prerequisites=(("KINE 2049",),),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("methods", "statistics"),
        sections=(
            Section("A", ("Mon", "Wed"), "12:00", "13:30", "Dr. Mina Kapoor"),
            Section("B", ("Fri",), "13:00", "16:00", "Dr. Gabriel Stone"),
        ),
    ),
    Course(
        code="KINE 3000",
        title="Psychology of Physical Activity and Health",
        credits=3,
        prerequisites=(("KINE 1000",),),
        difficulty=3,
        workload_hours=7,
        requirement_tags=("upper-year", "psychology"),
        sections=(
            Section("A", ("Tue", "Thu"), "13:00", "14:30", "Dr. Mina Kapoor"),
            Section("B", ("Mon", "Wed"), "17:30", "19:00", "Dr. Celeste Morgan"),
        ),
    ),
    Course(
        code="KINE 3012",
        title="Human Physiology II",
        credits=3,
        prerequisites=(("KINE 2011",),),
        difficulty=5,
        workload_hours=12,
        requirement_tags=("upper-year", "physiology"),
        sections=(
            Section("A", ("Tue", "Thu"), "16:00", "17:30", "Dr. Avery Riddell"),
            Section("B", ("Mon", "Wed"), "10:30", "12:00", "Dr. Gabriel Stone"),
        ),
    ),
    Course(
        code="KINE 3020",
        title="Skilled Performance and Motor Learning",
        credits=3,
        prerequisites=(("KINE 2011", "KINE 2031"),),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("upper-year", "motor-learning"),
        sections=(
            Section("A", ("Mon", "Wed"), "16:00", "17:30", "Dr. Jordan Sato"),
            Section("B", ("Tue", "Thu"), "09:00", "10:30", "Dr. Nadia Brooks"),
        ),
    ),
    Course(
        code="KINE 3030",
        title="Biomechanics of Human Movement",
        credits=3,
        prerequisites=(("KINE 2011", "KINE 2031"),),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("upper-year", "biomechanics"),
        sections=(
            Section("A", ("Mon", "Wed"), "13:00", "14:30", "Dr. Theo Campbell"),
            Section("B", ("Fri",), "09:00", "12:00", "Dr. Nadia Brooks"),
        ),
    ),
    Course(
        code="KINE 4010",
        title="Exercise Physiology",
        credits=3,
        prerequisites=(("KINE 3012",),),
        difficulty=5,
        workload_hours=12,
        requirement_tags=("fourth-year", "physiology"),
        sections=(
            Section("A", ("Tue", "Thu"), "12:00", "13:30", "Dr. Avery Riddell"),
            Section("B", ("Mon", "Wed"), "14:30", "16:00", "Dr. Gabriel Stone"),
        ),
    ),
)

YORK_PSYCHOLOGY_COURSES: tuple[Course, ...] = (
    Course(
        code="PSYC 1010",
        title="Introduction to Psychology",
        credits=6,
        prerequisites=(),
        difficulty=2,
        workload_hours=7,
        requirement_tags=("major-core", "first-year"),
        sections=(
            Section("A", ("Mon", "Wed"), "10:30", "12:00", "Dr. Elaine Moretti"),
            Section("B", ("Tue", "Thu"), "14:30", "16:00", "Dr. Jonah Reed"),
        ),
    ),
    Course(
        code="PSYC 2020",
        title="Statistical Methods I",
        credits=3,
        prerequisites=(("PSYC 1010",),),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("methods", "major-core"),
        sections=(
            Section("A", ("Mon", "Wed"), "09:00", "10:30", "Dr. Sofia Martins"),
            Section("B", ("Fri",), "09:00", "12:00", "Dr. Rachel Kim"),
        ),
    ),
    Course(
        code="PSYC 2030",
        title="Research Methods in Psychology",
        credits=3,
        prerequisites=(("PSYC 1010",),),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("methods", "major-core"),
        sections=(
            Section("A", ("Tue", "Thu"), "10:30", "12:00", "Dr. Sofia Martins"),
            Section("B", ("Mon", "Wed"), "16:00", "17:30", "Dr. Patrick Lewis"),
        ),
    ),
    Course(
        code="PSYC 2120",
        title="Social Psychology",
        credits=3,
        prerequisites=(("PSYC 1010",),),
        difficulty=2,
        workload_hours=6,
        requirement_tags=("area", "social"),
        sections=(
            Section("A", ("Tue", "Thu"), "12:00", "13:30", "Dr. Aisha Grant"),
            Section("B", ("Fri",), "13:00", "16:00", "Dr. Jonah Reed"),
        ),
    ),
    Course(
        code="PSYC 2130",
        title="Personality",
        credits=3,
        prerequisites=(("PSYC 1010",),),
        difficulty=2,
        workload_hours=5,
        requirement_tags=("area", "social"),
        sections=(
            Section("A", ("Mon", "Wed"), "13:00", "14:30", "Dr. Elaine Moretti"),
            Section("B", ("Tue",), "18:00", "21:00", "Dr. Patrick Lewis"),
        ),
    ),
    Course(
        code="PSYC 2240",
        title="Biological Basis of Behaviour",
        credits=3,
        prerequisites=(("PSYC 1010",),),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("area", "biological"),
        sections=(
            Section("A", ("Mon", "Wed"), "14:30", "16:00", "Dr. Rachel Kim"),
            Section("B", ("Tue", "Thu"), "09:00", "10:30", "Dr. Sofia Martins"),
        ),
    ),
    Course(
        code="PSYC 3140",
        title="Abnormal Psychology",
        credits=3,
        prerequisites=(("PSYC 1010",), ("PSYC 2020", "PSYC 2030")),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("upper-year", "clinical"),
        sections=(
            Section("A", ("Tue", "Thu"), "16:00", "17:30", "Dr. Aisha Grant"),
            Section("B", ("Fri",), "10:00", "13:00", "Dr. Patrick Lewis"),
        ),
    ),
    Course(
        code="PSYC 3265",
        title="Memory and Cognition",
        credits=3,
        prerequisites=(("PSYC 1010",), ("PSYC 2020", "PSYC 2030")),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("upper-year", "cognitive"),
        sections=(
            Section("A", ("Mon", "Wed"), "12:00", "13:30", "Dr. Sofia Martins"),
            Section("B", ("Tue", "Thu"), "13:00", "14:30", "Dr. Rachel Kim"),
        ),
    ),
)

YORK_COMMERCE_COURSES: tuple[Course, ...] = (
    Course(
        code="ADMS 1000",
        title="Introduction to Administrative Studies",
        credits=3,
        prerequisites=(),
        difficulty=2,
        workload_hours=5,
        requirement_tags=("foundation", "business"),
        sections=(
            Section("A", ("Mon", "Wed"), "09:00", "10:30", "Prof. Daniel Rossi"),
            Section("B", ("Tue", "Thu"), "13:00", "14:30", "Prof. Meera Shah"),
        ),
    ),
    Course(
        code="ADMS 1010",
        title="Exploring the Functions of Business",
        credits=3,
        prerequisites=(),
        difficulty=2,
        workload_hours=6,
        requirement_tags=("foundation", "business"),
        sections=(
            Section("A", ("Mon", "Wed"), "10:30", "12:00", "Prof. Hannah Yu"),
            Section("B", ("Fri",), "09:00", "12:00", "Prof. Lucas Martin"),
        ),
    ),
    Course(
        code="ADMS 2200",
        title="Introductory Marketing",
        credits=3,
        prerequisites=(("ADMS 1000", "ADMS 1010"),),
        difficulty=3,
        workload_hours=7,
        requirement_tags=("marketing", "core"),
        sections=(
            Section("A", ("Tue", "Thu"), "10:30", "12:00", "Prof. Meera Shah"),
            Section("B", ("Mon", "Wed"), "14:30", "16:00", "Prof. Nathan White"),
        ),
    ),
    Course(
        code="ADMS 2320",
        title="Quantitative Methods I",
        credits=3,
        prerequisites=(("ADMS 1000", "ADMS 1010"),),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("analytics", "core"),
        sections=(
            Section("A", ("Tue", "Thu"), "09:00", "10:30", "Prof. Amira Khan"),
            Section("B", ("Fri",), "10:00", "13:00", "Prof. Nathan White"),
        ),
    ),
    Course(
        code="ADMS 2400",
        title="Introduction to Organizational Behaviour",
        credits=3,
        prerequisites=(("ADMS 1000", "ADMS 1010"),),
        difficulty=2,
        workload_hours=5,
        requirement_tags=("management", "core"),
        sections=(
            Section("A", ("Mon", "Wed"), "13:00", "14:30", "Prof. Hannah Yu"),
            Section("B", ("Tue", "Thu"), "16:00", "17:30", "Prof. Daniel Rossi"),
        ),
    ),
    Course(
        code="ADMS 2500",
        title="Introduction to Financial Accounting",
        credits=3,
        prerequisites=(("ADMS 1000", "ADMS 1010"),),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("accounting", "core"),
        sections=(
            Section("A", ("Mon", "Wed"), "16:00", "17:30", "Prof. Amira Khan"),
            Section("B", ("Tue", "Thu"), "12:00", "13:30", "Prof. Lucas Martin"),
        ),
    ),
    Course(
        code="ADMS 2510",
        title="Introduction to Management Accounting",
        credits=3,
        prerequisites=(("ADMS 2500",),),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("accounting", "core"),
        sections=(
            Section("A", ("Mon", "Wed"), "12:00", "13:30", "Prof. Nathan White"),
            Section("B", ("Tue", "Thu"), "14:30", "16:00", "Prof. Amira Khan"),
        ),
    ),
    Course(
        code="ADMS 3330",
        title="Business Analytics",
        credits=3,
        prerequisites=(("ADMS 2320",),),
        difficulty=5,
        workload_hours=11,
        requirement_tags=("analytics", "upper-year"),
        sections=(
            Section("A", ("Mon", "Wed"), "17:30", "19:00", "Prof. Daniel Rossi"),
            Section("B", ("Fri",), "13:00", "16:00", "Prof. Meera Shah"),
        ),
    ),
)

YORK_BIOLOGY_COURSES: tuple[Course, ...] = (
    Course(
        code="BIOL 1000",
        title="Biology I: Cells, Molecular Biology and Genetics",
        credits=3,
        prerequisites=(),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("foundation", "biology"),
        sections=(
            Section("A", ("Mon", "Wed"), "09:00", "10:30", "Dr. Naomi Fischer"),
            Section("B", ("Tue", "Thu"), "14:30", "16:00", "Dr. Mateo Alvarez"),
        ),
    ),
    Course(
        code="BIOL 1001",
        title="Biology II: Evolution, Ecology, Biodiversity and Conservation",
        credits=3,
        prerequisites=(),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("foundation", "biology"),
        sections=(
            Section("A", ("Tue", "Thu"), "10:30", "12:00", "Dr. Vivian Lau"),
            Section("B", ("Fri",), "09:00", "12:00", "Dr. Ryan Singh"),
        ),
    ),
    Course(
        code="CHEM 1000",
        title="Chemical Structure",
        credits=3,
        prerequisites=(),
        difficulty=4,
        workload_hours=9,
        requirement_tags=("chemistry", "science-core"),
        sections=(
            Section("A", ("Mon", "Wed"), "12:00", "13:30", "Dr. Emily Carter"),
            Section("B", ("Tue", "Thu"), "16:00", "17:30", "Dr. Ibrahim Okafor"),
        ),
    ),
    Course(
        code="CHEM 1001",
        title="Chemical Dynamics",
        credits=3,
        prerequisites=(("CHEM 1000",),),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("chemistry", "science-core"),
        sections=(
            Section("A", ("Mon", "Wed"), "14:30", "16:00", "Dr. Emily Carter"),
            Section("B", ("Fri",), "10:00", "13:00", "Dr. Ibrahim Okafor"),
        ),
    ),
    Course(
        code="BIOL 2020",
        title="Biochemistry",
        credits=3,
        prerequisites=(("BIOL 1000",), ("CHEM 1000",)),
        difficulty=5,
        workload_hours=12,
        requirement_tags=("upper-year", "molecular"),
        sections=(
            Section("A", ("Tue", "Thu"), "12:00", "13:30", "Dr. Naomi Fischer"),
            Section("B", ("Mon", "Wed"), "16:00", "17:30", "Dr. Mateo Alvarez"),
        ),
    ),
    Course(
        code="BIOL 2040",
        title="Genetics",
        credits=3,
        prerequisites=(("BIOL 1000",),),
        difficulty=4,
        workload_hours=10,
        requirement_tags=("upper-year", "genetics"),
        sections=(
            Section("A", ("Mon", "Wed"), "10:30", "12:00", "Dr. Vivian Lau"),
            Section("B", ("Tue", "Thu"), "09:00", "10:30", "Dr. Ryan Singh"),
        ),
    ),
    Course(
        code="BIOL 2050",
        title="Ecology",
        credits=3,
        prerequisites=(("BIOL 1001",),),
        difficulty=3,
        workload_hours=8,
        requirement_tags=("upper-year", "ecology"),
        sections=(
            Section("A", ("Mon", "Wed"), "13:00", "14:30", "Dr. Naomi Fischer"),
            Section("B", ("Fri",), "13:00", "16:00", "Dr. Vivian Lau"),
        ),
    ),
    Course(
        code="BIOL 3150",
        title="Microbiology",
        credits=3,
        prerequisites=(("BIOL 2020", "BIOL 2040"),),
        difficulty=5,
        workload_hours=12,
        requirement_tags=("upper-year", "lab"),
        sections=(
            Section("A", ("Tue", "Thu"), "16:00", "17:30", "Dr. Emily Carter"),
            Section("B", ("Mon", "Wed"), "17:30", "19:00", "Dr. Ibrahim Okafor"),
        ),
    ),
)

PROGRAM_CATALOGS: dict[str, ProgramCatalog] = {
    "Kinesiology and Health Science": ProgramCatalog(
        slug="kinesiology-health-science",
        name="Kinesiology and Health Science",
        courses=YORK_KINESIOLOGY_COURSES,
        professor_ratings=YORK_KINESIOLOGY_RATINGS,
        default_completed_courses=("KINE 1000", "KINE 1020"),
        default_required_courses=("KINE 2011", "KINE 2031", "KINE 2049", "KINE 2050", "KINE 3000", "KINE 3012", "KINE 3030"),
    ),
    "Computer Science": ProgramCatalog(
        slug="computer-science",
        name="Computer Science",
        courses=YORK_CS_COURSES,
        professor_ratings=YORK_CS_PROFESSOR_RATINGS,
        default_completed_courses=("EECS 1012", "EECS 1022", "MATH 1019", "EECS 2030", "EECS 2011"),
        default_required_courses=("EECS 2021", "EECS 2031", "EECS 3101", "EECS 3311", "EECS 3421", "EECS 3482"),
    ),
    "Psychology": ProgramCatalog(
        slug="psychology",
        name="Psychology",
        courses=YORK_PSYCHOLOGY_COURSES,
        professor_ratings=YORK_SOCIAL_SCIENCE_RATINGS,
        default_completed_courses=("PSYC 1010",),
        default_required_courses=("PSYC 2020", "PSYC 2030", "PSYC 2120", "PSYC 2130", "PSYC 2240", "PSYC 3140"),
    ),
    "Commerce": ProgramCatalog(
        slug="commerce",
        name="Commerce",
        courses=YORK_COMMERCE_COURSES,
        professor_ratings=YORK_BUSINESS_RATINGS,
        default_completed_courses=("ADMS 1000", "ADMS 1010"),
        default_required_courses=("ADMS 2200", "ADMS 2320", "ADMS 2400", "ADMS 2500", "ADMS 2510", "ADMS 3330"),
    ),
    "Biology": ProgramCatalog(
        slug="biology",
        name="Biology",
        courses=YORK_BIOLOGY_COURSES,
        professor_ratings=YORK_SCIENCE_RATINGS,
        default_completed_courses=("BIOL 1000", "BIOL 1001", "CHEM 1000"),
        default_required_courses=("CHEM 1001", "BIOL 2020", "BIOL 2040", "BIOL 2050", "BIOL 3150"),
    ),
}

DEFAULT_PROGRAM = "Kinesiology and Health Science"

PROGRAM_ALIASES: dict[str, str] = {
    "kinesiology": "Kinesiology and Health Science",
    "kinensilogy": "Kinesiology and Health Science",
    "kine": "Kinesiology and Health Science",
    "kinesiology health science": "Kinesiology and Health Science",
    "kinesiology and health science": "Kinesiology and Health Science",
    "kinesiology-health-science": "Kinesiology and Health Science",
}


def list_programs() -> list[dict[str, str]]:
    return [
        {"name": catalog.name, "slug": catalog.slug}
        for catalog in PROGRAM_CATALOGS.values()
    ]


def get_program_catalog(program: str | None) -> ProgramCatalog:
    if program in PROGRAM_CATALOGS:
        return PROGRAM_CATALOGS[program]

    normalized = (program or "").strip().casefold()
    if normalized in PROGRAM_ALIASES:
        return PROGRAM_CATALOGS[PROGRAM_ALIASES[normalized]]

    for catalog in PROGRAM_CATALOGS.values():
        if normalized in {catalog.name.casefold(), catalog.slug.casefold()}:
            return catalog

    return PROGRAM_CATALOGS[DEFAULT_PROGRAM]

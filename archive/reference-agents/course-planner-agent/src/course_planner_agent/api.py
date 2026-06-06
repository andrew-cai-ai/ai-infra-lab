"""FastAPI API for the AI Course Planning Assistant MVP."""

from __future__ import annotations

from dataclasses import replace

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from course_planner_agent import __version__
from course_planner_agent.data.york_catalog import get_program_catalog, list_programs
from course_planner_agent.engine import build_plans
from course_planner_agent.models import StudentProfileInput, to_student_profile
from course_planner_agent.ui import render_planner_ui

app = FastAPI(
    title="AI Course Planning Assistant",
    version=__version__,
    description="MVP agentic course planning API using mock York University program data.",
)


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    return HTMLResponse(render_planner_ui())


@app.get("/api")
def api_root() -> dict[str, object]:
    return {
        "project": "AI Course Planning Assistant",
        "status": "running",
        "message": "Use / for the planner UI, /docs for interactive API docs, or POST /plans with a student profile.",
        "endpoints": {
            "ui": "/",
            "docs": "/docs",
            "health": "/health",
            "programs": "/mock-data/programs",
            "mockCourses": "/mock-data/courses",
            "createPlans": "/plans",
        },
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/mock-data/programs")
def mock_programs() -> dict[str, object]:
    return {
        "university": "York University",
        "programs": list_programs(),
    }


@app.get("/mock-data/courses")
def mock_courses(program: str = Query("Kinesiology and Health Science")) -> dict[str, object]:
    catalog = get_program_catalog(program)
    return {
        "university": "York University",
        "program": catalog.name,
        "courseCount": len(catalog.courses),
        "defaultCompletedCourses": list(catalog.default_completed_courses),
        "defaultRequiredCourses": list(catalog.default_required_courses),
        "courses": [
            {
                "code": course.code,
                "title": course.title,
                "credits": course.credits,
                "difficulty": course.difficulty,
                "workloadHours": course.workload_hours,
                "requirementTags": list(course.requirement_tags),
                "prerequisites": [list(group) for group in course.prerequisites],
                "sections": [
                    {
                        "id": section.id,
                        "days": list(section.days),
                        "start": section.start,
                        "end": section.end,
                        "professor": section.professor,
                    }
                    for section in course.sections
                ],
            }
            for course in catalog.courses
        ],
    }


@app.post("/plans")
def create_plans(profile: StudentProfileInput) -> dict[str, object]:
    catalog = get_program_catalog(profile.program)
    student_profile = replace(to_student_profile(profile), program=catalog.name)
    return build_plans(
        profile=student_profile,
        courses=catalog.courses,
        professor_ratings=catalog.professor_ratings,
    )

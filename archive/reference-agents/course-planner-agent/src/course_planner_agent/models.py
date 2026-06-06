"""FastAPI request models and adapters."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from course_planner_agent.engine import PreferredSchedule, StudentProfile


class PreferredScheduleInput(BaseModel):
    days: list[str] = Field(default_factory=list, examples=[["Mon", "Wed", "Fri"]])
    earliest_start: str = Field("09:00", examples=["09:00"])
    latest_end: str = Field("17:30", examples=["17:30"])


class StudentProfileInput(BaseModel):
    university: str = Field("York University", examples=["York University"])
    program: str = Field("Kinesiology and Health Science", examples=["Kinesiology and Health Science"])
    completed_courses: list[str] = Field(default_factory=list, examples=[["KINE 1000", "KINE 1020"]])
    required_courses: list[str] = Field(
        default_factory=list,
        examples=[["KINE 2011", "KINE 2031", "KINE 2049", "KINE 2050"]],
    )
    preferred_schedule: PreferredScheduleInput = Field(default_factory=PreferredScheduleInput)
    target_mode: Literal["easy", "balanced", "hard"] = "balanced"


def to_student_profile(payload: StudentProfileInput) -> StudentProfile:
    schedule = payload.preferred_schedule
    return StudentProfile(
        university=payload.university,
        program=payload.program,
        completed_courses=tuple(payload.completed_courses),
        required_courses=tuple(payload.required_courses),
        preferred_schedule=PreferredSchedule(
            days=tuple(schedule.days),
            earliest_start=schedule.earliest_start,
            latest_end=schedule.latest_end,
        ),
        target_mode=payload.target_mode,
    )

from dataclasses import dataclass, field
from typing import List


@dataclass
class Employment:

    company: str | None = None

    job_title: str | None = None

    start_date: str | None = None

    end_date: str | None = None

    responsibilities: List[str] = field(
        default_factory=list
    )

    technologies: List[str] = field(
        default_factory=list
    )


@dataclass
class Education:

    degree: str | None = None

    field_of_study: str | None = None

    institution: str | None = None

    start_date: str | None = None

    end_date: str | None = None


@dataclass
class Project:

    name: str | None = None

    technologies: List[str] = field(
        default_factory=list
    )

    responsibilities: List[str] = field(
        default_factory=list
    )

    outcomes: List[str] = field(
        default_factory=list
    )


@dataclass
class StudentProfile:

    name: str | None = None

    emails: List[str] = field(
        default_factory=list
    )

    phones: List[str] = field(
        default_factory=list
    )

    locations: List[str] = field(
        default_factory=list
    )

    skills: List[str] = field(
        default_factory=list
    )

    employments: List[Employment] = field(
        default_factory=list
    )

    education: List[Education] = field(
        default_factory=list
    )

    projects: List[Project] = field(
        default_factory=list
    )

    certifications: List[str] = field(
        default_factory=list
    )

    achievements: List[str] = field(
        default_factory=list
    )

    """
FILE PURPOSE:
Defines the structured StudentProfile representation created from
resume extraction results.

It organizes information such as skills, employment, education,
projects, certifications, and achievements into a reusable format.

This profile becomes the main input for future resume-to-JD matching
and ranking instead of repeatedly processing the original resume.

LIMITATION:
The current schema is an initial version and will be expanded with
richer evidence, confidence, dates, and additional resume information.
"""
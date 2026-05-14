from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from .models import ApplicationStatus, Location


class ErrorResponse(BaseModel):
    error: str
    detail: str


class JobBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    department: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1)
    location: Location
    salary_min: int = Field(ge=0)
    salary_max: int = Field(ge=0)
    required_skills: list[str] = Field(min_length=1)
    max_applicants: int | None = Field(default=None, gt=0)
    deadline: date

    @field_validator("title", "department", "description")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank")
        return cleaned

    @field_validator("required_skills")
    @classmethod
    def normalize_skills(cls, skills: list[str]) -> list[str]:
        cleaned = [skill.strip() for skill in skills if skill.strip()]
        if not cleaned:
            raise ValueError("At least one required skill is required")
        return cleaned

    @model_validator(mode="after")
    def validate_salary_range(self) -> "JobBase":
        if self.salary_min >= self.salary_max:
            raise ValueError("salary_min must be strictly less than salary_max")
        return self


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_closed: bool
    created_at: datetime
    closed_at: datetime | None
    application_count: int = 0


class PaginatedJobs(BaseModel):
    total_count: int
    page: int
    per_page: int
    results: list[JobRead]


class ApplicationCreate(BaseModel):
    applicant_name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    years_experience: int = Field(ge=0)
    cv_summary: str = Field(min_length=1, max_length=1000)
    linkedin_url: str | None = None

    @field_validator("applicant_name", "cv_summary")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank")
        return cleaned

    @field_validator("linkedin_url")
    @classmethod
    def validate_linkedin_url(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        if not (
            value.startswith("https://linkedin.com/")
            or value.startswith("https://www.linkedin.com/")
        ):
            raise ValueError("linkedin_url must start with https://linkedin.com/ or https://www.linkedin.com/")
        return value


class StatusHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_status: ApplicationStatus | None
    to_status: ApplicationStatus
    note: str
    created_at: datetime


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    applicant_name: str
    email: EmailStr
    years_experience: int
    cv_summary: str
    linkedin_url: str | None
    status: ApplicationStatus
    created_at: datetime
    history: list[StatusHistoryRead] = []


class StatusUpdate(BaseModel):
    status: ApplicationStatus
    note: str = Field(min_length=1)

    @field_validator("note")
    @classmethod
    def strip_note(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("A manager note is required for every status change")
        return cleaned


class StatsRead(BaseModel):
    total_jobs: int
    open_jobs: int
    closed_jobs: int
    total_applications: int
    avg_applications_per_job: float
    top_department: str | None

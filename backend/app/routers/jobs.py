from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ApplicationStatus, Location
from ..schemas import ApplicationCreate, ApplicationRead, JobCreate, JobRead, PaginatedJobs
from .. import services


router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db)) -> dict:
    job = services.create_job(db, payload)
    return services.serialize_job(db, job)


@router.get("", response_model=PaginatedJobs)
def list_jobs(
    department: str | None = None,
    location: Location | None = None,
    skill: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=50),
    include_closed: bool = False,
    db: Session = Depends(get_db),
) -> dict:
    total_count, jobs = services.list_jobs(
        db=db,
        department=department,
        location=location,
        skill=skill,
        page=page,
        per_page=per_page,
        include_closed=include_closed,
    )
    return {
        "total_count": total_count,
        "page": page,
        "per_page": per_page,
        "results": [services.serialize_job(db, job) for job in jobs],
    }


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: int, db: Session = Depends(get_db)) -> dict:
    job = services.get_job_or_404(db, job_id)
    return services.serialize_job(db, job)


@router.post("/{job_id}/applications", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def submit_application(
    job_id: int,
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
):
    return services.submit_application(db, job_id, payload)


@router.get("/{job_id}/applications", response_model=list[ApplicationRead])
def list_applications(
    job_id: int,
    status: ApplicationStatus | None = None,
    db: Session = Depends(get_db),
):
    return services.list_applications(db, job_id, status)


@router.patch("/{job_id}/close", response_model=JobRead)
def close_job(job_id: int, db: Session = Depends(get_db)) -> dict:
    job = services.close_job(db, job_id)
    return services.serialize_job(db, job)

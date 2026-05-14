from datetime import date, datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from .models import Application, ApplicationStatus, Job, Location, StatusHistory
from .schemas import ApplicationCreate, JobCreate, StatusUpdate


VALID_TRANSITIONS: dict[ApplicationStatus, set[ApplicationStatus]] = {
    ApplicationStatus.pending: {ApplicationStatus.shortlisted, ApplicationStatus.rejected},
    ApplicationStatus.shortlisted: {ApplicationStatus.offered, ApplicationStatus.rejected},
    ApplicationStatus.offered: {ApplicationStatus.rejected},
    ApplicationStatus.rejected: set(),
}


def api_error(status_code: int, error: str, detail: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"error": error, "detail": detail})


def application_count(db: Session, job_id: int) -> int:
    return db.scalar(select(func.count(Application.id)).where(Application.job_id == job_id)) or 0


def serialize_job(db: Session, job: Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "department": job.department,
        "description": job.description,
        "location": job.location,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "required_skills": job.required_skills,
        "max_applicants": job.max_applicants,
        "deadline": job.deadline,
        "is_closed": job.is_closed,
        "created_at": job.created_at,
        "closed_at": job.closed_at,
        "application_count": application_count(db, job.id),
    }


def get_job_or_404(db: Session, job_id: int) -> Job:
    job = db.get(Job, job_id)
    if job is None:
        raise api_error(status.HTTP_404_NOT_FOUND, "not_found", "Job not found")
    return job


def get_application_or_404(db: Session, application_id: int) -> Application:
    application = db.scalar(
        select(Application)
        .where(Application.id == application_id)
        .options(selectinload(Application.history))
    )
    if application is None:
        raise api_error(status.HTTP_404_NOT_FOUND, "not_found", "Application not found")
    return application


def create_job(db: Session, payload: JobCreate) -> Job:
    job = Job(**payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def list_jobs(
    db: Session,
    department: str | None,
    location: Location | None,
    skill: str | None,
    page: int,
    per_page: int,
    include_closed: bool,
) -> tuple[int, list[Job]]:
    query = select(Job)
    today = date.today()

    if not include_closed:
        query = query.where(Job.is_closed.is_(False), Job.deadline >= today)
    if department:
        query = query.where(func.lower(Job.department) == department.strip().lower())
    if location:
        query = query.where(Job.location == location)

    jobs = list(db.scalars(query.order_by(Job.created_at.desc(), Job.id.desc())).all())
    if skill:
        skill_term = skill.strip().lower()
        jobs = [
            job
            for job in jobs
            if any(skill_term in required_skill.lower() for required_skill in job.required_skills)
        ]

    total_count = len(jobs)
    start = (page - 1) * per_page
    end = start + per_page
    return total_count, jobs[start:end]


def submit_application(db: Session, job_id: int, payload: ApplicationCreate) -> Application:
    job = get_job_or_404(db, job_id)
    today = date.today()

    if job.is_closed:
        raise api_error(status.HTTP_409_CONFLICT, "job_closed", "This job is closed and no longer accepts applications")
    if job.deadline < today:
        raise api_error(status.HTTP_409_CONFLICT, "deadline_passed", "This job deadline has passed")

    current_count = application_count(db, job.id)
    if job.max_applicants is not None and current_count >= job.max_applicants:
        raise api_error(status.HTTP_409_CONFLICT, "max_applicants_reached", "This job has reached its applicant cap")

    existing = db.scalar(
        select(Application).where(
            Application.job_id == job.id,
            func.lower(Application.email) == str(payload.email).lower(),
        )
    )
    if existing is not None:
        raise api_error(
            status.HTTP_409_CONFLICT,
            "duplicate_application",
            "This email has already applied to this job",
        )

    application = Application(job_id=job.id, **payload.model_dump())
    db.add(application)
    db.flush()
    db.add(
        StatusHistory(
            application_id=application.id,
            from_status=None,
            to_status=ApplicationStatus.pending,
            note="Application submitted",
        )
    )
    db.commit()
    db.refresh(application)
    return get_application_or_404(db, application.id)


def list_applications(
    db: Session,
    job_id: int,
    status_filter: ApplicationStatus | None,
) -> list[Application]:
    get_job_or_404(db, job_id)
    query = (
        select(Application)
        .where(Application.job_id == job_id)
        .options(selectinload(Application.history))
        .order_by(Application.created_at.desc(), Application.id.desc())
    )
    if status_filter is not None:
        query = query.where(Application.status == status_filter)
    return list(db.scalars(query).all())


def update_status(db: Session, application_id: int, payload: StatusUpdate) -> Application:
    application = get_application_or_404(db, application_id)
    current_status = application.status
    new_status = payload.status

    if new_status == current_status:
        raise api_error(status.HTTP_400_BAD_REQUEST, "invalid_transition", "Application is already in that status")

    if new_status not in VALID_TRANSITIONS[current_status]:
        raise api_error(
            status.HTTP_400_BAD_REQUEST,
            "invalid_transition",
            f"Cannot move application from {current_status.value} to {new_status.value}",
        )

    application.status = new_status
    db.add(
        StatusHistory(
            application_id=application.id,
            from_status=current_status,
            to_status=new_status,
            note=payload.note,
        )
    )
    db.commit()
    return get_application_or_404(db, application.id)


def close_job(db: Session, job_id: int) -> Job:
    job = get_job_or_404(db, job_id)
    if not job.is_closed:
        job.is_closed = True
        job.closed_at = datetime.utcnow()
        db.commit()
        db.refresh(job)
    return job


def get_stats(db: Session) -> dict:
    today = date.today()
    total_jobs = db.scalar(select(func.count(Job.id))) or 0
    open_jobs = db.scalar(
        select(func.count(Job.id)).where(Job.is_closed.is_(False), Job.deadline >= today)
    ) or 0
    closed_jobs = total_jobs - open_jobs
    total_applications = db.scalar(select(func.count(Application.id))) or 0
    avg_applications_per_job = round(total_applications / total_jobs, 2) if total_jobs else 0.0

    top_department_row = db.execute(
        select(Job.department, func.count(Application.id).label("application_count"))
        .outerjoin(Application, Application.job_id == Job.id)
        .group_by(Job.department)
        .order_by(func.count(Application.id).desc(), Job.department.asc())
        .limit(1)
    ).first()

    return {
        "total_jobs": total_jobs,
        "open_jobs": open_jobs,
        "closed_jobs": closed_jobs,
        "total_applications": total_applications,
        "avg_applications_per_job": avg_applications_per_job,
        "top_department": top_department_row[0] if top_department_row else None,
    }

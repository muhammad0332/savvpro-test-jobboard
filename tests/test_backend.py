from datetime import date, timedelta


def job_payload(**overrides):
    payload = {
        "title": "Senior Backend Engineer",
        "department": "Engineering",
        "description": "Build reliable APIs for internal hiring workflows.",
        "location": "remote",
        "salary_min": 90000,
        "salary_max": 130000,
        "required_skills": ["Python", "FastAPI", "SQL"],
        "max_applicants": None,
        "deadline": (date.today() + timedelta(days=30)).isoformat(),
    }
    payload.update(overrides)
    return payload


def application_payload(**overrides):
    payload = {
        "applicant_name": "Ayesha Khan",
        "email": "ayesha@example.com",
        "years_experience": 4,
        "cv_summary": "FastAPI developer with production API experience.",
        "linkedin_url": "https://www.linkedin.com/in/ayesha",
    }
    payload.update(overrides)
    return payload


def create_job(client, **overrides):
    response = client.post("/api/jobs", json=job_payload(**overrides))
    assert response.status_code == 201, response.json()
    return response.json()


def apply_to_job(client, job_id: int, **overrides):
    response = client.post(f"/api/jobs/{job_id}/applications", json=application_payload(**overrides))
    assert response.status_code == 201, response.json()
    return response.json()


def test_job_creation_rejects_invalid_salary_range(client):
    response = client.post("/api/jobs", json=job_payload(salary_min=130000, salary_max=90000))

    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


def test_job_listing_supports_pagination_and_filters(client):
    create_job(client, title="Backend Engineer", department="Engineering", required_skills=["Python"])
    create_job(client, title="Frontend Engineer", department="Engineering", required_skills=["React"])
    create_job(client, title="People Partner", department="People", required_skills=["Hiring"])

    response = client.get("/api/jobs", params={"department": "Engineering", "page": 1, "per_page": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["total_count"] == 2
    assert body["page"] == 1
    assert body["per_page"] == 1
    assert len(body["results"]) == 1

    skill_response = client.get("/api/jobs", params={"skill": "react"})
    assert skill_response.json()["total_count"] == 1
    assert skill_response.json()["results"][0]["title"] == "Frontend Engineer"


def test_duplicate_application_is_rejected(client):
    job = create_job(client)
    apply_to_job(client, job["id"], email="same@example.com")

    response = client.post(
        f"/api/jobs/{job['id']}/applications",
        json=application_payload(email="same@example.com"),
    )

    assert response.status_code == 409
    assert response.json()["error"] == "duplicate_application"


def test_status_workflow_allows_forward_transitions_and_blocks_backwards(client):
    job = create_job(client)
    application = apply_to_job(client, job["id"])

    shortlisted = client.patch(
        f"/api/applications/{application['id']}/status",
        json={"status": "shortlisted", "note": "Strong backend experience"},
    )
    assert shortlisted.status_code == 200
    assert shortlisted.json()["status"] == "shortlisted"
    assert len(shortlisted.json()["history"]) == 2

    backwards = client.patch(
        f"/api/applications/{application['id']}/status",
        json={"status": "pending", "note": "Trying to move backwards"},
    )
    assert backwards.status_code == 400
    assert backwards.json()["error"] == "invalid_transition"


def test_closed_jobs_block_new_applications_but_keep_pending_status(client):
    job = create_job(client)
    application = apply_to_job(client, job["id"], email="pending@example.com")

    close_response = client.patch(f"/api/jobs/{job['id']}/close")
    assert close_response.status_code == 200
    assert close_response.json()["is_closed"] is True

    blocked = client.post(
        f"/api/jobs/{job['id']}/applications",
        json=application_payload(email="late@example.com"),
    )
    assert blocked.status_code == 409
    assert blocked.json()["error"] == "job_closed"

    applications = client.get(f"/api/jobs/{job['id']}/applications").json()
    assert applications[0]["id"] == application["id"]
    assert applications[0]["status"] == "pending"


def test_stats_are_computed_from_database(client):
    engineering_job = create_job(client, department="Engineering")
    create_job(client, department="People")
    apply_to_job(client, engineering_job["id"], email="one@example.com")
    apply_to_job(client, engineering_job["id"], email="two@example.com")

    response = client.get("/api/stats")

    assert response.status_code == 200
    body = response.json()
    assert body["total_jobs"] == 2
    assert body["open_jobs"] == 2
    assert body["closed_jobs"] == 0
    assert body["total_applications"] == 2
    assert body["avg_applications_per_job"] == 1.0
    assert body["top_department"] == "Engineering"

# User Guide

Start the backend first:

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Feature 1: Post A Job Listing

Use the `Create Job Listing` form on `/`, or call:

```bash
curl -X POST http://localhost:8000/api/jobs ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Backend Engineer\",\"department\":\"Engineering\",\"description\":\"Build APIs\",\"location\":\"remote\",\"salary_min\":90000,\"salary_max\":130000,\"required_skills\":[\"Python\",\"FastAPI\"],\"max_applicants\":2,\"deadline\":\"2026-06-30\"}"
```

## Feature 2: Browse And Search Jobs

Use filters on `/`, or call:

```bash
curl "http://localhost:8000/api/jobs?department=Engineering&location=remote&skill=python&page=1&per_page=5"
```

Include closed or expired jobs:

```bash
curl "http://localhost:8000/api/jobs?include_closed=true"
```

## Feature 3: Apply To A Job

Open `/jobs/1`, fill the application form, or call:

```bash
curl -X POST http://localhost:8000/api/jobs/1/applications ^
  -H "Content-Type: application/json" ^
  -d "{\"applicant_name\":\"Ayesha Khan\",\"email\":\"ayesha@example.com\",\"years_experience\":4,\"cv_summary\":\"FastAPI developer with hiring workflow experience.\",\"linkedin_url\":\"https://www.linkedin.com/in/ayesha\"}"
```

## Feature 4: Application Status Workflow

Open `/jobs/1/applications` and use the status controls. Valid flow:

```text
pending -> shortlisted -> offered
pending -> rejected
shortlisted -> rejected
offered -> rejected
```

Update by API:

```bash
curl -X PATCH http://localhost:8000/api/applications/1/status ^
  -H "Content-Type: application/json" ^
  -d "{\"status\":\"shortlisted\",\"note\":\"Strong FastAPI experience\"}"
```

Filter applications by status:

```bash
curl "http://localhost:8000/api/jobs/1/applications?status=shortlisted"
```

## Feature 5: Job Analytics

Open `/dashboard`, or call:

```bash
curl http://localhost:8000/api/stats
```

Example response:

```json
{
  "total_jobs": 2,
  "open_jobs": 2,
  "closed_jobs": 0,
  "total_applications": 3,
  "avg_applications_per_job": 1.5,
  "top_department": "Engineering"
}
```

## Feature 6: Close A Job Listing

Open `/jobs/1/applications` and click `Close job`, or call:

```bash
curl -X PATCH http://localhost:8000/api/jobs/1/close
```

After a job is closed, new applications return `409 job_closed`. Existing pending applications are left unchanged by design.

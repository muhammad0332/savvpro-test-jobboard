# AI Usage Log

AI tool used: Cursor AI coding agent.

I directed the AI in small implementation phases, reviewed the generated code against `TASK.md`, ran tests, and corrected gaps before moving to the next phase.

## Verbatim Prompts

### Prompt 1

```text
Actually i am doing this for my job technical Assesment. so kindly understand each and everything clearly as this depends on my career=>Instructions link
https://github.com/savvpro/savvpro-test-jobboard/blob/main/README.md

Task Link:
https://github.com/savvpro/savvpro-test-jobboard/blob/main/TASK.md

Repository Link:
https://github.com/savvpro/savvpro-test-jobboard
```

### Prompt 2

```text
first start building the backend and also create a new branch like this is describe . Muhammad Adnan<muhammad0332> and then start working
```

### Prompt 3

```text
JobBoard Pro Assessment Plan

Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.
```

### Prompt 4

```text
Read-only exploration of the repository at d:\Sidework\JobBoard Pro\savvpro-test-jobboard. Focus on TASK.md, README.md, and any existing backend-related files. Return: repo structure, backend requirements, expected API endpoints/business rules/data model, and any testing/documentation expectations. Thoroughness: medium.
```

### Prompt 5

```text
Build the FastAPI backend first with SQLite persistence, SQLAlchemy models, Pydantic schemas, structured validation errors, job filtering and pagination, application submission, duplicate blocking, status history, job closing, and live stats.
```

### Prompt 6

```text
Add pytest coverage for salary validation, job pagination and filtering, duplicate applications, status workflow transitions, close-job behavior, and computed stats.
```

### Prompt 7

```text
Create the required Next.js frontend pages and reusable components: job listings with filters and pagination, job detail with application form, applications pipeline with status controls, and dashboard analytics.
```

## AI Mistakes And Corrections

### Mistake 1: Missing Job Creation In The First Frontend Pass

The first frontend pass covered browsing, applying, pipeline management, and dashboard analytics, but did not expose job creation in the UI. I caught this by checking Feature 1 again and added a `Create Job Listing` form on `/` that calls `POST /api/jobs`.

### Mistake 2: Non-ASCII UI Separators

The AI introduced symbols such as arrows and middle dots in React components. I corrected them to plain ASCII text so the codebase stays simple and consistent.

### Mistake 3: Frontend Build Environment Assumption

The AI attempted to run `npm install`, but the local environment had Node.js without `npm` on PATH. I kept the frontend source and documented standard npm commands, while backend tests were run successfully.

## Verification Performed

```text
python -m pytest tests
```

Result: 6 tests passed.

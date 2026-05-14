# JobBoard Pro

Full-stack assessment implementation for job listings, applications, status workflow, and analytics.

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Open `http://localhost:8000/docs` for the FastAPI documentation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:3000`. By default, `/api/*` requests are **proxied** to FastAPI (see `frontend/next.config.js`) so the browser does not hit cross-origin or IPv4/IPv6 `localhost` mismatches.

- Optional `frontend/.env.local`: `BACKEND_API_URL=http://127.0.0.1:8000` if your API is not on port 8000.
- Set `NEXT_PUBLIC_API_BASE_URL` only if you need the browser to call the API host directly instead of the proxy.

### Tests

```bash
python -m pytest tests
```

## Product Assumptions

- There is no authentication; manager actions are trust-based as requested.
- Duplicate applications are blocked permanently for the same email and job.
- Closing a job blocks new applications but leaves existing pending applications unchanged.
- Hitting `max_applicants` stops new applications without auto-closing the listing.

## Main API Endpoints

- `POST /api/jobs`
- `GET /api/jobs`
- `GET /api/jobs/{id}`
- `POST /api/jobs/{id}/applications`
- `GET /api/jobs/{id}/applications`
- `PATCH /api/applications/{id}/status`
- `PATCH /api/jobs/{id}/close`
- `GET /api/stats`

## Original Submission Guide

# Step-by-Step Guide: How to Fork, Clone, and Submit Your Assessment

**Repository:** https://github.com/savvpro/savvpro-test-jobboard

---

## Step 1: Fork the Repository

1. Go to the repository: https://github.com/savvpro/savvpro-test-jobboard
2. Click the **Fork** button in the top-right corner.
3. This will create a copy of the repository in your GitHub account.

---

## Step 2: Clone Your Fork

1. Open your forked repository in your GitHub account.
2. Click the green **Code** button and copy the URL.
3. Run the following commands:

```bash
git clone https://github.com/your-username/savvpro-test-jobboard.git
cd savvpro-test-jobboard
```

---

## Step 3: Read the Task

Open and read **TASK.md** carefully before writing any code.

- TASK.md URL: https://github.com/savvpro/savvpro-test-jobboard/blob/main/TASK.md

---

## Step 4: Create a New Branch

Branch pattern: `candidate-<your-github-username>`

```bash
git checkout -b candidate-<your-github-username>
```

**Example:**
```bash
git checkout -b candidate-johndoe
```

---

## Step 5: Complete the Task

Build the full application on your branch.

---

## Step 6: Push Your Branch

```bash
git add .
git commit -m "feat: complete JobBoard assessment"
git push origin candidate-<your-github-username>
```

---

## Step 7: Create a Pull Request

1. Go to your **forked** repository on GitHub (`https://github.com/your-username/savvpro-test-jobboard`).
2. Click **Compare & pull request** (GitHub will show this banner after you push your branch).
3. Ensure the following settings in the PR form:
   - **Base repository:** `savvpro/savvpro-test-jobboard` ← the original repo
   - **Base branch:** `main`
   - **Head repository:** `your-username/savvpro-test-jobboard` ← your fork
   - **Compare branch:** `candidate-<your-github-username>`
4. Use the title: `feat: complete JobBoard assessment`
5. Submit the pull request.

> 💡 **Tip:** If you don't see the banner, go to the original repo (`savvpro/savvpro-test-jobboard`), click the **Pull requests** tab, then click **New pull request** → **compare across forks**.

---

> ⚠️ **Important:** No submissions will be accepted after the deadline.

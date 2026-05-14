"use client";

import { FormEvent, useEffect, useState } from "react";
import { JobCard } from "../components/JobCard";
import { PaginationControls } from "../components/PaginationControls";
import { apiFetch } from "../lib/api";
import { Job, Location, PaginatedJobs } from "../types";

export default function HomePage() {
  const [jobs, setJobs] = useState<PaginatedJobs | null>(null);
  const [department, setDepartment] = useState("");
  const [location, setLocation] = useState<Location | "">("");
  const [skill, setSkill] = useState("");
  const [page, setPage] = useState(1);
  const [message, setMessage] = useState("");

  async function loadJobs(nextPage = page) {
    setMessage("");
    const params = new URLSearchParams({ page: String(nextPage), per_page: "5" });
    if (department) params.set("department", department);
    if (location) params.set("location", location);
    if (skill) params.set("skill", skill);
    try {
      setJobs(await apiFetch<PaginatedJobs>(`/api/jobs?${params.toString()}`));
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to load jobs");
    }
  }

  function search(event: FormEvent) {
    event.preventDefault();
    setPage(1);
    loadJobs(1);
  }

  async function createJob(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    const form = new FormData(event.currentTarget);
    const payload = {
      title: String(form.get("title")),
      department: String(form.get("department")),
      description: String(form.get("description")),
      location: String(form.get("location")),
      salary_min: Number(form.get("salary_min")),
      salary_max: Number(form.get("salary_max")),
      required_skills: String(form.get("required_skills"))
        .split(",")
        .map((skill) => skill.trim())
        .filter(Boolean),
      max_applicants: form.get("max_applicants") ? Number(form.get("max_applicants")) : null,
      deadline: String(form.get("deadline")),
    };
    try {
      const created = await apiFetch<Job>("/api/jobs", { method: "POST", body: JSON.stringify(payload) });
      event.currentTarget.reset();
      setMessage(`Created job ${created.title}`);
      loadJobs(1);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to create job");
    }
  }

  useEffect(() => {
    loadJobs(1);
  }, []);

  return (
    <div className="stack">
      <section className="panel stack">
        <h1>Open Roles</h1>
        <form className="row" onSubmit={search}>
          <input value={department} onChange={(event) => setDepartment(event.target.value)} placeholder="Department" />
          <select value={location} onChange={(event) => setLocation(event.target.value as Location | "")}>
            <option value="">Any location</option>
            <option value="remote">Remote</option>
            <option value="hybrid">Hybrid</option>
            <option value="onsite">Onsite</option>
          </select>
          <input value={skill} onChange={(event) => setSkill(event.target.value)} placeholder="Skill" />
          <button className="button" type="submit">
            Search
          </button>
        </form>
      </section>
      <section className="panel stack">
        <h2>Create Job Listing</h2>
        <form className="grid two-column" onSubmit={createJob}>
          <input name="title" placeholder="Title" required />
          <input name="department" placeholder="Department" required />
          <select name="location" required>
            <option value="remote">Remote</option>
            <option value="hybrid">Hybrid</option>
            <option value="onsite">Onsite</option>
          </select>
          <input name="deadline" required type="date" />
          <input min="0" name="salary_min" placeholder="Salary min" required type="number" />
          <input min="1" name="salary_max" placeholder="Salary max" required type="number" />
          <input name="required_skills" placeholder="Skills, comma separated" required />
          <input min="1" name="max_applicants" placeholder="Max applicants (optional)" type="number" />
          <textarea name="description" placeholder="Description" required rows={4} />
          <button className="button" type="submit">
            Create job
          </button>
        </form>
      </section>
      {message && <p className="error">{message}</p>}
      <div className="grid">
        {jobs?.results.map((job) => (
          <JobCard job={job} key={job.id} />
        ))}
      </div>
      {jobs && (
        <PaginationControls
          page={page}
          perPage={jobs.per_page}
          totalCount={jobs.total_count}
          onPageChange={(nextPage) => {
            setPage(nextPage);
            loadJobs(nextPage);
          }}
        />
      )}
    </div>
  );
}

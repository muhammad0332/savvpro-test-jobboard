"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import { apiFetch } from "../../../lib/api";
import { Application, Job } from "../../../types";

export default function JobDetailPage() {
  const params = useParams<{ id: string }>();
  const [job, setJob] = useState<Job | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiFetch<Job>(`/api/jobs/${params.id}`).then(setJob).catch((error) => setMessage(error.message));
  }, [params.id]);

  async function apply(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    const form = new FormData(event.currentTarget);
    const payload = {
      applicant_name: String(form.get("applicant_name")),
      email: String(form.get("email")),
      years_experience: Number(form.get("years_experience")),
      cv_summary: String(form.get("cv_summary")),
      linkedin_url: String(form.get("linkedin_url") || ""),
    };
    try {
      const application = await apiFetch<Application>(`/api/jobs/${params.id}/applications`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      event.currentTarget.reset();
      setMessage(`Application submitted with status ${application.status}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Application failed");
    }
  }

  if (!job) {
    return <p>{message || "Loading job..."}</p>;
  }

  return (
    <div className="grid two-column">
      <section className="panel stack">
        <h1>{job.title}</h1>
        <p className="muted">
          {job.department} - {job.location} - deadline {job.deadline}
        </p>
        <p>{job.description}</p>
        <div className="row">
          {job.required_skills.map((skill) => (
            <span className="badge pending" key={skill}>
              {skill}
            </span>
          ))}
        </div>
        <p>
          Salary ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
        </p>
        <Link className="button secondary" href={`/jobs/${job.id}/applications`}>
          Manage applications
        </Link>
      </section>

      <section className="panel stack">
        <h2>Apply</h2>
        <form className="stack" onSubmit={apply}>
          <label className="field">
            Name
            <input name="applicant_name" required />
          </label>
          <label className="field">
            Email
            <input name="email" required type="email" />
          </label>
          <label className="field">
            Years experience
            <input min="0" name="years_experience" required type="number" />
          </label>
          <label className="field">
            LinkedIn URL
            <input name="linkedin_url" placeholder="https://www.linkedin.com/in/you" />
          </label>
          <label className="field">
            CV summary
            <textarea maxLength={1000} name="cv_summary" required rows={6} />
          </label>
          <button className="button" type="submit">
            Submit application
          </button>
        </form>
        {message && <p className={message.startsWith("Application submitted") ? "success" : "error"}>{message}</p>}
      </section>
    </div>
  );
}

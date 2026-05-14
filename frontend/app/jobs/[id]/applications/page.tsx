"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ApplicationRow } from "../../../../components/ApplicationRow";
import { apiFetch } from "../../../../lib/api";
import { Application, ApplicationStatus, Job } from "../../../../types";

export default function ApplicationsPage() {
  const params = useParams<{ id: string }>();
  const [job, setJob] = useState<Job | null>(null);
  const [applications, setApplications] = useState<Application[]>([]);
  const [status, setStatus] = useState<ApplicationStatus | "">("");
  const [message, setMessage] = useState("");

  async function loadApplications(filter = status) {
    const query = filter ? `?status=${filter}` : "";
    try {
      const [jobResponse, applicationResponse] = await Promise.all([
        apiFetch<Job>(`/api/jobs/${params.id}`),
        apiFetch<Application[]>(`/api/jobs/${params.id}/applications${query}`),
      ]);
      setJob(jobResponse);
      setApplications(applicationResponse);
      setMessage("");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to load applications");
    }
  }

  async function closeJob() {
    try {
      const closed = await apiFetch<Job>(`/api/jobs/${params.id}/close`, { method: "PATCH" });
      setJob(closed);
      setMessage("Job closed. Pending applications were intentionally left unchanged.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to close job");
    }
  }

  useEffect(() => {
    loadApplications("");
  }, [params.id]);

  return (
    <div className="stack">
      <section className="panel stack">
        <div className="row">
          <h1>{job ? `${job.title} pipeline` : "Applications"}</h1>
          {job?.is_closed && <span className="badge rejected">Closed</span>}
        </div>
        <div className="row">
          <select
            value={status}
            onChange={(event) => {
              const nextStatus = event.target.value as ApplicationStatus | "";
              setStatus(nextStatus);
              loadApplications(nextStatus);
            }}
          >
            <option value="">All statuses</option>
            <option value="pending">Pending</option>
            <option value="shortlisted">Shortlisted</option>
            <option value="offered">Offered</option>
            <option value="rejected">Rejected</option>
          </select>
          <button className="button secondary" disabled={job?.is_closed} onClick={closeJob}>
            Close job
          </button>
        </div>
        {message && <p className={message.startsWith("Job closed") ? "success" : "error"}>{message}</p>}
      </section>

      <div className="grid">
        {applications.map((application) => (
          <ApplicationRow
            application={application}
            key={application.id}
            onUpdated={(updated) =>
              setApplications((current) =>
                current.map((applicationItem) => (applicationItem.id === updated.id ? updated : applicationItem)),
              )
            }
          />
        ))}
        {applications.length === 0 && <p className="muted">No applications found.</p>}
      </div>
    </div>
  );
}

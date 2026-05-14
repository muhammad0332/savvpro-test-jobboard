"use client";

import { useState } from "react";
import { apiFetch } from "../lib/api";
import { Application, ApplicationStatus } from "../types";
import { StatusBadge } from "./StatusBadge";

type Props = {
  application: Application;
  onUpdated: (application: Application) => void;
};

const statuses: ApplicationStatus[] = ["pending", "shortlisted", "offered", "rejected"];

export function ApplicationRow({ application, onUpdated }: Props) {
  const [status, setStatus] = useState<ApplicationStatus>(application.status);
  const [note, setNote] = useState("");
  const [message, setMessage] = useState("");

  async function updateStatus() {
    setMessage("");
    try {
      const updated = await apiFetch<Application>(`/api/applications/${application.id}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status, note }),
      });
      setNote("");
      onUpdated(updated);
      setMessage("Status updated");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Status update failed");
    }
  }

  return (
    <div className="card stack">
      <div className="row">
        <strong>{application.applicant_name}</strong>
        <StatusBadge status={application.status} />
      </div>
      <p className="muted">
        {application.email} - {application.years_experience} years experience
      </p>
      <p>{application.cv_summary}</p>
      <div className="row">
        <select value={status} onChange={(event) => setStatus(event.target.value as ApplicationStatus)}>
          {statuses.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        <input value={note} onChange={(event) => setNote(event.target.value)} placeholder="Manager note" />
        <button className="button" onClick={updateStatus}>
          Update
        </button>
      </div>
      {message && <p className={message === "Status updated" ? "success" : "error"}>{message}</p>}
      <details>
        <summary>Status history ({application.history.length})</summary>
        <div className="stack">
          {application.history.map((event) => (
            <p className="muted" key={event.id}>
              {event.from_status || "new"} to {event.to_status}: {event.note}
            </p>
          ))}
        </div>
      </details>
    </div>
  );
}

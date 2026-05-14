"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import { Stats } from "../../types";

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiFetch<Stats>("/api/stats").then(setStats).catch((error) => setMessage(error.message));
  }, []);

  if (!stats) {
    return <p>{message || "Loading dashboard..."}</p>;
  }

  const cards = [
    ["Total jobs", stats.total_jobs],
    ["Open jobs", stats.open_jobs],
    ["Closed jobs", stats.closed_jobs],
    ["Applications", stats.total_applications],
    ["Avg applications/job", stats.avg_applications_per_job],
    ["Top department", stats.top_department || "None"],
  ];

  return (
    <section className="stack">
      <h1>Hiring Dashboard</h1>
      <div className="grid two-column">
        {cards.map(([label, value]) => (
          <div className="card" key={label}>
            <p className="muted">{label}</p>
            <h2>{value}</h2>
          </div>
        ))}
      </div>
    </section>
  );
}

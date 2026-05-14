import Link from "next/link";
import { Job } from "../types";

export function JobCard({ job }: { job: Job }) {
  return (
    <article className="card stack">
      <div>
        <h2>{job.title}</h2>
        <p className="muted">
          {job.department} - {job.location} - deadline {job.deadline}
        </p>
      </div>
      <p>{job.description}</p>
      <div className="row">
        {job.required_skills.map((skill) => (
          <span className="badge pending" key={skill}>
            {skill}
          </span>
        ))}
      </div>
      <p className="muted">
        Salary ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()} - Applications{" "}
        {job.application_count}
      </p>
      <div className="row">
        <Link className="button" href={`/jobs/${job.id}`}>
          View and apply
        </Link>
        <Link className="button secondary" href={`/jobs/${job.id}/applications`}>
          Pipeline
        </Link>
      </div>
    </article>
  );
}

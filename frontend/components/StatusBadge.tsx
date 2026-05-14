import { ApplicationStatus } from "../types";

export function StatusBadge({ status }: { status: ApplicationStatus }) {
  return <span className={`badge ${status}`}>{status}</span>;
}

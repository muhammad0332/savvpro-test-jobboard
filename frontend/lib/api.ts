/**
 * When unset, use same-origin `/api/...` so Next.js rewrites (see next.config.js) proxy to FastAPI.
 * Set NEXT_PUBLIC_API_BASE_URL only if the browser must call the API host directly (e.g. deployed split origins).
 */
const explicitBase = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
const API_BASE_URL = explicitBase ? explicitBase.replace(/\/$/, "") : "";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  let response: Response;
  try {
    response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      cache: "no-store",
    });
  } catch {
    throw new ApiError(
      "Could not reach the API. Start the FastAPI server (uvicorn) and ensure it matches BACKEND_API_URL in frontend/.env.local if you changed the port.",
      0,
    );
  }

  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail =
      typeof body?.detail === "string"
        ? body.detail
        : typeof body?.detail === "object" && body?.detail !== null
          ? JSON.stringify(body.detail)
          : body?.error || "Request failed";
    throw new ApiError(detail, response.status);
  }
  return body as T;
}

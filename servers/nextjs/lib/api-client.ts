const DEFAULT_DEV_BASE_URL = "http://localhost:8000";
const DEFAULT_PROD_BASE_URL = "https://presenton-1.onrender.com";

const sanitizeBaseUrl = (baseUrl: string | undefined | null) => {
  if (!baseUrl) return "";
  return baseUrl.replace(/\s+/g, "").replace(/\/+$/, "");
};

const envBaseUrl = sanitizeBaseUrl(process.env.NEXT_PUBLIC_FASTAPI_URL);
const isVercelRuntime = Boolean(sanitizeBaseUrl(process.env.NEXT_PUBLIC_VERCEL_URL));

let cachedBaseUrl: string | null = envBaseUrl || null;

const shouldForwardToBackend = (input: string) => {
  return input.startsWith("/api/v1") || input.startsWith("/app_data/");
};

const resolveBackendBaseUrl = () => {
  if (cachedBaseUrl !== null) {
    return cachedBaseUrl;
  }

  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      cachedBaseUrl = DEFAULT_DEV_BASE_URL;
      return cachedBaseUrl;
    }
  }

  if (isVercelRuntime) {
    cachedBaseUrl = DEFAULT_PROD_BASE_URL;
    return cachedBaseUrl;
  }

  cachedBaseUrl = "";
  return cachedBaseUrl;
};

export const buildBackendUrl = (input: string) => {
  if (!shouldForwardToBackend(input)) {
    return input;
  }

  const baseUrl = resolveBackendBaseUrl();
  if (!baseUrl) {
    return input;
  }

  return `${baseUrl}${input}`;
};

export const apiFetch = (input: RequestInfo | URL, init?: RequestInit) => {
  if (typeof input === "string") {
    return fetch(buildBackendUrl(input), init);
  }

  return fetch(input, init);
};

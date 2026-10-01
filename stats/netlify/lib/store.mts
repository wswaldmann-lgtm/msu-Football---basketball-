// Shared helpers: production data in the global store; previews get their own throwaway store.
import { getStore, getDeployStore } from "@netlify/blobs";

export function store(name: string) {
  return Netlify.context?.deploy?.context === "production" ? getStore(name) : getDeployStore(name);
}

// The app lives on GitHub Pages, so only that origin may call these endpoints from the browser.
const APP_ORIGIN = "https://wswaldmann-lgtm.github.io";
export function cors(req: Request): Record<string, string> {
  return req.headers.get("origin") === APP_ORIGIN
    ? { "Access-Control-Allow-Origin": APP_ORIGIN, "Access-Control-Allow-Methods": "GET, POST", "Access-Control-Allow-Headers": "Content-Type", "Vary": "Origin" }
    : {};
}

export const ID_RE = /^[a-z0-9]{8,24}$/;
export const clean = (v: unknown, max: number) => String(v ?? "").replace(/[\u0000-\u001f]/g, " ").trim().slice(0, max);

export async function sha256(s: string) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
}

export async function readBody(req: Request) {
  try { return JSON.parse((await req.text()).slice(0, 8000)); } catch { return null; }
}

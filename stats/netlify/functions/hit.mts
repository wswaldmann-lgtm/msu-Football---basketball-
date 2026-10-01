// Records one app open. No names, no IP addresses: just the date, the US state
// (or country) Netlify detects, and a random ID the app makes for each device.
// Each open is its own tiny record, so simultaneous opens never overwrite each other.
import type { Context, Config } from "@netlify/functions";
import { getStore, getDeployStore } from "@netlify/blobs";

function store() {
  return Netlify.context?.deploy?.context === "production" ? getStore("opens") : getDeployStore("opens");
}

export default async (req: Request, context: Context) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });
  const raw = (await req.text()).trim().slice(0, 64);
  const vid = /^[a-z0-9]{8,32}$/i.test(raw) ? raw.toLowerCase() : "unknown";
  const day = new Date().toLocaleDateString("en-CA", { timeZone: "America/New_York" }); // YYYY-MM-DD
  const country = (context.geo?.country?.code || "XX").replace(/[^A-Z]/gi, "");
  const sub = (context.geo?.subdivision?.code || "").replace(/[^A-Z0-9]/gi, "");
  const place = country === "US" && sub ? "US-" + sub : country || "XX";
  const key = `o/${day}/${place}/${vid}/${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
  await store().set(key, "");
  return new Response(null, { status: 204 });
};

export const config: Config = { path: "/api/hit" };

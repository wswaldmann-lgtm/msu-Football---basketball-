// Totals the open records into daily opens, unique devices, and places.
import type { Config } from "@netlify/functions";
import { getStore, getDeployStore } from "@netlify/blobs";

function store() {
  return Netlify.context?.deploy?.context === "production" ? getStore("opens") : getDeployStore("opens");
}

export default async () => {
  const { blobs } = await store().list({ prefix: "o/" });
  const days: Record<string, { opens: number; devices: Set<string> }> = {};
  const places: Record<string, number> = {};
  const allDevices = new Set<string>();
  for (const b of blobs) {
    const [, day, place, vid] = b.key.split("/");
    if (!day) continue;
    days[day] ??= { opens: 0, devices: new Set() };
    days[day].opens++;
    days[day].devices.add(vid);
    allDevices.add(vid);
    places[place] = (places[place] || 0) + 1;
  }
  // devices seen in the last 7 days (Eastern time), counted once each
  const now = new Date();
  const recent = new Set(Array.from({ length: 7 }, (_, i) =>
    new Date(now.getTime() - i * 86400000).toLocaleDateString("en-CA", { timeZone: "America/New_York" })));
  const week = new Set<string>();
  for (const d of Object.keys(days)) if (recent.has(d)) days[d].devices.forEach(v => week.add(v));
  const out = {
    week7Devices: week.size,
    totalOpens: blobs.length,
    totalDevices: allDevices.size,
    days: Object.keys(days).sort().reverse().map(d => ({ day: d, opens: days[d].opens, devices: days[d].devices.size })),
    places: Object.entries(places).sort((a, b) => b[1] - a[1]).map(([place, opens]) => ({ place, opens })),
    updated: new Date().toISOString(),
  };
  return Response.json(out, { headers: { "Cache-Control": "no-store" } });
};

export const config: Config = { path: "/api/stats" };

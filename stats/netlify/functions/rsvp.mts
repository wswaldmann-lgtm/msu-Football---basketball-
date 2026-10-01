// Answers to a watch party.  POST /api/rsvp {id, rid, name, status, count, via}
// Each phone gets its own answer slot (rid), so changing your answer just overwrites it.
// The host can remove an answer with {id, rid, remove: true, hostKey}.
import type { Config } from "@netlify/functions";
import { store, cors, ID_RE, clean, sha256, readBody } from "../lib/store.mts";

export default async (req: Request) => {
  const h = cors(req);
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
  if (req.method !== "POST") return new Response("POST only", { status: 405, headers: h });
  const b = await readBody(req);
  if (!b || !ID_RE.test(b.id || "") || !ID_RE.test(b.rid || "")) return Response.json({ error: "bad request" }, { status: 400, headers: h });
  const party: any = await store("parties").get(b.id, { type: "json" });
  if (!party) return Response.json({ error: "not found" }, { status: 404, headers: h });
  const rsvps = store("rsvps"), key = `${b.id}/${b.rid}`;

  if (b.remove) {
    if (!ID_RE.test(b.hostKey || "") || (await sha256(b.hostKey)) !== party.hostKeyHash)
      return Response.json({ error: "host only" }, { status: 403, headers: h });
    await rsvps.delete(key);
    return Response.json({ ok: true }, { headers: h });
  }
  const status = ["in", "maybe", "out"].includes(b.status) ? b.status : null;
  const name = clean(b.name, 40);
  if (!status || !name) return Response.json({ error: "name and answer required" }, { status: 400, headers: h });
  const count = Math.min(20, Math.max(1, parseInt(b.count) || 1));
  await rsvps.setJSON(key, { name, status, count: status === "in" ? count : 1, via: clean(b.via, 40), updated: new Date().toISOString() });
  return Response.json({ ok: true }, { headers: h });
};

export const config: Config = { path: "/api/rsvp" };

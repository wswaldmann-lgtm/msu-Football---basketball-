// Watch parties.  GET /api/party?id=...  -> party details + everyone's answers
//                 POST /api/party        -> create or (host only) update a party
import type { Config } from "@netlify/functions";
import { store, cors, ID_RE, clean, sha256, readBody } from "../lib/store.mts";

export default async (req: Request) => {
  const h = cors(req);
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
  const parties = store("parties"), rsvps = store("rsvps");

  if (req.method === "GET") {
    const id = new URL(req.url).searchParams.get("id") || "";
    if (!ID_RE.test(id)) return Response.json({ error: "bad id" }, { status: 400, headers: h });
    const p = await parties.get(id, { type: "json" });
    if (!p) return Response.json({ error: "not found" }, { status: 404, headers: h });
    const { blobs } = await rsvps.list({ prefix: id + "/" });
    const list = (await Promise.all(blobs.map(async b => {
        const r: any = await rsvps.get(b.key, { type: "json" });
        return r ? { ...r, rid: b.key.split("/")[1] } : null;
      })))
      .filter(Boolean)
      .sort((a: any, b: any) => (a.updated || "").localeCompare(b.updated || ""));
    const totals = { in: 0, maybe: 0, out: 0, people: 0 };
    for (const r of list as any[]) { totals[r.status as "in" | "maybe" | "out"]++; if (r.status === "in") totals.people += r.count || 1; }
    const { hostKeyHash, ...pub } = p as any;
    const isHost = !!req.headers.get("x-host-key") && (await sha256(req.headers.get("x-host-key")!)) === hostKeyHash;
    // rids let the host remove a response; everyone else just sees names
    return Response.json({ party: pub, rsvps: list.map((r: any) => isHost ? r : { ...r, rid: undefined }), totals, isHost },
      { headers: { ...h, "Cache-Control": "no-store" } });
  }

  if (req.method === "POST") {
    const b = await readBody(req);
    if (!b || !ID_RE.test(b.id || "") || !ID_RE.test(b.hostKey || "")) return Response.json({ error: "bad request" }, { status: 400, headers: h });
    const existing: any = await parties.get(b.id, { type: "json" });
    const keyHash = await sha256(b.hostKey);
    if (existing && existing.hostKeyHash !== keyHash) return Response.json({ error: "not your party" }, { status: 403, headers: h });
    const party = {
      id: b.id,
      hostKeyHash: keyHash,
      sport: clean(b.sport, 20) || "basketball",
      game: clean(b.game, 80),
      gameDate: clean(b.gameDate, 40),
      place: clean(b.place, 80),
      address: clean(b.address, 160),
      time: clean(b.time, 40),
      host: clean(b.host, 40),
      note: clean(b.note, 300),
      created: existing?.created || new Date().toISOString(),
      updated: new Date().toISOString(),
    };
    if (!party.place) return Response.json({ error: "place required" }, { status: 400, headers: h });
    await parties.setJSON(b.id, party);
    return Response.json({ ok: true, id: b.id }, { headers: h });
  }
  return new Response("Method not allowed", { status: 405, headers: h });
};

export const config: Config = { path: "/api/party" };

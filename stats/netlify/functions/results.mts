// Final scores for one team's finished games, so the schedule cards fill in
// results on their own (no hand edits needed after each game).
//   GET /api/results?sport=football|basketball&espn=127
//   -> { ok, games: [{ date: "YYYY-MM-DD" (Eastern), us, them, won }] }
import type { Config } from "@netlify/functions";

const ESPN_PATH: Record<string, string> = {
  football: "football/college-football",
  basketball: "basketball/mens-college-basketball",
};
const CORS = { "Access-Control-Allow-Origin": "*" };

const num = (s: any) => {
  const v = s?.displayValue ?? s?.value ?? s;
  const n = parseInt(String(v ?? ""), 10);
  return Number.isFinite(n) ? n : null;
};

export default async (req: Request) => {
  const q = new URL(req.url).searchParams;
  const sport = q.get("sport") === "basketball" ? "basketball" : "football";
  const espnId = (q.get("espn") || "").replace(/\D/g, "");
  try {
    const r = await fetch(`https://site.api.espn.com/apis/site/v2/sports/${ESPN_PATH[sport]}/teams/${espnId}/schedule`,
      { headers: { "User-Agent": "gameday-tracker" }, signal: AbortSignal.timeout(6000) });
    if (!r.ok) throw new Error(String(r.status));
    const d = await r.json();
    const games = [];
    for (const e of d.events || []) {
      const c = e.competitions?.[0];
      if (c?.status?.type?.state !== "post" && !c?.status?.type?.completed) continue;
      const mine = (c.competitors || []).find((t: any) => String(t.team?.id) === espnId);
      const opp = (c.competitors || []).find((t: any) => String(t.team?.id) !== espnId);
      const us = num(mine?.score), them = num(opp?.score);
      if (us === null || them === null) continue;
      const date = new Date(e.date).toLocaleDateString("en-CA", { timeZone: "America/New_York" });
      games.push({ date, us, them, won: us > them });
    }
    return new Response(JSON.stringify({ ok: true, games }), {
      headers: { ...CORS, "Content-Type": "application/json", "Cache-Control": "public, max-age=600" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ ok: false, error: String(err) }), {
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
};

export const config: Config = { path: "/api/results" };

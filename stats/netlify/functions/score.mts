// Live score for one team, fetched server-side so the phone never hits CORS
// limits or stale caches. Tries ESPN's daily scoreboard, then ESPN's per-game
// feed, then the NCAA scoreboard (ESPN sometimes never marks a game as live).
//   GET /api/score?sport=football|basketball&espn=127&ncaa=michigan-st
import type { Config } from "@netlify/functions";

type Team = { name: string; score: string; mine: boolean };
type Score = { source: string; state: "pre" | "in" | "post"; detail: string; teams: Team[] };

const ESPN_PATH: Record<string, string> = {
  football: "football/college-football",
  basketball: "basketball/mens-college-basketball",
};
const ESPN_GROUP: Record<string, string> = { football: "80", basketball: "50" };
const NCAA_PATH: Record<string, string> = { football: "football/fbs", basketball: "basketball-men/d1" };

async function json(url: string): Promise<any> {
  const r = await fetch(url, { headers: { "User-Agent": "gameday-tracker" }, signal: AbortSignal.timeout(6000) });
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r.json();
}

function fromEspnComp(comp: any, espnId: string, source: string): Score | null {
  if (!comp) return null;
  const st = comp.status?.type || {};
  const teams = (comp.competitors || []).map((t: any) => ({
    name: t.team?.shortDisplayName || t.team?.displayName || "?",
    score: String(t.score?.displayValue ?? t.score?.value ?? t.score ?? ""),
    mine: String(t.team?.id) === espnId,
  }));
  return { source, state: st.state || "pre", detail: st.shortDetail || st.detail || "", teams };
}

async function espn(sport: string, espnId: string): Promise<{ score: Score | null; eventId?: string }> {
  const ymd = new Date().toLocaleDateString("en-CA", { timeZone: "America/New_York" }).replace(/-/g, "");
  const d = await json(`https://site.api.espn.com/apis/site/v2/sports/${ESPN_PATH[sport]}/scoreboard?groups=${ESPN_GROUP[sport]}&limit=400&dates=${ymd}`);
  const ev = (d.events || []).find((e: any) =>
    (e.competitions?.[0]?.competitors || []).some((t: any) => String(t.team?.id) === espnId));
  return { score: ev ? fromEspnComp(ev.competitions[0], espnId, "espn") : null, eventId: ev?.id };
}

async function espnSummary(sport: string, espnId: string, eventId: string): Promise<Score | null> {
  const d = await json(`https://site.api.espn.com/apis/site/v2/sports/${ESPN_PATH[sport]}/summary?event=${eventId}`);
  return fromEspnComp(d.header?.competitions?.[0], espnId, "espn-game");
}

async function ncaa(sport: string, slug: string): Promise<Score | null> {
  const d = await json(`https://ncaa-api.henrygd.me/scoreboard/${NCAA_PATH[sport]}`);
  const g = (d.games || []).map((x: any) => x.game)
    .find((g: any) => g && (g.home?.names?.seo === slug || g.away?.names?.seo === slug));
  if (!g) return null;
  const state = g.gameState === "final" ? "post" : g.gameState === "live" ? "in" : "pre";
  const team = (t: any) => ({ name: t.names?.short || "?", score: String(t.score ?? ""), mine: t.names?.seo === slug });
  const detail = state === "post" ? "Final" : state === "in" ? `${g.contestClock || ""} ${g.currentPeriod || ""}`.trim() : g.startTime || "";
  return { source: "ncaa", state, detail, teams: [team(g.home), team(g.away)] };
}

export default async (req: Request) => {
  const q = new URL(req.url).searchParams;
  const sport = q.get("sport") === "basketball" ? "basketball" : "football";
  const espnId = (q.get("espn") || "").replace(/\D/g, "");
  const slug = (q.get("ncaa") || "").replace(/[^a-z0-9-]/gi, "").toLowerCase();
  let best: Score | null = null;
  const tried: string[] = [];

  try {
    const e = await espn(sport, espnId);
    best = e.score;
    if (best?.state === "pre" && e.eventId) {
      try { best = (await espnSummary(sport, espnId, e.eventId)) || best; } catch (err) { tried.push(String(err)); }
    }
  } catch (err) { tried.push(String(err)); }

  if (!best || best.state === "pre") {
    try {
      const n = slug ? await ncaa(sport, slug) : null;
      if (n && (n.state !== "pre" || !best)) best = n;
    } catch (err) { tried.push(String(err)); }
  }

  return new Response(JSON.stringify(best ? { ok: true, ...best } : { ok: false, tried }), {
    headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=15" },
  });
};

export const config: Config = { path: "/api/score" };
